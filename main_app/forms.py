from django import forms

from .models import Household

class HouseholdForm (forms.ModelForm) :
    passcode = forms.CharField(widget = forms.PasswordInput)
    passcode_confirmation = forms.CharField(widget = forms.PasswordInput)

    class Meta :
        model = Household
        fields = ('street_address', 'city', 'state', 'zip_code', 'passcode')

    def clean (self) :
        cleaned_data = super().clean()
        passcode = cleaned_data.get('passcode')
        passcode_confirmation = cleaned_data.get('passcode_confirmation')

        if passcode and passcode != passcode_confirmation :
            self.add_error('passcode_confirmation', 'Passcodes do not match.')
        
        return cleaned_data