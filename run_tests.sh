#!/bin/bash

rm -rf htmlcov
rm -rf htmllint

coverage run --source="." manage.py test
coverage html --omit="*/migrations/*"

mkdir htmllint
cd ..

pylint --ignore=migrations meta -f html > meta/htmllint/pylint.html

firefox meta/htmllint/pylint.html
firefox meta/htmlcov/index.html
