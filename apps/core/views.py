from django.shortcuts import render
from vanilla import TemplateView

from apps.core.models import App

class HomeView(TemplateView):
    template_name = "models_template.jinja"
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        app = App.objects.get(id=int(self.kwargs["app"]))
        all_apps = app.classmodel_set.all().order_by("name")
        all_apps_sorted = sorted(all_apps, key=lambda num: len(num.relationship_fields_set.all()), reverse=True)
        context["class_list"] = all_apps_sorted #.order_by("relationship_fields_set").order_by("name")
        return context





