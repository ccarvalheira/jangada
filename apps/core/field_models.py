from django.db import models

from django.template.loader import render_to_string
from django.db.models import Q

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


KEY_TYPES = (
    ("fk", "ForeignKey"),
    ("m2m", "ManyToManyField"),
)



FORM_FIELD_CHOICES = (
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
    """
    Abstract class for the fields classes.
    """
    name = models.CharField(max_length=50, help_text="Name of this field.")
    is_blank = models.BooleanField(help_text="Whether this field has the attribute 'blank'.")
    is_null = models.BooleanField(help_text="Whether this field has the attribute 'null'.")

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
    
    def get_name(self):
        return self.name.lower().replace(" ","")


class RelationshipFieldModel(GenericFieldModel):
    """
    Abstract class for relationship-type fields.
    """
    this_class = models.ForeignKey("ClassModel", related_name="relationship_this_class_set")
    target_class = models.ForeignKey("ClassModel", related_name="relationship_fields_set")
    key_type = models.CharField(max_length=30, choices=KEY_TYPES)


    def field_options(self):
        """ Returns list of field options. If more are needed, insert ifs/elifs. """
        opt = [op for op in self.base_field_options()]
        opt = ['"'+self.target_class.class_name()+'"'] + opt #the class name referenced
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


class FieldModel(GenericFieldModel):
    this_class = models.ForeignKey("ClassModel", related_name="regular_fields_set", help_text="The models to which this field belongs to.")
    field_type = models.CharField(max_length=20, choices=FIELD_CHOICES, help_text="The type of this field.")
    is_str = models.BooleanField(help_text="Whether this field is the string representation of this class. Only one field in this class may have this attribute. If more than one, the first will be chosen.")
    list_display = models.BooleanField(help_text="Whether to include this field in the 'list_display' attribute of the respective admin class.")
    filter_on_this = models.BooleanField(help_text="Whether to include this field in the 'list_filter' attribute of the respective admin class.")
    search_on_this = models.BooleanField(help_text="Whether to include this field in the 'search_fields' attribute of the respective admin class.")
    default = models.CharField(max_length=200, blank=True, help_text="The default value of this field. This value will be taken as is (so if you want a string as the default you should write 'mydefault'.")
    editable = models.BooleanField(default=True, help_text="Whether this field has the attribute editable.")

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
            opt.append("default=%s" % self.default)
        if self.field_class() == "CharField":
            opt.append("max_length=%s" % self.field_type.split()[1])

        return opt


class FormFieldModel(GenericFieldModel):
    form_model = models.ForeignKey("FormModel")
    field_type = models.CharField(max_length=20, choices=FORM_FIELD_CHOICES)
