from django.db import models

from django.template.loader import render_to_string
from django.db.models import Q


class Pip(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True,null=True)
    installed_apps_text = models.TextField()
    requirements_pkg_name = models.CharField(max_length=50)
    requirements_version = models.CharField(max_length=10,blank=True,null=True)
    hard_config = models.TextField(blank=True,null=True)
    soft_config = models.TextField(blank=True,null=True)

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

    def __unicode__(self):
        return self.name

    def get_sane_name(self,replace_value="_"):
        return self.name.replace(" ",replace_value)

    def models_file_content(self):
        """using template"""
        con = {}
        con["class_list"] = self.classmodel_set.all()
        models_file = render_to_string("models_template.jinja", con)
        return models_file

    def admin_file_content(self):
        """using templates"""
        con = {}
        con["class_list"] = self.classmodel_set.all().order_by("-relationship_fields_set").order_by("name")
        admin_file = render_to_string("admin_template.jinja", con)
        return admin_file


class ClassModel(models.Model):
    name = models.CharField(max_length=50)
    app = models.ForeignKey(App)
    register_admin = models.BooleanField()
    is_stacked = models.BooleanField()
    is_tabular = models.BooleanField()

    requires_pass = True

    def get_str_attribute(self):
        """ Detects the str attribute of this class. It is the first attribute found, regardless of other attributes found. """
        return self.regular_fields_set.filter(is_str=True)[0].name

    def __unicode__(self):
        return self.name

    def class_name(self):
        """ Returns CamelCase class name. """
        return self.name.title().replace(" ", "")

    def admin_name(self):
        """ Returns CamelCase admin class name. """
        aname = self.class_name()+"Admin"
        if self.is_stacked or self.is_tabular:
            aname += "Inline"
        return str(aname)

    def admin_import(self):
        """ Returns a dictionary with keys app_name,class_name to be imported in the admin. """
        return {"app_name": self.app.get_sane_name(), "class_name": self.class_name()}
        #aimport = "from apps."+self.app.name+".models import "+self.final_class_name()
        #return aimport

    def admin_register(self):
        """ Returns a dictionary with keys class_name,admin_name to be registered in the admin.
            Returns False if it's an inline class. (so it's not registered"""
        if "Inline" not in self.admin_name():
            return {"class_name":self.class_name(), "admin_name":self.admin_name()}
        return False
        #aregister = "admin.site.register("+self.class_name()+", "+self.admin_name()+")"
        #return aregister

    def admin_class_inherit(self):
        """ Returns the admin class from which this one inherits. """
        if self.is_stacked:
            return "StackedInline"
        elif self.is_tabular:
            return "TabularInline"
        else:
            return "ModelAdmin"

    def get_admin_fields(self, *args, **kwargs):
        """ Returns a list of fields to be inserted into various admin class attributes (like list_display, for example).
            Takes the same **kwargs as FieldModel. """
        admin_fields = self.regular_fields_set.filter(**kwargs)
        if admin_fields:
            self.requires_pass = False
        return admin_fields

    def get_all_fields(self):
        """ Returns all fields of this class. """
        return c.regular_fields_set.all() | c.relationship_this_class_set.all()


    def get_inlines(self):
        return self.app.classmodel_set.filter(Q(is_stacked=True) | Q(is_tabular=True))




FIELD_CHOICES = (
    ("char 10", "CharField 10",),
    ("char 20", "CharField 20"),
    ("char 50", "CharField 50"),
    ("char 100", "CharField 100"),
    ("char 200", "CharField 200"),
    ("int", "IntegerField"),
    ("txt", "TextField"),
    ("bool", "BooleanField",),
    ("datetime autonow", "DateTime autonow"),
    ("datetime", "DateTime"),
    ("date autonow", "Date now"),
    ("date", "Date"),
)

class GenericFieldModel(models.Model):
    name = models.CharField(max_length=50)
    is_blank = models.BooleanField()
    is_null = models.BooleanField()

    def base_field_options(self):
        opt = []
        if self.is_blank:
            opt.append("blank=True")
        if self.is_null:
            opt.append("null=True")
        return opt

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

KEY_TYPES = (
    ("fk", "ForeignKey"),
    ("m2m", "ManyToManyField"),
)

class RelationshipFieldModel(GenericFieldModel):
    this_class = models.ForeignKey(ClassModel, related_name="relationship_this_class_set")
    target_class = models.ForeignKey(ClassModel, related_name="relationship_fields_set")
    key_type = models.CharField(max_length=30, choices=KEY_TYPES)


    def field_options(self):
        """ Returns list of field options. If more are needed, insert ifs/elifs. """
        opt = [op for op in self.base_field_options()]
        opt.append(self.target_class.class_name()) #the class name referenced
        return opt

    def field_class(self):
        """ Returns the type of relationship. """
        keytype = ""
        if self.key_type == "fk":
            keytype = "ForeignKey"
        elif self.key_type == "m2m":
            keytype = "ManyToManyField"
        else:
            keytype = "ForeignKey" #you never know...
        return keytype

    def field_definition(self):
        opt = [op for op in self.base_field_options()]
        if self.key_type == "fk":
            keytype = "ForeignKey"
        elif self.key_type == "m2m":
            keytype = "ManyToManyField"
        else:
            keytype = "ForeignKey" #you never know...
        definition = "%s(%s,%s)" % (keytype, self.target_class.final_class_name(), ",".join(options))
        return definition

class FieldModel(GenericFieldModel):
    this_class = models.ForeignKey(ClassModel, related_name="regular_fields_set")
    field_type = models.CharField(max_length=20, choices=FIELD_CHOICES)
    is_str = models.BooleanField()
    list_display = models.BooleanField()
    filter_on_this = models.BooleanField()
    search_on_this = models.BooleanField()
    default = models.CharField(max_length=200, blank=True)
    editable = models.BooleanField(default=True)

    def field_class(self):
        """ Returns the django.models class of the field. When more classes are needed, just insert another elif
            We could probably use a dictionary lookup with FIELD_CHOICES, but this works for now. """
        t = ""
        if self.field_type.startswith("char"):
            t = "CharField"
        elif self.field_type.startswith("date"):
            t = "Date"
            if self.field_type.startswith("datetime"):
                t += "Time"
            t += "Field"
        elif self.field_type == "int":
            t = "IntegerField"
        elif self.field_type == "txt":
            t = "TextField"
        elif self.field_type == "bool":
            t = "BooleanField"
        return t

    def field_options(self):
        """ Returns list of field options. CharField takes a required option. If other options are added, just make another if. """
        opt = [op for op in self.base_field_options()]
        if not self.editable:
            opt.append("editable=False")
        if self.default:
            opt.append("default=\"%s\"" % self.default)
        if self.field_class() == "CharField":
            opt.append("max_length=%s" % self.field_type.split()[1])

        return opt

"""
    #TODO needs rework
    def field_definition(self):
        definition = ""
        options = []
        if self.field_type.startswith("char"):
            definition += "CharField"
            options.append("max_length="+self.field_type.split()[1])
        elif self.field_type.startswith("date"):
            definition += "Date"
            if self.field_type.startswith("datetime"):
                definition += "Time"
            definition += "Field"
            if len(self.field_type.split()) > 1 and self.field_type.split()[1] == "autonow":
                options.append("auto_now_add=True")
        elif self.field_type == "int":
            definition += "IntegerField"
        elif self.field_type == "txt":
            definition += "TextField"
        elif self.field_type == "bool":
            definition += "BooleanField"
        #field options
        if self.is_blank:
            options.append("blank=True")
        if self.is_null:
            options.append("null=True")
        if self.editable:
            options.append("editable=True")
        if self.default:
            options.append("default=%s" % self.default)
        definition += "("+",".join(options)+")"
        return definition
"""

class Projecto(models.Model):
    name = models.CharField(max_length=50)
    used_pips = models.ManyToManyField(Pip)
    used_apps = models.ManyToManyField(App)

    def __unicode__(self):
        return self.name

    def get_sane_name(self, replace_value="_"):
        return self.name.replace(" ", replace_value)

    def used_pips_installed_apps(self):
        return [ap for ap in p.installed_apps_list() for p in self.used_pips.all()]

    def settings_file_content(self):
        con = {}
        con["language"] = "pt-pt"
        con["use_i18n"] = "True"
        con["use_l10n"] = "True"
        con["used_pips"] = self.used_pips_installed_apps.all()
        con["used_apps"] = self.used_apps()
        con["project_name"] = self.get_sane_name()
        settings_file = render_to_string("settings_template.jinja", con)
        return settings_file

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


class ViewModel(models.Model):
    name = models.CharField(max_length=50)
    pass
