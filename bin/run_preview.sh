#!/bin/bash
sk --ansi -i -c 'rg --color=always --line-number  "{}"' --preview "preview.sh {}"
