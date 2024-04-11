# DJANGO DECLARATIONS
from django.contrib import admin

# IMPORTATIONS DISTRIPHA
import app.models as am


@admin.register(am.PermissionsUserProfile)
class PermissionsUserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(am.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass
