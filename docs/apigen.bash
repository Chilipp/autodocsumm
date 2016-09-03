#!/bin/bash
# script to automatically generate the autodocsumm api documentation using
# sphinx-apidoc and sed
sphinx-apidoc -f -M -e  -T -o api ../autodocsumm/
# replace chapter title in autodocsumm.rst
sed -i '' -e 1,1s/.*/'API Reference'/ api/autodocsumm.rst
