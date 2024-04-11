# DJANGO DECLARATIONS
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count, F, Max, Min


# DECLARING GLOBAL VARIABLES
TASK_END_TYPES = [
    ('Front end', 'Front end'),
    ('Back end', 'Back end'),
    ('Full stack', 'Full stack')
]

TASK_TYPES = [
    ('Bug', 'Bug'),
    ('Small adjustment', 'Small adjustment'),
    ('Architecture tuning', 'Architecture tuning'),
    ('New feature', 'New feature'),
]

TASK_STATUS = [
    ('Open', 'Open'),
    ('In progress', 'In progress'),
    ('Pending verification', 'Pending verification'),
    ('Closed', 'Closed'),
]

PRIORITY_TYPES = [
    ('Normal', 'Normal'),
    ('Urgent', 'Urgent'),
    ('Critical', 'Critical'),
]


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_profile')
    complete_name = models.CharField(
        max_length=200,
        blank=False,
        null=False)
    permissions = models.TextField(default='*')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.complete_name
        

class PermissionsUserProfile(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=False, blank=False)
    permission_name = models.CharField(
        max_length=200,
        blank=False,
        null=False)
    views = models.TextField(null=False, blank=False)

