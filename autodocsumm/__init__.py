"""Sphinx extension that defines new auto documenters with autosummary.

The :class:`AutoSummModuleDocumenter` and :class:`AutoSummClassDocumenter`
classes defined here enable an autosummary-style listing of the corresponding
members.

This extension gives also the possibility to choose which data shall be shown
and to include the docstring of the ``'__call__'`` attribute.
"""
from itertools import chain

from sphinx.util import logging
import re
import six

from docutils import nodes

import sphinx

from sphinx.util.docutils import SphinxDirective

from sphinx.ext.autodoc import (
    ClassDocumenter, ModuleDocumenter, ALL, PycodeError,
    ModuleAnalyzer, bool_option, AttributeDocumenter, DataDocumenter, Options,
    prepare_docstring)
import sphinx.ext.autodoc as ad

signature = Signature = None

from sphinx.ext.autodoc.directive import (
    AutodocDirective, AUTODOC_DEFAULT_OPTIONS, process_documenter_options,
    DocumenterBridge
)

from sphinx.ext.autodoc import get_documenters

try:
    from sphinx.util.inspect import signature, stringify_signature
except ImportError:
    from sphinx.ext.autodoc import Signature

sphinx_version = list(map(float, re.findall(r'\d+', sphinx.__version__)[:3]))

from sphinx.util import force_decode


try:
    from cyordereddict import OrderedDict
except ImportError:
    try:
        from collections import OrderedDict
    except ImportError:
        from ordereddict import OrderedDict

if six.PY2:
    from itertools import imap as map

__version__ = '0.2.1'

__author__ = "Philipp S. Sommer"

logger = logging.getLogger(__name__)

#: Options of the :class:`sphinx.ext.autodoc.ModuleDocumenter` that have an
#: effect on the selection of members for the documentation
member_options = {
    'members', 'undoc-members', 'inherited-members', 'exclude-members',
    'private-members', 'special-members', 'imported-members',
    'ignore-module-all'}


if signature is not None:  # sphinx >= 2.4.0
    def process_signature(obj):
        sig = signature(obj)
        return stringify_signature(sig)
elif Signature is not None:  # sphinx >= 1.7
    def process_signature(obj):
        try:
            args = Signature(obj).format_args()
        except TypeError:
            return None
        else:
            args = args.replace('\\', '\\\\')
            return args


def list_option(option):
    """Transform a string to a list by splitting at ;;."""
    return [s.strip() for s in option.split(";;")]


class AutosummaryDocumenter(object):
    """Abstract class for for extending Documenter methods

    This classed is used as a base class for Documenters in order to provide
    the necessary methods for generating the autosummary."""

    #: List of functions that may filter the members
    filter_funcs = []

    #: Grouper functions
    grouper_funcs = []

    def __init__(self):
        raise NotImplementedError

    def get_grouped_documenters(self, all_members=False):
        """Method to return the member documenters

        This method is somewhat like a combination of the
        :meth:`sphinx.ext.autodoc.ModuleDocumenter.generate` method and the
        :meth:`sphinx.ext.autodoc.ModuleDocumenter.document_members` method.
        Hence it initializes this instance by importing the object, etc. and
        it finds the documenters to use for the autosummary option in the same
        style as the document_members does it.

        Returns
        -------
        dict
            dictionary whose keys are determined by the :attr:`member_sections`
            dictionary and whose values are lists of tuples. Each tuple
            consists of a documenter and a boolean to identify whether a module
            check should be made describes an attribute or not.

        Notes
        -----
        If a :class:`sphinx.ext.autodoc.Documenter.member_order` value is not
        in the :attr:`member_sections` dictionary, it will be put into an
        additional `Miscellaneous` section."""
        use_sections = self.options.autosummary_sections

        self.parse_name()
        self.import_object()
        # If there is no real module defined, figure out which to use.
        # The real module is used in the module analyzer to look up the module
        # where the attribute documentation would actually be found in.
        # This is used for situations where you have a module that collects the
        # functions and classes of internal submodules.
        self.real_modname = None or self.get_real_modname()

        # try to also get a source code analyzer for attribute docs
        try:
            self.analyzer = ModuleAnalyzer.for_module(self.real_modname)
            # parse right now, to get PycodeErrors on parsing (results will
            # be cached anyway)
            self.analyzer.find_attr_docs()
        except PycodeError as err:
            logger.debug('[autodocsumm] module analyzer failed: %s', err)
            # no source file -- e.g. for builtin and C modules
            self.analyzer = None
            # at least add the module.__file__ as a dependency
            if hasattr(self.module, '__file__') and self.module.__file__:
                self.directive.filename_set.add(self.module.__file__)
        else:
            self.directive.filename_set.add(self.analyzer.srcname)

        self.env.temp_data['autodoc:module'] = self.modname
        if self.objpath:
            self.env.temp_data['autodoc:class'] = self.objpath[0]

        if not self.options.autosummary_force_inline:
            docstring = self.get_doc()
            autodocsumm_directive = '.. auto%ssumm::' % self.objtype
            for s in chain.from_iterable(docstring):
                if autodocsumm_directive in s:
                    return {}

        # set the members from the autosummary member options
        options_save = {}
        for option in member_options.intersection(self.option_spec):
            autopt = 'autosummary-' + option
            if getattr(self.options, autopt):
                options_save[option] = getattr(self.options, option)
                self.options[option] = getattr(self.options, autopt)

        want_all = all_members or self.options.inherited_members or \
            self.options.members is ALL
        # find out which members are documentable
        members_check_module, members = self.get_object_members(want_all)

        # remove members given by exclude-members
        if self.options.exclude_members:
            members = [(membername, member) for (membername, member) in members
                       if membername not in self.options.exclude_members]

        # document non-skipped members
        memberdocumenters = []
        registry = get_documenters(self.env.app)

        for (mname, member, isattr) in self.filter_members(members, want_all):
            classes = [cls for cls in six.itervalues(registry)
                       if cls.can_document_member(member, mname, isattr, self)]
            if not classes:
                # don't know how to document this member
                continue
            # prefer the documenter with the highest priority
            classes.sort(key=lambda cls: cls.priority)
            # give explicitly separated module name, so that members
            # of inner classes can be documented
            full_mname = self.modname + '::' + \
                '.'.join(self.objpath + [mname])

            documenter = classes[-1](self.directive, full_mname, self.indent)
            memberdocumenters.append((documenter,
                                      members_check_module and not isattr))

        member_order = (
            self.options.member_order or self.env.config.autodoc_member_order
        )
        memberdocumenters = self.sort_members(memberdocumenters, member_order)

        documenters = OrderedDict()
        for e in memberdocumenters:
            section = self.member_sections.get(
                e[0].member_order, 'Miscellaneous')
            if self.env.app:
                e[0].parse_name()
                e[0].import_object()
                user_section = self.env.app.emit_firstresult(
                    'autodocsumm-grouper', self.objtype, e[0].object_name,
                    e[0].object, section, self.object)
                section = user_section or section
            if not use_sections or section in use_sections:
                documenters.setdefault(section, []).append(e)
        self.options.update(options_save)
        return documenters

    def add_autosummary(self):
        """Add the autosammary table of this documenter."""
        if self.options.autosummary:

            grouped_documenters = self.get_grouped_documenters()

            sourcename = self.get_sourcename()

            for section, documenters in grouped_documenters.items():
                if not self.options.autosummary_no_titles:
                    self.add_line('**%s:**' % section, sourcename)

                self.add_line('', sourcename)

                self.add_line('.. autosummary::', sourcename)
                self.add_line('', sourcename)
                indent = '    '

                for (documenter, _) in documenters:
                    self.add_line(
                        indent + '~' + documenter.fullname, sourcename)
                self.add_line('', sourcename)


class AutoSummModuleDocumenter(ModuleDocumenter, AutosummaryDocumenter):
    """Module documentor with autosummary tables of its members.

    This class has the same functionality as the base
    :class:`sphinx.ext.autodoc.ModuleDocumenter` class but with an additional
    `autosummary`.
    It's priority is slightly higher than the one of the ModuleDocumenter.
    """

    #: slightly higher priority than
    #: :class:`sphinx.ext.autodoc.ModuleDocumenter`
    priority = ModuleDocumenter.priority + 0.1

    #: original option_spec from :class:`sphinx.ext.autodoc.ModuleDocumenter`
    #: but with additional autosummary boolean option
    option_spec = ModuleDocumenter.option_spec.copy()
    option_spec['autosummary'] = bool_option
    option_spec['autosummary-no-nesting'] = bool_option
    option_spec['autosummary-sections'] = list_option
    option_spec['autosummary-no-titles'] = bool_option
    option_spec['autosummary-force-inline'] = bool_option

    #: Add options for members for the autosummary
    for _option in member_options.intersection(option_spec):
        option_spec['autosummary-' + _option] = option_spec[_option]
    del _option

    member_sections = OrderedDict([
        (ad.ClassDocumenter.member_order, 'Classes'),
        (ad.ExceptionDocumenter.member_order, 'Exceptions'),
        (ad.FunctionDocumenter.member_order, 'Functions'),
        (ad.DataDocumenter.member_order, 'Data'),
        ])
    """:class:`~collections.OrderedDict` that includes the autosummary sections

    This dictionary defines the sections for the autosummmary option. The
    values correspond to the :attr:`sphinx.ext.autodoc.Documenter.member_order`
    attribute that shall be used for each section."""

    def add_content(self, *args, **kwargs):
        super().add_content(*args, **kwargs)

        self.add_autosummary()

        if self.options.autosummary_no_nesting:
            self.options.autosummary = False


class AutoSummClassDocumenter(ClassDocumenter, AutosummaryDocumenter):
    """Class documentor with autosummary tables for its members.

    This class has the same functionality as the base
    :class:`sphinx.ext.autodoc.ClassDocumenter` class but with an additional
    `autosummary` option to provide the ability to provide a summary of all
    methods and attributes.
    It's priority is slightly higher than the one of the ClassDocumenter
    """

    #: slightly higher priority than
    #: :class:`sphinx.ext.autodoc.ClassDocumenter`
    priority = ClassDocumenter.priority + 0.1

    #: original option_spec from :class:`sphinx.ext.autodoc.ClassDocumenter`
    #: but with additional autosummary boolean option
    option_spec = ClassDocumenter.option_spec.copy()
    option_spec['autosummary'] = bool_option
    option_spec['autosummary-no-nesting'] = bool_option
    option_spec['autosummary-sections'] = list_option
    option_spec['autosummary-no-titles'] = bool_option
    option_spec['autosummary-force-inline'] = bool_option

    #: Add options for members for the autosummary
    for _option in member_options.intersection(option_spec):
        option_spec['autosummary-' + _option] = option_spec[_option]
    del _option

    member_sections = OrderedDict([
        (ad.ClassDocumenter.member_order, 'Classes'),
        (ad.MethodDocumenter.member_order, 'Methods'),
        (ad.AttributeDocumenter.member_order, 'Attributes'),
        ])
    """:class:`~collections.OrderedDict` that includes the autosummary sections

    This dictionary defines the sections for the autosummmary option. The
    values correspond to the :attr:`sphinx.ext.autodoc.Documenter.member_order`
    attribute that shall be used for each section."""

    def add_content(self, *args, **kwargs):
        super().add_content(*args, **kwargs)

        self.add_autosummary()


class CallableDataDocumenter(DataDocumenter):
    """:class:`sphinx.ext.autodoc.DataDocumenter` that uses the __call__ attr
    """

    priority = DataDocumenter.priority + 0.1

    def format_args(self):
        # for classes, the relevant signature is the __init__ method's
        callmeth = self.get_attr(self.object, '__call__', None)
        if callmeth is None:
            return None
        return process_signature(callmeth)

    def get_doc(self, encoding=None, ignore=1):
        """Reimplemented  to include data from the call method"""
        content = self.env.config.autodata_content
        if content not in ('both', 'call') or not self.get_attr(
                self.get_attr(self.object, '__call__', None), '__doc__'):
            return super(CallableDataDocumenter, self).get_doc(
                encoding=encoding, ignore=ignore)

        # for classes, what the "docstring" is can be controlled via a
        # config value; the default is both docstrings
        docstrings = []
        if content != 'call':
            docstring = self.get_attr(self.object, '__doc__', None)
            docstrings = [docstring + '\n'] if docstring else []
        calldocstring = self.get_attr(
            self.get_attr(self.object, '__call__', None), '__doc__')
        if docstrings:
            docstrings[0] += calldocstring
        else:
            docstrings.append(calldocstring + '\n')

        doc = []
        for docstring in docstrings:
            if not isinstance(docstring, six.text_type):
                docstring = force_decode(docstring, encoding)
            doc.append(prepare_docstring(docstring, ignore))

        return doc


class CallableAttributeDocumenter(AttributeDocumenter):
    """:class:`sphinx.ext.autodoc.AttributeDocumenter` that uses the __call__
    attr
    """

    priority = AttributeDocumenter.priority + 0.1

    def format_args(self):
        # for classes, the relevant signature is the __init__ method's
        callmeth = self.get_attr(self.object, '__call__', None)
        if callmeth is None:
            return None
        return process_signature(callmeth)

    def get_doc(self, encoding=None, ignore=1):
        """Reimplemented  to include data from the call method"""
        content = self.env.config.autodata_content
        if content not in ('both', 'call') or not self.get_attr(
                self.get_attr(self.object, '__call__', None), '__doc__'):
            return super(CallableAttributeDocumenter, self).get_doc(
                encoding=encoding, ignore=ignore)

        # for classes, what the "docstring" is can be controlled via a
        # config value; the default is both docstrings
        docstrings = []
        if content != 'call':
            docstring = self.get_attr(self.object, '__doc__', None)
            docstrings = [docstring + '\n'] if docstring else []
        calldocstring = self.get_attr(
            self.get_attr(self.object, '__call__', None), '__doc__')
        if docstrings:
            docstrings[0] += calldocstring
        else:
            docstrings.append(calldocstring + '\n')

        doc = []
        for docstring in docstrings:
            if not isinstance(docstring, six.text_type):
                docstring = force_decode(docstring, encoding)
            doc.append(prepare_docstring(docstring, ignore))

        return doc


def dont_document_data(config, fullname):
    """Check whether the given object should be documented

    Parameters
    ----------
    config: sphinx.Options
        The configuration
    fullname: str
        The name of the object

    Returns
    -------
    bool
        Whether the data of `fullname` should be excluded or not"""
    if config.document_data is True:
        document_data = [re.compile('.*')]
    else:
        document_data = config.document_data
    if config.not_document_data is True:
        not_document_data = [re.compile('.*')]
    else:
        not_document_data = config.not_document_data
    return (
            # data should not be documented
            (any(re.match(p, fullname) for p in not_document_data)) or
            # or data is not included in what should be documented
            (not any(re.match(p, fullname) for p in document_data)))


class NoDataDataDocumenter(CallableDataDocumenter):
    """DataDocumenter that prevents the displaying of large data"""

    #: slightly higher priority as the one of the CallableDataDocumenter
    priority = CallableDataDocumenter.priority + 0.1

    def __init__(self, *args, **kwargs):
        super(NoDataDataDocumenter, self).__init__(*args, **kwargs)
        fullname = '.'.join(self.name.rsplit('::', 1))
        if hasattr(self.env, 'config') and dont_document_data(
                self.env.config, fullname):
            self.options = Options(self.options)
            self.options.annotation = ' '


class NoDataAttributeDocumenter(CallableAttributeDocumenter):
    """AttributeDocumenter that prevents the displaying of large data"""

    #: slightly higher priority as the one of the CallableAttributeDocumenter
    priority = CallableAttributeDocumenter.priority + 0.1

    def __init__(self, *args, **kwargs):
        super(NoDataAttributeDocumenter, self).__init__(*args, **kwargs)
        fullname = '.'.join(self.name.rsplit('::', 1))
        if hasattr(self.env, 'config') and dont_document_data(
                self.env.config, fullname):
            self.options = Options(self.options)
            self.options.annotation = ' '


class AutoDocSummDirective(SphinxDirective):
    """A directive to generate an autosummary.

    Usage::

        .. autoclasssum:: <Class>

        .. automodsum:: <module>

    The directive additionally supports all options of the ``autoclass`` or
    ``automod`` directive respectively. Sections can be a list of section titles
    to be included. If ommitted, all sections are used.
    """

    has_content = False

    option_spec = AutodocDirective.option_spec

    required_arguments = 1
    optional_arguments = 0

    def run(self):
        reporter = self.state.document.reporter

        try:
            source, lineno = reporter.get_source_and_line(self.lineno)
        except AttributeError:
            source, lineno = (None, None)

        # look up target Documenter
        objtype = self.name[4:-4]  # strip prefix (auto-) and suffix (-summ).
        doccls = self.env.app.registry.documenters[objtype]

        self.options['autosummary-force-inline'] = True
        self.options['autosummary'] = True
        if 'no-members' not in self.options:
            self.options['members'] = True

        # process the options with the selected documenter's option_spec
        try:
            documenter_options = process_documenter_options(doccls, self.config,
                                                            self.options)
        except (KeyError, ValueError, TypeError) as exc:
            # an option is either unknown or has a wrong type
            logger.error(
                'An option to %s is either unknown or has an invalid '
                'value: %s', self.name, exc,
                location=(self.env.docname, lineno))
            return []

        # generate the output
        params = DocumenterBridge(self.env, reporter, documenter_options,
                                  lineno, self.state)
        documenter = doccls(params, self.arguments[0])
        documenter.add_autosummary()

        node = nodes.paragraph()
        node.document = self.state.document
        self.state.nested_parse(params.result, 0, node)

        return node.children


def setup(app):
    """setup function for using this module as a sphinx extension"""
    app.setup_extension('sphinx.ext.autosummary')
    app.setup_extension('sphinx.ext.autodoc')
    app.add_directive('autoclasssumm', AutoDocSummDirective)
    app.add_directive('automodulesumm', AutoDocSummDirective)

    AUTODOC_DEFAULT_OPTIONS.extend(
        [option for option in AutoSummModuleDocumenter.option_spec
         if option not in AUTODOC_DEFAULT_OPTIONS])

    AUTODOC_DEFAULT_OPTIONS.extend(
        [option for option in AutoSummClassDocumenter.option_spec
         if option not in AUTODOC_DEFAULT_OPTIONS])

    # make sure to allow inheritance when registering new documenters
    registry = get_documenters(app)
    for cls in [AutoSummClassDocumenter, AutoSummModuleDocumenter,
                CallableAttributeDocumenter, NoDataDataDocumenter,
                NoDataAttributeDocumenter]:
        if not issubclass(registry.get(cls.objtype), cls):
            app.add_autodocumenter(cls, override=True)

    # group event
    app.add_event('autodocsumm-grouper')

    # config value
    app.add_config_value('autodata_content', 'class', True)
    app.add_config_value('document_data', True, True)
    app.add_config_value('not_document_data', [], True)
    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}
