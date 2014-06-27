from django.db import models

from django.template.loader import render_to_string
from django.db.models import Q

"""
This module has the models which generate classes in the new project. 
"""

VIEW_TYPE_CHOICES = (
    ("tv", "TemplateView"),
    ("fv", "FormView"),
    )

class GenericClassModel(models.Model):
    """
    Abstract class for the classes models.
    """
    name = models.CharField(max_length=50, help_text="App name.")
    app = models.ForeignKey("App", help_text="The app to which this class belongs.")
    
    def __unicode__(self):
        return self.name
    
    def class_name(self):
        """ Returns CamelCase class name. """
        return self.name.title().replace(" ", "")
        
    class Meta:
        abstract = True



class FormModel(GenericClassModel):
    output_file = models.CharField(max_length=50, default="forms.py", help_text="File to which this class should be written. Not implemented.")
    

class ClassModel(GenericClassModel):
    register_admin = models.BooleanField(help_text="Whether to register this class in the admin or not.")
    is_stacked = models.BooleanField(help_text="Whether this class in the admin is StackedInline.")
    is_tabular = models.BooleanField(help_text="Whether this class in the admin is TabularInline.")
    output_file = models.CharField(max_length=50, default="models.py", help_text="File to which this class should be written. Not implemented.")
    
    requires_pass = True

    def get_str_attribute(self):
        """ Detects the str attribute of this class. It is the first attribute found, regardless of other attributes found. """
        return self.regular_fields_set.filter(is_str=True)[0].name

    def admin_name(self):
        """ Returns CamelCase admin class name. """
        aname = self.class_name()+"Admin"
        if self.is_stacked or self.is_tabular:
            aname += "Inline"
        return str(aname)

    def admin_import(self):
        """ Returns a dictionary with keys app_name,class_name to be imported in the admin. """
        return {"app_name": self.app.get_sane_name(), "class_name": self.class_name()}

    def admin_register(self):
        """ Returns a dictionary with keys class_name,admin_name to be registered in the admin.
            Returns False if it's an inline class. (so it's not registered"""
        if "Inline" not in self.admin_name() and self.register_admin:
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
        fields = [f for f in self.regular_fields_set.all()]
        for f1 in self.relationship_this_class_set.all():
            fields.append(f1)
        return fields


    def get_inlines(self):
        return self.app.classmodel_set.filter(Q(is_stacked=True) | Q(is_tabular=True))



class ViewModel(GenericClassModel):
    #urls.py
    url_regex = models.CharField(max_length=100, blank=True, null=True, help_text="Regex of the URL that triggers this view.")
    #urls.py
    override_url_prefix = models.BooleanField(default=False, help_text="Views' URLs are prefixed by their app prefix. Set this to True to override this and put the URL of this view in the root path.")
    view_type = models.CharField(max_length=3, choices=VIEW_TYPE_CHOICES, help_text="The type of this view.")
    
    #only used with formview
    form_class = models.ForeignKey(FormModel, null=True, blank=True, help_text="Form to be used with this view. Only used in formview.")
    success_url = models.CharField(max_length=100, null=True, blank=True, help_text="The success URL to be used with this view. Only used in formview.")
    
    #only used with templateview
    template = models.ForeignKey("TemplateModel", null=True, blank=True, help_text="Template to be used with this view. Only used with templateview.")
    
    output_file = models.CharField(max_length=50, default="views.py", help_text="File to which this class should be written. Not implemented.")

    def get_view_type(self):
        """
        Returns the view type of this view. "template" for templateview or "form" for formview.
        :return: view type, string
        """
        if self.view_type == "tv":
            return "template"
        elif self.view_type == "fv":
            return "form"

        
