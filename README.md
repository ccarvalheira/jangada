Jangada
=========

## Introduction
Jangada is a tool that generates a new Django project following the configuration the user specifies using the admin interface.

Its intended use is to speed up project creation by generating code and folder structure and promoting the reuse of common components, like packages and apps (since they will be stored in the database for future projects to use).

## Installation
You should use something like virtualenv, but it's not mandatory.
```bash
mkdir jangada
cd jangada
virtualenv env
source env/bin/activate
git clone https://github.com/ccarvalheira/jangada.git
cd jangada
pip install -r requirements.txt
cp .env.example .env
python manage.py syncdb
python manage.py loaddata fixtures/initial_data.json
mkdir generated_projects
honcho start
```

This will populate the database with some test data and start the server, which should be enough to have something working.

## Usage
Navigate to the admin and login (default port on Procfile is 8000).
To create a new project, use the admin interface to do so.
Projects have apps, which have classes (models) which, in turn, have fields.
Pips are packages on PyPI which are installed by pip.
For now Jangada generates models, the respective admin classes, some settings, the url confs and the requirements file.

To export a project, select it in the list and run the admin action.
Try exporting the project already in the database to have an idea of what the application does.
It will not create the virtualenv, just the requirements.txt file.

To prepare the new project do the following, after you've run the admin action:
```bash
cd generated_projects/tutorial_django/tutorial_django/
<create a virtualenv>
pip install -r requirements.txt
cp .env.example .env
python manage.py syncdb
honcho start
```
You may now navigate to localhost:8001 and see the new project working (sort of)!
The admin is working and the urls already map to the respective views.
It will complain about missing templates; that's future work.

## Future
Implementing the boilerplate generation for views and forms is planned.
In fact you can already see them in the models and the admin, but some of the features are not yet implemented.

The project template will also be refined.

Some support for template autogeneration and inheritance is a possibility, but I'm not sure how this will connect with the other objects, if at all.
Packages which must be built against system libraries need them already in place.
There is a possibility of automating that too, but you'd need to be a privileged user, so the best Jangada can do is to write an .sh file and ask you to run it.


## Other considerations
The current known good setup is Ubuntu 12.04 with Python 2.7.3 and Django 1.6.1 in a virtualenv (it's what I use...).
The export code uses shell commands directly using the subprocess module.
It will likely work on other linuxes, but not on windows.

WARNING: The database fields Project.name and App.name are used to create folders in the filesystem.
These fields are not (yet) escaped properly, so writing something other than valid names will have unintended consequences, INCLUDING REMOVING SOME DIRECTORY YOU DON'T WANT DELETED. (writing "my cool project" is good, writing "/home/myuser/" is not...)

