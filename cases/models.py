from django.db import models
from django.urls import reverse
from timezone_field import TimeZoneField
from django.core.exceptions import ValidationError
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from tinymce.models import HTMLField

class Representative(models.Model):
    title = models.CharField(max_length=250)
    date_added=models.DateTimeField(auto_now=True)
    """Model definition for Representative."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for Representative."""

        verbose_name = 'Representation'
        verbose_name_plural = 'Representations'
        ordering = ['title']

    def __str__(self):
        """Unicode representation of Representative."""
        return self.title

class ReportType(models.Model):
    title=models.CharField(max_length=250)

    def __str__(self):
        return self.title


class CaseType(models.Model):
    title=models.CharField(max_length=250)

    def __str__(self):
        return self.title


class Frequency(models.Model):
    title=models.CharField(max_length=250)
    value=models.IntegerField()


    class Meta:
            """Meta definition for Frequency."""


            ordering=['-pk']
            verbose_name = 'Frequency'
            verbose_name_plural = 'Frequencies'


    def __str__(self):
        return self.title



class Court(models.Model):
    name = models.CharField(max_length=250)
    date_modified = models.DateTimeField(auto_now=True)

    """Model definition for Courts."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for Courts."""

        verbose_name = 'Courts'
        verbose_name_plural = 'Courts'
        ordering = ['name']

    def __str__(self):
        """Unicode representation of Courts."""
        return self.name


class Category(models.Model):
    """Model definition for Category."""
    name = models.CharField(max_length=250)
    date_added = models.DateTimeField(auto_now=True)
    parent=models.ForeignKey('self',null=True,blank=True, on_delete=models.SET_NULL)


    # TODO: Define fields here

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    
    

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        if k is not None:
            full_path.append(k.name)
            # k = k.parent
        return ' / '.join(full_path[::1])

    def get_absolute_url(self):
        return reverse("cases:cat_detail", kwargs={"pk": self.pk})

    # TODO: Define custom methods here


class Status(models.Model):
    """Model definition for Status."""
    title = models.CharField(max_length=50)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Status."""

        verbose_name = 'Status'
        verbose_name_plural = 'Status'

    def __str__(self):
        """Unicode representation of Status."""
        return self.title

    def get_absolute_url(self):
        return reverse("cases:status_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("cases:status_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("cases:status_delete", kwargs={"pk": self.pk})


DEFAULT_STATUS_ID = 2


class Case(models.Model):
    name = models.CharField(max_length=350)
    description = RichTextField(blank=True,null=True)
    category = models.ManyToManyField(Category, blank = True)
    court_number = models.CharField(max_length=250, null=True, blank=True)
    suit_number = models.CharField(max_length=250,null=True,blank=True)
    case_number = models.CharField(max_length=250, null=True, blank=True)
    representative = models.ForeignKey(
        Representative, null=True,blank=True ,on_delete=models.SET_NULL)
    lead_professional=models.ForeignKey('lawyers.Lawyer',related_name='lead_professional' ,null=True,on_delete=models.SET_NULL)
    confidential=models.BooleanField(default=False)
    team=models.ForeignKey('lawyers.Team',null=True, on_delete=models.SET_NULL)
    type=models.ForeignKey(CaseType,null=True, on_delete=models.SET_NULL)
    lawyer = models.ManyToManyField("lawyers.Lawyer", blank=True)
    #########################pytthon####### added #############################
    staff = models.ManyToManyField("lawyers.OtherStaff", blank=True)
    chinese_wall=models.BooleanField(default=False)


    client = models.ManyToManyField('clients.Client')
    date_updated = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now=False)
    date_received = models.DateTimeField(default=now,editable=True)
    court = models.ForeignKey(Court, null=True, on_delete=models.SET_NULL)
    closed = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    comments = GenericRelation(Comment)
    added_by = models.ForeignKey("lawyers.user", on_delete=models.CASCADE)




    """Model definition for Case."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for Case."""

        verbose_name = 'Case'
        verbose_name_plural = 'Cases'

    def __str__(self):
        """Unicode representation of Case."""
        return self.name

    def get_absolute_url(self):
        return reverse("cases:case_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("cases:case_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("cases:case_delete", kwargs={"pk": self.pk})


class ChineseWall(models.Model):
    mycase = models.ForeignKey(Case,null=True, on_delete=models.SET_NULL)
    chinese_lawyer = models.ManyToManyField("lawyers.Lawyer", blank=True)
    chineses_staff = models.ManyToManyField("lawyers.OtherStaff", blank=True)


class CaseFile(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    title = models.CharField(default="", max_length=250)
    file = models.FileField(upload_to="attachments/")
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for CaseFile."""

        verbose_name = 'Case File'
        verbose_name_plural = 'Case Files'
        ordering = ['title']

    def __str__(self):
        """Unicode representation of CaseFile."""
        return self.case.name


class PriorityLevel(models.Model):
    """Model definition for PriorityLevel."""
    priority = models.CharField(max_length=250)

    # TODO: Define fields here

    class Meta:
        """Meta definition for PriorityLevel."""

        verbose_name = 'Priority Level'
        verbose_name_plural = 'Priority Levels'

    def __str__(self):
        """Unicode representation of PriorityLevel."""
        return self.priority


class CaseTask(models.Model):
    """Model definition for CaseTask."""
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    task = models.CharField(max_length=250)
    description = RichTextField(blank=True,null=True)

    date_modefied = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(auto_now=False)
    priority_level = models.ForeignKey(
        PriorityLevel, null=True, on_delete=models.SET_NULL)
    complete = models.BooleanField(default=False)
    frequency=models.ForeignKey(Frequency,null=True,on_delete=models.CASCADE)
    box_number = models.CharField(default="", max_length=250, null=True)
    aisle_number = models.CharField(default="", max_length=250, null=True)
    shelf = models.CharField(default="", max_length=250, null=True)
    dated_created = models.DateTimeField(auto_now=True)

    # TODO: Define fields here


    class Meta:
        """Meta definition for CaseTask."""

        verbose_name = 'Case Task'
        verbose_name_plural = 'Case Tasks'
        ordering = ['dated_created', 'deadline']

    def __str__(self):
        """Unicode representation of CaseTask."""
        return self.task



class CaseArchive(models.Model):
    """Model definition for CaseArchives."""
    case = models.OneToOneField(Case, null=True, on_delete=models.SET_NULL)
    archived_by = models.ForeignKey(
        "lawyers.OtherStaff", null=True, on_delete=models.SET_NULL)
    date_archived = models.DateTimeField(auto_now=True)
    date_modefied = models.DateTimeField(auto_now=True)
    box_number=models.CharField(max_length=250,default="")
    aisle_number=models.CharField(max_length=250,default="")
    shelf=models.CharField(max_length=250,default="")

    # TODO: Define fields here

    class Meta:
        """Meta definition for CaseArchives."""

        verbose_name = 'Archived  Cases'
        verbose_name_plural = 'Archived Cases'

    def __str__(self):
        """Unicode representation of CaseArchive."""
        return self.case.name

    def get_absolute_url(self):
        return reverse("cases:archive_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("cases:archive_update", kwargs={"pk": self.pk})


class LegalArgument(models.Model):
    argument = models.CharField(max_length=350, unique=True)
    authorities = models.TextField()
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.argument

    class Meta:

        verbose_name = 'Legal Argument'
        verbose_name_plural = 'Legal Arguments'




class CourtSession(models.Model):
    lawyer = models.ForeignKey(
        'lawyers.User', null=True, on_delete=models.SET_NULL)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=250)
    start_time = models.DateTimeField(auto_now=False)

    end_time = models.DateTimeField(auto_now=False)

    def __str__(self):
        return self.case.name

    def get_absolute_url(self):
        return reverse("cases:session_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("cases:session_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("cases:session_delete", kwargs={"pk": self.pk})


class Process(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    process = models.CharField(max_length=250, blank=True,null=True)
    description = RichTextField(blank=True,null=True)

    date_added = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(
        "lawyers.User", null=True, on_delete=models.SET_NULL)
    process_file=models.FileField(upload_to="processes/", null=True)
    box_number = models.CharField(max_length=250,default="")
    aisle_number=models.CharField(max_length=250,default="")
    shelf=models.CharField(max_length=250,default="")
    archived=models.BooleanField(default=False)

    def __str__(self):
        process = "Process :{}".format(self.process)
        return process
    def get_absolute_url(self):
        return reverse("cases:process_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'Process'
        verbose_name_plural = 'Processes'
        ordering = ['-date_added']




class Bill(models.Model):
    case=models.ForeignKey(Case,on_delete=models.CASCADE)
    rate=models.IntegerField()
    total=models.IntegerField()


    def __str__(self):
        return self.case



class PostAction(models.Model):
    case=models.ForeignKey(Case,null=True, on_delete=models.SET_NULL)
    bod=models.TextField()
    next_business=models.DateTimeField(auto_now=False)
    title=models.CharField(max_length=250, default="")
    report_type=models.ForeignKey(ReportType,null=True,blank=True,on_delete=models.SET_NULL)


    def __str__(self):

        return self.title


    class Meta:
        verbose_name='Post Action Report'
        verbose_name_plural="Post Action Report"







class RequestArchive(models.Model):
    case_title=models.CharField(max_length=250,null=True)
    case_number=models.CharField(max_length=250,null=True)
    suit_number=models.CharField(max_length=250,null=True)
    client_name=models.CharField(max_length=250,null=True)
    requested_by=models.ForeignKey("lawyers.User",null=True, on_delete=models.SET_NULL)
    approved=models.BooleanField(default=False)


    def __str__(self):
        return self.case_title

    class Meta:



        verbose_name = 'Request From Archive'
        verbose_name_plural = 'Request From Archives'




class Timer(models.Model):
    case=models.ForeignKey(Case, related_name='cases', on_delete=models.CASCADE)
    is_active=models.BooleanField(default=False)

    name_task = models.CharField(max_length = 200,null=True)
    purpose_of_task = models.CharField(max_length = 9000,null=True)
    hour_time = models.IntegerField(null=True)
    minutes_time = models.IntegerField(null=True)
    seconds_time = models.IntegerField(null=True)
    total_charge_payment = models.FloatField(null=True)
    user=models.ForeignKey('lawyers.User',on_delete=models.CASCADE)
    date_time_created = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.case.name


class TermsOfEngagement(models.Model):
    title = models.CharField(default="", max_length=250)
    case=models.ForeignKey(Case,null=True,on_delete=models.CASCADE)
    date_add=models.DateTimeField(auto_now=True)
    upload_file=models.FileField(upload_to="terms/",null=True,blank=True)
    added_by=models.ForeignKey('lawyers.User',null=True,on_delete=models.CASCADE)




class EngagementTerm(models.Model):
    """Model definition for EngagementTerm."""
    case=models.ForeignKey(Case,null=True,on_delete=models.CASCADE)
    client=models.ForeignKey('clients.Client',null=True,on_delete=models.CASCADE)
    terms= RichTextField(blank=True,null=True)
    date_add=models.DateTimeField(auto_now=True)
    seen=models.BooleanField(default=False)
    file=models.FileField(upload_to="terms/",null=True,blank=True)
    added_by=models.ForeignKey('lawyers.User',null=True,on_delete=models.CASCADE)


    def get_absolute_url(self):

        return reverse('clients:terms_detail', kwargs={'pk': self.pk})


    # TODO: Define fields here

    class Meta:
        """Meta definition for EngagementTerm."""

        verbose_name = 'Terms of Engagement'
        verbose_name_plural = 'Terms of Engagement'


    def __str__(self):
        """Unicode representation of EngagementTerm."""
        return f"{self.client.name} - Terms of Engagement"

    # def save(self):
    #     """Save method for EngagementTerm."""
    #     pass

    # def get_absolute_url(self):
    #     """Return absolute url for EngagementTerm."""
    #     return ('')

    # TODO: Define custom methods here


THE_EXPENSE_CATEGORY = (
    ('Its_Denied','Its_Denied'),
    ('Approved', 'Approved'),
    ('Expense_Pending', 'Expense_Pending'),
    ('Already_exit', 'Already_exit'),

)

EXPENSE_CATEGORY = (
    ('Denied','Denied'),
    ('Approved', 'Approved'),
    ('Pending', 'Pending'),
    ('Exists', 'Exists'),

)

class Expense(models.Model):
    """Model definition for Expense."""
    case=models.ForeignKey(Case, related_name='expense', on_delete=models.CASCADE)
    amount=models.FloatField(null=False,default=0.00)
    user=models.ForeignKey('lawyers.User',null=True,on_delete=models.SET_NULL)
    description = RichTextField(blank=True,null=True)
    timestamp=models.DateTimeField(auto_now=True)
    expense_category = models.CharField(max_length=100, choices=THE_EXPENSE_CATEGORY, default='Already_exit')
    is_approved = models.BooleanField(default = False)
    categories = models.CharField(max_length=100, choices=EXPENSE_CATEGORY, default='Exists')




    # TODO: Define fields here

    class Meta:
        """Meta definition for Expense."""

        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'

    def __str__(self):
        """Unicode representation of Expense."""
        return self.case.name

    # def save(self):
    #     """Save method for Expense."""
    #     pass

    def get_absolute_url(self):

        return reverse('cases:expense_detail', kwargs={'pk': self.pk})
    # TODO: Define custom methods here


class Renumeration(models.Model):
    case=models.ForeignKey(Case,related_name='renumeration',null=True,on_delete=models.SET_NULL)
    lead=models.ForeignKey('lawyers.Lawyer',related_name='renum_requests',null=True,on_delete=models.SET_NULL)
    timestamp=models.DateTimeField(auto_now=True)
    approved=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.case.name} / {self.lead.user}"

    class Meta:
        ordering=['timestamp']

class PaymentStatus(models.Model):
    status=models.CharField(max_length=250)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = "Payment Status"

class PaymentEnquiry(models.Model):
    case=models.ForeignKey(Case,related_name='case_enquiry',null=True,on_delete=models.SET_NULL)
    client=models.ManyToManyField('clients.Client',related_name='enquired_clients')
    lead=models.ForeignKey('lawyers.Lawyer',related_name='payment',null=True,on_delete=models.SET_NULL)
    timestamp=models.DateTimeField(auto_now=True)
    status=models.ForeignKey(PaymentStatus,null=True,blank=True, on_delete=models.SET_NULL)
    approved=models.BooleanField(default=False)
    updated_by=models.ForeignKey('lawyers.User',null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.case.name} requested by {self.lead}'


    class Meta:
        ordering=['timestamp']
        verbose_name_plural = "Payment Enquiries"


class Invoice(models.Model):
    case=models.ForeignKey(Case, related_name='invoice_cases', on_delete=models.CASCADE)
    name_task = models.ManyToManyField(Timer)
    expenses = models.ManyToManyField(Expense, blank=True)
    total_charge_payment = models.FloatField(null=True)
    timestamp=models.DateTimeField(auto_now=True)
    Total_amount = models.FloatField(null=True)
    total_expense = models.FloatField(null=True)
    Paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.case.name} invoice'