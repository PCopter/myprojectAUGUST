from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone

class Country(models.Model):
    name = models.CharField(max_length=255,unique=True)
    image_relative_url = models.CharField(max_length=255, default='default.jpg')
    stakeholders_email = models.ManyToManyField('Stakeholder', related_name='countries')

    caution_threshold = models.IntegerField(default=180)
    serious_threshold = models.IntegerField(default=120)
    critical_threshold = models.IntegerField(default=60)

    def __str__(self):
        return self.name
    

class Regulation(models.Model):
    country = models.ForeignKey(Country, related_name='regulations', on_delete=models.CASCADE)
    regulation = models.CharField(max_length=350)
    regulation_image_url = models.CharField(max_length=255, null=True, blank=True)

    STATUS_CHOICES = (
        ('activating', 'Activating'),
        ('caution', 'Caution'),
        ('serious', 'Serious'),
        ('critical', 'Critical'),
        ('expired', 'Expired'),
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='activating')

    MANDATORY_VOLUNTORY_CHOICES = [
        ('Mandatory', 'Mandatory'),
        ('Voluntary', 'Voluntary'),
        ('N/A', 'N/A'),
    ]
    mandatory_voluntory = models.CharField(max_length=10, choices=MANDATORY_VOLUNTORY_CHOICES)
    
    standard = models.CharField(max_length=355, null=True, blank=True)
    # ต้องดำเนินการให้แล้วเสร็จก่อน effective_date
    effective_date = RichTextField(null=True, blank=True)
    expire_date = models.DateTimeField(null=True, blank=True)
    action = RichTextField(null=True, blank=True)
    scope = RichTextField(null=True, blank=True)
    scope_image_url = models.CharField(max_length=255, null=True, blank=True)
    detail = RichTextField(null=True, blank=True)
    detail_image_url = models.CharField(max_length=255, null=True, blank=True)
    by = models.CharField(max_length=255, null=True, blank=True)
    remark = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.regulation} - {self.mandatory_voluntory} - {self.standard}"
    

    # ใช้อัพเดทสถานะ status ตามที่ตั้ง threshold ที่ตั้งไว้
    def update_status(self):
        current_date = timezone.localtime(timezone.now()).date()
        if self.expire_date:
            days_until_expiry = (self.expire_date.date() - current_date).days
        else:
            days_until_expiry = None

        if days_until_expiry is not None:
            if days_until_expiry < 0:
                self.status = 'expired'  
            elif days_until_expiry > self.country.caution_threshold:
                self.status = 'activating'
            elif days_until_expiry > self.country.serious_threshold:
                self.status = 'caution'
            elif days_until_expiry > self.country.critical_threshold:
                self.status = 'serious'
            else:
                self.status = 'critical'
        else:
            self.status = 'activating'
    
    def save(self, *args, **kwargs):
        self.update_status()
        super().save(*args, **kwargs)


class Stakeholder(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

