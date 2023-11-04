from django import forms
from .models import Correspondent


class DateInput(forms.DateInput):

    input_type = 'date'
    # date_field=


class CorrespondentForm(forms.ModelForm):
    """Form definition for Correspondent."""
    date_added = forms.DateField(label = "Dead Line",widget=DateInput)
    correspondent = forms.CharField(label = "Message",widget = forms.Textarea(attrs={'name':'body', 'rows':6, 'cols':5}))

    class Meta:
        """Meta definition for Correspondentform."""

        model = Correspondent
        fields = ('correspondent', 'date_added',)


class CaseCorrespondentForm(forms.ModelForm):
    """Form definition for Correspondent."""
    date_added = forms.DateField(label = "Dead Line",widget=DateInput)
    correspondent = forms.CharField(label = "Message",widget = forms.Textarea(attrs={'name':'body', 'rows':6, 'cols':5}))
    class Meta:
        """Meta definition for Correspondentform."""

        model = Correspondent
        fields = ('correspondent', 'date_added',
                  )
