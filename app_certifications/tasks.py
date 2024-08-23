from celery import shared_task
from .utils import send_email_to_stakeholders
from .models import Country, CertificateNumber
import logging
from datetime import date
from django.utils import timezone

logger = logging.getLogger(__name__)

@shared_task
def send_weekly_email():
    try:
        logger.info("Sending weekly email")

        countries = Country.objects.all()
        today = timezone.now().date()
        for country in countries:
            certificates = CertificateNumber.objects.filter(certification__country=country).exclude(status='activating')
            certificates_info = []

            for certificate in certificates:
                days_until_expiry = (certificate.expire_date.date() - today).days if certificate.expire_date else None
                certificate_info = {
                    'certificate_no': certificate.certificate_no,
                    'certificate_no_link' : certificate.certificate_no_link,
                    'status': certificate.status,
                    'issue_date': certificate.issue_date,
                    'expire_date': certificate.expire_date,
                    'days_until_expiry': days_until_expiry,
                    'indoor_models': certificate.indoor_models.all(),
                    'outdoor_models': certificate.outdoor_models.all(),
                }
                certificates_info.append(certificate_info)

            send_email_to_stakeholders(country, certificates_info)

        logger.info("Weekly emails sent to all stakeholders")
        return "Weekly emails sent to all stakeholders"
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise e



