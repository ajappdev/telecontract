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


@admin.register(am.Contrat)
class ContratAdmin(admin.ModelAdmin):
    pass

@admin.register(am.Article)
class ArticleAdmin(admin.ModelAdmin):
    pass

@admin.register(am.Cycle)
class CycleAdmin(admin.ModelAdmin):
    pass
