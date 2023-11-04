from django.shortcuts import render, redirect, get_object_or_404
from lawyers.models import Lawyer, OtherStaff, User,Team,Role,LawyerStatus
from .forms import UserForm, OtherStaffForm, LawyerForm, OtherStaffForm, UpdateUserForm, UpdateForm, StaffUpdateForm, StaffProfileForm, LawyerProfileForm,TeamForm,RoleForm,LawyerStatusForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
# Create your views here.
from django.contrib.auth import update_session_auth_hash
from clients.models import Client
from django.contrib.auth.models import Group
from cases.user_actions import log_deletion,log_change,add_log

from django.views.generic import ListView,DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
from cases.models import Case, Status,Bill,CourtSession,EngagementTerm,Expense,Invoice,TermsOfEngagement
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from .decorators import group_required, groups_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from documents.models import DocumentRecord, Document, DocumentStatus
from cases.forms import CaseForms
from principles.forms import PrinciplesForm
from lawyers.models import Team
from django.db.models import Sum
from django.db.models import Q
from django.contrib.admin.models import LogEntry


@login_required
def accounts(request):
    lawyer_form = LawyerForm()
    user_form = UserForm()

    context = {
        'lawyer_form': lawyer_form,
        'user_form': user_form,
    }

    return render(request, 'accounts/signup.html', context)


@login_required
def lawyer_profile_view(request):

    if request.method == 'POST':
        user_form = UserForm(request.POST or None)
        lawyer_form = LawyerForm(request.POST or None)

        if user_form.is_valid() and lawyer_form.is_valid():
            team=user_form.cleaned_data['team']

            user = user_form.save(commit=False)
            add_log(request.user.pk,user,"added a lawyer")
            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password1')
            email = user_form.cleaned_data.get('email')
            user.set_password(password)
            user.save()
            # user = authenticate(request, username=email, password=password)




            my_group = Group.objects.get(pk=2)
            my_group.user_set.add(user)
            lawyer = Lawyer.objects.create(
                user=user, bar_number=lawyer_form.instance.bar_number, lawyer_status=lawyer_form.instance.lawyer_status)

            if team:
                lawyer_team=Team.objects.get(pk=team.pk)
                lawyer_team.lawyer.add(lawyer)

            messages.success(request, "Lawyer has been added")

            return HttpResponseRedirect(reverse('accounts:lawyer_detail', args=[lawyer.pk]))
        else:
            messages.error(request,user_form.errors)
            return redirect('accounts:lawyer_list')

    else:
        messages.error(request, "Lawyer could not be added")

        lawyer_form = LawyerForm()
        user_form = UserForm()

    return render(request, 'accounts/signup.html', {'user_form': user_form, 'lawyer_form': lawyer_form})


@login_required
def lawyer_list(request):
    lawyers = Lawyer.objects.all()
    user_form = UserForm(request.POST or None)
    lawyer_form = LawyerForm(request.POST or None)
    context = {
        'lawyers': lawyers,
        'lawyer_form': lawyer_form,
        'user_form': user_form
    }

    return render(request, 'accounts/lawyers.html', context)


@login_required
def lawyer_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    all_team = Team.objects.filter(team_leader__user = request.user)
    lawyer = get_lawyer(user)
    user_form = LawyerProfileForm(request.POST or None, instance=request.user)
    lawyer_form = LawyerForm(request.POST or None, instance=lawyer)
    cases = Case.objects.filter(lawyer=lawyer)
    # cases = Case.objects.select_related('lawyer').filter(lawyer__user=user)
    print(cases)
    pending = Case.objects.filter(closed=False)
    completed = Case.objects.filter(closed=True)
    case_form = CaseForms()
    context = {
        'lawyer': lawyer,
        'user_form': user_form,
        'lawyer_form': lawyer_form,
        'cases': cases,
        'pending': pending,
        'completed': completed,
        'form': case_form,
        'p_form': PrinciplesForm(request.POST or None),
        'all_team':all_team,
    }

    return render(request, 'accounts/lawyer-profile.html', context)


@login_required
def lawyer_detail(request, pk):
    lawyer = get_object_or_404(Lawyer, pk=pk)
    team=Team.objects.filter(lawyer=lawyer)[0]
    cases=Case.objects.filter(
            Q(team=team) | Q(lawyer =lawyer) )
    logs=LogEntry.objects.filter(user_id=lawyer.user.id)
    # cases = Case.objects.filter(lawyer=lawyer)lead_professional 
    pending = Case.objects.filter(lawyer=lawyer, closed=False)
    completed = Case.objects.filter(lawyer=lawyer, closed=True)
    user_form = StaffUpdateForm(request.POST or None, instance=lawyer.user)
    lawyer_form = LawyerForm(request.POST or None, instance=lawyer)

    print(cases)
    print(cases.count())
    context = {
        'lawyer': lawyer,
        'cases': cases,
        'pending': pending,
        'completed': completed,
        'user_form': user_form,
        'lawyer_form': lawyer_form,
        'logs':logs,
    }

    return render(request, 'accounts/lawyer_detail.html', context)


@login_required
def other_staff(request):
    staff_list = OtherStaff.objects.all()
    staff_form = OtherStaffForm()
    user_form = UserForm()

    context = {
        'staff_list': staff_list,
        'staff_form': staff_form,
        'user_form': user_form
    }

    return render(request, 'accounts/staff_list.html', context)


def get_status(id):
    qs = Status.objects.get(id=id)
    if qs:
        return qs
    else:
        return None


@login_required
def update_lawyer_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    lawyer = get_lawyer(user)
    if request.method == 'POST':

        user_form = LawyerProfileForm(
            request.POST or None, request.FILES or None, instance=request.user)
        lawyer_form = LawyerForm(request.POST or None, instance=lawyer)

        if user_form.is_valid() and lawyer_form.is_valid():
            user = user_form.save(commit=False)

            lawyer_form.instance.user = request.user

            user.save()
            lawyer_form.save()
            log_change(request.user.pk,user,"updated lawyer profile")
            messages.success(request, "profile has been updated")
            print("success")

            return HttpResponseRedirect(reverse('accounts:lawyer_profile', args=[user.pk]))

        else:
            print("failed")
            return HttpResponseRedirect(reverse('accounts:lawyer_profile', args=[user.pk]))

    else:

        user_form = LawyerProfileForm(
            request.POST or None, instance=request.user)
        lawyer_form = LawyerForm(request.POST or None, instance=lawyer)

    return render(request, "accounts/lawyer-profile.html", {'lawyer_form': lawyer_form, 'user_form': user_form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            log_change(request.user.pk,user,"changed password")
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('logout')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


@login_required
def add_staff(request):

    if request.method == "POST":
        staff_form = OtherStaffForm(request.POST or None)
        user_form = UserForm(request.POST or None)

        if user_form.is_valid() and staff_form.is_valid():

            user = user_form.save(commit=False)
            team=user_form.cleaned_data['team']
            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password1')
            email = user_form.cleaned_data.get('email')
            user.set_password(password)

            user.save()
            my_group = Group.objects.get(pk=1)
            my_group.user_set.add(user)

            staff_form.instance.user = user
            staff=staff_form.save()
            if team:

                staff_team=Team.objects.get(pk=team.pk)
                staff_team.support_staff.add(staff)

            add_log(request.user.pk,staff,"added a staff")
            messages.success(request,"user has been added")
            return redirect('accounts:staff_list')
        else:
            messages.error(request, user_form.errors)
            return redirect('accounts:staff_list')

    else:
        staff_form = OtherStaffForm()
        user_form = UserForm()

    return render(request, "accounts/add_staff.html", {'staff_form': staff_form, 'user_form': user_form})


@login_required
def staff_details(request, pk):
    staff = get_object_or_404(OtherStaff, pk=pk)
    user_form = StaffUpdateForm(instance=staff.user)
    staff_form = OtherStaffForm(instance=staff)

    logs=LogEntry.objects.filter(user_id=staff.user.id)

    
    team=Team.objects.filter(support_staff=staff)[0]
    cases=Case.objects.filter(
            Q(team=team) | Q(staff =staff) )




    doc = Document.objects.filter(added_by=staff.user)
    rec = DocumentRecord.objects.filter(approved_by=staff)
    print(rec)
    not_available = Document.objects.select_related(
        'status').filter(status__title='Not Available')

    context = {
        'staff': staff,
        'user_form': user_form,
        'staff_form': staff_form,
        'rec': rec,
        'doc': doc,
        'logs':logs,
        'cases':cases,
    }

    return render(request, 'accounts/staff_detail.html', context)


@login_required
def update_staff(request, pk):
    staff = get_object_or_404(OtherStaff, pk=pk)

    if request.method == "POST":
        user_form = StaffUpdateForm(
            request.POST, request.FILES, instance=staff.user)
        staff_form = OtherStaffForm(request.POST or None, instance=staff)

        if user_form.is_valid() and staff_form.is_valid():

            user_form.save()
            staff_form.instance.user = staff.user
            staff.save()

            log_change(request.user.pk,staff,"updated a staff")
            messages.success(request, 'User has been Updated')

            return HttpResponseRedirect(reverse('accounts:staff_detail', args=[staff.pk]))
        else:
            print(user_form.errors)
            print(staff_form.errors)
            messages.error(request, 'Failed to update user')
            return HttpResponseRedirect(reverse('accounts:staff_detail', args=[staff.pk]))
    else:
        user_form = StaffUpdateForm
        staff_form = OtherStaffForm()

    return render(request, "accounts/staff_detail.html", {'user_form': user_form, 'staff_form': staff_form})

@login_required
def staff_detail_view(request, pk):
    try:
        user = get_object_or_404(User, pk=pk)
        staff=get_object_or_404(OtherStaff,user=user)
        user_form = StaffProfileForm(request.POST or None, instance=request.user)
        staff_form = OtherStaffForm(request.POST or None, instance=staff)
        doc = Document.objects.filter(added_by=request.user)
        rec = DocumentRecord.objects.select_related(
        'approved_by').filter(approved_by__user=request.user)
        print(rec)
        not_available = Document.objects.select_related(
        'status').filter(status__title='Not Available')
        team=Team.objects.filter(support_staff=staff)[0]
        cases=Case.objects.filter(
            Q(team=team) | Q(staff =staff) )

    except:
        return redirect("/")

    context = {
        'staff': staff,
        'rec': rec,
        'doc': doc,
        'not_status': not_available,
        'user_form': user_form,
        'staff_form': staff_form,
        'cases':cases
    }

    return render(request, "accounts/staff_profile.html", context)

@login_required
def update_staff_profile(request, pk):
    staff = get_object_or_404(OtherStaff, pk=pk)

    if request.method == 'POST':

        user_form = StaffProfileForm(
            request.POST or None,request.FILES or None, instance=request.user)
        staff_form = OtherStaffForm(request.POST or None, instance=staff)

        if user_form.is_valid() and staff_form.is_valid():
            user = user_form.save(commit=False)

            staff_form.instance.user = request.user
            # test=Case.objects.filter(team__support_staff=staff)[0]


            user.save()
            staff_form.save()
            log_change(request.user.pk,user,"updated staff profile")
            messages.success(request, "profile has been updated")
            print("success")

            return HttpResponseRedirect(reverse('accounts:staff_profile', args=[user.pk]))

        else:
            print("failed")
            return HttpResponseRedirect(reverse('accounts:staff_profile', args=[user.staff]))

    else:

        user_form = StaffProfileForm(
            request.POST or None, instance=request.user)
        staff_form = OtherStaffForm(request.POST or None, instance=staff)

    return render(request, "accounts/lawyer-profile.html", {'staff_form': staff_form, 'staff_form': user_form})


@login_required
def update_lawyers_profile(request, pk):
    lawyer = get_object_or_404(Lawyer, pk=pk)

    if request.method == 'POST':

        user_form = StaffUpdateForm(
            request.POST, request.FILES, instance=lawyer.user)
        lawyer_form = LawyerForm(request.POST , instance=lawyer)
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

        if user_form.is_valid() and lawyer_form.is_valid():

            user_form.save()
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            print(user_form.errors)
            print(lawyer_form.errors)
            # lawyer_form.instance.user=request.user

            x = lawyer_form.save()
            log_change(request.user.pk,x,"updated lawyer profile")
            messages.success(request, "profile has been updated")

            return HttpResponseRedirect(reverse('accounts:lawyer_detail', args=[lawyer.pk]))

        else:
            print("failed")

            print(lawyer_form.errors)
            print(user_form.errors)

            return HttpResponseRedirect(reverse('accounts:lawyer_detail', args=[lawyer.pk]))

    else:

        user_form = StaffUpdateForm(
            request.POST or None, instance=request.user)
        staff_form = OtherStaffForm(request.POST or None, instance=staff)

    return render(request, "accounts/lawyer-profile.html", {'lawyer_form': lawyer_form, 'user_form': user_form})


def get_lawyer(user):
    lawyer = Lawyer.objects.get(user=user)
    if lawyer:
        return lawyer
    else:
        return None


@login_required
def delete_lawyer(request, pk):
    lawyer = get_object_or_404(Lawyer, pk=pk)
    if request.method == "POST":
        log_deletion(request.user.pk,lawyer,"deleted a lawyer")
        lawyer.delete()
        messages.success(request, "Lawyer has been deleted")

        return redirect("accounts:lawyer_list")

    return render(redirect, "accounts/lawyer.html")


@login_required
def delete_staff(request, pk):
    staff = get_object_or_404(OtherStaff, pk=pk)
    if request.method == "POST":
        log_deletion(request.user.pk,staff,"deleted a staff")
        staff.delete()
        messages.success(request, "Staff has been deleted")

        return redirect("accounts:staff_list")

    return render(redirect, "accounts/staff_list.html")



@login_required
def client_dashboard(request,pk):
    client=get_object_or_404(Client,pk=pk)
    user=client.user

    case_list=Case.objects.filter(client=client)
    closed_list=Case.objects.filter(client=client,closed=True)
    active_list=Case.objects.filter(client=client,closed=False)
    bill_list=Bill.objects.filter(case__client=client)


    context={
        'client':client,
        'case_list':case_list,
        'active_list':active_list,
        'closed_list':closed_list,
        'bill_list':bill_list,


    }

    return render(request,'client_dash/home.html',context)


@login_required
def get_case_details(request,pk):
    case=get_object_or_404(Case,pk=pk)
    client=Client.objects.get(user=request.user)
    lawyers = case.lawyer.all()
    session_list=CourtSession.objects.filter(case=case)

    context={
        'case':case,
        'client':client,
        'session_object': CourtSession.objects.filter(case=case).reverse(),
        'lawyers':lawyers,
        'session_list':session_list


    }

    return render(request,'client_dash/case_detail.html',context)



@login_required()
def team_list_view(request):
    team_list=Team.objects.all()
    context={
        'team_list':team_list,
        'form':TeamForm(request.POST or None )
    }


    return render(request,'accounts/teams/list.html',context)

@login_required()
def add_team(request):

    if request.method=="POST":
        form=TeamForm(request.POST or None , request.FILES or None)

        if form.is_valid():
            x = form.save()
            add_log(request.user.pk,x,"added a team")
            messages.success(request,"Team has been added")
            return redirect('accounts:teams')
        else:
            messages.error(request,form.errors)

    else:
        form=TeamForm()


    return render(request,'accounts/teams/list.html',{'form':form})





def team_detail(request,pk):

    team=get_object_or_404(Team,pk=pk)
    form=TeamForm(request.POST or None,request.FILES or None , instance=team)
    lawyers=team.lawyer.all()
    s_staff=team.support_staff.all()


    context={
        'team':team,
        'form':form,
        'lawyers':lawyers,
        's_staff':s_staff
        }

    return render (request, 'accounts/teams/team-detail.html',context)




def update_team(request,pk):

    team=get_object_or_404(Team,pk=pk)
    if request.method=="POST":


        form = TeamForm(request.POST or None, request.FILES or None, instance=team)

        if form.is_valid():

            x=form.save()
            log_change(request.user.pk,x,"updated team")
            messages.success(request,'team has been updated')
            return HttpResponseRedirect(reverse('accounts:team_detail' ,args=[team.pk]))
        else:
            messages.error(request,form.erros)
            return HttpResponseRedirect(reverse('accounts:team_detail' ,args=[team.pk]))
    else:
           form=TeamForm()
    return render(request,'accounts/teams/team-detail.html',{'form':form})



def delete_team(request,pk):
    team=get_object_or_404(Team,pk=pk)

    if team:
        log_deletion(request.user.pk,team,"deleted team")
        team.delete()
        messages.success(request,"team has been deleted")
        return redirect('accounts:teams')
    else:
        messages.error(request,"this team does not exist")

    return render(request,'accounts/teams/team-detail.html')


def team_update(request,pk):
    team=get_object_or_404(Team,pk=pk)

    if request.method=="POST":
        form=TeamForm(request.POST or None,request.FILES or None, instance=team)

        if form.is_valid():
            x = form.save()
            log_change(request.user.pk,x,"updated team")
            messages.success(request,"Team has been updated")
            return HttpResponseRedirect(reverse('accounts:team_detail', args=[team.pk]))
        else:
            messages.error(request,"failed to upload team")

    else:
        form=TeamForm(request.POST or None,request.FILES or None , instance=team)
    return render(request,'accounts/teams/update-team.html',{'form':form,'team':team})






@login_required
def add_role(request):

    if request.method=="POST":
        form= RoleForm(request.POST or None)
        if form.is_valid():
            role=form.save()
            user=request.user
            add_log(user.pk,role,'added a new role')
            messages.success(request,"role has been added")
            return redirect('accounts:role_list')
        else:
            messages.error(request,form.errors)
            return redirect('accounts:role_list')

    else:
        form=RoleForm()
    return render(request,"accounts/roles/role_list.html",{'form':form})

@login_required
def role_list(request):
    role_list=Role.objects.all().order_by('-pk')
    return render(request,"accounts/roles/role_list.html",{"role_list":role_list,'form':RoleForm()})

@login_required
def role_detail(request,pk):
    role=get_object_or_404(Role,pk=pk)
    form=RoleForm(request.POST or None , instance=role)
    # log_change(request.user.pk,role,"viewed a role")
    context={"role":role,"form":form}
    return render(request,"accounts/roles/role_detail.html",context)

@login_required
def update_role(request,pk):
    role=get_object_or_404(Role,pk=pk)
    if request.method=="POST":
        form=RoleForm(request.POST or None , instance=role)
        if form.is_valid():
            statusr=form.save()
            log_change(request.user.pk,statusr,"updated a role")
            messages.success(request,"role has been updated")
            return HttpResponseRedirect(reverse('accounts:role_detail', args=[role.pk]))
        else:
            messages.error(request,form.errors)
            return HttpResponseRedirect(reverse('accounts:role_detail', args=[role.pk]))
    else:
        form=RoleForm(request.POST or None , instance=role)
    return render(request,"accounts/roles/role_detail.html",{'form':form})

@login_required
def delete_role(request,pk):
    role=get_object_or_404(Role,pk=pk)
    if role:
        log_deletion(request.user.pk,role,"deleted a statusresentation")
        role.delete()
        messages.success(request,"statusresentation has been deleted")
        return redirect('accounts:role_list')
    else:
        messages.error(request,f"{role} couldnt not be deleted because it doesnt exist")
        return HttpResponseRedirect(reverse('accounts:role_detail', args=[role.pk]))
    return render(request,"accounts/roles/role_detail.html")








@login_required
def add_status(request):

    if request.method=="POST":
        form= LawyerStatusForm(request.POST or None)
        if form.is_valid():
            status=form.save()
            user=request.user
            add_log(user.pk,status,'added a post a new lawyer status')
            messages.success(request,"lawyer status has been added")
            return redirect('accounts:status_list')
        else:
            messages.error(request,form.errors)
            return redirect('accounts:status_list')
    else:
        form=LawyerStatusForm()
    return render(request,"accounts/status/status_list.html",{'form':form})

@login_required
def status_list(request):
    status_list=LawyerStatus.objects.all().order_by('-pk')
    return render(request,"accounts/status/status_list.html",{"status_list":status_list,'form':LawyerStatusForm()})

@login_required
def status_detail(request,pk):
    status=get_object_or_404(LawyerStatus,pk=pk)
    form=LawyerStatusForm(request.POST or None , instance=status)
    # log_change(request.user.pk,status,"viewed a statusresentation")
    context={"status":status,"form":form}
    return render(request,"accounts/status/status_detail.html",context)

@login_required
def update_status(request,pk):
    status=get_object_or_404(LawyerStatus,pk=pk)
    if request.method=="POST":
        form=LawyerStatusForm(request.POST or None , instance=status)
        if form.is_valid():
            statusr=form.save()
            log_change(request.user.pk,statusr,"updated a statusresentation")
            messages.success(request,"statusresentation has been updated")
            return HttpResponseRedirect(reverse('accounts:status_detail', args=[status.pk]))
        else:
            messages.error(request,form.errors)
            return HttpResponseRedirect(reverse('accounts:status_detail', args=[status.pk]))
    else:
        form=LawyerStatusForm(request.POST or None , instance=status)
    return render(request,"accounts/status/status_detail.html",{'form':form})

@login_required
def delete_status(request,pk):
    status=get_object_or_404(LawyerStatus,pk=pk)
    if status:
        log_deletion(request.user.pk,status,"deleted a statusresentation")
        status.delete()
        messages.success(request,"statusresentation has been deleted")
        return redirect('accounts:status_list')
    else:
        messages.error(request,f"{status} couldnt not be deleted because it doesnt exist")
        return HttpResponseRedirect(reverse('cases:status_detail', args=[status.pk]))
    return render(request,"accounts/status/status_detail.html")





@group_required('Accounts')
@login_required
def case_detail_acc(request,pk):
    case=get_object_or_404(Case,pk=pk)
    try:
        terms=EngagementTerm.objects.filter(case=case)[0]
        timer=Timer.objects.filter(case=case)
        timer_sum=Timer.objects.filter(case=case).aggregate(Sum('time_spent'))
        timer_average=Timer.objects.filter(case=case).aggregate(Avg('time_spent'))

        ts=round((timer_sum['time_spent__sum']/3600),2)
        ta=round((timer_average['time_spent__avg']/3600),2)

    except:
        terms=None
        timer=None
        ts=0
        ta=0

    lawyers = case.lawyer.all()
    team=case.team
    team_lawyers=team.lawyer.all()
    support_staff=team.support_staff.all()
    users = []



    for lawyer in lawyers:
        users.append(lawyer.user)
    for i in team_lawyers:
        users.append(i.user)

    sm=Expense.objects.filter(case=case).aggregate(Sum('amount'))



    users=list(dict.fromkeys(users))
    print(terms)



    termsofengagement = TermsOfEngagement.objects.filter(case = case)
    retainertermsofengagement = EngagementTerm.objects.filter(case = case)

    context={
        'case':case,
        'terms':terms,
        'clients':case.client.all(),
        'users':users,
        'timer_list':timer,
        'timer_sum':ts ,
        'timer_avg':ta,
        'support_staff':support_staff,
        'session_object': CourtSession.objects.filter(case=case).reverse(),
        'expense_list':Expense.objects.filter(case=case),
        'expense_sum':sm['amount__sum'],
        'termsofengagement': termsofengagement,
        'retainertermsofengagement':retainertermsofengagement

    }
    print(case.client.all())

    return render(request,"acc_dash/case_detail.html",context)


@login_required
def account_expense(request):
    expense_list = Expense.objects.filter(
        Q(categories='Exists') | Q(categories ='Approved'))
    
    context = {
        'expense_list' : expense_list,
    }
    return render(request,"acc_dash/all_expenses.html",context)

class AccountExpense(LoginRequiredMixin,ListView):
    model=Expense
    template_name='acc_dash/all_expenses.html'
    

@login_required
def get_case_expenses(request,pk):
    case=get_object_or_404(Case,pk=pk)
    expense_list=Expense.objects.filter(
        Q(categories='Exists') | Q(categories ='Approved'),
        case=case)
    expense_sum=Expense.objects.filter(
        Q(categories='Exists') | Q(categories ='Approved'),case=case).aggregate(Sum('amount'))
    return render(request,'acc_dash/case_expense.html',{'expense_list':expense_list,'case':case,'expense_sum':expense_sum['amount__sum']})



@login_required
def invoice_list(request):
    invoice = Invoice.objects.all()
    
    context = {
        'invoice_list' : invoice,
    }
    return render(request,"invoice/invoice_list.html",context)


@login_required
def invoice_detail(request,pk):
    invoice =get_object_or_404(Invoice,id=pk)
    total_pay = round((invoice.total_expense + invoice.Total_amount),2)
    
    context = {
        'invoice_detail' : invoice,
        'total_pay' : total_pay,
    }
    return render(request,'invoice/account_invoice.html',context)

def approve_invoice(request,pk):
    Invoice.objects.filter(id = pk).update(
        Paid = True
        )

    messages.success(request,"invoice has been paid")
    
    return redirect(request.META['HTTP_REFERER'])
    
