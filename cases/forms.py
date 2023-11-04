from django import forms
from .models import (Case, Category, Status, CaseTask, CaseFile, CaseArchive, LegalArgument,
Court, CourtSession, Representative, Process, PostAction,RequestArchive,Representative,Expense,PaymentStatus,PaymentEnquiry,ChineseWall,TermsOfEngagement)
from lawyers.models import User, Lawyer, OtherStaff
from clients.models import Client
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from tinymce.widgets import TinyMCE

class DateInput(forms.DateInput):

    input_type = 'date'
    # date_field=forms.DateField(widget=DateInput)


class CaseTaskForm(forms.ModelForm):
    deadline = forms.DateField(widget=DateInput)
    description = forms.CharField(widget = CKEditorWidget(attrs={'class' : 'form-control', 'id': 'fourth'}))

    class Meta:
        model = CaseTask
        fields = ("task", "description", "deadline","frequency")


# choice=User.objects.a

class CaseForm(forms.ModelForm):
    # attachments = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
    #     'multiple': True
    # }))

    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    description = RichTextField()

    date_added = forms.DateField(widget=DateInput(
        attrs={'class': 'form-control', 'id': 'date-format'}),label="Date Filed")
    date_received = forms.DateField(widget=DateInput(
        attrs={'class': 'form-control'}))

    client = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(
        attrs={'id': 'e2', 'class': 'form-control'}), required=True, help_text="Please Select Clients From The List",
        queryset=Client.objects.order_by('name'))

    lawyer = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(
        attrs={'id': 'e1', 'class': 'form-control'}), required=True, help_text="Please Select Lawyers From The List",
        queryset=Lawyer.objects.order_by('user__first_name'))

    staff = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(
            attrs={'id':'e3','class':'form-control' }),required=False, help_text="Please other staff not part of Team (Optional)" ,queryset=OtherStaff.objects.order_by('user__first_name'))

    lead_professional = forms.ModelChoiceField(widget=forms.Select(attrs={'id': 'e3', 'class': 'form-control', }),
                                               queryset=Lawyer.objects.order_by('user__first_name'))

    court = forms.ModelChoiceField(queryset=Court.objects.order_by('name'))

    category=forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(
        attrs={'id': 'e4', 'class': 'form-control'}), required=True, help_text="Please Select Categories From The List",
        queryset=Category.objects.order_by('name'))

    case_number=forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}),label="File Number")


    class Meta:
        model = Case



        fields = ("name","client","description","lead_professional","lawyer","staff","category", "case_number",'court_number',
                  'date_added','date_received','court','team',"confidential","type")


class CaseFileForm(forms.ModelForm):
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = CaseFile
        fields = ("file",)


class TermsOfEngagementForm(forms.ModelForm):
    upload_file = forms.FileField(label = "Upload file(s)",
        widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = TermsOfEngagement
        fields = ("upload_file",)


class CaseArchiveForm(forms.ModelForm):
    case = forms.ModelChoiceField(widget=forms.Select(attrs={'id': 'e3', 'class': 'form-control', }),
                                  queryset=Case.objects.filter(closed=True,archived=False), label="Case")

    class Meta:
        model = CaseArchive
        fields = ('case','box_number','aisle_number','shelf')




class ChineseWallForm(forms.ModelForm):
    chinese_lawyer = forms.ModelMultipleChoiceField(required=False,widget=forms.SelectMultiple(
            attrs={'id':'chinese_lawyer','class':'form-control' }),help_text="Please Select Lawyers who can access the case" ,queryset=Lawyer.objects.order_by('user__first_name'))
    chinese_staff = forms.ModelMultipleChoiceField(required=False,widget=forms.SelectMultiple(
            attrs={'id':'chinese_staff','class':'form-control' }),help_text="Please other staff who can access the case (Optional)" ,queryset=OtherStaff.objects.order_by('user__first_name'))

    class Meta:
        model = ChineseWall
        fields = ('chinese_lawyer', 'chinese_staff')


class ChineseWallFormEdit(forms.ModelForm):
    chinese_lawyer = forms.ModelMultipleChoiceField(required=False,widget=forms.SelectMultiple(
            attrs={'id':'chinese_lawyer_edit','class':'form-control' }),help_text="Please Select Lawyers who can access the case" ,queryset=Lawyer.objects.order_by('user__first_name'))
    chinese_staff = forms.ModelMultipleChoiceField(required=False,widget=forms.SelectMultiple(
            attrs={'id':'chinese_staff_edit','class':'form-control' }),help_text="Please other staff who can access the case (Optional)" ,queryset=OtherStaff.objects.order_by('user__first_name'))

    class Meta:
        model = ChineseWall
        fields = ('chinese_lawyer', 'chinese_staff')



class CaseForms(forms.ModelForm):
    name = forms.CharField(required=True)
    description = RichTextField()

    date_added = forms.DateField(widget=DateInput(
        attrs={'class': 'form-control'}),label="Date Filed")
    date_received = forms.DateField(widget=DateInput(
        attrs={'class': 'form-control'}))

    client=forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(
                 attrs={'id':'e2','class':'form-control' }),required=True,help_text="Please Select Clients From The List" ,queryset=Client.objects.order_by('name'))

    lawyer = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(
            attrs={'id':'e1','class':'form-control' }),required=True,help_text="Please Select Lawyers From The List" ,queryset=Lawyer.objects.order_by('user__first_name'))


    court = forms.ModelChoiceField(queryset=Court.objects.order_by('name'))


    staff = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(
            attrs={'id':'e3','class':'form-control' }),required=False,help_text="Please other staff not part of Team (Optional)" ,queryset=OtherStaff.objects.order_by('user__first_name'))

    lead_professional = forms.ModelChoiceField(widget=forms.Select(attrs={'id': 'e3', 'class': 'form-control', }),
                                  queryset=Lawyer.objects.order_by('user__first_name'))

    category=forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(
        attrs={'id': 'e4', 'class': 'form-control'}), required=True, help_text="Please Select Clients From The List",
        queryset=Category.objects.all().order_by('name'))

    case_number=forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}),label="File Number")



    class Meta:
        model = Case
        fields = ['name', 'client', 'description',  "lead_professional", 'category' , "case_number",'court_number',
                  'lawyer','staff',  'date_added','date_received', 'court','team', "confidential", "type"]




class CategoryForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}),label='Category')
    parent = forms.ModelChoiceField(widget=forms.Select(attrs={'id': 'e3', 'class': 'form-control', }),
                                  queryset=Category.objects.all(),label='parent category',required=False)
    class Meta:
        model = Category
        fields = ['name','parent' ]


class LegalArgumentForm(forms.ModelForm):
    class Meta:
        model = LegalArgument
        fields = ['argument', 'authorities']


class CourtForm(forms.ModelForm):

    class Meta:
        model = Court
        fields = ("name",)


class CourtSessionForm(forms.ModelForm):
    purpose = forms.CharField(required=True, label='Purpose/Court Remarks')


    class Meta:
        model = CourtSession
        fields = ("purpose",)


class ProcessForm(forms.ModelForm):
    process_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
    
    class Meta:
        model = Process
        fields =('process','description','process_file',)



class ProcessForm2(forms.ModelForm):
    case = forms.ModelChoiceField(widget=forms.Select(attrs={'id': 'e3', 'class': 'form-control', }),
                                    queryset=Case.objects.all() , label="Cases")
    description = forms.CharField(widget = CKEditorWidget(attrs={'class' : 'form-control', 'id': 'third'}))

    date_created=forms.DateField(widget=DateInput)
    box_number=forms.CharField(required=False)
    shelf=forms.CharField(required=False)
    aisle_number=forms.CharField(required=False)

    class Meta:
        model = Process
        fields =('case','process','description','process_file','date_created','box_number','aisle_number','shelf')



class ArchiveUpdateForm(forms.ModelForm):
    # case = forms.ModelChoiceField(widget=forms.Select(attrs={'id': 'e3', 'class': 'form-control', }),
    #                               queryset=Case.objects.filter(closed=True,archived=False), label="Case")

    class Meta:
        model = CaseArchive
        fields = ('box_number','aisle_number','shelf')



class PostActionForm(forms.ModelForm):
    next_business=forms.DateField(widget=DateInput)
    bod=forms.CharField()
    class Meta:
        model=PostAction
        fields=['title','bod','next_business','report_type']




class RepresentationForm(forms.ModelForm):

    class  Meta:
        model=Representative
        fields=('title',)






class RequestForm(forms.ModelForm):
    class Meta:
        model=RequestArchive
        fields=["case_title","case_number","suit_number","client_name"]



class ExpenseForm(forms.ModelForm):
    """ExpenseForm definition."""
    case=forms.ModelChoiceField(widget=forms.Select(attrs={'id': 'e3', 'class': 'form-control', }),
                                    queryset=Case.objects.order_by('name') , label="Case")

    description = forms.CharField(widget = CKEditorWidget())

    # TODO: Define form fields here
    class Meta:
        model=Expense
        fields=['amount', 'description','case']

class PaymentEnquiryForm(forms.ModelForm):
    case=forms.ModelChoiceField(widget=forms.Select(attrs={'id': 'e3', 'class': 'form-control', }),
                                    queryset=Case.objects.all() , label="Case",disabled=True)
    lead= forms.ModelChoiceField(widget=forms.Select(attrs={'id': 'e3', 'class': 'form-control', }),
                                               queryset=Lawyer.objects.all(),disabled=True,label="Requested By")
    client = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(
        attrs={'id': 'e2', 'class': 'form-control'}), required=False, help_text="Please Select Clients From The List",
        queryset=Client.objects.all(),disabled=True)

    class Meta:
        model=PaymentEnquiry
        fields=['case','lead','client','status']
