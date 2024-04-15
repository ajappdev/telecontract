# DJANGO DECLARATIONS
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings

# APP DECLARATIONS
import app.models as am
import app.forms as af
import app.common as ac
import app.methods as af

# GENERAL DECLARATIONS
import os
import json
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import random

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
def add_contrat(request):
    template = 'contrat/add-edit-contrat.html'
    context = {}
    return render(request, template, context)


@login_required(login_url='/auth/login/')
def edit_contrat(request, pk: int):
    contrat = am.Contrat.objects.get(id=pk)
    articles = am.Article.objects.filter(contrat=contrat)
    articles_list = [
        {"numero_mobile": a.numero_mobile,
         "designation": a.designation,
         "mensualite": a.mensualite} for a in articles]
    template = 'contrat/add-edit-contrat.html'
    context = {"contrat": contrat, "articles_list": articles_list}
    return render(request, template, context)


@login_required(login_url='/auth/login/')
def contrats(request):
    template = 'contrat/contrats.html'
    context = {}
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
def get_prolongation_file(request, pk):
    cycle = am.Cycle.objects.get(id=pk)
    return af.generate_pdf(request, cycle)

@login_required(login_url='/auth/login/')
def afficher_document(request, pk: int):
    cycle = am.Cycle.objects.get(id=pk)
    file_name = ""
    for filename in os.listdir('media/documents/'):
        name, extension = os.path.splitext(filename)
        if name == str(cycle.id):
            file_name = name + extension

    if file_name != "":
        return render(
            request, 'view-file.html',
            {'file_name': file_name,
                "MEDIA_URL": settings.MEDIA_URL})
    else:
        return render(request, 'file-not-found.html')

@login_required(login_url='/auth/login/')
def save_cycle(request):

    if request.method == 'POST':
        cycle_id = request.POST.get('cycle_id')
        new_date_debut = request.POST.get('new_date_debut')
        new_date_fin = request.POST.get('new_date_fin')
        file = request.FILES.get('file')

        cycle = am.Cycle.objects.get(
            id=int(cycle_id))
        if cycle.statut == "En cours":
            cycle.date_debut = datetime.strptime(
                str(new_date_debut),
                ac.DATE_SHORT_LOCAL_WITH_DASH)
            cycle.date_fin = datetime.strptime(
                str(new_date_fin),
                ac.DATE_SHORT_LOCAL_WITH_DASH)
            cycle.save()

        if file:
            file_name, file_extension = os.path.splitext(file.name)

            for filename in os.listdir('media/documents/'):
                name, extension = os.path.splitext(filename)
                if name == str(cycle.id):
                    file_path = os.path.join("media/documents/", filename)
                    os.remove(file_path)

            with open(f'media/documents/{cycle.id}{file_extension}', 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)

        data_dict = {
            "date_debut": cycle.date_debut.strftime(ac.DATE_SHORT_LOCAL_WITH_DASH),
            "date_fin": cycle.date_fin.strftime(ac.DATE_SHORT_LOCAL_WITH_DASH),
            "statut": cycle.statut}
        
    return JsonResponse(data=data_dict, safe=False)

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

        elif action == "delete_file":
            cycle = am.Cycle.objects.get(id=int(received_json_data['cycle_id']))
            for filename in os.listdir('media/documents/'):
                name, extension = os.path.splitext(filename)
                if name == str(cycle.id):
                    file_path = os.path.join("media/documents/", filename)
                    os.remove(file_path)
            data_dict = {}

        elif action == "filter_contrats_list":

            filter_contrat_end_in = received_json_data['filter_contrat_end_in']
            contrat_date = received_json_data['date_contrat']
            numero_client = received_json_data['numero_client']
            raison_sociale = received_json_data['raison_sociale']
            filter_contrat_telephone = received_json_data['filter_contrat_telephone']
            rue = received_json_data['rue']
            zipcode = received_json_data['zipcode']
            npa = received_json_data['npa']
            localite = received_json_data['localite']
            nom_interlocuteur = received_json_data['nom_interlocuteur']
            prenom_interlocuteur = received_json_data['prenom_interlocuteur']
            
            page = received_json_data['page']

            if contrat_date:
                contrat_before = datetime.strptime(
                    str(contrat_date.split(" - ")[1]),
                    ac.DATE_SHORT_LOCAL_WITH_DASH)
                contrat_after = datetime.strptime(
                    str(contrat_date.split(" - ")[0]),
                    ac.DATE_SHORT_LOCAL_WITH_DASH)

                contrats = am.Contrat.objects.filter(
                    numero_client__icontains = numero_client,
                    raison_sociale__icontains = raison_sociale,
                    rue__icontains = rue,
                    zipcode__icontains = zipcode,
                    npa__icontains = npa,
                    localite__icontains = localite,
                    nom_interlocuteur__icontains = nom_interlocuteur,
                    prenom_interlocuteur__icontains = prenom_interlocuteur,
                    date_contrat__lte=contrat_before,
                    date_contrat__gte=contrat_after
                ).order_by("-date_contrat")

            else:
                contrats = am.Contrat.objects.filter(
                numero_client__icontains = numero_client,
                raison_sociale__icontains = raison_sociale,
                rue__icontains = rue,
                zipcode__icontains = zipcode,
                npa__icontains = npa,
                localite__icontains = localite,
                nom_interlocuteur__icontains = nom_interlocuteur,
                prenom_interlocuteur__icontains = prenom_interlocuteur,
                ).order_by("-date_contrat")

            if filter_contrat_telephone != "":
                articles = am.Article.objects.filter(
                    contrat_id__in=[c.id for c in contrats],
                    numero_mobile__icontains=filter_contrat_telephone)
                contrats = [a.contrat for a in articles]

            if filter_contrat_end_in != "":
                jours = int(filter_contrat_end_in.split(" jours")[0])
                jour_reference = date.today() + timedelta(jours)
            else:
                jour_reference = date.today() + timedelta(60000)

            cycles = am.Cycle.objects.filter(
                contrat_id__in=[c.id for c in contrats],
                statut='En cours',
                date_fin__lte=jour_reference).order_by("date_fin")
            
            contrats = [c.contrat for c in cycles]

            contrats_list = ac.pagination(page, 10, contrats)

            html = render_to_string(
                        template_name="contrat/widgets/table-contrats.html", 
                        context={
                            "contrats": contrats_list,
                            "MEDIA_URL": settings.MEDIA_URL
                        }
                    )
            
            data_dict = {"html": html}

        elif action == "delete_contrat":
            error = 0
            error_text = ""
            try:
                am.Contrat.objects.filter(
                    id=int(received_json_data['contrat_id'])).delete()
            except Exception as e:
                error_text = "EXCEPTION, AJAX_CALLS, DELETE_CONTRAT, 1, " + str(e)
                error = 1
            data_dict = {"error": error, "error_text": str(error_text)}

        elif action == "save_contrat":
            error_message = ""
            errors = 0
            contrat_id = 0
            try:
                id_contrat = int(received_json_data['id_contrat'])
                data = received_json_data['data']
                if id_contrat > 0:
                    contrat = am.Contrat.objects.get(id=id_contrat)
                else:
                    contrat = am.Contrat()
                contrat.numero_client = data['numero_client']
                contrat.raison_sociale = data['raison_sociale']
                contrat.rue = data['rue']
                contrat.zipcode = data['zipcode']
                contrat.npa = data['npa']
                contrat.localite = data['localite']
                contrat.sexe_interlocuteur = data['sexe_interlocuteur']
                contrat.nom_interlocuteur = data['nom_interlocuteur']
                contrat.prenom_interlocuteur = data['prenom_interlocuteur']
                contrat.duree_contrat = int(data['duree_contrat'])
                try:
                    contrat.date_contrat = datetime.strptime(
                        str(data['date_contrat']),
                        ac.DATE_SHORT_LOCAL_WITH_DASH)
                except Exception as e:
                    print(e)
                    contrat.date_contrat = date.today()
                contrat.save()
                contrat_id = contrat.id
                if id_contrat == 0:
                    new_cycle = am.Cycle()
                    new_cycle.contrat = contrat
                    new_cycle.date_debut = contrat.date_contrat
                    new_cycle.date_fin = contrat.date_contrat + relativedelta(
                        months=contrat.duree_contrat)
                    new_cycle.duree_prolongation = contrat.duree_contrat
                    new_cycle.save()
                am.Article.objects.filter(contrat=contrat).delete()
                for c in data['articles']:
                    new_article = am.Article()
                    new_article.contrat = contrat
                    new_article.numero_mobile = c['numero_mobile']
                    new_article.designation = c['designation']
                    new_article.mensualite = float(c['mensualite'])
                    new_article.save()
            except Exception as e:
                error_message = e
                errors = 1
            data_dict = {"error_message": str(error_message), "errors": errors, "contrat_id": contrat_id}

        elif action == "get_cycle_info":
            cycle = am.Cycle.objects.get(
                id=int(received_json_data['cycle_id']))
            file_name = ""
            for filename in os.listdir('media/documents/'):
                name, extension = os.path.splitext(filename)
                if name == str(cycle.id):
                    file_name = name + extension
            print(settings.MEDIA_URL)
            data_dict = {
                "date_debut": cycle.date_debut.strftime(ac.DATE_SHORT_LOCAL_WITH_DASH),
                "date_fin": cycle.date_fin.strftime(ac.DATE_SHORT_LOCAL_WITH_DASH),
                "statut": cycle.statut,
                "paye_le": cycle.statut,
                "file_name": file_name,
                "MEDIA_URL": settings.MEDIA_URL,
                "duree_prolongation": cycle.duree_prolongation}
            
        elif action == "marquer_cycle_comme_paye":
            errors = 0
            error_message = ""
            try:
                cycle = am.Cycle.objects.get(
                    id=int(received_json_data['cycle_id']))
                cycle.statut = "Payé"
                cycle.date_fin = date.today()
                cycle.paye_le = date.today()
                cycle.duree_prolongation = relativedelta(date.today(), cycle.date_debut).month
                cycle.save()
                new_cycle = am.Cycle()
                new_cycle.contrat = cycle.contrat
                new_cycle.date_debut = date.today()
                new_cycle.date_fin = date.today() + relativedelta(
                    months=cycle.contrat.duree_contrat)
                new_cycle.duree_prolongation = relativedelta(new_cycle.date_fin, date.today()).month
                new_cycle.save()
            except Exception as e:
                errors = 1
                error_message = e
            data_dict = {"errors": errors, "error_message": str(error_message)}

        elif action == "supprimer_cycle_payment":
            errors = 0
            error_message = ""
            try:
                contrat = am.Cycle.objects.get(
                    id=int(received_json_data['cycle_id'])).contrat
                am.Cycle.objects.filter(
                    id=int(received_json_data['cycle_id'])).delete()
                if len(contrat.cycles()) == 0:
                    new_cycle = am.Cycle()
                    new_cycle.contrat = contrat
                    new_cycle.date_debut = date.today()
                    new_cycle.date_fin = date.today() + relativedelta(
                        months=contrat.duree_contrat)
                    new_cycle.duree_prolongation = contrat.duree_contrat
                    new_cycle.save()
                else:
                    dernier_cycle = am.Cycle.objects.filter(
                        contrat=contrat).order_by("-id")[0]
                    dernier_cycle.statut = "En cours"
                    dernier_cycle.paye_le = None
                    dernier_cycle.save()
            except Exception as e:
                errors = 1
                error_message = e
            data_dict = {"errors": errors, "error_message": str(error_message)}
            
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