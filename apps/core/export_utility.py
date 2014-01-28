import subprocess


from django.template.loader import render_to_string
import virtualenv

def export_project(modeladmin,request,queryset):
    p = queryset[0]
    project_name = p.get_sane_name()
    project_base_folder = "generated_projects/%s" % project_name
    project_folder = "%s/%s" % (project_base_folder, project_name)

    #clean up
    subprocess.call("rm -rf %s" % project_base_folder, shell = True)

    ##create new project from template
    subprocess.call("cd generated_projects && mkdir %s/" % project_name, shell = True)

    subprocess.call("cp -r project_template %s" % project_base_folder, shell = True)
    subprocess.call("mv %s/project_template %s/%s" % (project_base_folder, project_base_folder, project_name), shell = True)

    #generate requirements file
    freq = open("%s/requirements.txt" % project_folder,"w")
    freq.write(p.get_requirements())
    freq.close()
    
    virtualenv.create_environment("%s/env/" % project_base_folder)
    
    #because installing takes too long...
    #request may timeout!
    SHOULD_WE_INSTALL_REQUIREMENTS = False
    if SHOULD_WE_INSTALL_REQUIREMENTS:
        #localshop = "-i http://localhost:9000/simple/"
        localshop = ""
        subprocess.call("cd %s && ../env/bin/pip install -r requirements.txt %s"
                    % (project_folder, localshop), shell=True)
    
        #pip freeze and replace requirements file
        ###TODO
        VENV_RELATIVE_LOCATION = ""
    else:
        VENV_RELATIVE_LOCATION = "../../../"
    #process apps
    #write settings
    fset = open("%s/confs/settings.py" % project_folder, "w")
    fset.write(p.settings_file_content())
    fset.close()
    
    #write urlconf
    furl = open("%s/confs/urls.py" % project_folder, "w")
    furl.write(p.urlconf_file_content())
    furl.close()
    
    for app in p.used_apps.all():
        #depending on the relative location, we either use the django in this venv or the one
        #in the newly created venv
        call_startapp = "cd %s/apps && . %s../../env/bin/activate && python ../manage.py startapp %s" % (#project_base_folder,
            project_folder, VENV_RELATIVE_LOCATION, app.get_sane_name())
        subprocess.check_call(call_startapp,shell=True)

        #write models
        fmodels = open("%s/apps/%s/models.py" % (project_folder,app.name),"w")
        fmodels.write(app.models_file_content()+"\n")
        fmodels.close()

        #write admin
        fadmin = open("%s/apps/%s/admin.py" % (project_folder,app.name),"w")
        fadmin.write(app.admin_file_content()+"\n")
        fadmin.close()

    return


    ###TODO

    #install UI framework
    ###TODO



export_project.short_description = "Export project"
