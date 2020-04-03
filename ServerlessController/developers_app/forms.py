from django import forms
from developers_app.models import Services


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ('name', 'docker_container')
