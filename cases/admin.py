from django.contrib import admin
from .models import *
from django.contrib.admin.models import LogEntry,ContentType, ADDITION,CHANGE,DELETION


class CaseAdmin(admin.ModelAdmin):
    list_display = ('name','court_number','case_number','lead_professional')
    search_fields=['name','court_number']

admin.site.register(Case, CaseAdmin)
admin.site.register(Invoice)
admin.site.register(LogEntry)

admin.site.register(Frequency)
admin.site.register(Timer)
admin.site.register(TermsOfEngagement)
admin.site.register(EngagementTerm)

admin.site.register(Category)
admin.site.register(ChineseWall)


admin.site.register(Process)
admin.site.register(Renumeration)
admin.site.register(PostAction)
admin.site.register(CourtSession)
admin.site.register(Court)
admin.site.register(RequestArchive)
admin.site.register(ReportType)
admin.site.register(PaymentStatus)
admin.site.register(PaymentEnquiry)
admin.site.register(CaseType)
admin.site.register(Expense)
admin.site.site_header = "Lawyer System. Admin"
admin.site.site_title = "Lawyer System. Admin Portal"
admin.site.index_title = "Welcome to Lawyer System. Admin Portal"