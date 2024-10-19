from django import forms

from .models import Household, Member, Store, Item

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
    
class ItemCreateForm (forms.ModelForm) :
    class Meta :
        model = Item
        fields = ('name', 'description', 'price', 'unit', 'current_stock', 'ideal_stock', 'minimum_stock')

    def __init__ (self, *args, **kwargs) :
        # remove default values 

        super(ItemCreateForm, self).__init__(*args, **kwargs)
        self.fields['price'].initial = None
        self.fields['unit'].initial = ''
        self.fields['current_stock'].initial = None

    def clean (self) :
        cleaned_data = super().clean()

        for field in ['name', 'description', 'unit'] :
            cleaned_data[field] = cleaned_data[field].strip().lower()

        # adding default value back
        cleaned_data['price'] = cleaned_data['price'] if cleaned_data['price'] else 0
        cleaned_data['current_stock'] = cleaned_data['current_stock'] if cleaned_data['current_stock'] else 0

        if cleaned_data['price']  < 0 or cleaned_data['current_stock'] < 0 or cleaned_data['ideal_stock'] < 0 or cleaned_data['minimum_stock'] < 0 :
            raise forms.ValidationError('Price and stock data must be greater than 0')
        
        if cleaned_data['minimum_stock'] > cleaned_data['ideal_stock'] :
            raise forms.ValidationError('Minimum stock cannot be greater than ideal stock')

        return cleaned_data

