from django.shortcuts import render
from .models import Country, ItemTest, Specification, CountryTestRequirement

def minstandardtest_view(request):
    countries = Country.objects.all()
    item_tests = ItemTest.objects.all().order_by('no')
    specifications = Specification.objects.all()

    selected_country_id = request.GET.get('country')
    selected_item_test_id = request.GET.get('item_test')
    selected_specification_id = request.GET.get('specification')

    filtered_item_tests = []
    selected_country = None
    filtered_specifications = Specification.objects.none()
    filtered_countries = set()

    if selected_country_id:
        selected_country_id = int(selected_country_id)
        selected_country = countries.get(id=selected_country_id)

    if selected_item_test_id:
        selected_item_test_id = int(selected_item_test_id)
        item_tests = item_tests.filter(id=selected_item_test_id)

    for item_test in item_tests:
        specs = item_test.specifications.all()

        if selected_specification_id:
            selected_specification_id = int(selected_specification_id)
            specs = specs.filter(id=selected_specification_id)

        if selected_country:
            specs = specs.filter(countrytestrequirement__country=selected_country, countrytestrequirement__requirement__in=["1", "2", "3", "4"])

        if specs.exists():
            filtered_item_tests.append((item_test, specs))
            for spec in specs:
                for requirement in spec.countrytestrequirement_set.all():
                    filtered_countries.add(requirement.country)

    context = {
        'countries': filtered_countries if filtered_countries else countries,
        'item_tests': filtered_item_tests,
        'all_item_tests': ItemTest.objects.all().order_by('no'),
        'specifications': specifications,
        'selected_country': selected_country,
        'selected_item_test_id': selected_item_test_id,
        'selected_specification_id': selected_specification_id,
    }
    return render(request, 'app_standard/minstandardtest.html', context)
