from django.contrib import admin




# Register your models here.
from .models import ClientCategory, Client,ClientType,Payment

admin.site.register(ClientCategory)
admin.site.register(Client)
admin.site.register(ClientType)
admin.site.register(Payment)



