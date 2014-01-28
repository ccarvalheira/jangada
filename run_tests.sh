#!/bin/bash

rm -rf htmlcov
rm -rf htmllint

coverage run --source="." manage.py test
coverage html --omit="*/migrations/*"

mkdir htmllint
cd ..

#pylint --ignore=migrations jangada -f html > jangada/htmllint/pylint.html

#firefox jangada/htmllint/pylint.html
#firefox jangada/htmlcov/index.html
