from django import forms

from .models import Household, Member, Store

class HouseholdCreateForm (forms.ModelForm) :
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
    
class HouseholdLoginForm (forms.Form) :
    street_address = forms.CharField(max_length = 100, label = 'Street Address')
    city = forms.CharField(max_length = 100, label = 'City')
    state = forms.CharField(max_length = 2, label = 'State')
    zip_code = forms.CharField(max_length = 5, label = 'Zip Code')
    passcode = forms.CharField(widget = forms.PasswordInput, label = 'Passcode')

    def clean (self) : 
        cleaned_data = super().clean()

        for field in ['street_address', 'city', 'state'] :
            cleaned_data[field] = cleaned_data[field].strip().lower()
        
        cleaned_data['zip_code'] = cleaned_data['zip_code'].strip()
        
        return cleaned_data
    
class MemberCreateForm (forms.ModelForm) :
    password = forms.CharField(widget = forms.PasswordInput)
    password_confirmation = forms.CharField(widget = forms.PasswordInput)

    class Meta :
        model = Member
        fields = ('name', 'password')

    def clean (self) :
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password != password_confirmation :
            self.add_error('password_confirmation', 'Passwords do not match.')
        
        return cleaned_data

class StoreCreateForm (forms.ModelForm) :
    class Meta :
        model = Store
        fields = ('name', 'street_address', 'city', 'state', 'zip_code')
    
    def clean (self) :
        cleaned_data = super().clean()

        for field in ['name', 'street_address', 'city', 'state'] :
            cleaned_data[field] = cleaned_data[field].strip().lower()
        
        cleaned_data['zip_code'] = cleaned_data['zip_code'].strip()

        return cleaned_data

