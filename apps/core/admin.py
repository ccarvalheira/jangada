
from django.contrib import admin

from apps.core.models import Project
from apps.core.models import Pip
from apps.core.models import App
from apps.core.models import ClassModel
from apps.core.models import FieldModel
from apps.core.models import RelationshipFieldModel
from apps.core.models import ViewModel
from apps.core.models import FormModel
from apps.core.models import FormFieldModel
from apps.core.models import TemplateModel

from apps.core.export_utility import export_project

class PipAdmin(admin.ModelAdmin):
    pass

class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ["used_pips", "used_apps"]
    actions = [export_project]


class FieldModelInlineAdmin(admin.TabularInline):
    model = FieldModel

class ClassModelInlineAdmin(admin.TabularInline):
    model = ClassModel

class RelationshipFieldModelAdmin(admin.TabularInline):
    model = RelationshipFieldModel
    fk_name = "this_class"

class AppAdmin(admin.ModelAdmin):
    inlines = [ClassModelInlineAdmin]
    list_display = ("name",)

class ClassModelAdmin(admin.ModelAdmin):
    inlines = [FieldModelInlineAdmin, RelationshipFieldModelAdmin]
    list_filter = ("app__name",)
    list_display = ("name",)

class FieldModelAdmin(admin.ModelAdmin):
    list_display = ("name", "is_str")
    list_filter = ("this_class__name",)

class FormFieldModelAdmin(admin.TabularInline):
    model = FormFieldModel

class FormModelAdmin(admin.ModelAdmin):
    inlines = [FormFieldModelAdmin]

class ViewModelAdmin(admin.ModelAdmin):
    pass

class TemplateModelAdmin(admin.ModelAdmin):
    pass

admin.site.register(Pip, PipAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(App, AppAdmin)
admin.site.register(ClassModel, ClassModelAdmin)
#admin.site.register(FieldModel, FieldModelAdmin)
admin.site.register(ViewModel, ViewModelAdmin)
admin.site.register(FormModel, FormModelAdmin)
admin.site.register(TemplateModel, TemplateModelAdmin)
#admin.site.register(RelationshipFieldModel, RelationshipFieldModelAdmin)



