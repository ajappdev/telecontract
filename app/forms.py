# DJNAGO DECLARATIONS
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# APP DECLARATIONS
import app.models as am

# DECLARING CLASSES
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class TaskForm(forms.ModelForm):

    class Meta:
        model = am.Task
        fields = (
            'id',
            'version',
            'task_name',
            'task_description',
            'task_type',
            'task_end',
            'user_profile',
            'priority',
            'status')

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['version'].required = True
        self.fields['task_name'].required = True
        self.fields['task_description'].required = True
        self.fields['task_type'].required = True
        self.fields['task_end'].required = True
        self.fields['user_profile'].required = True
        self.fields['status'].required = True
        self.fields['priority'].required = True


class VersionForm(forms.ModelForm):

    class Meta:
        model = am.Version
        fields = ("project", "version_name", "date_of_release")

    def __init__(self, *args, **kwargs):
        super(VersionForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProjectForm(forms.ModelForm):

    class Meta:
        model = am.Project
        fields = ("company", "project_name", "project_description")

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'