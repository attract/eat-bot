from django import forms

from core.widgets import PhotoWidget
from users.models import User


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        exclude = []
        widgets = {
            'photo': PhotoWidget(),
        }