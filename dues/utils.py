from .models import Due
from django.utils import timezone
from datetime import timedelta
from auth_app.utils import EmailThread
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from user_profile.models import UserProfile
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail


def queryset_filter(filter_by):
    today_date_time = timezone.localtime()
    if filter_by.lower() == 'today':
        dues = Due.objects.filter(date = today_date_time.date())

    elif filter_by.lower() == 'week':
        week_date_time = today_date_time - timedelta(days=7)
        dues = Due.objects.filter(date__gte=week_date_time.date())
    
    elif filter_by.lower() == 'month':
        dues = Due.objects.filter(date__year=today_date_time.year,date__month=today_date_time.month)
    
    else:
        dues = Due.objects.filter(date__year=today_date_time.year)
    
    return dues
