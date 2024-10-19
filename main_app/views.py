from django.shortcuts import render, redirect
from django.urls import reverse

from django.views import View
from django.views.generic.edit import CreateView
from django.db import IntegrityError
from django.contrib import messages

from .models import Household, Member
from .forms import HouseholdCreateForm, HouseholdLoginForm, MemberCreateForm, StoreCreateForm

def home (request) :
    return render(request, 'home.html')

class HouseholdCreate (CreateView) :
    model = Household
    form_class = HouseholdCreateForm
    template_name = 'household/household_create.html'

    def form_valid (self, form) :
        try :
            household = form.save(commit = False)
            self.request.session['household'] = household.id
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
                request.session['household'] = household.id
                return redirect(household.get_absolute_url())
            
            else :
                messages.error(self.request, 'Invalid address or passcode. Please try again')
        
        return render(request, self.template_name, { 'form': form })

class MemberCreate (CreateView) :
    model = Member
    form_class = MemberCreateForm
    template_name = 'member/member_create.html'

    def form_valid (self, form) :
        try :
            household_id = self.request.session.get('household')

            if not household_id :
                messages.error(self.request, 'Household not found. Please try again')
                return redirect('household_select')
            
            household = Household.objects.get(id = household_id)

            member = form.save(commit = False)
            member.household = household

            self.request.session['member'] = member.id
            return super().form_valid(form)
        
        except Household.DoesNotExist :
            self.request.session.pop('household', None)
            return redirect('household_select')
        
        except IntegrityError :
            messages.error(self.request, 'Member already exists. Please try again')
            return self.form_invalid(form)

class MemberSelect (View) :
    template_name = 'member/member_select.html'

    def get (self, request, *args, **kwargs) :
        household_id = request.session.get('household')

        if not household_id :
            return redirect('household_select')
    
        try :
            household = Household.objects.get(id = household_id)
        
        except Household.DoesNotExist :
            request.session.pop('household', None)
            return redirect('household_select')
        
        members = household.members.all()

        if not members :
            return redirect('member_create')

        return render(request, self.template_name, { 'members': members })
    
    def post (self, request, *args, **kwargs) :
        household_id = request.session.get('household')
        
        if not household_id :
            return redirect('household_select')
        
        member_id = request.POST.get('member_id')
        password = request.POST.get('password').strip()
        
        try :
            household = Household.objects.get(id = household_id)
            member = household.members.get(id = member_id)

            if member and member.verify_password(password) :
                request.session['member'] = member.id
                return redirect(member.get_absolute_url())
            
            else :
                messages.error(self.request, 'Invalid password. Please try again')

        except Household.DoesNotExist :
            request.session.pop('household', None)
            return redirect('household_select')
    
        except Member.DoesNotExist :
            messages.error(request, 'Member does not exist')
        
        members = household.members.all()
        return render(request, self.template_name, { 'members': members })


class StoreCreate (CreateView) :
    form_class = StoreCreateForm
    template_name = 'store/store_create.html'

    def form_valid (self, form) :
        try :
            household_id = self.request.session.get('household')

            if not household_id :
                messages.error(self.request, 'Household not found. Please try again')
                return redirect('household_select')
            
            household = Household.objects.get(id = household_id)

            store = form.save(commit = False)
            store.household = household

            return super().form_valid(form)
        
        except IntegrityError :
            messages.error(self.request, 'Store already exists. Please try again')
            return self.form_invalid(form)
        
    def get_success_url (self) :
        return reverse('store_list')

class StoreList (View) :
    template_name = 'store/store_list.html'

    def get (self, request, *args, **kwargs) :
        household_id = request.session.get('household')

        if not household_id :
            return redirect('household_select')
    
        try :
            household = Household.objects.get(id = household_id)
        
        except Household.DoesNotExist :
            request.session.pop('household', None)
            return redirect('household_select')
        
        stores = household.stores.all()

        if not stores :
            return redirect('store_create')

        return render(request, self.template_name, { 'stores': stores })