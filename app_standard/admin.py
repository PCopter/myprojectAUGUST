from django.contrib import admin
from .models import Country, ItemTest, Specification ,CountryTestRequirement

admin.site.register(Country)
admin.site.register(ItemTest)
admin.site.register(Specification)
admin.site.register(CountryTestRequirement)

 