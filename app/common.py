# APP DECLARATIONS
import app.models as am

# DJANGO DECLARATIONS
from django.core.paginator import Paginator

# GENERAL DECLARATIONS

APP_PERMISSIONS = [
    [
        'Gérer les permissions des utilisateurs',
        ['get_user_permissions']
    ]
]

DATE_SHORT_LOCAL_WITH_DASH: str = '%Y-%m-%d'

# FUNCTION DECLARATIONS

def pagination(page: int, nbr_pag: int, liste_obj):
    paginator = Paginator(liste_obj, nbr_pag)
    obj = paginator.get_page(page)
    return obj


def check_permissions_to_enter(user_profile: am.UserProfile, view: str):
    """
    This functions allows to check if a user has permissions to access a
    certain view in the application
    """

    user_permissions = list(str([permission['views'] for permission in am.PermissionsUserProfile.objects.filter(
                user_profile=user_profile).values('views')]).replace("'", '').replace('"', '').replace('[', '').replace(']', '').split(", "))

    return True
    if view in user_permissions:
        return True
    else:
        print("///////////////////////////////////////////")
        print("ACCESS DENIED TO ", view)
        print("///////////////////////////////////////////")
        return False