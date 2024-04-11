# APP DECLARATIONS
import app.models as am

# GENERAL DECLARATIONS

APP_PERMISSIONS = [
    [
        'See projects list',
        ['projects_list']
    ]
]

# FUNCTION DECLARATIONS

def check_permissions_to_enter(user_profile: am.UserProfile, view: str):
    """
    This functions allows to check if a user has permissions to access a
    certain view in the application
    """

    user_permissions = list(str([permission['views'] for permission in am.PermissionsUserProfile.objects.filter(
                user_profile=user_profile).values('views')]).replace("'", '').replace('"', '').replace('[', '').replace(']', '').split(", "))

    if view in user_permissions:
        return 200
    else:
        print("///////////////////////////////////////////")
        print("ACCESS DENIED TO ", view)
        print("///////////////////////////////////////////")
        return 400