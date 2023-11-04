from django.db import models

# Create your models here.
from lawyers.models import Lawyer, User
from django.urls import reverse
from django.db.models.signals import post_save
import uuid

class ClientCategory(models.Model):
    title = models.CharField(max_length=250)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:

        verbose_name = 'Client Category'
        verbose_name_plural = 'Client Categories'

class ClientType(models.Model):
    types=models.CharField(max_length=250)

    def __str__(self):
        return self.types


class Client(models.Model):
    user=models.ForeignKey('lawyers.User',related_name='user_client',null=True,on_delete=models.SET_NULL)
    name=models.CharField(max_length=250,blank=True,null=True,default='')
    client_email=models.CharField(max_length=250,blank=True,null=True)
    phone=models.CharField(max_length=250,blank=True,null=True, verbose_name = "Business Phone")

    address = models.TextField()
    lead_professional=models.ForeignKey("lawyers.Lawyer",null=True,on_delete=models.SET_NULL)
    client_type=models.ForeignKey(ClientType,null=True, on_delete=models.SET_NULL)

    # New models by Dartisan
    contact_person=models.CharField(max_length=250,blank=True,null=True)
    contact_number=models.CharField(max_length=250,blank=True,null=True)




    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(ClientCategory, on_delete=models.CASCADE)

    def __str__(self):
        # fullname="{} {}".format(self.user.first_name,self.user.last_name)
        try:

            return self.name
        except Exception:
            return "None"

    class Meta:

        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['name']

    def get_absolute_url(self):
        # from django.core.urlresolvers import reverse
        return reverse('clients:client_detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        # from django.core.urlresolvers import reverse
        return reverse('clients:client_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        # from django.core.urlresolvers import reverse
        return reverse('clients:client_delete', kwargs={'pk': self.pk})





class PaymentMethod(models.Model):
    method= models.CharField(max_length=250)


    def __str__(self):

        return self.method




class Payment(models.Model):
    """Model definition for Payement."""
    client=models.ForeignKey(Client,null=True, on_delete=models.SET_NULL)
    amount= models.FloatField(blank=True,null=True)
    full_payment=models.BooleanField(default=False)
    case=models.ForeignKey('cases.Case',null=True,blank=True,on_delete=models.SET_NULL)
    date_received=models.DateTimeField(auto_now=False)
    payment_method=models.ForeignKey(PaymentMethod,null=True, on_delete=models.SET_NULL)
    payment_id=models.CharField(null=True,blank=True, unique=True, max_length=250)
    added_by=models.ForeignKey('lawyers.User',null=True,on_delete=models.SET_NULL)


    # TODO: Define fields here

    class Meta:
        """Meta definition for Payement."""

        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'




    def __str__(self):
        """Unicode representation of Payement."""
        return self.client.name


def add_pid(sender,instance,**kwargs):
    my_str=uuid.uuid4().hex[:3].upper()

    if not instance.payment_id:

        instance.payment_id=f"{my_str}-{instance.id}"
        instance.save()


post_save.connect(add_pid,sender=Payment)



