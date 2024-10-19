from django.db import models
from django.urls import reverse

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib.auth.hashers import make_password, check_password

class Household (models.Model) :
    street_address = models.CharField(max_length = 100, null = False, blank = False)
    city = models.CharField(max_length = 100, null = False, blank = False)
    state = models.CharField(max_length = 2, null = False, blank = False)
    zip_code =  models.CharField(max_length = 5, null = False, blank = False)
    passcode = models.CharField(max_length = 128, null = False, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta :
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

        self.passcode = make_password(self.passcode.strip())
        super(Household, self).save(*args, **kwargs)

    def verify_passcode (self, raw_passcode) :
        return check_password(raw_passcode, self.passcode)
    
    def get_absolute_url (self) :
        return reverse('member_select')

    def __str__ (self) :
        return f'{self.street_address.title()} {self.city.title()}, {self.state.upper()} {self.zip_code}'


class Member (models.Model) :
    name = models.CharField(max_length = 30, null = False, blank = False)
    password = models.CharField(max_length = 128, null = False, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)
    household = models.ForeignKey(Household, on_delete = models.CASCADE, related_name = 'members', null = False, blank = False)

    class Meta :
        # unique member name within a household
        constraints = [
            models.UniqueConstraint(
                fields = ['household', 'name'], 
                name = 'unique_member_name_within_household'
            )
        ]

    def save (self, *args, **kwargs) :
        self.name = self.name.strip().lower()
        self.password = make_password(self.password.strip())
        super(Member, self).save(*args, **kwargs)

    def verify_password (self, raw_password) :
        return check_password(raw_password, self.password)
    
    def get_absolute_url (self) :
        return reverse('store_list')

    def __str__ (self) :
        return f'{self.name.title()} at {self.household}'
    

class Store (models.Model) :
    name = models.CharField(max_length = 30, null = False, blank = False)
    street_address = models.CharField(max_length = 100, null = False, blank = False)
    city = models.CharField(max_length = 100, null = False, blank = False)
    state = models.CharField(max_length = 2, null = False, blank = False)
    zip_code =  models.CharField(max_length = 5, null = False, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)
    household = models.ForeignKey(Household, on_delete = models.CASCADE, related_name = 'stores', null = False, blank = False)

    class Meta :
        # unique store name within a household
        constraints = [
            models.UniqueConstraint(
                fields = ['household', 'name'], 
                name = 'unique_store_name_within_household'
            )
        ]
    
    def save (self, *args, **kwargs) :
        self.name = self.name.strip().lower()
        super(Store, self).save(*args, **kwargs)

    def __str__ (self) :
        return f'{self.name.title()} at {self.street_address.title()} {self.city.title()}, {self.state.upper()} {self.zip_code}'
    

class Item (models.Model) :
    name = models.CharField(max_length = 30, null = False, blank = False)
    description = models.CharField(max_length = 100, default = '', blank = True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00, validators = [MinValueValidator(0)], null = False, blank = True)
    unit = models.CharField(max_length = 30, default = 'each', null = False, blank = True)
    current_stock = models.IntegerField(default = 0, validators = [MinValueValidator(0)], null = False, blank = True)
    ideal_stock = models.IntegerField(validators = [MinValueValidator(0)], null = False, blank = False)
    minimum_stock = models.IntegerField(validators = [MinValueValidator(0)], null = False, blank = False)
    average_usage = models.IntegerField(default = 0, validators = [MinValueValidator(0)], null = False, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    store = models.ForeignKey(Store, on_delete = models.CASCADE, related_name = 'items', null = False, blank = False)

    class Meta :
        # minimum_stock has to be less than ideal_stock
        constraints = [
            models.CheckConstraint(
                check = models.Q(minimum_stock__lte = models.F('ideal_stock')),
                name = 'minimum_stock_le_ideal_stock'
            )
        ]

    def save (self, *args, **kwargs) :
        if self.minimum_stock > self.ideal_stock :
            raise ValidationError('Minimum stock cannot be greater than ideal stock')
        
        self.name = self.name.strip().lower()
        self.description = self.description.strip().lower() if self.description else ''
        self.unit = self.unit.strip().lower()

        super(Item, self).save(*args, **kwargs)

    def __str__ (self) :
        return f'{self.name} from {self.store.name}'