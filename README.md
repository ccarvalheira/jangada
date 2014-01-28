Jangada
=========

## Introduction
Jangada is a tool that generates a new Django project following the configuration the user specifies using the admin interface.

Its intended use is to speed up project creation by generating code and folder structure and promoting the reuse of common components, like packages and apps (since they will be stored in the database for future projects to use).

## Installation
git clone it somewhere. You should probably use virtualenv.
```bash
pip install -r requirements.txt
cp .env.example .env
python manage.py syncdb
python manage.py loaddata fixtures/initial_data.json
honcho start
```

This will populate the database with some test data and start the server, which should be enough to have something working.

## Usage
Navigate to the admin and login (default port on Procfile is 8000).
To create a new project, use the admin interface to do so.
Projects have apps, which have classes (models) which, in turn, have fields.
Pips are packages on PyPI which are installed by pip.
For now Jangada generates models, the respective admin classes, some settings and the requirements file.

To export a project, select it in the list and run the admin action.
Try exporting the project already in the database to have an idea of what the application does.
The exporter will generate the project files, create a new virtualenv and install its dependencies, which may take a while. (using localshop can significantly speed up your install; in that case, you will want to check out apps.core.export_utility and look for the variable localshop (and also the package on PyPI))

To prepare the new project do the following:
```bash
cd generated_projects/tutorial_django/tutorial_django/
source ../env/bin/activate
python manage.py syncdb
<change Procfile default port>
honcho start
```
Edit the Procfile on tutorial_django/ and change the port (to 8001, for example) so the system won't complain because port 8000 is already in use.

You may now navigate to localhost:8001/admin and see the new project working!

## Future
Implementing the boilerplate generation for views, forms and urls is planned. In fact you can already see them in the models and the admin, but the features are not yet implemented.
Some support for template autogeneration and inheritance is a possibility, but I'm not sure how this will connect with the other objects, if at all.
Packages which must be built against system libraries need those already in place. There is a possibility of automating that too, but you'd need to be a privileged user, so the best Jangada can do is writing an .sh file and ask you to run it.

## Other considerations
The current known good setup is Ubuntu 12.04 with Python 2.7.3 and Django 1.6.1 in a virtualenv (it's what I use...).
The export code uses shell commands directly using the subprocess module. It will likely work on other linuxes, but not on windows.

WARNING: The database fields Project.name and App.name are used to create folders in the filesystem. These fields are not (yet) escaped properly, so writing something other than valid names will have unintended consequences, INCLUDING REMOVING SOME DIRECTORY YOU DON'T WANT DELETED. (writing "my cool project" is good, writing "/home/myuser/" is not...)

