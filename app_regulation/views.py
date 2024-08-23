from django.shortcuts import render
from app_regulation.models import Country, Regulation
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from app_regulation.utils import send_email_to_stakeholders


def regulation_list(request):
    regulations = Regulation.objects.all().select_related('country')
    countries = Country.objects.all()

    # คำนวณ days_until_expiry สำหรับแต่ละ regulation
    today = timezone.now().date()
    for regulation in regulations:
        if regulation.expire_date:
            regulation.days_until_expiry = (regulation.expire_date.date() - today).days
        else:
            # หรือค่าที่เหมาะสมในกรณีที่ไม่มี expiry_date
            regulation.days_until_expiry = 'N/A'
    return render(request, 'app_regulation/regulations.html', {'regulations': regulations, 'countries': countries})


def regulations_manualmail(request):
    countries = Country.objects.all().prefetch_related('stakeholders_email', 'regulations')
    
    for country in countries:
        # Calculate the status counts with explicit zero initialization
        status_counts = {
            'activating': Regulation.objects.filter(country=country, status='activating').count(),
            'caution': Regulation.objects.filter(country=country, status='caution').count(),
            'serious': Regulation.objects.filter(country=country, status='serious').count(),
            'critical': Regulation.objects.filter(country=country, status='critical').count(),
            'expired': Regulation.objects.filter(country=country, status='expired').count(),
        }

        # Calculate the total count of regulations for the country
        regulation_count = Regulation.objects.filter(country=country).count()

        # Attach the status counts and regulation count to the country object
        country.status_counts = status_counts
        country.regulation_count = regulation_count

    return render(request, 'app_regulation/regulations_manualmail.html', {'countries': countries})


def send_manual_email(request, country_id):
    # Retrieve the specified country object
    country = get_object_or_404(Country, id=country_id)
    
    # Retrieve all regulations associated with the country, excluding those with status 'activating'
    regulations = Regulation.objects.filter(country=country).exclude(status='activating')
    
    # Prepare the regulations information to be sent via email
    regulations_info = []

    current_time = timezone.now()
    for regulation in regulations:
        # Calculate days until expiry if the expire_date is present
        if regulation.expire_date:
            expire_date = timezone.make_aware(regulation.expire_date) if timezone.is_naive(regulation.expire_date) else regulation.expire_date
            days_until_expiry = (expire_date - current_time).days
        else:
            days_until_expiry = None
        
        # Append regulation details to the regulations_info list
        regulations_info.append({
            'regulation': regulation.regulation,
            'status': regulation.status,
            'mandatory_voluntory': regulation.mandatory_voluntory,
            'standard': regulation.standard,
            'effective_date': regulation.effective_date,
            'expire_date': regulation.expire_date,
            'days_until_expiry': days_until_expiry,
            'action': regulation.action,
            'scope': regulation.scope,
            'by': regulation.by,
            'remark': regulation.remark,
        })

    # Send the email to stakeholders with the prepared regulations information
    send_email_to_stakeholders(country, regulations_info)

    # Display a success message after the emails have been sent
    messages.success(request, f'Emails sent to stakeholders of {country.name}.')
    
    # Redirect to the desired URL after the email has been sent successfully
    return redirect('regulations_manualmail')  # Adjust 'country_list' to the URL you want to redirect to

