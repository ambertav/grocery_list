from django.db import models
from django.urls import reverse

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.hashers import make_password, check_password

class Household (models.Model) :
    street_address = models.CharField(max_length = 100)
    city = models.CharField(max_length = 100)
    state = models.CharField(max_length = 2)
    zip_code =  models.CharField(max_length = 5)
    passcode = models.CharField(max_length = 128)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        # unique address constraint
        constraints = [
            models.UniqueConstraint(
                fields = ['street_address', 'city', 'state', 'zip_code'], 
                name = 'unique_household_address'
            )
        ]

    def save (self, *args, **kwargs) :
        for field in ['street_address', 'city', 'state'] :
            value = getattr(self, field)
            setattr(self, field, value.strip().lower())

        self.zip_code = self.zip_code.strip()

        self.passcode = make_password(self.passcode)
        super(Household, self).save(*args, **kwargs)

    def verify_passcode (self, raw_passcode) :
        return check_password(raw_passcode, self.passcode)
    
    def get_absolute_url (self) :
        return reverse('member_select')

    def __str__ (self) :
        return f'{self.street_address.title()} {self.city.title()}, {self.state.upper()} {self.zip_code}'


class Member (AbstractUser) :
    username = None 
    first_name = None
    last_name = None
    email = None 
    groups = models.ManyToManyField(Group, related_name = 'member_set', blank = True)
    user_permissions = models.ManyToManyField(Permission, related_name = 'member_set', blank = True)

    name = models.CharField(max_length = 30)
    password = models.CharField(max_length = 128)
    is_active = models.BooleanField(default = True)
    last_login = models.DateTimeField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    household = models.ForeignKey(Household, on_delete = models.CASCADE, related_name = 'members', null = False, blank = False)

    class Meta:
        # unique member name within a household
        constraints = [
            models.UniqueConstraint(
                fields = ['household', 'name'], 
                name = 'unique_member_name_within_household'
            )
        ]

    def save (self, *args, **kwargs) :
        self.name = self.name.strip().lower()
        self.password = make_password(self.password)
        super(Member, self).save(*args, **kwargs)

    def verify_password (self, raw_password) :
        return check_password(raw_password, self.password)

    def __str__ (self) :
        return f'{self.name.title()} at {self.household}'

    