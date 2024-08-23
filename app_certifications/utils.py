# utils.py
from django.core.mail import send_mail
from django.template.loader import render_to_string 

def send_email_to_stakeholders(country, certificates_info):
    stakeholders = country.stakeholders_email.all()
    recipient_list = [stakeholder.email for stakeholder in stakeholders]
    subject = f'Certificate Status Update for {country.name}'
    html_message = render_to_string('app_certifications/email_template.html', {'country': country, 'certificates': certificates_info})
    send_mail(subject, '', 'your_email@example.com', recipient_list, html_message=html_message)









