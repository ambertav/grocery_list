from django.shortcuts import render, redirect

from django.views import View
from django.views.generic.edit import CreateView
from django.db import IntegrityError
from django.contrib import messages

from .models import Household
from .forms import HouseholdCreateForm, HouseholdLoginForm

def home (request) :
    return render(request, 'home.html')

class HouseholdCreate (CreateView) :
    model = Household
    form_class = HouseholdCreateForm
    template_name = 'household/household_form.html'

    def form_valid (self, form) :
        try :
            return super().form_valid(form)
        
        except IntegrityError :
            messages.error(self.request, 'Household address already exists. Please try again')
            return self.form_invalid(form)
        
class HouseholdSelect (View) :
    form_class = HouseholdLoginForm
    template_name = 'household/household_select.html'

    def get (self, request, *args, **kwargs) :
        return render(request, self.template_name, { 'form': self.form_class() })

    def post (self, request, *args, **kwargs) :
        form = self.form_class(request.POST)

        if form.is_valid() :
            household = Household.objects.filter(
            street_address = form.cleaned_data['street_address'],
            city = form.cleaned_data['city'],
            state = form.cleaned_data['state'],
            zip_code = form.cleaned_data['zip_code']
        ).first()

            if household and household.verify_passcode(form.cleaned_data['passcode']) :
                return redirect(household.get_absolute_url())
            
            else :
                print('invalid passcode?')
                messages.error(self.request, 'Invalid address or passcode. Please try again')
        
        return render(request, self.template_name, { 'form': form })


