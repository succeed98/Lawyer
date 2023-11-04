from django.shortcuts import render,get_object_or_404,redirect
from cases.models import *
from documents.models import Document,DocumentRecord
from lawyers.models import *
from cases.models import Case, CaseTask
from documents.models import Document
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.decorators import group_required, groups_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from cases.models import
from datetime import datetime, date
from datetime import datetime, timedelta
from cases.tasks import notify_user
from clients.models import Client
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import Group
from notify.models import Notification
from django.http import HttpResponseNotFound
from sentry_sdk import capture_message
from django.contrib import messages
from django.contrib.admin.models import LogEntry
from cases.user_actions import add_log,log_change,log_deletion

@login_required
def index(request):
    if request.user.groups.filter(name ='Accounts').exists():
        return redirect('account_dash')
    elif request.user.groups.filter(name ='Client').exists():
        get_client = Client.objects.filter(user=request.user).first()
        return HttpResponseRedirect(
                reverse("clients:client_detail", args=[get_client.id])
            )
    else:

        user=get_object_or_404(User,pk=request.user.id)
        user_id=user.pk
        logs_count=LogEntry.objects.filter(user_id=user_id).count()
        logs=LogEntry.objects.filter(user_id=user_id)


        lawyer = Lawyer.objects.all()
        lawyer_count = Lawyer.objects.all().count()
        case = Case.objects.all()
        document = Document.objects.all()
        user = request.user
        recs = DocumentRecord.objects.filter(approved=False)
        request.session['recs'] = recs.count()
        pending = Case.objects.filter(closed=False)
        request.session['pending'] = pending.count()

        completed = Case.objects.filter(closed=True)
        request.session['completed'] = completed.count()
    # request.session['other_staff']=Otherstaff.objects.get(user=request.user)
        date_me = datetime.now()+timedelta(15)
        close = CaseTask.objects.filter(
        deadline__lte=date_me)


        c = CaseTask.objects.all()
    
    all_cases = Case.objects.all()
    events = CaseTask.objects.all()
    events_month = CaseTask.objects.all()
    event_list = []
    event_list1 = []
    
    # users = []
    for all_case in all_cases:
        users = []
        lawyers = all_case.lawyer.all()
        staffs = all_case.staff.all()
        team=all_case.team
        team_lawyers=team.lawyer.all()
        
        for lawyer in lawyers:
            users.append(lawyer.user)
            print("@@@@@lawyer@@@@")
            print(lawyer)
        for i in staffs:
            print("@@@@@staff@@@@")
            print(i)
            users.append(i.user)

        for k in team_lawyers:
            print("@@@@@team@@@@")
            print(k)

            users.append(k.user)

        print(all_case)
        print("jkm")
        print(users)
        for i in users:
            print("sdfsdf")
            if request.user == i:
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                print("printsfd")
                event_list1.append(all_case)
                for event in events:
                    if event.case == all_case:
                        print("\n\n\n\n\n\n\n\n\n\n")
                        print("Yes")
                        event_list.append(
                            {
                                "id": event.id,
                                "title": all_case.name,
                                "start": event.deadline.date().strftime("%Y-%m-%dT%H:%M:%S"),
                                "end": event.deadline.date().strftime("%Y-%m-%dT%H:%M:%S"),
                            }
                        )


    context = {
        'lawyer': lawyer,
        'case': case,
        'document': document,
        "events": event_list, 
        "events_month": events_month,
        'logs_count':logs_count,
        'logs':logs,
        'lawyer_count':lawyer_count,
    }

    return render(request, 'firm/index.html', context)


class FirmChart(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        doc = Document.objects.all()
        case = Case.objects.all()
        available = Document.objects.select_related(
            'status').filter(status__title='Available')
        not_available = Document.objects.select_related(
            'status').filter(status__title='Not Available')
        complete = Case.objects.filter(closed=True)
        pending = Case.objects.filter(closed=False)

        clients = Client.objects.all()
        client_count = clients.count()

        case_count = case.count()
        comp_count = complete.count()
        pend_count = pending.count()
        doc_count = doc.count()
        default = [client_count, case_count, comp_count, pend_count]
        avail_count = available.count()

        labels = [
            'Clients', 'Cases', 'Closed/Archived Cases', 'Active Cases'
        ]

        data2 = [doc_count, available.count(), not_available.count()]
        label1 = ['All Documents', 'Available Documents',
                  'Unavailable Documents']
        data = {
            'labels': labels,
            'default': default,
            'label1': label1,
            'data2': data2



        }

        return Response(data)


@login_required
def user_path(request):
    lawyer=Group.objects.get(pk=2)
    staff=Group.objects.get(pk=1)
    client=Group.objects.get(pk=3)
    group = request.user.groups.all()


    print(group)
    if get_lawyer(request.user):
        return HttpResponseRedirect(reverse('accounts:lawyer_profile', args=[request.user.pk]))
    elif get_staff(request.user):

        return HttpResponseRedirect(reverse('index'))
    elif get_client(request.user):
        client=get_client(request.user)
        return HttpResponseRedirect(reverse('accounts:client_dashboard',args=[client.pk]))

    else:
        return HttpResponseRedirect(reverse('index'))

    template='user_path.html'
    return render(request,template)



def get_staff(user):
    try:


        qs = OtherStaff.objects.get(user=user)
        if qs:
            return qs
    except:
        return None




def get_lawyer(user):
    try:

        qs = Lawyer.objects.get(user=user)
        if qs :
            return qs
    except:
        return None


def get_client(user):
    try:

        qs = Client.objects.get(user=user)
        if qs:
            return qs
    except:
        return None

@login_required
def my_notifications(request):
    notifications=Notification.objects.filter(recipient=request.user.pk)[:15]
    unread_list=Notification.objects.filter(recipient=request.user.pk,read=False)[:15]
    read_list=Notification.objects.filter(recipient=request.user.pk,read=True)[:15]
    context={
        'notifications':notifications,
        'unread_list':unread_list,
        'read_list':read_list
    }



    return render(request,'notifications/includes/default.html',context)

def all_read(request):
    user=request.user
    notifications=Notification.objects.filter(recipient=request.user.pk,read=False)


    for i in notifications:

        i.read=True
        i.save()

    print(notifications)
    messages.success(request,"all notifications have been read")
    return redirect('user_notifications')


    return render(request,"notifications/includes/default.html")




def all_unread(request):
    user=request.user
    notifications=Notification.objects.filter(recipient=request.user.pk,read=True)

    for i in notifications:

        i.read=False
        i.save()

    print(notifications)

    messages.error(request,"all notifications have been unread")
    return redirect('user_notifications')
    return render(request,"notifications/includes/default.html")


def mark_as_read(request,pk):
    object=get_object_or_404(Notification,pk=pk)

    if object:
        object.read=True
        object.save()
        messages.success(request,'Message marked as read')
        return redirect('user_notifications')
    else:
        messages.error(request,'failed to mark notification as read')
        return redirect('user_notifications')
    return render(request,'notifications/includes/default.html')


def go_to_target(request,pk):
    try:
        myobjects=get_object_or_404(Notification,pk=pk)
        # case = get_object_or_404(Case, pk=pk)


        if myobjects:
            myobjects.read=True
            x = myobjects.save()
            log_change(request.user.pk,x,"message marked as read")
            messages.success(request,'Message marked as read')
        else:
            messages.error(request,'failed to mark notification as read')
        main_url = myobjects.target.get_absolute_url()
        
        print("\n\n\n\n\n\n\n\n\n")
        print(main_url)
        return redirect(main_url)

    except:
        messages.error(request,'There are no reference')
        return redirect(request.META['HTTP_REFERER'])


    





def mark_as_unread(request,pk):
    object=get_object_or_404(Notification,pk=pk)

    if object:
        object.read=False
        x = object.save()
        log_change(request.user.pk,x,"message marked as unread")
        messages.success(request,'Message marked as unread')
        return redirect('user_notifications')
    else:
        messages.error(request,'failed to mark notification as unread')
        return redirect('user_notifications')
    return render(request,'notifications/includes/default.html')




def mark_as_deleted(request,pk):
    object=get_object_or_404(Notification,pk=pk)

    if object:
        object.soft_delete=True
        log_deletion(request.user.pk,object,"deleted message")
        messages.success(request,'Notification has been deleted')
        return redirect('user_notifications')
    else:
        messages.error(request,'notification has been deleted')
        return redirect('user_notifications')
    return render(request,'notifications/includes/default.html')



def my_custom_page_not_found_view(*args, **kwargs):
    capture_message("Pages not found!", level="error")

    # return any response here, e.g.:
    return HttpResponseNotFound("Not found")


@login_required
def user_logs(request,pk):
    user=get_object_or_404(User,pk=pk)
    user_id=user.pk
    logs=LogEntry.objects.filter(user_id=user_id)
    context={
        'logs':logs,
        'user':user
    }
    # TODO Mark all as REad
    return render(request,'firm/user_logs.html',context)



def account_dash(request):
    cases=Case.objects.all()
    clients=Client.objects.all()
    print(cases.count())
    print(clients.count())
    context={
        'cases':cases,
        'case_count':cases.count(),
        'client_count':clients.count()
    }
    return render(request,"acc_dash/index.html",context)

#TODO mark all as unread



@login_required
def view_team_logs(request):
    try:
        # all_team = get_object_or_404(Team,team_leader_user = request.user )
        all_team = Team.objects.filter(team_leader__user = request.user).first()
        
        team_lawyers = all_team.lawyer.all()
        team_support_staff = all_team.support_staff.all()

        user_list = []

        all_logs = []

        for lawyer in team_lawyers:
            user_list.append(lawyer.user)
        
        for staff in team_support_staff:
            user_list.append(staff.user)
        
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n")

        for i in user_list:
            user=get_object_or_404(User,id=i.id)
            user_id=user.pk
            logs=LogEntry.objects.filter(user_id=user_id)
            all_logs.extend(logs)

        

        # all_team = Team.objects.all()

        print("\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print(all_logs)
    except:
        all_logs = []
        

    context = {
        'logs':all_logs,
    }
    return render(request, 'cases/user_logs_team.html', context) 