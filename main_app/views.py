from django.shortcuts import render

from django.views.generic.edit import CreateView
from django.db import IntegrityError
from django.contrib import messages

from .models import Household
from .forms import HouseholdForm

def home (request) :
    return render(request, 'home.html')

class HouseholdCreate (CreateView) :
    model = Household
    form_class = HouseholdForm
    template_name = 'household_form.html'

    def form_valid (self, form) :
        try :
            return super().form_valid(form)
        
        except IntegrityError :
            messages.error(self.request, 'Household address already exists. Please try again')
            return self.form_invalid(form)

