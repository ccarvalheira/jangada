from django.test import TestCase

from apps.core.models import FieldModel
from apps.core.models import RelationshipFieldModel
from apps.core.models import ClassModel
from apps.core.models import App

from apps.core.models import Pip

"""
App
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True, null=True)
"""

"""
ClassModel
    name = models.CharField(max_length=50)
    app = models.ForeignKey(App)
    register_admin = models.BooleanField()
    is_stacked = models.BooleanField()
    is_tabular = models.BooleanField()
"""

"""
FieldModel
    name = models.CharField(max_length=50)
    this_class = models.ForeignKey(ClassModel)
    field_type = models.CharField(max_length=20,choices=FIELD_CHOICES)
    is_blank = models.BooleanField()
    is_null = models.BooleanField()
    is_str = models.BooleanField()
    list_display = models.BooleanField()
    filter_on_this = models.BooleanField()
    search_on_this = models.BooleanField()
"""

"""
FIELD_CHOICES = (
    ("char 10","CharField 10",),
    ("char 20","CharField 20"),
    ("char 50","CharField 50"),
    ("char 100","CharField 100"),
    ("int","IntegerField"),
    ("txt","TextField"),
    ("bool","BooleanField",),
    ("datetime autonow","DateTime autonow"),
    ("date autonow","Date now"),
    ("datetime","DateTime"),
    ("date","Date"),
)
"""

"""
class FieldModelTest(TestCase):
    def setUp(self):
        app = App(name="myapp",description="asd")
        app.save()

        tclass = ClassModel(name="post",app=app,register_admin=True,is_stacked=False,is_tabular=False)
        tclass.save()

        FieldModel.objects.create(name="title",this_class=tclass,
                                field_type="char 50",is_blank=False,is_null=False,is_str=True,list_display=True,
                                filter_on_this=False,search_on_this=True)
        FieldModel.objects.create(name="body",this_class=tclass,
                                field_type="text",is_blank=False,is_null=False,is_str=False,list_display=False,
                                filter_on_this=False,search_on_this=False)



    def test_field_definition_output(self):
        pass

"""


class ClassAppFieldModelTest(TestCase):
    def setUp(self):
        self.app = App(name="myapp",description="asd")
        self.app.save()

        self.tclass = ClassModel(name="post",app=self.app,register_admin=True,is_stacked=False,is_tabular=False)
        self.tclass.save()

        self.authorclass = ClassModel(name="author",app=self.app,register_admin=True,is_stacked=False,is_tabular=False)
        self.authorclass.save()

        self.f1 = FieldModel(name="title",this_class=self.tclass,
                                field_type="char 50",is_blank=False,is_null=False,is_str=True,list_display=True,
                                filter_on_this=False,search_on_this=True)

        self.f2 = FieldModel(name="body",this_class=self.tclass,
                                field_type="txt",is_blank=False,is_null=False,is_str=False,list_display=False,
                                filter_on_this=False,search_on_this=False)

        self.f3 = FieldModel(name="num_views",this_class=self.tclass,
                                field_type="int",is_blank=True,is_null=True,is_str=False,list_display=True,
                                filter_on_this=False,search_on_this=False)

        self.f4 = FieldModel(name="published",this_class=self.tclass,
                                field_type="bool",is_blank=False,is_null=True,is_str=False,list_display=True,
                                filter_on_this=True,search_on_this=False)

        self.f5 = FieldModel(name="lorem",this_class=self.tclass,
                                field_type="txt",is_blank=False,is_null=False,is_str=True,list_display=False,
                                filter_on_this=False,search_on_this=False,editable=False,default="Lorem Ipsum")

        self.f6 = RelationshipFieldModel(name="author",this_class=self.tclass,
                                is_blank=False,is_null=False, target_class=self.authorclass,key_type="fk")


        self.pizza_class = ClassModel(name="pizza",app=self.app,register_admin=True,is_stacked=False,is_tabular=False)
        self.pizza_class.save()

        self.top_class = ClassModel(name="toppings",app=self.app,register_admin=True,is_stacked=False,is_tabular=False)
        self.top_class.save()

        self.pizzaname = FieldModel(name="name",this_class=self.pizza_class,
                                field_type="char 50",is_blank=False,is_null=False,is_str=True,list_display=True,
                                filter_on_this=False,search_on_this=True)
        self.pizzaname.save()

        self.top_name = FieldModel(name="name",this_class=self.top_class,
                                field_type="char 50",is_blank=False,is_null=False,is_str=True,list_display=True,
                                filter_on_this=False,search_on_this=True)
        self.top_name.save()

        self.pizza_m2m = RelationshipFieldModel(name="toppings",this_class=self.pizza_class,
                                is_blank=False,is_null=False, target_class=self.top_class,key_type="m2m")

        self.space_class = ClassModel(name="spam and eggs",app=self.app,register_admin=True,is_stacked=False,is_tabular=False)
        self.space_class.save()

        self.stacked_class = ClassModel(name="inlinesta",app=self.app,register_admin=True,is_stacked=True,is_tabular=False)
        self.space_class.save()

        self.tabular_class = ClassModel(name="inlinetab",app=self.app,register_admin=True,is_stacked=False,is_tabular=True)
        self.space_class.save()

        self.both_inline_class = ClassModel(name="inlineboth",app=self.app,register_admin=True,is_stacked=True,is_tabular=True)
        self.space_class.save()

        self.f1.save()
        self.f2.save()
        self.f3.save()
        self.f4.save()
        self.f5.save()
        self.f6.save()


    def test_field_class(self):
        """ Checks whether the class of the field is correct. """
        self.assertEqual(self.f1.field_class(), "CharField")
        self.assertEqual(self.f2.field_class(), "TextField")
        self.assertEqual(self.f3.field_class(), "IntegerField")
        self.assertEqual(self.f4.field_class(), "BooleanField")

        self.assertEqual(self.f6.field_class(), "ForeignKey")
        self.assertEqual(self.pizza_m2m.field_class(), "ManyToManyField")

    def test_field_options(self):
        """ Checks if field options are being correctly returned. """
        self.assertItemsEqual(["max_length=50"], self.f1.field_options())
        self.assertItemsEqual([], self.f2.field_options())
        self.assertItemsEqual(["blank=True","null=True"], self.f3.field_options())
        self.assertItemsEqual(["null=True"], self.f4.field_options())
        self.assertItemsEqual(["editable=False","default=\"Lorem Ipsum\""], self.f5.field_options())
        self.assertItemsEqual(["Author"], self.f6.field_options())
        self.assertItemsEqual(["Toppings"], self.pizza_m2m.field_options())

    def test_class_name(self):
        """ Checks whether the correct CamelCase class name is returned. """
        self.assertEqual(self.pizza_class.class_name(), "Pizza")
        self.assertEqual(self.space_class.class_name(), "SpamAndEggs")

    def test_str_attribute(self):
        """ Checks whether the correct str attribute is detected. """
        self.assertEqual(self.tclass.get_str_attribute(), "title")
        self.assertEqual(self.top_class.get_str_attribute(), "name")

    def test_admin_class(self):
        """ Checks whether the correct CamelCase admin class name is returned. """
        self.assertEqual(self.tclass.admin_name(), "PostAdmin")
        self.assertEqual(self.space_class.admin_name(), "SpamAndEggsAdmin")
        self.assertEqual(self.stacked_class.admin_name(), "InlinestaAdminInline")
        self.assertEqual(self.tabular_class.admin_name(), "InlinetabAdminInline")
        self.assertEqual(self.both_inline_class.admin_name(), "InlinebothAdminInline")

    def test_admin_inherit(self):
        """ Checks whether the correct admin class is inherited. """
        self.assertEqual(self.stacked_class.admin_class_inherit(), "StackedInline")
        self.assertEqual(self.tabular_class.admin_class_inherit(), "TabularInline")
        self.assertEqual(self.both_inline_class.admin_class_inherit(), "StackedInline")
        self.assertEqual(self.tclass.admin_class_inherit(), "ModelAdmin")


class PipTest(TestCase):
    def setUp(self):
        self.p1 = Pip(name="south", installed_apps_text="south\nthings", requirements_pkg_name="South")
        self.p2 = Pip(name="south versioned", installed_apps_text="south\nother_things", requirements_pkg_name="South", requirements_version="0.6.0")
        self.p3 = Pip(name="south versioned oneiapp", installed_apps_text="south", requirements_pkg_name="South", requirements_version="0.6.0")

        self.p1.save()
        self.p2.save()
        self.p3.save()

    def test_requirements(self):
        """ Checks if requirements for pip format are returned correctly """
        self.assertEqual(self.p1.get_requirements(), "South")
        self.assertEqual(self.p2.get_requirements(), "South==0.6.0")

    def test_installed_apps_pip(self):
        """ Checks if installed apps list for this pip is correct """
        self.assertItemsEqual(["south","things"], self.p1.installed_apps_list())
        self.assertItemsEqual(["south","other_things"], self.p2.installed_apps_list())
        self.assertItemsEqual(["south"], self.p3.installed_apps_list())





