from django.db import models
from django.urls import reverse

from django.contrib.auth.hashers import make_password, check_password

class Household (models.Model) :
    street_address = models.CharField(max_length = 100)
    city = models.CharField(max_length = 100)
    state = models.CharField(max_length = 2)
    zip_code =  models.CharField(max_length = 5)
    passcode = models.CharField(max_length = 100)

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
        return check_password(self.passcode, raw_passcode)

    def __str__ (self) :
        return f'{self.street_address.title()} {self.city.title()}, {self.state.upper()} {self.zip_code}'

