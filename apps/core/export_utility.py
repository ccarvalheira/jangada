import subprocess


from django.template.loader import render_to_string

"""
def list_dquot(req):
        result = "["
        for r in req:
            result += '"'+r+'",'
        result = result[:len(result)-1]
        result += "]"
        return result
"""

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

    #create venv and install pips
    #TODO uncomment with pip install is working
    #subprocess.check_call("virtualenv %s/env" % project_base_folder, shell = True)

    #TODO
    #wtf not installing pips...
    #subprocess.call(". %s/env/bin/activate %% pip install -r %s/requirements.txt -i http://localhost:9000/simple/" % (project_base_folder, project_folder), shell = True)

    #pip freeze and replace requirements file
    ###TODO

    #process apps
    for app in p.used_apps.all():
        #write settings
        fset = open("%s/confs/settings.py" % project_folder, "w")
        fset.write(p.settings_file_content())
        fset.close()

        #using generic venv with django for now! FIXME
        #replace ".." with "%s" and uncomment end of following line
        call_startapp = "cd %s/apps && . ../../../../../env/bin/activate && python ../manage.py startapp %s" % (#project_base_folder,
            project_folder, app.name)
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
