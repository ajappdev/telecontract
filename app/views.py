# DJANGO DECLARATIONS
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# APP DECLARATIONS
import app.models as am
import app.forms as af
import app.common as ac

# GENERAL DECLARATIONS
import json


# DECLARING FONCTIONS
@login_required(login_url='/auth/login/')
def landing_page(request):
    template = 'blank.html'
    context = {}
    return render(request, template, context)


def register(request):
    register_form = af.RegisterForm()
    registration_errors = ""
    if request.method == "POST":
        register_form = af.RegisterForm(request.POST)
        if register_form.is_valid():
            print("sss")
            if am.User.objects.filter(email=request.POST['email']).exists():
                registration_errors = "Another account exists with the same email"
                template = 'registration/register.html'
                context = {
                    "register_form": register_form,
                    "registration_errors": registration_errors}
                return render(request, template, context)

            elif request.POST['password1'] != request.POST['password2']:
                registration_errors = "The two passwords are not identical"
                template = 'registration/register.html'
                context = {
                    "register_form": register_form,
                    "registration_errors": registration_errors}
                return render(request, template, context)
            else:
                user = am.User.objects.create_user(
                    request.POST['email'].split("@")[0],
                    request.POST['email'],
                    request.POST['password1']
                )
                company = am.Company()
                company.company_name = request.POST['id_company']
                company.save()

                user_profile = am.UserProfile()
                user_profile.user = user
                user_profile.complete_name = request.POST['id_complete_name']
                user_profile.company = company
                user_profile.save()

                # Giving all permissions to the user
                for per in ac.APP_PERMISSIONS:
                    user_permission = am.PermissionsUserProfile()
                    user_permission.user_profile = user_profile
                    user_permission.permission_name = per[0]
                    user_permission.views = [view for view in per[1]]
                    user_permission.save()

                login(request, user)

                return redirect("/")
        else:
            registration_errors = register_form.errors

    template = 'registration/register.html'
    context = {
        "register_form": register_form,
        "registration_errors": registration_errors}
    return render(request, template, context)


@login_required(login_url='/auth/login/')
def projects_list(request):
    """
    In this view, we see the list of projects with a button to see the roadmap
    and detail of versions
    """

    projects = am.Project.objects.filter(
        company=request.user.user_profile.company)

    template = 'project/projects-list.html'
    context = {
        "page_title": "Projects list",
        "projects": projects}
    return render(request, template, context)


@login_required(login_url='/auth/login/')
def add_project(request):
    form = af.ProjectForm(initial={'company':request.user.user_profile.company})
    errors = ""
    success = 0
    if request.method == "POST":
        form = af.ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/projects/?message_success=3")
        else:
            errors = form.errors

    template = 'project/add-project.html'
    context = {
        "form": form,
        "errors": errors,
        "success": success}
    return render(request, template, context)


###############################################
# User management bloc #
###############################################


@login_required(login_url='/auth/login/')
def manage_users(request):

    users = am.UserProfile.objects.filter(~Q(user_id=request.user.id))
    app_permissions_list = [perm[0] for perm in ac.APP_PERMISSIONS]

    template = 'settings/manage-users.html'
    context = {
        "users": users,
        "page_title": "Manage users",
        "app_permissions_list": app_permissions_list}
    return render(request, template, context)


def no_permissions(request):

    template = 'no-permissions.html'
    context = {}
    return render(request, template, context)

@login_required(login_url='/auth/login/')
def ajax_calls(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        action = received_json_data['action']

        if not ac.check_permissions_to_enter(
                request.user.user_profile, "ajax_" + action):
            data_dict = {"no_permission": True}

        elif action == "get_user_permissions":
            user_id = received_json_data['user_id']
            user_permissions = list(am.PermissionsUserProfile.objects.filter(
                user_profile=am.UserProfile.objects.get(
                    user_id=user_id)).values("permission_name"))
            user_permissions = [p['permission_name'] for p in user_permissions]
            all_permissions = [p[0] for p in ac.APP_PERMISSIONS]
            html_return = '''<div style="padding:10px; text-align:left;">'''

            for permission in all_permissions:
                html_return += '''
                        <div class="checkbox-fade fade-in-primary">
                        <label class="permission_label">'''

                if permission in user_permissions:
                    html_return += '''
                            <input class="permission_label_checkbox" type="checkbox" checked="" value="">'''
                else:
                    html_return += '''
                            <input class="permission_label_checkbox" type="checkbox" value="">'''

                html_return += '''
                            <span class="cr">
                                <i class="cr-icon icofont icofont-ui-check txt-primary"></i>
                            </span>
                            <span class="permission_text">'''+permission+'''</span>
                            </label>
                            </div><br>'''

            html_return += '</div>'

            data_dict = {"html_return": html_return}

        elif action == "save_user_permissions":
            permissions_array = received_json_data['permissions_array']
            user_id = received_json_data['user_id']
            am.PermissionsUserProfile.objects.filter(
                user_profile=am.UserProfile.objects.get(
                    user_id=user_id)).delete()

            for permission in permissions_array:
                for per in ac.APP_PERMISSIONS:
                    if per[0] == permission: 
                        user_permission = am.PermissionsUserProfile()
                        user_permission.user_profile = am.UserProfile.objects.get(
                            user_id=user_id)
                        user_permission.permission_name = permission
                        user_permission.views = [view for view in per[1]]
                        user_permission.save()
                        break

            data_dict = {}

        elif action == "add_user":

            nv_id = 0
            if am.User.objects.filter(
                    email=received_json_data['user_email']).exists():
                message = "Un autre utilisateur avec cet email existe déja"
                status = "Error"
            else:
                user = am.User.objects.create_user(
                    received_json_data['user_email'].split("@")[0],
                    received_json_data['user_email'],
                    received_json_data['user_password']
                )
                nv_id = user.id
                user_profile = am.UserProfile()
                user_profile.user = user
                user_profile.complete_name = received_json_data['user_nom']
                user_profile.save()
                message = "Utilisateur crée avec succès!"
                status = "Success"
            data_dict = {"nv_id": nv_id, "message": message, "status": status}
            
        elif action == "delete_user":
            am.User.objects.filter(
                id=received_json_data["id_to_delete"]).delete()
            data_dict = {}


    return JsonResponse(data=data_dict, safe=False)




