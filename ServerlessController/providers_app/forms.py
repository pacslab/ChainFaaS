from django import forms
from profiles.models import Provider


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ('ram', 'cpu')
