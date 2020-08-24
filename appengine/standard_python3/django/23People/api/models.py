from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .validators import is_valid_rut


def validate_rut(value):
    if is_valid_rut(value):
        pass
    else:
        raise ValidationError(
            _('%(value)s is not a valid Rut, please enter a valid Rut'),
            params={'value': value},
        )



def validate_dose(value):
    if value >= 0.15 and value <= 1.0:
        pass
    else:
        raise ValidationError(
            _('The Dose value must be greater than or equal to 0.15 and less than or equal to 1.0'),
            params={'value': value},
        )


#Create BD Class Named Drug
class Drug(models.Model):
    name = models.CharField(max_length=50)
    code = models.IntegerField(max_length=10, unique=True)
    description =  models.CharField(max_length=255)
       
    def __str__(self):
        return self.code

    class Meta:
        ordering = ["id"]
        verbose_name = "Drug"

#Create BD Class Named Vaccination
class Vaccination(models.Model):
    rut = models.CharField(max_length=12, validators=[validate_rut])
    dose = models.DecimalField(max_digits = 3,  decimal_places = 2, validators=[validate_dose]) 
    date = models.DateField()
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.code

    class Meta:
        ordering = ["id"]
        verbose_name = "Vaccination"

