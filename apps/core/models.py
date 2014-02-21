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
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True,null=True)
    installed_apps_text = models.TextField(blank=True, null=True)
    requirements_pkg_name = models.CharField(max_length=50)
    requirements_version = models.CharField(max_length=10,blank=True,null=True)
    hard_config = models.TextField(blank=True,null=True)
    soft_config = models.TextField(blank=True,null=True)
    syspackages_needed = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name

    def installed_apps_list(self):
        """ Returns the list of apps to be inserted in settings.INSTALLED_APPS """
        return self.installed_apps_text.split("\n")

    def get_requirements(self):
        """ Returns the requirements line to be inserted in requirements.txt in the format <pkg_name>[==<pkg_version>] """
        req = self.requirements_pkg_name
        if self.requirements_version:
            req += "=="+self.requirements_version
        return req


class App(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True, null=True)
    url_prefix = models.CharField(max_length=100, blank=True, null=True)
    keep_templates = models.BooleanField(help_text="Check to store this app's templates inside the app folder and not in the projectwide template folder.")

    def __unicode__(self):
        return self.name

    def get_sane_name(self,replace_value="_"):
        return self.name.strip().replace(" ",replace_value)

    def models_file_content(self,language="python"):
        """using template"""
        con = {}
        #attempt to avoid model fk dependency
        con["class_list"] = sorted(self.classmodel_set.all(), key=lambda num: len(num.relationship_fields_set.all()), reverse=True)
        
        return render_to_string(language+"/models_template.jinja", con)
    
    def models_files(self, language="python"):
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
            final_list.append((f,render_to_string(language+"/models_template.jinja", con)))
            #write_to_file("generated_projects/%s/apps/%s/models.py" % (self.project.get_sane_name(),app.get_sane_name()), stri+"\n")
        return final_list
            

    def admin_file_content(self, language="python"):
        """using templates"""
        con = {}
        con["class_list"] = self.classmodel_set.filter(register_admin=True).order_by("-relationship_fields_set").order_by("name")
        return render_to_string(language+"/admin_template.jinja", con)
    
    def views_file_content(self, language="python"):
        con = {}
        con["view_list"] = self.viewmodel_set.all()
        
        reg = re.compile("<\w+>")
        param_list = []
        for v in self.viewmodel_set.all():
            for match in reg.findall(v.url_regex):
                match = match[1:-1]
                param_list.append(match)
        con["url_params"] = param_list
        return render_to_string(language+"/views_template.jinja", con)
    
    def urls_file_content(self, language="python"):
        con = {}
        con["view_list"] = self.viewmodel_set.all()
        con["app"] = self
        return render_to_string(language+"/app_urls_template.jinja", con)



class Project(models.Model):
    name = models.CharField(max_length=50)
    used_pips = models.ManyToManyField(Pip)
    used_apps = models.ManyToManyField(App)
    css_framework = models.CharField(max_length=2, choices=CSS_FRAMEWORK_CHOICES)
    
    def __unicode__(self):
        return self.name

    def get_sane_name(self, replace_value="_"):
        return self.name.strip().replace(" ", replace_value)

    def used_pips_installed_apps(self):
        return [ap for p in self.used_pips.all() for ap in p.installed_apps_list() if ap]

    def settings_file_content(self, language="python"):
        con = {}
        con["language"] = "en-uk"
        con["use_i18n"] = "True"
        con["use_l10n"] = "True"
        con["used_pips"] = self.used_pips_installed_apps()
        con["used_apps"] = self.used_apps.all()
        con["project_name"] = self.get_sane_name()
        con["more_config"] = [pip.hard_config for pip in self.used_pips.all()]
        return render_to_string(language+"/settings_template.jinja", con)

    
    def Procfile_file_content(self, dev=False):
        con = {}
        con["dev_proc"] = dev
        if "django-zurb-foundation" in self.get_requirements_list():
            con["using_foundation"] = True
        return render_to_string("Procfile_template.jinja", con)
    
    def urlconf_file_content(self, language="python"):
        con = {}
        con["urls_list"] = []
        con["app_list"] = self.used_apps.all()
        override = []
        for a in self.used_apps.all():
            for over in a.viewmodel_set.filter(override_url_prefix=True):
                override.append(over)
        con["override_app_prefix_list"] = override
        return render_to_string(language+"/urls_template.jinja", con)
    
    def example_env_content(self):
        con = {}
        con["env_vars"] = []
        
        con["env_vars"].append(("DEBUG","True"))
        con["env_vars"].append(("SECRET_KEY","123abc"))
        if "honcho" in self.get_requirements_list():
            con["env_vars"].append(("SERVER_PORT","8001"))
        return render_to_string("env_example_template.jinja",con)

    def get_requirements_list(self):
        """ Returns the list of requirements. """
        return [p.get_requirements() for p in self.used_pips.all()]

    def get_requirements(self):
        req = []
        for pip in self.used_pips.all():
            line = {}
            line["package"] = pip.requirements_pkg_name
            if pip.requirements_version:
                line["version"] = "=="+pip.requirements_version
            req.append(line)
        con = {}
        con["requirements"] = req
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

