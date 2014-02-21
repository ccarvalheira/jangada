import subprocess


from django.template.loader import render_to_string
import virtualenv

def write_to_file(file, stri):
    f = open(file,"w+")
    f.write(stri)
    f.close()

def export_project(modeladmin,request,queryset):
    p = queryset[0]
    project_name = p.get_sane_name()
    project_base_folder = "generated_projects"
    project_folder = "%s/%s" % (project_base_folder, project_name)

    #clean up
    subprocess.call("rm -rf %s" % project_folder, shell = True)

    ##create new project from template
    #subprocess.call("mkdir %s/%s/" % (project_base_folder, project_name), shell = True)

    subprocess.call("cp -r project_template %s/" % project_base_folder, shell = True)
    subprocess.call("mv %s/project_template %s/%s" % (project_base_folder, project_base_folder, project_name), shell = True)

    #generate requirements file
    write_to_file("%s/requirements.txt" % project_folder, p.get_requirements())
    
    #virtualenv.create_environment("%s/env/" % project_base_folder)
    
    #because installing takes too long...
    #request may timeout!
    #SHOULD_WE_INSTALL_REQUIREMENTS = False
    #if SHOULD_WE_INSTALL_REQUIREMENTS:
        #localshop = "-i http://localhost:9000/simple/"
    #    localshop = ""
    #    subprocess.call("cd %s && ../env/bin/pip install -r requirements.txt %s"
    #                % (project_folder, localshop), shell=True)
    
        #pip freeze and replace requirements file
        ###TODO
    #    VENV_RELATIVE_LOCATION = ""
    #else:
    #    VENV_RELATIVE_LOCATION = "../../../"

    #takes too long
    #SHOULD_WE_INSTALL_ZURB = False
    #if SHOULD_WE_INSTALL_ZURB:
    #    if "django-zurb-foundation" in p.get_requirements_list():
    #        subprocess.check_call("cd %s && foundation new foundation" % project_folder,shell=True)
    
    if "honcho" in p.get_requirements_list():
        write_to_file("%s/Procfile" % project_folder, p.Procfile_file_content())
        write_to_file("%s/Procfile_dev" % project_folder, p.Procfile_file_content(dev=True))
    
    write_to_file("%s/.env.example" % project_folder, p.example_env_content())
    
    write_to_file("%s/confs/settings.py" % project_folder, p.settings_file_content())

    write_to_file("%s/confs/urls.py" % project_folder, p.urlconf_file_content())
    
    try:
        base_name = p.templatemodel_set.filter(is_base=True)[0].name
        write_to_file("%s/templates/%s.html" % (project_folder, base_name), p.base_template_content())
    except IndexError as e:
        print "The project must have a base template."
        raise e
    
    for app in p.used_apps.all():
        #depending on the relative location, we either use the django in this venv or the one
        #in the newly created venv
        
        subprocess.call("cd %s/apps/ && mkdir %s" % (project_folder, app.get_sane_name()),shell=True)
        subprocess.call("cd %s/apps/%s && touch __init__.py" % (project_folder, app.get_sane_name()),shell=True)
        #call_startapp = "cd %s/apps && . %s../../env/bin/activate && python ../manage.py startapp %s" % (#project_base_folder,
        #    project_folder, VENV_RELATIVE_LOCATION, app.get_sane_name())
        #subprocess.check_call(call_startapp,shell=True)


        write_to_file("%s/apps/%s/models.py" % (project_folder,app.get_sane_name()), app.models_file_content()+"\n")
        #app.models_files()

        write_to_file("%s/apps/%s/admin.py" % (project_folder,app.get_sane_name()), app.admin_file_content()+"\n")
        
        write_to_file("%s/apps/%s/views.py" % (project_folder,app.get_sane_name()), app.views_file_content()+"\n")
        
        write_to_file("%s/apps/%s/urls.py" % (project_folder,app.get_sane_name()), app.urls_file_content()+"\n")
        
        #subprocess.call("cd %s/templates/ && mkdir %s" % (project_folder, app.get_sane_name()), shell=True)
        
        for view in app.viewmodel_set.all():
            write_to_file("%s/templates/%s.html" % (project_folder, view.template.name), view.template.template_file_contents())
        

    return


    ###TODO

    #install UI framework
    ###TODO



export_project.short_description = "Export project"
