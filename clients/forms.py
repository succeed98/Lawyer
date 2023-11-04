from django import forms
from .models import Client, ClientCategory,Payment, ClientType
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField
from cases.models import Case,EngagementTerm
from wills.models import Will
from lawyers.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from lawyers.models import Lawyer
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget


class ClientForm(forms.ModelForm):
    # category = AutoCompleteSelectField(
    #     channel='category', required=True, help_text="enter category")
    lead_professional = forms.ModelChoiceField(widget=forms.Select(attrs={'id': 'e3', 'class': 'form-control', }),
                                               queryset=Lawyer.objects.order_by('user__first_name'))

    client_type = forms.ModelChoiceField(queryset=ClientType.objects.order_by('types'))

    category = forms.ModelChoiceField(queryset=ClientCategory.objects.order_by('title'))

    client_email=forms.EmailField()

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    
    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    

    class Meta:
        model = Client
        fields = ['name','client_email','phone','address','category','lead_professional' ,'client_type', 'contact_person', 'contact_number'] # i360-Daniel: Added new fields

    

class ClientCategoryForm(forms.ModelForm):

    class Meta:
        model = ClientCategory
        fields = ['title']

class ClientTypeForm(forms.ModelForm):

    class Meta:
        model = ClientType
        fields = ['types']


class DateInput(forms.DateInput):

    input_type = 'date'
    # date_field=forms.DateField(widget=DateInput)


class ClientCaseForm(forms.ModelForm):
    # category = AutoCompleteSelectField(
    #     channel='category', required=True, help_text="enter category")


    date_added=forms.DateField(widget=DateInput)


    class Meta:
        model = Case
        fields = [ 'name', 'description','category','case_number','suit_number','court','court_number','lawyer','date_added' ,'representative',]


class ClientWillForm(forms.ModelForm):
    date_deposited= forms.DateField(widget=DateInput)
    date_of_execution=  forms.DateField(widget=DateInput)



    class Meta:
        model=Will
        fields=['date_of_execution','date_deposited','internal_depository','receipt_number','court','user']




class UpdateUserForm(UserChangeForm):
    """
    Update User Form. Doesn't allow changing password in the Admin.
    """


    class Meta:
        model = User
        fields = (
            'first_name','last_name','email','username','phone','avatar'
        )
        # exclude=()


class EngagementForm(forms.ModelForm):
    """Form definition for Engagement."""
    # case=forms.ModelChoiceField(widget=forms.Select(attrs={'id': 'e3', 'class': 'form-control', }),
    #                               queryset=Case.objects.filter())



    class Meta:
        """Meta definition for Engagementform."""


        model = EngagementTerm
        fields = ('file',)




class PaymentForm(forms.ModelForm):
    """Form definition for Payment."""
    date_received=forms.DateField(widget=DateInput)
    client=forms.ModelChoiceField(widget=forms.Select(attrs={'id': 'e3', 'class': 'form-control', }),
                                  queryset=Client.objects.filter())
    case=forms.ModelChoiceField(widget=forms.Select(attrs={'id': 'e2', 'class': 'form-control', }),
                                  queryset=Case.objects.filter())


    class Meta:
        """Meta definition for Paymentform."""


        model = Payment
        fields = ('client','case','amount','full_payment','date_received')


