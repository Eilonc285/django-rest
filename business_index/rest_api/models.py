from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Business(models.Model):
    title = models.CharField(max_length=250)
    sub_title = models.CharField(max_length=250, null=True, blank=True)
    street = models.CharField(max_length=250)
    number = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=250)
    grade = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self):
        fields_to_display = ['title', 'sub_title', 'street', 'number', 'city', 'grade']
        model_string = f'{self.id}'
        for field in fields_to_display:
            sub_str = ', '
            sub_str += str(getattr(self, field)) if str(getattr(self, field)) else f'no-{field}'
            model_string += sub_str
        return model_string
