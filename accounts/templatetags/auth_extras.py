from django import template
from django.contrib.auth.models import Group 
import datetime
from datetime import timedelta, time


register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name): 
    group = Group.objects.get(name=group_name) 
    return True if group in user.groups.all() else False


@register.simple_tag
def total_time(start,end):
    tots=(end-start).total_seconds()

    return round((tots/3600)*200,2)



    