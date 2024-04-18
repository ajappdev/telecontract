# DJANGO DECLARATIONS
from django.urls import path, include

# APP DECLARATIONS
import app.views as av


urlpatterns = [
    path('', av.landing_page, name='landing_page'),
    path('ajax-calls/', av.ajax_calls, name='ajax_calls'),
    path('contrat/add/', av.add_contrat, name='add_contrat'),
    path('contrat/filtre/', av.contrats, name='contrats'),
    path('contrat/edit/<int:pk>', av.edit_contrat, name='edit_contrat'),
    path('prolongation/<int:pk>', av.get_prolongation_file, name='get_prolongation_file'),
    path('settings/manage-user/', av.manage_users, name='manage_users'),
    path('no-permissions/', av.no_permissions, name='no_permissions'),
    path('save-cycle/', av.save_cycle, name='save_cycle'),
    path('afficher-document/<int:pk>', av.afficher_document, name='afficher_document'),
]


urlpatterns += [
    path('auth/', include('django.contrib.auth.urls')),
]