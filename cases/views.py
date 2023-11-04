from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import (Case, Category, Status, CaseTask,CaseFile, LegalArgument, Court, CourtSession,Process,
PostAction,Representative,RequestArchive,Timer,Expense,Renumeration,PaymentEnquiry,PaymentStatus,ChineseWall,Invoice,TermsOfEngagement)
from lawyers.models import Lawyer, OtherStaff, User,Role
# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .forms import (CaseForm, CaseTaskForm, CaseFileForm, CaseArchiveForm, CaseForms,
                         CategoryForm, LegalArgumentForm, CourtForm,
                         CourtSessionForm, ProcessForm,ProcessForm2,ExpenseForm,
                         ArchiveUpdateForm,PostActionForm,RepresentationForm,RequestForm,PaymentEnquiryForm,ChineseWallForm, ChineseWallFormEdit,TermsOfEngagementForm)
from django.urls import reverse
from accounts.decorators import group_required, groups_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import CaseArchive, Invoice
from django.utils.crypto import get_random_string
from .tasks import notify_user, notify_staff, notify_task
from django.core.paginator import Paginator
# from datetime import datetime, timedelta
from django.utils import timezone
from correspondents.forms import CaseCorrespondentForm
from correspondents.models import Correspondent
import datetime
from notify.signals import notify
from cases.user_actions import add_log,log_change,log_deletion
from django.core.mail import send_mail

from datetime import timedelta, time
from django.conf import settings
from django.utils.timezone import make_aware
import uuid
from background_task.models import Task
from django.contrib.admin.models import LogEntry,ContentType, ADDITION,CHANGE,DELETION
from django.db.models import Sum , Avg
from django.contrib.auth.models import Group
from clients.models import Payment, Client #Dartisan 12.04.2021 --> Added Client class from clients.models
from django.contrib.auth import get_user_model
from django.db.models import Q



@login_required
def pending_list(request):
    form = CaseForms()


    pending = Case.objects.filter(closed=False)
    request.session['pending'] = pending.count()
    chinese_form = ChineseWallForm()
    # print(pending)

    context = {

        'form': form,
        'pending': pending,
        'chinese_form': chinese_form,
    }

    return render(request, 'cases/pending.html', context)


@login_required
def completed_list(request):
    form = CaseArchiveForm()
    file_form=CaseFileForm()

    completed = CaseArchive.objects.filter(case__closed=True,case__archived=True)

    request.session['completed'] = completed.count()


    context = {

        'form': form,
        'completed': completed,
        'file_form':file_form
    }

    return render(request, 'cases/completed.html', context)


@login_required
def case_detail(request, pk):

    case = get_object_or_404(Case, pk=pk)
    task_form = CaseTaskForm()
    file_form = CaseFileForm(request.POST or None, request.FILES or None)
    terms_form = TermsOfEngagementForm(request.POST or None, request.FILES or None)
    arguments = LegalArgument.objects.filter(case=case)[:4]
    corrs_form = CaseCorrespondentForm(request.POST or None)
    corrs_object=Correspondent.objects.filter(case=case)[:6]
    processes=Process.objects.filter(case=case)


    team=case.team
    team_lawyers=team.lawyer.all()
    team_staff=team.support_staff.all()
    support_staff=team.support_staff.all()
    lawyers = case.lawyer.all()
    staffs = case.staff.all()
    task_list = CaseTask.objects.filter(case=case).reverse()[:5]
    form = CaseForm(instance=case)
    case_files = CaseFile.objects.filter(case=case)[:5]
    users = []
    chinese_wall_users = []

    


    if case.chinese_wall == True:
        # chinese_wall_al = ChineseWall.objects.filter(mycase = case)
        chinese_wall = ChineseWall.objects.get(mycase = case)
        chinese_wall_form = ChineseWallFormEdit(instance = chinese_wall)
        chinese_wall_people = chinese_wall.chinese_lawyer.all()
        chinese_wall_people1 = chinese_wall.chineses_staff.all()

        for chinese_lawyer in chinese_wall_people:
            chinese_wall_users.append(chinese_lawyer.user)

        for chinese_lawyer in chinese_wall_people1:
            chinese_wall_users.append(chinese_lawyer.user)
    
    else:
        chinese_wall_form = ChineseWallFormEdit()




        for lawyer in lawyers:
            print(lawyer)
            users.append(lawyer.user)


        for i in team_lawyers:
            print(i)
            users.append(i.user)


        for i in team_staff:
            print(i)
            users.append(i.user)


        for i in staffs:
            print("@@@@@")
            print(i)
            users.append(i.user)

    try:
        payment=Payment.objects.filter(case=case)[0]
    except:
        payment=None

    users=list(dict.fromkeys(users))
    print("\n\n\n\n\n\n\n\n")
    print(users)

    context = {
        'case': case,
        'lawyers': lawyers,
        'form1': form,
        'chinese_wall_users':chinese_wall_users,
        'task_list': task_list,
        'task_form': task_form,
        'file_form': file_form,
        'case_files': case_files,
        'users': users,
        'arg_form': LegalArgumentForm(request.POST or None),
        'arguments': arguments,
        'corrs_form': corrs_form,
        'session_form': CourtSessionForm(request.POST or None),
        'session_object': CourtSession.objects.filter(case=case).reverse(),
        'corrs_object':corrs_object,
        'process_form':ProcessForm(request.POST or None),
        'processes':processes,
        'action_form':PostActionForm(request.POST or None),
        'payment':payment,
        'chinese_wall_form': chinese_wall_form,
        'terms_form':terms_form,
    }

    return render(request, 'cases/case_detail.html', context)


@login_required
def add_case(request):

    if request.method == "POST":
        form = CaseForms(request.POST or None, request.FILES or None)

        if form.is_valid():
            form.instance.added_by = request.user

            name = request.user
            x = form.save()
            add_log(request.user.id,x,"added a new brief")
            x.save()
            team = x.team.lawyer.all()
            added_stuffs = x.staff.all()
            s_staff = x.team.support_staff.all()
            team_list = list(map(lambda y: y.user, team))
            staff_list = list(map(lambda k:k.user, s_staff))
            added_stuffs_list = list(map(lambda l:l.user, added_stuffs))
            lawyer = x.lawyer.all()
            lawyer_list = list(map(lambda n: n.user, lawyer))
           

            if team:
                notify.send(request.user, recipient_list=added_stuffs_list, actor=request.user,
                            verb='added a new ', nf_type='followed_by_one_user', object=x, target=x)
                for i in added_stuffs:
                    msg1 = "New Case - {}".format(x.name)
                    msg2 = "Dear {} {}, You have been added by {} {} to a new case :{} ".format(
                        i.user.first_name, i.user.last_name, name.first_name, name.last_name, x.name)
                    notify_user(msg1, msg2, i.user.id)

            if added_stuffs:
                notify.send(request.user, recipient_list=staff_list, actor=request.user,
                            verb='added a new ', nf_type='followed_by_one_user', object=x, target=x)
                for i in s_staff:
                    msg1 = "New Case - {}".format(x.name)
                    msg2 = "Dear {} {} , You have been added by {} {} to a new case :{} ".format(
                        i.user.first_name, i.user.last_name, name.first_name, name.last_name, x.name)
                    notify_user(msg1, msg2, i.user.id)

            if s_staff:
                notify.send(request.user, recipient_list=staff_list, actor=request.user,
                            verb='added a new ', nf_type='followed_by_one_user', object=x, target=x)
                for i in s_staff:
                    msg1 = "New Case - {}".format(x.name)
                    msg2 = "Dear {} {} , You have been added by {} {} to a new case :{} ".format(
                        i.user.first_name, i.user.last_name, name.first_name, name.last_name, x.name)
                    notify_user(msg1, msg2, i.user.id)

            if lawyer:
                notify.send(request.user, recipient_list=lawyer_list, actor=request.user,
                            verb='added a new ', nf_type='followed_by_one_user', object=x, target=x)
                for i in lawyer:
                    msg1 = "New Case - {}".format(x.name)
                    msg2 = "Dear {} {} , You have been added by {} {} to a new case :{} ".format(
                        i.user.first_name, i.user.last_name, name.first_name, name.last_name, x.name)
                    notify_user(msg1, msg2, i.user.id)

            print(lawyer)
            messages.success(request, "Case has been added")
            return redirect('cases:case_list')

        else:
            messages.error(
                request, form.errors)
            print(form.errors)
            return redirect('cases:case_list')

    else:
        form = CaseForms()

    return render(request, "cases/case_list_view.html", {'form': form,'form_errors':form.errors})


@login_required
def update_case(request, pk):
    case = get_object_or_404(Case, pk=pk)
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("@@@@@@@@@@@@@@@@@@@@@@@")
    print("sdfasfjasf")
    if request.method == "POST":
        form = CaseForm(request.POST or None,
                        request.FILES or None, instance=case)


        chinese_form = ChineseWallFormEdit(request.POST or None,request.FILES or None)
        # chinese_form = ChineseWallFormEdit(request.POST or None)
        if form.is_valid():
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            print("@@@@@@@@@@@@@@@@@@@@@@@")
            print("sdfasfjasf")
            print(request.POST)


            
            # form_chinese = request.POST['chinese_wall']
            # print(form_chinese)
            form.instance.user = request.user

            name = request.user

            




            x=form.save()


            
            team = x.team.lawyer.all()
            s_staff = x.team.support_staff.all()
            team_list = list(map(lambda y: y.user, team))
            staff_list = list(map(lambda k: k.user, s_staff))
            lawyer = x.lawyer.all()
            lawyer_list = list(map(lambda n: n.user, lawyer))

            if team:
                notify.send(request.user, recipient_list=team_list, actor=request.user,
                            verb='added a new ', nf_type='followed_by_one_user', object=x, target=x)
                for i in team:
                    msg1 = "New Case - {}".format(x.name)
                    msg2 = "Dear {} {} , You have been added by {} {} to a new case :{} ".format(
                        i.user.first_name, i.user.last_name, name.first_name, name.last_name, x)
                    notify_user(msg1, msg2, i.user.id)

            if s_staff:
                notify.send(request.user, recipient_list=staff_list, actor=request.user,
                            verb='added a new ', nf_type='followed_by_one_user', object=x, target=x)
                for i in s_staff:
                    msg1 = "New Case - {}".format(x.name)
                    msg2 = "Dear {} {} , You have been added by {} {} to a new case :{} ".format(
                        i.user.first_name, i.user.last_name, name.first_name, name.last_name, x)
                    notify_user(msg1, msg2, i.user.id)

            if lawyer:
                notify.send(request.user, recipient_list=lawyer_list, actor=request.user,
                            verb='added a new ', nf_type='followed_by_one_user', object=x, target=x)
                for i in lawyer:
                    msg1 = "New Case - {}".format(x.name)
                    msg2 = "Dear {} {} , You have been added by {} {} to a new case :{} ".format(
                        i.user.first_name, i.user.last_name, name.first_name, name.last_name, x)
                    notify_user(msg1, msg2, i.user.id)

            log_change(request.user.pk,x,"changed a brief")
            messages.success(request, 'brief has been updated')
            return HttpResponseRedirect(reverse('cases:case_detail', args=[case.id]))
        else:

            messages.error(request, 'something went horribly wrong')

            return HttpResponseRedirect(reverse('cases:case_detail', args=[case.id]))

    else:
        form = CaseForm(request.POST or None,
                        request.FILES or None, instance=case)

    return render(request, 'cases/case_detail.html', {'form': form})


@login_required
def delete_case(request, pk):
    case = get_object_or_404(Case, pk=pk)
    case.delete()
    log_deletion(request.user.pk,case,"deleted a brief")
    messages.success(request, 'brief has been deleted')
    return redirect('cases:case_list')


@login_required
def add_task(request, pk):
    case = get_object_or_404(Case, pk=pk)

    if request.method == "POST":
        task_form = CaseTaskForm(request.POST or None)



        if task_form.is_valid():





            task_form.instance.case = case
            frequency=task_form.instance.frequency
            print(frequency.value)
            task=task_form.save()

            lawyers = case.lawyer.all()


            days = task_form.instance.deadline-timezone.now()

            check = int(days.days)


            for l in lawyers:
                msg1 = "{} -{} ".format(task_form.instance.task, case.name)
                msg2 = "Dear {},please note that you have a task ({}-{})  scheduled for {}.".format(
                    l.user, task_form.instance.task, case.name,  task_form.instance.deadline)



                notify_task(msg1, msg2, l.user.id, repeat=frequency.value,
                                repeat_until=task_form.instance.deadline,creator=task)

                add_log(request.user.pk,task,"added a task")
                messages.success(request, "Task has been added")
                return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))
        else:
            messages.error(
                request, task_form.errors)
            return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))

    else:
        task_form = CaseTaskForm()

    return render(request, "cases/case_detail.html", {'task_form': task_form})



######################################################## EDIT TASK ############################################################################


def edit_task(request,pk):
    case_task=get_object_or_404(CaseTask,pk=pk)
    case=case_task.case
    lawyers=case.lawyer.all()



    if request.method == "POST":
        task_form = CaseTaskForm(request.POST or None, instance=case_task)

        if task_form.is_valid():
            task=get_task(case_task.pk)


            case=case_task.case
            lawyers=case.lawyer.all()
            frequency=task_form.instance.frequency






            if task:


                task.delete()

                ts=task_form.save()
                log_change(request.user.pk,ts,"changed a task")

                for l in lawyers:
                    msg1 = "{} -{} ".format(task_form.instance.task, case.name)
                    msg2 = "Dear {},please note that you have a task ({}-{})  scheduled for {}.".format(
                    l.user, task_form.instance.task, case.name,  task_form.instance.deadline)


                    notify_task(msg1, msg2, l.user.id, repeat=frequency.value,
                            repeat_until=task_form.instance.deadline,creator=task)




                messages.success(request,"Task has been updated")
                return HttpResponseRedirect(reverse('cases:edit_task', args=[case_task.pk] ))


            else:


                task_form.save()

                for l in lawyers:
                    msg1 = "{} -{} ".format(task_form.instance.task, case.name)
                    msg2 = "Dear {},please note that you have a task ({}-{})  scheduled for {}.".format(
                    l.user, task_form.instance.task, case.name,  task_form.instance.deadline)


                    notify_task(msg1, msg2, l.user.id, repeat=frequency.value,
                        repeat_until=task_form.instance.deadline,creator=task)

                messages.success(request,"Task has been updated")
                return HttpResponseRedirect(reverse('cases:edit_task', args=[case_task.pk] ))
        else:
            messages.warning(request,"please check your form")
            messages.warning(request,task_form.errors)
            return HttpResponseRedirect(reverse('cases:edit_task', args=[case_task.pk] ))




    else:
        task_form=CaseTaskForm(instance=case_task)


    return render(request,"cases/tasks/update_task.html",{'task_form':task_form,'task':case_task,'case':case})




def get_task(c_task):

    """ FETCH TASK FROM BACKGROUND_TASKS FROM A CONTENT TYPE INSTANCE """



    try:
        qs=Task.objects.get(creator_object_id=c_task)
        return qs
    except Task.MultipleObjectsReturned as e:
        print('ERR====>', e)
        return None

    except Task.DoesNotExist:
        return None



def upload_terms_files(request, pk):
    case = get_object_or_404(Case, pk=pk)

    if request.method == "POST":

        file_form = TermsOfEngagementForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('upload_file')
        if file_form.is_valid():
            for f in files:
                unique_id = get_random_string(length=2)
                case_title ="{}".format(f.name.split(".")[0])
                new_files = TermsOfEngagement.objects.create(
                    case=case, title=case_title, upload_file=f, added_by = request.user)
                add_log(request.user.pk,new_files,"added Terms Of Engagement files")

            messages.success(request, "Files have been added")
            return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))

        else:

            messages.error(
                request, "Failed to add Files, please check your form")
            return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))
    else:
        file_form = CaseFileForm()
        return render(request, "cases/case_detail.html", {'file_form': file_form})




def terms_files_list(request, pk):
    case = get_object_or_404(Case, pk=pk)

    termsofengagement = TermsOfEngagement.objects.filter(case = case)

    context = {
        'termsofengagement': termsofengagement
    }
    return render(request, "cases/termsofengagement.html",context)



def terms_edit(request):
    if request.method == "POST":
        files = request.FILES.get('upload_file')
        terms_id = request.POST['terms_id']
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        if files:
            get_terms = get_object_or_404(TermsOfEngagement, id = terms_id)
            TermsOfEngagement.objects.filter(id = terms_id).update(
                upload_file = files
            )
            print("ok oooooooooooooooooooooooooo")
        else:
            get_terms = get_object_or_404(TermsOfEngagement, id = terms_id)
            



        messages.success(request, "Files have been Edited")

        return redirect(request.META['HTTP_REFERER'])



def upload_files(request, pk):
    case = get_object_or_404(Case, pk=pk)

    if request.method == "POST":

        file_form = CaseFileForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('file')
        if file_form.is_valid():
            for f in files:
                unique_id = get_random_string(length=2)
                case_title ="{}".format(f.name.split(".")[0])
                new_files = CaseFile.objects.create(
                    case=case, title=case_title, file=f)
                print(f.name)
                print(new_files)
                add_log(request.user.pk,new_files,"added case files")

            messages.success(request, "Files have been added")
            return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))

        else:

            messages.error(
                request, "Failed to add Files, please check your form")
            return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))
    else:
        file_form = CaseFileForm()
        return render(request, "cases/case_detail.html", {'file_form': file_form})


@login_required
def new_case(request):

    if request.method == "POST":
        form = CaseForm(request.POST or None)


        if form.is_valid():
            form.instance.added_by = request.user
            print("this is  {}".format(request.user))


            form.save()
            messages.success(request, "Case has been added")
            return redirect('cases:case_list')
        else:
            print(form.errors)
            messages.error(
                request, "Oops Something went wrong , please try again")
            return redirect('cases:case_list')

    else:
        form = CaseForm()

    return render(request, "cases/new_case.html", {'form': form})


def get_staff(user):
    qs = OtherStaff.objects.get(user=user)
    if qs:
        return qs
    else:
        return None



class CaseCreateView(CreateView):
    # model = Case
    template_name = "cases/add_case.html"
    form_class = CaseForms()

    def form_valid(self):
        self.form.instance.added_by = self.request.user
        self.form.save()

        messages.success(self.request, "Case has been added")


class CaseList(ListView):
    model = Case
    template_name = "cases/case_list_view.html"

    def get_context_data(self, **kwargs):
        context = super(CaseList, self).get_context_data(**kwargs)
        context['form'] = CaseForms(self.request.POST or None)
        context['chinese_form'] = ChineseWallForm(self.request.POST or None)
        context['process_form'] = ProcessForm(self.request.POST or None)
        context['case_list']=Case.objects.all().order_by('-pk')

        return context


def get_status(status):

    qs = Status.objects.filter(title=status)
    if qs[0]:
        return
    else:
        return None


class CategoryListView(ListView):
    model = Category
    template_name = "cases/category/cat_list.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['form'] = CategoryForm(self.request.POST or None)
        context['category_list']=Category.objects.filter(parent=None)
        return context




@login_required
def cat_update(request, pk):
    cat = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            log_change(request.user.pk,cat,'changed a case category')
            messages.success(request, "Category has been updated")
            return HttpResponseRedirect(reverse('cases:cat_list'))

        else:
            messages.error(request, "Category was not updated")
            # return redirect('cases:cat_list.html')
            return HttpResponseRedirect(reverse('cases:cat_list'))

    else:
        form = CategoryForm()

    return render(request, "cases/category/delete.html")


@login_required
def cat_add(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat=form.save()
            add_log(request.user.pk,cat,'add a new category')
            messages.success(request, "Category has been added")
            return redirect('cases:cat_list')

        else:
            messages.error(request, "Category was not added")
            return redirect('cases:cat_list')

    else:
        form = CategoryForm()

    return render(request, "cases/category/delete.html")


@login_required
def delete_cat(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        cat.delete()
        log_deletion(request.user.pk,cat,"deleted category")
        messages.success(request, "Category has been deleted")
        return redirect('cases:cat_list')

    return render(request, "cases/category/delete.html")


@login_required
def add_argument(request, pk):
    case = get_object_or_404(Case, pk=pk)

    if request.method == "POST":
        arg_form = LegalArgumentForm(request.POST or None)

        if arg_form.is_valid():
            arg_form.instance.case = case
            # if not get_arg(arg_form.instance.argument):

            x = arg_form.save()
            add_log(request.user.pk,x,"added a legal argument")
            messages.success(request, " Legal Argument has been added")
            return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))

            #
        else:
            messages.error(request, "Please check your form for errors")
            return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))

    else:
        arg_form = LegalArgumentForm()

    return render(request, "cases/case_detail.html", {'arg_form': arg_form})


def get_arg(arg):
    qs = LegalArgument.objects.get(argument=arg)
    if qs:
        return True
    else:
        return False


@login_required
def cat_detail(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    # log_change(request.user.pk,cat,'viewed a category')
    case_list=Case.objects.filter(category=cat)

    context = {
        'cat': cat,
        'cat_form': CategoryForm(request.POST or None, instance=cat),
        'case_list':case_list,
        'subs':Category.objects.filter(parent=cat)

    }

    return render(request, 'cases/category/detail.html', context)


@login_required
def file_list(request, pk):
    case = get_object_or_404(Case, pk=pk)

    file_list = CaseFile.objects.filter(case=case)

    # log_change(request.user.pk,file_list,'viewed file list')
    context = {
        'case': case,
        'file_list': file_list,
        'file_form': CaseFileForm(request.POST or None, request.FILES or None)

    }

    return render(request, 'cases/file_list.html', context)


@login_required
def delete_files(request, pk):
    file = get_object_or_404(CaseFile, pk=pk)
    case = file.case
    if request.method == "POST":
        file.delete()
        log_deletion(request.user.pk,file,"deleted case files")
        messages.success(request, "File Has Been Deleted")
        return HttpResponseRedirect(reverse('cases:file_list', args=[case.pk]))

    return render(request, "cases/file_list.html")


@login_required
def task_view(request, pk):
    case = get_object_or_404(Case, pk=pk)

    tasks = CaseTask.objects.filter(case=case)
    task_list = CaseTask.objects.filter(case=case)

    # log_change(request.user.pk,task_list,'viewed a task view')

    paginator = Paginator(task_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    task_form = CaseTaskForm(request.POST or None)
    context = {

        'tasks': tasks,
        'page_obj': page_obj,
        'case': case,
        'task_form': task_form

    }

    return render(request, "cases/task_list.html", context)

# def task_list_view


@login_required
def task_list_view(request, pk):
    case = get_object_or_404(Case, pk=pk)

    tasks = CaseTask.objects.filter(case=case)
    task_list = CaseTask.objects.filter(case=case)

    paginator = Paginator(task_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    task_form = CaseTaskForm(request.POST or None)
    context = {

        'tasks': tasks,
        'page_obj': page_obj,
        'task_form': task_form,
        'case': case,

    }

    return render(request, "cases/list_tasks.html", context)


@login_required
def completed(request, pk):

    task = get_object_or_404(CaseTask, pk=pk)
    case = task.case

    context={'task':task,'case':case}

    if task.complete == False:
        task.complete = True
        task.save()
        
        log_change(request.user.pk,task,'completed a task')

        messages.success(request, "Task has been completed")
        return HttpResponseRedirect(reverse('cases:list_tasks', args=[case.pk]))

    else:
        task.complete = False
        task.save()
        messages.success(request, "Task has been  masrked as pending")

        return HttpResponseRedirect(reverse('cases:list_tasks', args=[case.pk]))

    return render(request, "cases/list_tasks.html", context)


@login_required
def delete_task(request, pk):
    task = get_object_or_404(CaseTask, pk=pk)
    case = task.case
    if task:
        task.delete()
        log_deletion(request.user.pk,task,'deleted a task')
        messages.success(request, "Task has been deleted")
        return HttpResponseRedirect(reverse('cases:list_tasks', args=[case.pk]))

    return render(request, "cases/list_tasks.html")


@login_required
def argument_list(request, pk):
    case = get_object_or_404(Case, pk=pk)
    argument_list = LegalArgument.objects.filter(case=case)

    context = {
        'form': LegalArgumentForm(request.POST or None),
        'argument_list': argument_list,
        'case': case
    }

    return render(request, 'cases/arg_list.html', context)


@login_required
def argument_detail(request, pk):
    arg = get_object_or_404(LegalArgument, pk=pk)
    case = arg.case
    context = {
        'arg': arg,
        'case': case,
        'form': LegalArgumentForm(request.POST or None, instance=arg)
    }

    return render(request, "cases/arg_detail.html", context)


@login_required
def arg_update(request, pk):
    arg = get_object_or_404(LegalArgument, pk=pk)
    if request.method == "POST":
        form = LegalArgumentForm(request.POST or None, instance=arg)
        if form.is_valid():
            x = form.save()

            log_change(request.user.pk,x,"updated a legal arguement")
            messages.success(request, "Argument has Been Updated")
            return HttpResponseRedirect(reverse('cases:argument_detail', args=[arg.pk]))

        else:
            messages.error(request, "Argument could not be updated")
            return HttpResponseRedirect(reverse('cases:argument_detail', args=[arg.pk]))

    else:
        form = LegalArgumentForm()

    return render(request, 'cases/arg_detail.html', {'form': form, 'case': arg.case})


@login_required
def arg_delete(request, pk):
    arg = get_object_or_404(LegalArgument, pk=pk)
    case = arg.case

    if arg:
        arg.delete()
        log_deletion(request.user.pk,arg,"deleted a legal argument")
        messages.success(request, "Argument has Been Deleted")
        return HttpResponseRedirect(reverse('cases:argument_list', args=[case.pk]))
    else:



        return HttpResponseRedirect(reverse('cases:argument_detail', args=[arg.pk]))

    return render(request, 'cases/arg_detail.html')


def case_filter(request):
    f = CaseFilter(request.GET, queryset=Case.objects.all())
    return render(request, 'cases/filter.html', {'filter': f})


@login_required
def complete_case(request, pk):
    case = get_object_or_404(Case, pk=pk)
    staff=OtherStaff.objects.filter(role__id=4)

    if case.closed:
        case.closed = False
        case.save()
        log_change(request.user.pk,case,'opened a case')
        messages.success(request, "case has been reopened")
        return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))

    else:
        case.closed = True
        case.save()
        log_change(request.user.pk,case,'closed a case')


        for st in staff:

            msg1 = f"{case} has been closed"
            msg2 = f"Dear {st}, {case} has been closed. Please scan the contents of this case and add it to the Archives"

            notify_staff(st.user.id, msg1, msg2)
            notify.send(request.user, recipient=st.user, actor=request.user,
                        verb='added a new ', nf_type='followed_by_one_user', object=case, target=case)

        messages.success(request, "case has been closed")
        return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))

    return render(request, "cases/case_detail.html")


@login_required
def court_list(request):
    courts = Court.objects.all()
    form = CourtForm

    context = {
        'courts': courts,
        'form': form
    }
    return render(request, 'cases/courts/court_list.html', context)


@login_required
def court_detail(request, pk):
    court = get_object_or_404(Court, pk=pk)
    # log_change(request.user.pk,court,'viewed a court')
    case_list=Case.objects.filter(court=court)

    context = {
        'court': court,
        'form': CourtForm(request.POST or None, instance=court),
        'case_list': case_list,

    }

    return render(request, 'cases/courts/court_detail.html', context)


@login_required
def add_court(request):
    if request.method == "POST":
        form = CourtForm(request.POST or None)

        if form.is_valid():
            court=form.save()
            add_log(request.user.pk,court,'added a court')

            messages.success(request, "court has been added")
            return redirect('cases:court_list')
    else:
        form = CourtForm()

    return render(request, 'cases/courts/courts_list.html', {'form': form})


@login_required
def update_court(request, pk):
    court = get_object_or_404(Court, pk=pk)

    if request.method == "POST":
        form = CourtForm(request.POST or None, instance=court)
        if form.is_valid():
            form.save()
            log_change(request.user.pk,court,'updated a court')
            messages.success(request, "court has been updated")
            return HttpResponseRedirect(reverse('cases:court_detail', args=[court.pk]))
        else:
            messages.error(request, "court could not updated")
            return HttpResponseRedirect(reverse('cases:court_detail', args=[court.pk]))
    else:
        form = CourtForm()

    return render(request, "cases/courts/court_detail.html", {'form': form})


@login_required
def court_delete(request, pk):
    court = get_object_or_404(Court, pk=pk)
    if request.method == "POST":

        log_deletion(request.user.pk,court,'deleted a court')
        court.delete()

        messages.success(request, "court has been deleted")
        return redirect('cases:court_list')
    else:
        messages.error(request, "court could not deleted")
        return HttpResponseRedirect(reverse('cases:court_detail', args=[court.pk]))

    return render(request, 'cases/courts/court_detail.html')


@login_required
def case_court(request, pk):
    court = get_object_or_404(Court, pk=pk)
    courts = Case.objects.filter(court=court)
    # log_change(request.user.pk,court,'viewed a court')

    context = {
        'court_list': courts,
        'cases':courts
    }

    return render(request, 'cases/case_list_view.html', context)


############################################### COURT SESSIONS ##############################################

@login_required
def add_session(request, pk):
    case = get_object_or_404(Case, pk=pk)
    if request.method == "POST":
        form = CourtSessionForm(request.POST or None)
        if form.is_valid():

            purpose = form.instance.purpose
            form.instance.case = case
            form.instance.lawyer = request.user
            start = request.POST.get("start_time")
            end = request.POST.get("end_time")
            s1 = start.replace("T", " ")
            e1 = end.replace("T", " ")

            start1 = datetime.datetime.strptime(
                s1, '%Y-%m-%d %H:%M')
            end1 = datetime.datetime.strptime(
                e1, '%Y-%m-%d %H:%M')

            settings.TIME_ZONE
            start1 = make_aware(start1)
            end1 = make_aware(end1)

            form.instance.start_time = start1
            form.instance.end_time = end1

            sess=form.save()
            add_log(request.user.pk,sess,'added a new court session')
            messages.success(request, "Court session has been added")
            return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))
        else:
            messages.error(request, "Court session could not be added")
            return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))

    else:
        form = CourtSessionForm()

    return render(request, 'cases/detail.html', {'session_form': form})


def edit_session(request,pk):
    object = get_object_or_404(CourtSession, pk=pk)
    case = object.case


    if request.method == "POST":
        form = CourtSessionForm(request.POST or None, instance=object)

        if form.is_valid():
            purpose = form.instance.purpose
            form.instance.case = case
            form.instance.lawyer = request.user
            start = request.POST.get("start_time")
            end = request.POST.get("end_time")
            s1 = start.replace("T", " ")
            e1 = end.replace("T", " ")

            start1 = datetime.datetime.strptime(
                s1, '%Y-%m-%d %H:%M')
            end1 = datetime.datetime.strptime(
                e1, '%Y-%m-%d %H:%M')

            settings.TIME_ZONE
            start1 = make_aware(start1)
            end1 = make_aware(end1)

            form.instance.start_time = start1
            form.instance.end_time = end1

            sess=form.save()
            log_change(request.user.pk,object,'Changed a court session')
            messages.success(request, "Court session has been updated")
            return HttpResponseRedirect(reverse('cases:session_detail', args=[object.pk]))

        else:
            messages.success(request, "Court session could not be updated")
            return HttpResponseRedirect(reverse('cases:session_detail', args=[object.pk]))

    else:
        form = CourtSessionForm(instance=object)


    return render(request,'cases/update_session.html',{'form':form,'case':case,'object':object})





@login_required
def update_session(request, pk):
    object = get_object_or_404(CourtSession, pk=pk)
    case = object.case

    if request.method == "POST":
        form = CourtSessionForm(request.POST or None, instance=object)

        if form.is_valid():
            purpose = form.instance.purpose
            form.instance.case = case
            form.instance.lawyer = request.user
            start = request.POST.get("start_time")
            end = request.POST.get("end_time")
            s1 = start.replace("T", " ")
            e1 = end.replace("T", " ")

            start1 = datetime.datetime.strptime(
                s1, '%Y-%m-%d %H:%M')
            end1 = datetime.datetime.strptime(
                e1, '%Y-%m-%d %H:%M')

            settings.TIME_ZONE
            start1 = make_aware(start1)
            end1 = make_aware(end1)

            form.instance.start_time = start1
            form.instance.end_time = end1

            form.save()
            log_change(request.user.pk,object,'Changed a court session')

            messages.success(request, "Court session has been updated")
            return HttpResponseRedirect(reverse('cases:session_detail', args=[object.pk]))

        else:
            messages.success(request, "Court session could not be updated")
            return HttpResponseRedirect(reverse('cases:session_detail', args=[object.pk]))

    else:
        form = CourtSessionForm()

    return render(request, "cases/session_detail.html", {'form': form})


@login_required
def detail_session(request, pk):
    object = get_object_or_404(CourtSession, pk=pk)
    case = object.case
    # log_change(request.user.pk, object, 'viewed a court session')

    return render(request, 'cases/session_detail.html', {'object': object, 'case': case, 'session_form': CourtSessionForm(request.POST or None, instance=object)})


@login_required
def delete_session(request, pk):
    object = get_object_or_404(CourtSession, pk=pk)
    case = object.case

    if request.method == "POST":
        log_deletion(request.user.pk,object,"deleted a court session")
        object.delete()
        messages.success(request, "Court session has been deleted")
        return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))
    else:
        messages.error(request, "Court session could not be deleted")
        return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))

    return render(request, "cases/session_detail.html")


@login_required
def add_process(request):

    if request.method == "POST":
        form = ProcessForm2(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.instance.added_by = request.user

            form.save()
            x=form.save()
            add_log(x.added_by.id,x,"added a new process")


            lawyers = x.case.lawyer.all()
            team=x.case.team.lawyer.all()
            s_staff=x.case.team.support_staff.all()
            team_list = list(map(lambda x: x.user, team))
            staff_list = list(map(lambda x: x.user, s_staff))
            lawyer_list = list(map(lambda x: x.user, lawyers))


            if lawyers:
                for lawyer in lawyers:
                    notify.send(request.user, recipient_list=lawyer_list, actor=request.user,
                                verb='added a new process', nf_type='followed_by_one_user', object=x,
                                target=x)
                    msg1 = "New Process {}".format(form.instance.process)
                    msg2 = "Dear {}, please note that you have new process {} for your case ({})".format(
                        lawyer, form.instance.process, x.case)
                    notify_staff(lawyer.user.id, msg1, msg2)
            if team:
                notify.send(request.user, recipient_list=team_list, actor=request.user,
                            verb='added a new process', nf_type='followed_by_one_user', object=x,
                            target=x)
                for lawyer in team:

                    msg1 = "New Process {}".format(form.instance.process)



                    msg2 = "Dear {}, please note that you have new process {} for your case ({})".format(
                        lawyer, form.instance.process, x.case)
                    notify_staff(lawyer.user.id, msg1, msg2)
            if s_staff:
                notify.send(request.user, recipient_list=staff_list, actor=request.user,
                            verb='added a new process', nf_type='followed_by_one_user', object=x, target=x)
                for staff in s_staff:
                    for lawyer in s_staff:
                        msg1 = "New Process {}".format(form.instance.process)
                        msg2 = "Dear {}, please note that you have new process {} for your case ({})".format(
                            lawyer, form.instance.process, x.case)
                        notify_staff(lawyer.user.id, msg1, msg2)




            messages.success(request, 'Process has been added')
            return redirect('cases:list_process')
        else:
            messages.error(request, form.errors)
            return redirect('cases:list_process')

    else:
        form = ProcessForm2()

    return render(request, "cases/processes/process_list.html", {'form': form})


@login_required
def generate_process1(request, pk):
    case = get_object_or_404(Case, pk=pk)
    if request.method == "POST":
        # name1 = request.FILES['process_file']
        name1 = request.FILES.get('file')
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print(name1)

        case = get_object_or_404(Case, pk=pk)

        form = ProcessForm(request.POST or None, request.FILES or None)
        file_name = name1.name
        file_name_only = file_name.split(".")[0]
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        # print(file_name_only)
        # form.instance.process = file_name_only
        # form.instance.added = request.user
        # form.instance.case = case
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        # print(form.instance.case)
        process = Process.objects.create(case = case, added_by= request.user, process = file_name_only,process_file= name1)

        # process=form.save()
        print(process)
        add_log(request.user.pk,process,"added new process")


        lawyers = case.lawyer.all()
        team = case.team.lawyer.all()
        s_staff = case.team.support_staff.all()
        team_list=list(map(lambda x:x.user,team))
        staff_list=list(map(lambda x:x.user,s_staff))
        lawyer_list=list(map(lambda x:x.user,lawyers))

        if lawyers:
            notify.send(request.user, recipient_list=lawyer_list, actor=request.user,
            verb='added a new process', nf_type='followed_by_one_user',object=process,target=process)
            for lawyer in lawyers:
                msg1 = "New Process {}".format(form.instance.process)
                msg2 = "Dear {}, please note that you have new process {} for your case ({})".format(
                    lawyer, form.instance.process, case)
                notify_staff(lawyer.user.id, msg1, msg2)

        if team:
            notify.send(request.user, recipient_list=team_list, actor=request.user,
                        verb='added a new process', nf_type='followed_by_one_user', object=process, target=process)
            for lawyer in team:

                msg1 = "New Process {}".format(form.instance.process)
                msg2 = "Dear {}, please note that you have new process {} for your case ({})".format(
                    lawyer, form.instance.process, case)
                notify_staff(lawyer.user.id, msg1, msg2)
        if s_staff:
            notify.send(request.user, recipient_list=staff_list, actor=request.user,
                        verb='added a new process', nf_type='followed_by_one_user', object=process, target=process)
            for staff in s_staff:
                for lawyer in s_staff:
                    msg1 = "New Process {}".format(form.instance.process)
                    msg2 = "Dear {}, please note that you have new process {} for your case ({})".format(
                        lawyer, form.instance.process, case)
                    notify_staff(lawyer.user.id, msg1, msg2)

        messages.success(request, 'Process has been added')
        return HttpResponseRedirect(reverse('cases:list_process'))
    else:
        messages.error(request, "Process could not be added")
        return HttpResponseRedirect(reverse('cases:list_process'))

    return render(request, "cases/case_detail.html", {'form': form})



























def generate_process(request, pk):
    case = get_object_or_404(Case, pk=pk)
    if request.method == "POST":
        # name1 = request.FILES['process_file']
        name1 = request.FILES['file']
        print("\n\n\n\n\n\n")
        print(name1)

    return HttpResponse("Ok")





































@login_required
def list_processes(request):
    staff=OtherStaff.objects.all()
    users=[]
    for i in staff:
        users.append(i.user)

    processes = Process.objects.all()
    return render(request, 'cases/processes/process_list.html', {'procs': processes,'form':ProcessForm2,'users':users})


######################################## BILLING ###########################################


@login_required
def bill_case(request,pk):
    case=get_object_or_404(Case,pk=pk)

    session_qs=CourtSession.objects.filter(case=case)
    session_intervals=list(map(lambda i: (i.end_time-i.start_time).total_seconds(),session_qs))



    billing_rate=200
    total_hours=sum(session_intervals)/3600

    bill=round((billing_rate*total_hours),2)

    context={
        'session_qs':session_qs,
        'session_intervals':session_intervals,
        'bill':bill,
        'case':case,
        'rate':billing_rate
    }

    return render(request,'cases/bill.html',context)



def generate_case_number(case_id,case_type):
    number=str(case_id).zfill(6)
    my_str=uuid.uuid4().hex[:3].upper()

    case_number="{}-{}-{}".format(case_type,my_str,number)

    return case_number

@login_required
def process_detail(request,pk):
    process=get_object_or_404(Process,pk=pk)
    # log_change(request.user.pk,process,'viewed a process')
    team=process.case.team
    lawyer_list = team.lawyer.all()
    staff_list = team.support_staff.all()
    user_list = []
    print("\n\n\n\n\n\n\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    for j in lawyer_list:
        user_list.append(j.user.id)
        print(j.user.id)

    for i in staff_list:
        user_list.append(j.user.id)
        print(i.user.id)


    for i in staff_list:
        user_list.append(j.user.id)
        print(i.user.id)

    print(request.user.id)
    print("\n\n\n\n\n\n\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")


    chinese_wall_users = []


    if process.case.chinese_wall == True:
        chinese_wall = ChineseWall.objects.get(mycase = process.case)
        chinese_wall_people = chinese_wall.chinese_lawyer.all()
        chinese_wall_people1 = chinese_wall.chineses_staff.all()

        for chinese_lawyer in chinese_wall_people:
            chinese_wall_users.append(chinese_lawyer.user)

        for chinese_lawyer in chinese_wall_people1:
            chinese_wall_users.append(chinese_lawyer.user)


    User = get_user_model()
    our_users = User.objects.all()
    all_users = []

    User = get_user_model()
    our_users = User.objects.all()
    all_users = []

    for i in our_users:
        all_users.append(i.id)
        # print(j.user.id)
    # if request.user.id in user_list:
    #     print("Yahhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")

    # print(user_list)
    # print(all_users)


    # print(user_list)
    # print(all_users)

    # for i in user_list:
    #     # all_users.remove(i)
    #     print(i)
    # print("\n\n\n\n\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    # print(all_users)




    # print(all_users)


    context={
        'process':process,
        'form':ProcessForm2(request.POST or None , request.FILES or None, instance=process),
        'users':user_list,
        'chinese_wall_users': chinese_wall_users,
        'wall':process.case.chinese_wall,


    }

    return render(request,'cases/processes/process_detail.html',context)




# @login_required
# def process_detail(request,pk):
#     process=get_object_or_404(Process,pk=pk)
#     log_change(request.user.pk,process,'viewed a process')

#     context={
#         'process':process,
#         'form':ProcessForm2(request.POST or None , request.FILES or None, instance=process)
#     }

#     return render(request,'cases/processes/process_detail.html',context)

@login_required
def update_process(request,pk):
    process=get_object_or_404(Process,pk=pk)
    case=process.case


    lawyers = case.lawyer.all()
    team = case.team.lawyer.all()
    s_staff = case.team.support_staff.all()

    if request.method=="POST":
        form=ProcessForm2(request.POST or None, request.FILES or None, instance=process)

        if form.is_valid():
            form.save()
            log_change(request.user.pk, process, 'updated a process')

            if lawyers:
                for lawyer in lawyers:
                    msg1 = "Process Update {}".format(form.instance.process)
                    msg2 = "Dear {}, please note that this process, {} , has been updated".format(
                        lawyer, form.instance.process)
                    notify_staff(lawyer.user.id, msg1, msg2)
            if team:
                for lawyer in team:
                    msg1 = "Process Update - {}".format(form.instance.process)
                    msg2 = "Dear {}, please note that this process, {} , has been updated".format(
                        lawyer, form.instance.process)
                    notify_staff(lawyer.user.id, msg1, msg2)
            if s_staff:
                for staff in s_staff:
                    for lawyer in s_staff:
                        msg1 = "Process Update - {}".format(form.instance.process)
                        msg2 = "Dear {}, please note that this process, {} , has been updated".format(
                            lawyer, form.instance.process)
                        notify_staff(lawyer.user.id, msg1, msg2)



            messages.success(request,"Process has been updated")
            return HttpResponseRedirect(reverse('cases:process_detail', args=[process.pk]))
        else:
            messages.error(request,form.errors)
            return HttpResponseRedirect(reverse('cases:process_detail', args=[process.pk]))

    else:
        form=ProcessForm2()
    return render(request,"cases/processes/process_detail.html",{'form':form,'process':process})




def delete_process(request,pk):
    process=get_object_or_404(Process,pk=pk)

    if process:
        log_deletion(request.user.pk, process, 'deleted a process')

        process.delete()

        messages.success(request,"Process has been deleted")
        return redirect('cases:list_process')
    else:
        messages.error(request,"Failed to delete process, this process doesnt exist")
        return HttpResponseRedirect(reverse('cases:process_detail', args[process.pk]))
    return render(request,"cases/processes/process_detail.html")



def add_to_archives(request):
    if request.method=="POST":
        form=CaseArchiveForm(request.POST or None )
        file_form=CaseFileForm(request.POST or None , request.FILES or None)
        files=request.FILES.getlist('file')
        if form.is_valid() and file_form.is_valid():
            case=form.instance.case
            case.archived=True
            case.save()
            arc=form.save()
            add_log(request.user.pk,arc,'archived a case')



            for f in files:
                unique_id = get_random_string(length=2)
                case_title = "{}".format(f.name.split(".")[0])
                new_files = CaseFile.objects.create(
                    case=case, title=case_title, file=f)

            messages.success(request,f"{case} has been added to archives")

            return redirect('cases:completed_list')
        else:
            messages.error(request,form.errors)
            messages.error(request,file_form.errors)
            return redirect('cases:completed_list')
    else:
        form=CaseArchiveForm()
        file_form=CaseFileForm()


    return redirect(request,'cases/completed.html',{'form':form,'file_form':file_form})

@login_required
def archive_detail(request,pk):
    arc=get_object_or_404(CaseArchive,pk=pk)
    files=CaseFile.objects.filter(case=arc.case)
    # log_change(request.user.pk,arc,'viewed an arhived case')
    archive_form=CaseArchiveForm(request.POST or None, instance=arc)
    context={
        'arc':arc,
        'form':archive_form,
        'upload_form':CaseFileForm(request.POST or None, request.FILES or None),
        'files':files
    }

    return render (request,'cases/archive_detail.html',context)


@login_required
def update_archive(request,pk):
    arch=get_object_or_404(CaseArchive,pk=pk)
    if request.method=="POST":
        form=ArchiveUpdateForm(request.POST or None, instance=arch)
        if form.is_valid():
            arc=form.save()
            log_change(request.user.pk, arc, 'updated an archive')

            messages.success(request,f'{arch.case} has been updated')
            return HttpResponseRedirect(reverse('cases:archive_detail', args=[arch.pk]))
        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect(reverse('cases:archive_detail', args=[arch.pk]))
    else:
        form=ArchiveUpdateForm()


    return redirect(request,'cases/archive_detail.html',{'form':form})

@login_required
def upload_archives(request, pk):
    arc = get_object_or_404(CaseArchive, pk=pk)
    case=arc.case

    if request.method == "POST":
        add_log(request.user.pk,arc,'uploaded files to archives')

        file_form = CaseFileForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('file')
        if file_form.is_valid():
            for f in files:
                unique_id = get_random_string(length=2)
                case_title = "{}".format(f.name.split(".")[0])
                new_files = CaseFile.objects.create(
                    case=case, title=case_title, file=f)
                print(f.name)
                print(new_files)

            messages.success(request, "Files have been added")
            return HttpResponseRedirect(reverse('cases:archive_detail', args=[arc.pk]))

        else:

            messages.error(
                request, "Failed to add Files, please check your form")
            return HttpResponseRedirect(reverse('cases:archive_detail', args=[arc.pk]))
    else:
        file_form = CaseFileForm()
        return render(request, "cases/archive_detail.html", {'file_form': file_form})


@login_required
def add_action_report(request,pk):
    case=get_object_or_404(Case,pk=pk)
    clients=case.client.all()

    if request.method=="POST":
        action_form=PostActionForm(request.POST or None)

        if action_form.is_valid():
            action_form.instance.case=case
            action=action_form.save()
            add_log(request.user.pk,action,'added a post action report')
            msg1=f"{action.title} ({case})"
            msg2=f"{action.bod} \nNext Business : {action.next_business} \nLead Professional:{case.lead_professional}"

            for client in clients:
                notify_staff(client.user.id, msg1, msg2)



            messages.success(request,"Action report has been sent")
            return HttpResponseRedirect(reverse('cases:case_detail',args=[case.pk]))
        else:
            messages.error(request,form.errors)
            return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))

    else:
        action_form=PostActionForm()

    return render(request,"cases/case_detail.html",{'action_form':action_form})

def list_action_reports(request,pk):
    case=get_object_or_404(Case,pk=pk)
    report_list=PostAction.objects.filter(case=case)

    context={
        'report_list':report_list,
        'form':PostActionForm(request.POST or None),
        'case':case,
    }


    return render(request,"cases/post_action.html",context)

@login_required
def post_action_detail(request,pk):
    action=get_object_or_404(PostAction,pk=pk)
    form=PostActionForm(request.POST or None, instance=action)
    # log_change(request.user.pk, action, 'viewed a post action report')

    context={
        'action':action,
        'form':form,
    }
    return render(request,"cases/action_detail.html",context)


@login_required
def update_action(request,pk):
    action=get_object_or_404(PostAction,pk=pk)
    case=action.case
    clients=case.client.all()
    if request.method=="POST":
        form = PostActionForm(request.POST or None, instance=action)
        if form.is_valid():
            form.save()
            log_change(request.user.pk,action,'updated a post action report')
            msg1 = f"{action.title} ({case})"
            msg2 = f"EDIT :  \n{action.bod} \nNext Business : {action.next_business} \nLead Professional:{case.lead_professional}"

            for client in clients:
                notify_staff(client.user.id, msg1, msg2)

            messages.success(request,'Post action report has been updated')
            return HttpResponseRedirect(reverse('cases:action_detail', args=[action.pk]))
        else:
            messages.error(request,form.errors)
            return HttpResponseRedirect(reverse('cases:action_detail', args=[action.pk]))
    else:
        form=PostActionForm()

    return render(request,'cases/action_detail.html',{'form':form})


@login_required
def delete_action(request,pk):
    action=get_object_or_404(PostAction,pk=pk)
    case=action.case

    if request.method=="POST":
        log_deletion(request.user.pk,action,'deleted a post action report')
        action.delete()
        messages.success(request, 'Post action report has been deleted')
        return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))

    else:
        messages.error(request, 'Ooops !! an error occured, please try again')
        return HttpResponseRedirect(reverse('cases:action_detail', args=[action.pk]))

    return render(request,'cases/action_detail.html')





####################representation################################
# TODO: case representation : insert,update,delete,list
@login_required
def add_rep(request):

    if request.method=="POST":
        form= RepresentationForm(request.POST or None)
        if form.is_valid():
            rep=form.save()
            user=request.user
            add_log(user.pk,rep,'added a post a new representaion')
            messages.success(request,"representaion has been added")
            return redirect('cases:rep_list')
        else:
            messages.error(request,form.errors)
            return redirect('cases:rep_list')
    else:
        form=RepresentationForm()
    return render(request,"cases/reps/rep_list.html",{'form':form})

@login_required
def rep_list(request):
    rep_list=Representative.objects.all().order_by('-pk')
    return render(request,"cases/reps/rep_list.html",{"rep_list":rep_list,'form':RepresentationForm()})

@login_required
def rep_detail(request,pk):
    rep=get_object_or_404(Representative,pk=pk)
    form=RepresentationForm(request.POST or None , instance=rep)
    # log_change(request.user.pk,rep,"viewed a representation")
    context={"rep":rep,"form":form,'case_list':Case.objects.filter(representative=rep)}
    return render(request,"cases/reps/rep_detail.html",context)

@login_required
def update_rep(request,pk):
    rep=get_object_or_404(Representative,pk=pk)
    if request.method=="POST":
        form=RepresentationForm(request.POST or None , instance=rep)
        if form.is_valid():
            repr=form.save()
            log_change(request.user.pk,repr,"updated a representation")
            messages.success(request,"representation has been updated")
            return HttpResponseRedirect(reverse('cases:rep_detail', args=[rep.pk]))
        else:
            messages.error(request,form.errors)
            return HttpResponseRedirect(reverse('cases:rep_detail', args=[rep.pk]))
    else:
        form=RepresentationForm(request.POST or None , instance=rep)
    return render(request,"cases/reps/rep_detail.html",{'form':form})

@login_required
def delete_rep(request,pk):
    rep=get_object_or_404(Representative,pk=pk)
    if rep:
        log_deletion(request.user.pk,rep,"deleted a representation")
        rep.delete()
        messages.success(request,"representation has been deleted")
        return redirect('cases:rep_list')
    else:
        messages.error(request,f"{rep} couldnt not be deleted because it doesnt exist")
        return HttpResponseRedirect(reverse('cases:rep_detail', args=[rep.pk]))
    return render(request,"cases/reps/rep_detail.html")



#################################### case history#################################################



@login_required
def case_history(request,pk):
    case=get_object_or_404(Case,pk=pk)
    case_logs=LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(case).pk,object_id=case.pk)


    return render(request,'firm/user_logs.html',{'logs':case_logs,'case':case})


# def request_from_archives(request,pk=pk):
#     arc=CaseArchive.objects.all(case=case)
#     staff=Otherstaff.objects.filter(role__id=3)






def request_file(request):
    if request.method=="POST":
        form=RequestForm(request.POST or None)
        if form.is_valid():

            form.instance.requested_by=request.user
            x=form.save()
            role=Role.objects.get(id=1)
            staff=OtherStaff.objects.filter(role=role)
            staff_list=list(map(lambda i:i.user,staff))
            if staff:
                for i in staff:


                    notify.send(request.user, recipient=i.user, actor=request.user,
                                verb='made a request for a case', nf_type='followed_by_one_user', object=x, target=x)
            add_log(request.user.pk,x,'made a request for a case')
            messages.success(request, "request has been made")
            return redirect('cases:case_list')
        else:
            messages.error(request, form.errors)
            return redirect('cases:case_list')
    else:
        form=RequestForm()
    return render(request,"cases/case_list_view.html")


def approve_request(request,pk):
    req=get_object_or_404(RequestArchive,pk=pk)

    if req:
        req.approved=True
        req.save()
        log_change(request.user.pk,req,"changed a request archive")
        messages.success(request,'approved')
        notify_user("Request Approved",f'Dear {req.requested_by}, your request has been approved', req.requested_by.pk)
        notify.send(request.user, recipient=req.requested_by, actor=request.user,
                            verb='approved your request', nf_type='followed_by_one_user', object=req, target=req)
        return redirect('cases:request_list')
    else:
        messages.error(request,'oops, an error occcured')
        return redirect('cases:request_list')

    return render(request,'cases/requests.html')


def request_list(request):
    rec_list=RequestArchive.objects.filter(approved=False).order_by('-pk')
    return render(request,'cases/request.html',{'rec_list':rec_list})

def make_request(request,pk):
    case=get_object_or_404(Case,pk=pk)
    client=case.client.all()[0]

    lop=RequestArchive.objects.create(case_title=case,case_number=case.case_number,suit_number=case.suit_number,client_name=client.user,requested_by=request.user)

    if lop:
        # add_log(request.user.pk,lop,"added a request archive")
        messages.success(request,'request has been sent')
        return redirect('cases:case_list')
    else:
        messages.error(request,'request could not be sent')
        return redirect('cases:case_list')
    return render(request,'case/case_list_view.html')


def all_files(request):
    files=CaseFile.objects.all()
    context={
        'case_files':files,
        }
    return render(request,'cases/all_files.html',context)




def start_timer(request):
    if request.method=="POST":
        user=request.user
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print(request.POST)


        case = request.POST['case_id']
        name_task = request.POST['name_task']
        purpose_of_task = request.POST['purpose']
        hour_payment = int(request.POST['hour'])
        minutes_payment = int(request.POST['minutes'])
        seconds_payment = int(request.POST['seconds_payment'])


        print(case)
        print(name_task)
        print(purpose_of_task)
        print(hour_payment)
        print(minutes_payment)
        print(seconds_payment)

        print(type(case))
        print(type(hour_payment))
        print(type(minutes_payment))
        print(type(seconds_payment))

        hour_pay = 0
        minutes_pay = 0
        seconds_pay = 0

        if request.user.groups.filter(name="Staff"):
            print(request.user.otherstaff.per_hour_charge)

            if int(hour_payment) == 0:
                hour_pay = 0
                print(hour_pay)
            else:
                hour_pay = hour_payment * request.user.otherstaff.per_hour_charge
                print(hour_pay)

            if int(minutes_payment) <= 0:
                minutes_pay = 0
                print(minutes_pay)
            else:
                minutes_pay = (minutes_payment / 60) * request.user.otherstaff.per_hour_charge
                print(minutes_pay)

            if int(seconds_payment) <= 0:
                seconds_pay = 0
                print(seconds_pay)
            elif int(seconds_payment) > 0:
                jkm = seconds_payment / 3600
                seconds_pay = jkm * request.user.otherstaff.per_hour_charge
                print(seconds_pay)



            total_payment = seconds_pay + minutes_pay + hour_pay

            case_id=get_object_or_404(Case,id=case)


            create_timer = Timer.objects.create(
                case = case_id,
                name_task = name_task,
                purpose_of_task = purpose_of_task,
                hour_time = hour_payment,
                minutes_time = minutes_payment,
                seconds_time = seconds_payment,
                total_charge_payment =  round(total_payment, 2),
                user = user,

            )

        elif request.user.groups.filter(name="Lawyer"):
            print(request.user.lawyer.per_hour_charge)

            if int(hour_payment) == 0:
                hour_pay = 0
                print(hour_pay)
            else:
                hour_pay = hour_payment * request.user.lawyer.per_hour_charge
                print(hour_pay)

            if int(minutes_payment) <= 0:
                minutes_pay = 0
                print(minutes_pay)
            else:
                minutes_pay = (minutes_payment / 60) * request.user.lawyer.per_hour_charge
                print(minutes_pay)

            if int(seconds_payment) <= 0:
                seconds_pay = 0
                print(seconds_pay)
            elif int(seconds_payment) > 0:
                jkm = seconds_payment / 3600
                seconds_pay = jkm * request.user.lawyer.per_hour_charge
                print(seconds_pay)



            total_payment = seconds_pay + minutes_pay + hour_pay

            case_id=get_object_or_404(Case,id=case)


            create_timer = Timer.objects.create(
                case = case_id,
                name_task = name_task,
                purpose_of_task = purpose_of_task,
                hour_time = hour_payment,
                minutes_time = minutes_payment,
                seconds_time = seconds_payment,
                total_charge_payment =  round(total_payment, 2),
                user = user,

            )
        else:
            messages.error(request,'Something went wrong')
            return redirect(request.META['HTTP_REFERER'])



        messages.success(request,'Your timer has been added successfully')
        return HttpResponseRedirect(reverse('cases:case_hours', args=[case_id.pk]))









def edit_start_timer(request):
    if request.method=="POST":
        user=request.user
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print(request.POST)


        timer = int(request.POST['timer_id'])
        name_task = request.POST['name_task']
        purpose_of_task = request.POST['purpose']
        hour_payment = int(request.POST['hour'])
        minutes_payment = int(request.POST['minutes'])
        seconds_payment = int(request.POST['seconds_payment'])

        timer_id_copy = Timer.objects.get(id = timer)
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

        print(name_task)
        print(purpose_of_task)
        print(hour_payment)
        print(minutes_payment)
        print(seconds_payment)

        print(type(timer))
        print(type(hour_payment))
        print(type(minutes_payment))
        print(type(seconds_payment))

        hour_pay = 0
        minutes_pay = 0
        seconds_pay = 0

        if request.user.groups.filter(name="Staff"):
            # print(timer_id_copy.user.otherstaff.per_hour_charge)

            if int(hour_payment) == 0:
                hour_pay = 0
                print(hour_pay)
            else:
                hour_pay = hour_payment * timer_id_copy.user.otherstaff.per_hour_charge
                print(hour_pay)

            if int(minutes_payment) <= 0:
                minutes_pay = 0
                print(minutes_pay)
            else:
                minutes_pay = (minutes_payment / 60) * timer_id_copy.user.otherstaff.per_hour_charge
                print(minutes_pay)

            if int(seconds_payment) <= 0:
                seconds_pay = 0
                print(seconds_pay)
            elif int(seconds_payment) > 0:
                jkm = seconds_payment / 3600
                seconds_pay = jkm * timer_id_copy.user.otherstaff.per_hour_charge
                print(seconds_pay)



            total_payment = seconds_pay + minutes_pay + hour_pay



            Timer.objects.filter(id = timer).update(
                name_task = name_task,
                purpose_of_task = purpose_of_task,
                hour_time = hour_payment,
                minutes_time = minutes_payment,
                seconds_time = seconds_payment,
                total_charge_payment =  round(total_payment, 2),

            )

        elif request.user.groups.filter(name="Lawyer"):
            print(timer_id_copy.user.lawyer.per_hour_charge)

            if int(hour_payment) == 0:
                hour_pay = 0
                print(hour_pay)
            else:
                hour_pay = hour_payment * timer_id_copy.user.lawyer.per_hour_charge
                print(hour_pay)

            if int(minutes_payment) <= 0:
                minutes_pay = 0
                print(minutes_pay)
            else:
                minutes_pay = (minutes_payment / 60) * timer_id_copy.user.lawyer.per_hour_charge
                print(minutes_pay)

            if int(seconds_payment) <= 0:
                seconds_pay = 0
                print(seconds_pay)
            elif int(seconds_payment) > 0:
                jkm = seconds_payment / 3600
                seconds_pay = jkm * timer_id_copy.user.lawyer.per_hour_charge
                print(seconds_pay)



            total_payment = seconds_pay + minutes_pay + hour_pay


            print("kldfasdjfhasldkjfhasjf")
            x = Timer.objects.filter(id = timer).first()
            log_change(request.user.pk,x,"edited a timer")
            Timer.objects.filter(id = timer).update(
                name_task = name_task,
                purpose_of_task = purpose_of_task,
                hour_time = hour_payment,
                minutes_time = minutes_payment,
                seconds_time = seconds_payment,
                total_charge_payment =  round(total_payment, 2),
            )
        else:
            messages.error(request,'Something went wrong')
            return redirect(request.META['HTTP_REFERER'])


        return redirect(request.META['HTTP_REFERER'])

def addpercharge(request):

    if request.method == 'POST':
        percharge = request.POST['percharge']

        jkm = request.user.groups.all()
        if request.user.groups.filter(name="Staff"):

            OtherStaff.objects.filter(id = request.user.otherstaff.id).update(
                per_hour_charge = percharge
            )
            messages.success(request,'Your update has been made')
            log_change(request.user.pk,jkm,"changed per unit charge")
        elif request.user.groups.filter(name="Lawyer"):
            Lawyer.objects.filter(id = request.user.lawyer.id).update(
                per_hour_charge = percharge
            )
            messages.success(request,'Your update has been made')
            log_change(request.user.pk,jkm,"changed per unit charge")
        else:
            messages.error(request,'There is a problem in updating your Information. Try going to profile to change it there')
            return redirect(request.META['HTTP_REFERER'])


        return redirect(request.META['HTTP_REFERER'])






@login_required
def case_hours(request,pk):
    case=get_object_or_404(Case,id=pk)
    print("\n\n\n\n\n\n\n\n\n\n\n\n")
    print(case)
    user=request.user
    try:
        timer=Timer.objects.filter(case=case)
        timer_sum=Timer.objects.filter(case=case).aggregate(Sum('hour_time'))
        timer_average=1
        qs1=Timer.objects.filter(user=user)
        qs2=Timer.objects.filter(case=case)
        session_case=qs2.intersection(qs1)[0]

        invoice_task_check = Invoice.objects.filter(case = case)
        task_list = [tasks for single_task_invoice in invoice_task_check for tasks in single_task_invoice.name_task.all()]
        timer=Timer.objects.filter(case=case)
        all_task = [tasks for tasks in timer.all()]
        for element in task_list:
            if element in all_task:
                all_task.remove(element)

        ts=1
        total_payment= round(Timer.objects.filter(case=case).aggregate(Sum('total_charge_payment'))['total_charge_payment__sum'],2)
        timer_sum= Timer.objects.filter(case=case).aggregate(Sum('hour_time'))['hour_time__sum']
        timer_min = Timer.objects.filter(case=case).aggregate(Sum('minutes_time'))['minutes_time__sum']
    except:

        timer=None
        session_case=None
        mt= Timer.objects.filter(case=case).aggregate(Sum('seconds_time'))['seconds_time__sum']
        total_payment=0
        timer_min = 0
        timer_sum = 0
        all_task = None




    context={
        'timer_list':all_task,
        'user_timer':session_case,
        'my_time':total_payment,
        'timer_sum': timer_sum,
        'timer_min':timer_min,
        'case':case,
        'all_tasks':timer,


    }
    return render(request,'cases/times.html',context)



@login_required
def add_expense(request):
    if request.method=='POST':
        form=ExpenseForm(request.POST or None)
        # name = request.POST.get('lead_professional')
        name = request.POST.get('case')
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        case_details = get_object_or_404(Case, pk=name)
        print(case_details.lead_professional)
        if form.is_valid():
            form.instance.user=request.user
            form.instance.categories= "Pending"
            x=form.save()



            # accounts=Group.objects.get(pk=4)
            # users=list(accounts.user_set.all())

            # notify.send(request.user, recipient_list=users, actor=request.user,
            #                 verb='Added a new expense', nf_type='followed_by_one_user', object=x, target=x)
            # add_log(request.user.pk,x,'add a new expense')

            # users=list(case_details.lead_professional.user)

            # notify.send(request.user, recipient_list=users, actor=request.user,
            #                 verb='Added a new expense', nf_type='followed_by_one_user', object=x, target=x)
            # add_log(request.user.pk,x,'add a new expense')
            # notify_staff(st.user.id, msg1, msg2)
            add_log(request.user.pk,x,"added an expense")
            notify.send(case_details.lead_professional.user, recipient=case_details.lead_professional.user, actor=request.user,
                        verb='added an expense for approval on', nf_type='followed_by_one_user', object=x, target=x)

            messages.success(request,'Expense has been added')
            return redirect('cases:expenses')
        else:
            messages.error(request,form.errors)
            return redirect('cases:expenses')
    else:
        form=ExpenseForm()

    return render(request,'cases/expenses.html',{'form':form})


def resend_expense(request, pk):
    x = Expense.objects.filter(id = pk).update(
            categories = "Pending"
        )


    log_change(request.user.pk,x,"changed an expense")
    expenses = get_object_or_404(Expense, id=pk)

    notify.send(expenses.case.lead_professional.user, recipient=expenses.case.lead_professional.user, actor=expenses.user,
                        verb='resends expense for approval', nf_type='followed_by_one_user', object=expenses, target=expenses)

    messages.success(request,'Expense has been Approved')

    return redirect(request.META['HTTP_REFERER'])


def accept_expense(request, pk):
    x = Expense.objects.filter(id = pk).update(
            categories = "Approved"
        )


    log_change(request.user.pk,x,"changed an expense")

    expenses = get_object_or_404(Expense, id=pk)

    notify.send(expenses.user, recipient=expenses.user, actor=expenses.case.lead_professional.user,
                        verb='approved your expense', nf_type='followed_by_one_user', object=expenses, target=expenses)

    messages.success(request,'Expense has been Approved')

    return redirect(request.META['HTTP_REFERER'])


def decline_expense(request, pk):
    x = Expense.objects.filter(id = pk).update(
            categories = "Denied"
        )

    log_change(request.user.pk,x,"changed an expense")

    expenses = get_object_or_404(Expense, id=pk)

    notify.send(expenses.user, recipient=expenses.user, actor=expenses.case.lead_professional.user,
                        verb='declined your expense ', nf_type='followed_by_one_user', object=expenses, target=expenses)

    messages.error(request,'Expense has been Declined')

    return redirect(request.META['HTTP_REFERER'])



class ExpenseListView(LoginRequiredMixin,ListView):
    model = Expense
    template_name = "cases/expenses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expense_list']=Expense.objects.filter(user=self.request.user)
        context['form']=ExpenseForm(self.request.POST or None)
        try:
            if self.request.user.groups.filter(name = 'Lawyer').exists():

                lawyer=get_lawyer(self.request.user)
                lead_cases=lawyer.lead_professional.all()
                team_qs=lawyer.team_lawyers.all()[0]
                case_qs=Case.objects.filter(team=team_qs)
                lawyer_cases=lawyer.case_lawyers.all()
                context['case_list']=lead_cases.union(lawyer_cases,case_qs)
            elif self.request.user.groups.filter(name="Staff").exists():
                staff=get_staff(self.request.user)
                team_qs=staff.team_staff.all()[0]
                case_qs=Case.objects.filter(added_by=self.request.user)
                team_cases=Case.objects.filter(team=team_qs)
                qs=case_qs.union(team_cases)
                context['case_list']=qs
                print(qs)
            else:
                context['case_list']=None


        except:
            pass
        return context










class PendingExpenseListView(LoginRequiredMixin,ListView):
    model = Expense
    template_name = "cases/pending_expenses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expense_list']=Expense.objects.filter(categories = "Pending", case__lead_professional = self.request.user.lawyer)
        context['form']=ExpenseForm(self.request.POST or None)

        return context
























class ExpenseDetailView(DetailView):
    model = Expense
    template_name = "cases/expense_detail.html"

    def get_queryset(self):
        expense = super().get_queryset()

        return expense

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form']=ExpenseForm(self.request.POST or None, instance=self.object)
        case_id=self.object.case.id
        case=get_object_or_404(Case,pk=case_id)
        context['case_expense_list']=Expense.objects.filter(case=case)
        ts=Expense.objects.filter(case=case).aggregate(Sum('amount'))
        context['total_expense']=ts['amount__sum']

        return context



def update_expense(request,pk):
    expense=get_object_or_404(Expense,pk=pk)
    if request.method=="POST":
        form=ExpenseForm(request.POST or None, instance=expense)
        if form.is_valid():
            x = form.save()

            log_change(request.user.pk,x,"changed an expense")
            messages.success(request,"Expense has been updated")
            return HttpResponseRedirect(reverse('cases:expense_detail', args=[expense.pk]))
        else:
            messages.error(request,form.errors)
            return HttpResponseRedirect(reverse('cases:expense_detail', args=[expense.pk]))
    else:
        form=ExpenseForm(request.POST or None, instance=expense)
    return render(request,'cases/expense_detail.html',{'form':form})


def delete_expense(request,pk):
    expense=get_object_or_404(Expense,pk=pk)
    if expense:
        log_deletion(request.user.pk,expense,"deleted an expense")
        expense.delete()
        messages.success(request,'expense has been deleted')
        return redirect('cases:expenses')
    else:
        return HttpResponseRedirect(reverse('cases:expense_detail' ,args[expense.pk]))
    return render(request,'cases/expense_detail.html')


class RenumerationList(LoginRequiredMixin,ListView):
    model =Renumeration
    context_object_name = 'Renumseration'
    template_name='acc_dash/requests.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['renumeration_list']=Renumeration.objects.filter(approved=False)
        context['renumeration_approved']=Renumeration.objects.filter(approved=True)

        return context


def get_lawyer(user):
    qs = Lawyer.objects.get(user=user)
    if qs:
        return qs
    else:
        return None



@login_required
def approve_renumeration(request,pk):
    object=get_object_or_404(Renumeration,pk=pk)
    if object.approved==False:
        object.approved=True
        object.save()
        notify.send(request.user, recipient=object.lead.user, actor=request.user,
                            verb='approved your request', nf_type='followed_by_one_user', object=object, target=object)


        # Send mail: 13.04.2021
        to_email=object.lead.user.email
        from_email="minkahpremoandco@gmail.com"
        subject="Renumeration Request Approval"
        body=f"Dear {object.lead}, your renumeration request has been approved. You will be notified when all necessary paperwork is completed. \n{request.user} \nAccounts Office"


        send_mail(
            subject,
            body,
            from_email,
            [to_email, 'daniel@integrisgh.com'], # The addresses you want the email sent to
            fail_silently=False
        )

        # END
        log_change(request.user.pk,object,"changed a renumeration")
        messages.success(request,'Request has been approved')
        return redirect('cases:renumerations')
    else:
        object.approved=False
        object.save()
        log_change(request.user.pk,object,"changed a renumeration")
        messages.error(request,'Approval has been rescinded')
        return redirect('cases:renumerations')

    return render(request,'acc_dash/requests.html')

@login_required
def request_renumeration(request,pk):
    case=get_object_or_404(Case,pk=pk)

    try:
        lead=get_lawyer(request.user)
        object=Renumeration.objects.create(case=case,lead=lead)



        accounts=Group.objects.get(pk=4)
        users=list(accounts.user_set.all())
        to_email=object.lead.user.email
        r_list=list(map(lambda i:i.email,users))
        from_email="minkahpremoandco@gmail.com"
        subject="Renumeration Request"
        body=f"{object.lead} has made a renumeration request, please provide feedback as soon as possible. \n"
        send_mail(subject,
                  body,from_email,
                  [to_email, r_list],
                  fail_silently=False
                  )
        notify.send(request.user, recipient_list=users, actor=request.user,
                            verb='made a renumeration request', nf_type='followed_by_one_user', object=object, target=object)

        
        add_log(request.user.pk,object,"added a Renumeration")
        messages.success(request,'renumeration request has been sent')
        return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))

    except Exception as e:
        messages.error(request,e)
        return HttpResponseRedirect(reverse('cases:case_detail', args=[case.pk]))

    return render(request,'cases/case_detail.html')


@login_required
def request_client_payment(request,pk):
    case=get_object_or_404(Case,pk=pk)
    clientqs=case.client.all()

    try:
        lawyer=get_lawyer(request.user)
        payment=PaymentEnquiry.objects.create(case=case,lead=lawyer)
        map(lambda i:print(i),clientqs)
        payment.client.add(*clientqs)
        payment.save()


        accounts=Group.objects.get(pk=4)
        users=list(accounts.user_set.all())
        r_list=list(map(lambda i:i.email,users))
        from_email="minkahpremoandco@gmail.com"
        subject="Client Payment Information Request"
        body=f"{payment.lead} has made a renumeration request, please provide feedback as soon as possible. \n"
        send_mail(subject,body,from_email,r_list,fail_silently=False)
        notify.send(request.user, recipient_list=users, actor=request.user,
                            verb='Asked for a client payement update', nf_type='followed_by_one_user', object=payment, target=payment)
        add_log(request.user.pk,payment,'requested for client payment update')



        messages.success(request,'request has been made')
        return HttpResponseRedirect(reverse('cases:case_detail',args=[case.pk]))
    except Exception as e:
        # messages.error(request,"Requ")
        print(e)
        return HttpResponseRedirect(reverse('cases:case_detail',args=[case.pk]))

    return render(request,'cases/case_detail.html')


@login_required
def update_client_payment(request,pk):
    payment=get_object_or_404(PaymentEnquiry,pk=pk)
    case=payment.case

    if request.method=="POST":
        form=PaymentEnquiryForm(request.POST or None , instance=payment)
        if form.is_valid():
            status=form.instance.status
            payment.approved=True
            payment.updated_by=request.user
            payment.status=status
            payment.save()
            log_change(request.user.pk,payment,"changed a payment enquiry")
            messages.success(request,'Update has been made')
            return HttpResponseRedirect(reverse('cases:update_payment_info', args=[payment.pk]))

            notify.send(request.user, recipient=payment.lead.user, actor=request.user,
                            verb='Sent client Payment information', nf_type='followed_by_one_user', object=payment, target=payment)
            log_change(request.user.pk,payment,'updated payment request')
            from_email="minkahpremoandco@gmail.com"
            subject="Client Payment Update"
            body=f"Dear {payment.lead},\n Your request has been processed. Client has made {payment.status}.\n{request.user} \nAccounts Office"
            send_mail(subject,body,from_email,r_list,fail_silently=False)

        else:
            messages.error(request,form.errors)
            return HttpResponseRedirect(reverse('cases:update_payment_info', args=[payment.pk]))
    else:
        form=PaymentEnquiryForm(request.POST or None , instance=payment)

    return render(request,'acc_dash/client_payment_detail.html',{'form':form,'payment':payment})


@login_required
def client_payment_list(request):
    request_list=PaymentEnquiry.objects.filter(approved=False)
    payments=PaymentEnquiry.objects.filter(approved=True)
    context={'payments':payments,'request_list':request_list}

    return render(request,'acc_dash/client_payment_list.html',context)


@login_required
def client_payment_detail(request,pk):
    payment=get_object_or_404(PaymentEnquiry,pk=pk)

    context={'payment':payment,'form':PaymentEnquiryForm(request.POST or None , instance=payment)}
    log_change(request.user.pk,payment,'view a new payment request')

    return render(request,'acc_dash/client_payment_detail.html',context)







@login_required
def generate_invoice_total(request,pk):
    case=get_object_or_404(Case,id=pk)

    if Invoice.objects.filter(case = case):
        invoice_task_check = Invoice.objects.filter(case = case)

        invoice_expense_check = Invoice.objects.filter(case = case)

        task_list = [tasks for single_task_invoice in invoice_task_check for tasks in single_task_invoice.name_task.all()]
        expense_list = [expenses for single_expense_invoice in invoice_expense_check for expenses in single_expense_invoice.expenses.all()]

        timer=Timer.objects.filter(case=case)
        all_tasks = [tasks for tasks in timer.all()]
        for element in task_list:
            if element in all_tasks:
                all_tasks.remove(element)


        if not all_tasks:
            total_payment = 0
        else:
            total_payment = 0

            for i in all_tasks:
                amount = i.total_charge_payment
                total_payment += amount





        expense = Expense.objects.filter(
            Q(categories='Exists') | Q(categories ='Approved'),case = case)
        all_expense = [expense for expense in expense.all()]
        for element in expense_list:
            if element in all_expense:
                all_expense.remove(element)


        if not all_expense:
            total_expense = 0
        else:
            total_expense = 0

            for i in all_expense:
                amount = i.amount
                total_expense += amount



        total_pay = round((total_payment +total_expense),2)



    else:
        all_tasks=Timer.objects.filter(case=case)
        total_payment= round(Timer.objects.filter(case=case).aggregate(Sum('total_charge_payment'))['total_charge_payment__sum'],2)


        if Expense.objects.filter(Q(categories='Exists') | Q(categories ='Approved'), case = case):
            all_expense = Expense.objects.filter(
                Q(categories='Exists') | Q(categories ='Approved'), case = case)
            total_expense= round(Expense.objects.filter(
                Q(categories='Exists') | Q(categories ='Approved'), case = case).aggregate(Sum('amount'))['amount__sum'],2)
        else:
            all_expense = Expense.objects.filter(
                Q(categories='Exists') | Q(categories ='Approved'), case = case)
            total_expense = 0

        total_pay = round((total_payment +total_expense),2)

    context = {
        'create_invoice' : all_tasks,
        'case':case,
        'total_payment':total_payment,
        'expense': all_expense,
        'total_expense' : total_expense,
        'total_pay': total_pay
    }
    return render(request,'invoice/generate_invoice_total.html',context)


@login_required
def generate_invoice_total_save(request,pk):
    case=get_object_or_404(Case,id=pk)

    if Invoice.objects.filter(case = case):
        invoice_task_check = Invoice.objects.filter(case = case)

        invoice_expense_check = Invoice.objects.filter(case = case)

        task_list = [tasks for single_task_invoice in invoice_task_check for tasks in single_task_invoice.name_task.all()]
        expense_list = [expenses for single_expense_invoice in invoice_expense_check for expenses in single_expense_invoice.expenses.all()]

        timer=Timer.objects.filter(case=case)
        all_tasks = [tasks for tasks in timer.all()]
        for element in task_list:
            if element in all_tasks:
                all_tasks.remove(element)


        if not all_tasks:
            total_payment = 0
        else:
            total_payment = 0

            for i in all_tasks:
                amount = i.total_charge_payment
                total_payment += amount





        expense = Expense.objects.filter(
            Q(categories='Exists') | Q(categories ='Approved'),case = case)
        all_expense = [expense for expense in expense.all()]

        for element in expense_list:
            if element in all_expense:
                all_expense.remove(element)

        if not all_expense:
            total_expense = 0
        else:
            total_expense = 0

            for i in all_expense:
                amount = i.amount
                total_expense += amount



        total_pay = round((total_payment +total_expense),2)



    else:
        all_tasks=Timer.objects.filter(case=case)
        total_payment= round(Timer.objects.filter(case=case).aggregate(Sum('total_charge_payment'))['total_charge_payment__sum'],2)


        if Expense.objects.filter(Q(categories='Exists') | Q(categories ='Approved'), case = case):
            all_expense = Expense.objects.filter(
                Q(categories='Exists') | Q(categories ='Approved'), case = case)
            total_expense= round(Expense.objects.filter(
                Q(categories='Exists') | Q(categories ='Approved'), case = case).aggregate(Sum('amount'))['amount__sum'],2)
        else:
            all_expense = Expense.objects.filter(
                Q(categories='Exists') | Q(categories ='Approved'), case = case)
            total_expense = 0

        total_pay = round((total_payment +total_expense),2)




    create_invoice = Invoice.objects.create(
        case = case,
        total_charge_payment = total_payment,
        Total_amount =total_payment,
        total_expense = total_expense
    )
    for x in all_tasks:
        create_invoice.name_task.add(x)

    for e in all_expense:
        create_invoice.expenses.add(e)

    add_log(request.user.pk,create_invoice,"added an invoice")
    messages.success(request, 'Total Invoice has been saved')
    return HttpResponseRedirect(reverse('cases:case_hours', args=[case.id]))





@login_required
def calendar(request):
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

    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    # print("@@@@@@@@Final oooooooooooo@@@@@@@@@@@@@@")
    # print(users)
    
    # print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    # print(users)

    # forms = self.form_class()
    
    # start: '2020-09-16T16:00:00'
    # for event in events:
    #     if request.user in users: 
    #         print("\n\n\n\n\n\n\n\n\n\n")
    #         print("Yes")
    #         event_list.append(
    #             {
    #                 "title": event.task,
    #                 "start": event.date_modefied.date().strftime("%Y-%m-%dT%H:%M:%S"),
    #                 "end": event.deadline.date().strftime("%Y-%m-%dT%H:%M:%S"),
    #             }
    #         )
    context = { "events": event_list, "events_month": events_month}

    return render(request, 'cases/calendar.html', context)








def all_user_logs(request):
    all_user_logs_per_user = LogEntry.objects.filter(user_id = request.user.id)
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    
    for i in all_user_logs_per_user:
        print(i.__dict__)
    print("#########")

    context = {
        'all_user_logs':all_user_logs_per_user,
    }
    return render(request, 'cases/user_logs.html', context)




def all_user_logs_per_case(request, pk):
    case = get_object_or_404(Case, pk=pk)
    all_user_logs = LogEntry.objects.filter(object_repr = case)
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    
    # for i in all_user_logs:
    #     print(i.__dict__)
        # print(i.action_flag.__dict__)
    print("#########")

    context = {
        'all_user_logs':all_user_logs,
    }
    return render(request, 'cases/user_logs.html', context)




