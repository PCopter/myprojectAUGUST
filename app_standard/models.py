from django.db import models
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ItemTest(models.Model):
    no = models.SmallIntegerField(default=0)
    name = models.CharField(max_length=100)

    def clean(self):
        if ItemTest.objects.filter(no=self.no).exclude(id=self.id).exists():
            raise ValidationError(f'ItemTest with number {self.no} already exists.')

    def __str__(self):
        return self.name


class Specification(models.Model):
    item_test = models.ForeignKey(ItemTest, on_delete=models.CASCADE, related_name='specifications')
    description = RichTextField(max_length=700, default="xxxxxxx")
    TYPE_CHOICES = [
        ('S', 'Sampling test'),
        ('R', 'Routine test'),
    ]
    test_type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='R')

    def clean(self):
        if Specification.objects.filter(description=self.description).exclude(id=self.id).exists():
            raise ValidationError(f'Specification with description {self.description} already exists.')

    def __str__(self):
        return f"{self.item_test.name} - {self.description} ({self.get_test_type_display()})"


class CountryTestRequirement(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE)
    REQUIREMENT_CHOICES = [
        ('1', 'Should be tested (If possible)'),
        ('2', 'Std.requirement (Must be tested)'),
        ('3', 'Std.requirement must be tested at external lab (CCC)'),
        ('4', 'Std.requirement which can select testing (Between Pressure and Refri. leakage test) (QCO)'),
    ]
    requirement = models.CharField(max_length=1, choices=REQUIREMENT_CHOICES ,)

    class Meta:
        unique_together = ('country', 'specification')

    def __str__(self):
        return f"{self.country.name} - {self.specification.description} ({self.get_requirement_display()})"
