from django.db import models

from django.template.loader import render_to_string
from django.db.models import Q

from .class_models import *
from .field_models import *

import re

def write_to_file(file, stri):
    f = open(file,"w+")
    f.write(stri)
    f.close()


CSS_FRAMEWORK_CHOICES = (
    ("fo", "Foundation"),
    ("bo", "Bootstrap"),
    )


BLOCK_TYPES = (
    ("head", "head"),
    ("body", "body"),
    ("script", "script"),
    )


class Pip(models.Model):
    name = models.CharField(max_length=50, help_text="Human readable name.")
    description = models.TextField(blank=True,null=True,help_text="Human readable description.")
    installed_apps_text = models.TextField(blank=True, null=True, help_text="Lines to include in INSTALLED_APPS on settings.py.")
    requirements_pkg_name = models.CharField(max_length=50, help_text="Package name to insert in requirements.txt.")
    requirements_version = models.CharField(max_length=10,blank=True,null=True, help_text="Package version.")
    hard_config = models.TextField(blank=True,null=True, help_text="One or more lines to include in settings.py.")
    soft_config = models.TextField(blank=True,null=True, help_text="One or more lines to include in .env.")
    syspackages_needed = models.TextField(blank=True, null=True, help_text="System packages nedded to build this package. Not implemented yet.")
    urls_config = models.TextField(blank=True, null=True, help_text="Lines to include in the main urls.py. These will be inserted directly in the file, as is. Commas will be inserted at the end of each line.")
    
    def __unicode__(self):
        return self.name

    def installed_apps_list(self):
        """ Returns the list of apps to be inserted in settings.INSTALLED_APPS """
        return self.installed_apps_text.split("\n")

    def get_requirements(self):
        """ Returns a tuple of (package name, version). If version is not specified, None is returned instead on the second item of the tuple. """

        if self.requirements_version:
            return (self.requirements_pkg_name, self.requirements_version)
        return (self.requirements_pkg_name,None)

    def get_urlconfig_list(self):
        return [conf.strip() for conf in self.urls_config.split("\n")]



class App(models.Model):
    name = models.CharField(max_length=50, help_text="Name of the app.")
    description = models.CharField(max_length=50, blank=True, null=True, help_text="Human readable description of this app.")
    url_prefix = models.CharField(max_length=100, blank=True, null=True, help_text="URL prefix for the views in this app.")
    keep_templates = models.BooleanField(help_text="Check to store this app's templates inside the app folder and not in the projectwide template folder.")

    def __unicode__(self):
        return self.name

    def get_sane_name(self,replace_value="_"):
        """
        Returns the sanitized name of the App (not really much sanitized yet...)
        :param replace_value:
        :return: sane_name
        """
        return self.name.strip().replace(" ",replace_value)

    def render_models(self):
        """
        Renders the models.py file.
        :return: models.py file content
        """
        con = {}
        #attempt to avoid model fk dependency
        con["class_list"] = sorted(self.classmodel_set.all(), key=lambda num: len(num.relationship_fields_set.all()), reverse=True)
        
        return render_to_string("models_template.jinja", con)
    
    def models_files(self):
        """

        :return:
        """
        #find all different files
        file_list = []
        for c in self.classmodel_set.all():
            if c.output_file not in file_list:
                file_list.append(c.output_file)
        
        final_list = []
        con = {}
        for f in file_list:
            con["is_modelspy"] = False
            if f == "models.py":
                con["is_modelspy"] = True
            con["class_list"] = self.classmodel_set.filter(output_file=f)
            final_list.append((f,render_to_string("models_template.jinja", con)))
            #write_to_file("generated_projects/%s/apps/%s/models.py" % (self.project.get_sane_name(),app.get_sane_name()), stri+"\n")
        return final_list
            

    def render_admin(self):
        """
        Renders the admin.py file.
        :return: admin.py file content
        """
        con = {}
        con["class_list"] = self.classmodel_set.filter(register_admin=True).order_by("-relationship_fields_set").order_by("name")
        return render_to_string("admin_template.jinja", con)
    
    def render_views(self):
        """
        Renders the views.py file.
        :return: views.py file content
        """
        con = {}
        con["view_list"] = self.viewmodel_set.all()
        
        reg = re.compile("<\w+>")
        param_list = []
        for v in self.viewmodel_set.all():
            for match in reg.findall(v.url_regex):
                match = match[1:-1]
                param_list.append(match)
        con["url_params"] = param_list
        return render_to_string("views_template.jinja", con)
    
    def render_urls(self):
        """
        Renders the <app>/urls.py file.
        :return: <app>/urls.py file content
        """
        con = {}
        con["view_list"] = self.viewmodel_set.all()
        con["app"] = self
        return render_to_string("app_urls_template.jinja", con)



class Project(models.Model):
    name = models.CharField(max_length=50, help_text="Name of the project.")
    used_pips = models.ManyToManyField(Pip, help_text="List of Pips this project uses.")
    used_apps = models.ManyToManyField(App, help_text="List of Apps this project uses.")
    css_framework = models.CharField(max_length=2, choices=CSS_FRAMEWORK_CHOICES, help_text="CSS framework this project uses. Not implemented.")
    
    def __unicode__(self):
        return self.name

    def get_sane_name(self, replace_value="_"):
        """
        Returns the sanitized name of this project. Not really implemented yet...
        :param replace_value:
        :return: sanitized name
        """
        return self.name.strip().replace(" ", replace_value)

    def used_pips_installed_apps(self):
        """
        Returns the list of installed apps the pips of this project define.
        :return: list of all installed apps
        """
        return [ap for p in self.used_pips.all() for ap in p.installed_apps_list() if ap]

    def render_settings(self):
        """
        Renders the settings.py file.
        :return: settings.py file content
        """
        con = {}
        con["language"] = "en-uk"
        con["use_i18n"] = "True"
        con["use_l10n"] = "True"
        con["used_pips"] = self.used_pips_installed_apps()
        con["used_apps"] = self.used_apps.all()
        con["project_name"] = self.get_sane_name()
        con["more_config"] = [pip.hard_config for pip in self.used_pips.all()]
        return render_to_string("settings_template.jinja", con)

    
    def render_Procfile(self, dev=False):
        """
        Renders the Procfile file.
        :param dev: boolean, whether to generate dev file or not
        :return: Procfile file content
        """
        con = {}
        con["dev_proc"] = dev
        if "django-zurb-foundation" in self.get_requirements_list():
            con["using_foundation"] = True
        return render_to_string("Procfile_template.jinja", con)
    
    def render_urlconf(self):
        """
        Renders the confs/urls.py file (main urls.py file)
        :return: urls.py file content
        """
        con = {}
        con["urls_list"] = []
        con["app_list"] = self.used_apps.all()
        con["pip_urls_list"] = [pp for pip in self.used_pips.all() if pip.urls_config for pp in pip.get_urlconfig_list()]
        override = []
        for a in self.used_apps.all():
            for over in a.viewmodel_set.filter(override_url_prefix=True):
                override.append(over)
        con["override_app_prefix_list"] = override
        return render_to_string("urls_template.jinja", con)
    
    def render_env(self):
        """
        Renders the .env file.
        :return: .env file content
        """
        con = {}
        con["env_vars"] = []
        
        con["env_vars"].append("DEBUG=True")
        con["env_vars"].append("SECRET_KEY=123abc")
        if "honcho" in self._get_requirements_list():
            con["env_vars"].append("SERVER_PORT=8001")
        for soft_config in [pp.soft_config for pp in self.used_pips.all() if pp.soft_config]:
            con["env_vars"].append(soft_config)
        return render_to_string("env_example_template.jinja",con)

    def _get_requirements_list(self):
        """ Returns the list of requirements. """
        return [p.get_requirements() for p in self.used_pips.all()]

    def render_requirements(self):
        """
        Renders the requirements.txt file.
        :return: requirements.txt file content
        """
        con = {}
        con["requirements"] = self._get_requirements_list()
        return render_to_string("requirements_template.jinja", con)
    
    def base_template_content(self, engine="django_templates"):
        return self.templatemodel_set.filter(is_base=True)[0].base_template_content(engine,self.css_framework)



class TemplateModel(models.Model):
    name = models.CharField(max_length=50)
    is_base= models.BooleanField()
    extend = models.ForeignKey("self", blank=True, null=True, help_text="If this template is base, this field will be ignored.")
    project = models.ForeignKey(Project, blank=True, null=True, help_text="Use only if this is the base model, otherwise leave empty.")
    def __unicode__(self):
        return self.name
    
    def template_file_contents(self, engine="django_templates"):
        con = {}
        con["block_list"] = self.templateblock_set.all()
        con["this"] = self
        return render_to_string(engine+"/generic_template_template.jinja", con)

    def base_template_content(self, engine="django_templates", css_framework="fo"): #alternative fmw is bo
        con = {}
        con["block_list"] = self.templateblock_set.all()
        con["base_template"] = self
        if css_framework == "bo":
            return render_to_string(engine+"/bootstrap_base_template_template.jinja", con)
        return render_to_string(engine+"/foundation_base_template_template.jinja", con)

class TemplateBlock(models.Model):
    name = models.CharField(max_length=50)
    template = models.ForeignKey(TemplateModel)
    block_type = models.CharField(max_length=6, choices=BLOCK_TYPES, default="body")
    
    def __unicode__(self):
        return self.name

