# DJANGO DECLARATIONS
from django.urls import path, include

# APP DECLARATIONS
import app.views as av


urlpatterns = [
    path('', av.landing_page, name='landing_page'),
    path('auth/register/', av.register, name='register'),
    path('ajax-calls/', av.ajax_calls, name='ajax_calls'),
    path('contrat/add/', av.add_contrat, name='add_contrat'),
    path('contrat/filtre/', av.contrats, name='contrats'),
    path('contrat/edit/<int:pk>', av.edit_contrat, name='edit_contrat'),
    path('prolongation/<int:pk>', av.get_prolongation_file, name='get_prolongation_file'),
    path('settings/manage-user/', av.manage_users, name='manage_users'),
    path('no-permissions/', av.no_permissions, name='no_permissions')
]


urlpatterns += [
    path('auth/', include('django.contrib.auth.urls')),
]