from django import forms
from .models import Will, Agreement, AgreementCategory
from lawyers.models import Lawyer
from clients.models import Client


class DateInput(forms.DateInput):

    input_type = 'date'
    # date_field=forms.DateField(widget=DateInput)


class WillForm(forms.ModelForm):
    """WillForm definition."""
    date_of_execution = forms.DateField(
        widget=DateInput, required=False)
    date_deposited = forms.DateField(widget=DateInput)
    client=forms.ModelChoiceField(widget=forms.Select(attrs={'id':'e3','class':'form-control',}),queryset=Client.objects.all() )
    user = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(
            attrs={'id':'e1','class':'form-control' }),required=True,help_text="Please Select Lawyers From The List" ,queryset=Lawyer.objects.all())

    class Meta:
        model = Will
        fields = ['client', 'user', 'date_of_execution', 'date_deposited',
                  'receipt_number', 'court', 'internal_depository']

    # TODO: Define form fields here


class AgreementForm(forms.ModelForm):
    """WillForm definition."""
    date_of_execution = forms.DateField(widget=DateInput, required=False)
    date_of_registration = forms.DateField(widget=DateInput)


    class Meta:
        model = Agreement
        exclude = ('user',)


class AgreementCategoryForm(forms.ModelForm):

    class Meta:
        model = AgreementCategory
        fields = ('__all__')
