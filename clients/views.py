from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

# from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse
from .forms import (
    ClientForm,
    ClientCategoryForm,
    ClientCaseForm,
    ClientWillForm,
    UpdateUserForm,
    EngagementForm,
    PaymentForm,
    ClientTypeForm,
)

# Create your views here.
from .models import Client, ClientCategory, Payment, ClientType
from django.contrib import messages
from cases.models import Case, EngagementTerm
from django.contrib.auth.decorators import login_required
from lawyers.models import Lawyer, User
from accounts.forms import UserForm
from django.contrib.auth.models import Group
from cases.user_actions import add_log, log_change, log_deletion
from django.core.mail import send_mail
from random_username.generate import generate_username


@login_required
def client_create_view(request):
    if request.method == "POST":
        form = ClientForm(request.POST or None)

        if form.is_valid():
            print("##########################")
            print(generate_username())
            user_name = generate_username()[0]
            obj = User.objects.filter(username=user_name)
            while obj.exists():
                obj = User.objects.filter(username=user_name)
                user_name = generate_username()[0]

            create_user = User.objects.create(
                username=user_name, phone=form.instance.phone
            )

            create_user.set_password("password")
            create_user.save()

            client = Client.objects.create(
                user=create_user,
                name=form.instance.name,
                client_email=form.instance.client_email,
                phone=form.instance.phone,
                added_by=request.user,
                category=form.instance.category,
                address=form.instance.address,
                lead_professional=form.instance.lead_professional,
                client_type=form.instance.client_type,
            )
            client.save()

            my_group = Group.objects.filter(name="Client").first()
            my_group.user_set.add(create_user)

            add_log(request.user.pk, client, "added a new client")

            messages.success(
                request, "{} has been added to your client list".format(client)
            )
            return HttpResponseRedirect(
                reverse("clients:client_detail", args=[client.pk])
            )

        else:
            messages.error(request, form.errors)
            return redirect("clients:client_list")

    else:
        form = ClientForm()

    return render(request, "clients/client_list.html", {"form": form})


@login_required
def client_list(request):
    client_list = Client.objects.all()
    form = ClientForm(request.POST or None)

    context = {"client_list": client_list, "user_form": UserForm(), "form": form}

    return render(request, "clients/client_list.html", context)


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST or None, instance=client)
    client_cases = Case.objects.filter(client=client)
    # log_change(request.user.pk,client,"viewed a client")
    print(client_cases)

    context = {
        "client": client,
        "form": form,
        "user_form": UpdateUserForm(instance=client.user),
        "client_cases": client_cases,
        "case_form": ClientCaseForm(request.POST or None),
        "will_form": ClientWillForm(request.POST or None),
        "terms": EngagementTerm.objects.filter(client=client),
        "term_form": EngagementForm(request.POST or None, request.FILES or None),
    }

    return render(request, "clients/client_detail.html", context)


@login_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        form = ClientForm(request.POST or None, instance=client)

        if form.is_valid():
            form.instance.added_by = request.user
            form.save()

            log_change(request.user.pk, client, "updated a client")

            messages.success(request, "client has been updated")

            return HttpResponseRedirect(
                reverse("clients:client_detail", args=[client.pk])
            )

    else:
        form = ClientForm()

    return render(request, "clients/client_detail.html", {"form": form})


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        client.delete()
        messages.success(request, "Client has been deleted")

        return redirect("clients:client_list")

    return render(request, "clients/clients_detail.html")


@login_required
def category_list(request):
    cats = ClientCategory.objects.all()
    form = ClientCategoryForm

    context = {"cats": cats, "form": form}
    return render(request, "clients/cat_list.html", context)


@login_required
def cat_detail(request, pk):
    cat = get_object_or_404(ClientCategory, pk=pk)

    # log_change(request.user.pk,cat,'viewed a client category')

    context = {
        "cat": cat,
        "form": ClientCategoryForm(request.POST or None, instance=cat),
    }

    return render(request, "clients/cat_detail.html", context)


@login_required
def add_cat(request):
    if request.method == "POST":
        form = ClientCategoryForm(request.POST or None)

        if form.is_valid():
            cat = form.save()
            add_log(request.user.pk, cat, "added a new client category")
            messages.success(request, "Category has been added")
            return redirect("clients:cat_list")
    else:
        form = ClientCategoryForm()

    return render(request, "clients/cat_list.html", {"form": form})


@login_required
def update_cat(request, pk):
    cat = get_object_or_404(ClientCategory, pk=pk)

    if request.method == "POST":
        form = ClientCategoryForm(request.POST or None, instance=cat)
        if form.is_valid():
            form.save()
            log_change(request.user.pk, cat, "updated a client category")

            messages.success(request, "Category has been updated")
            return HttpResponseRedirect(reverse("clients:cat_detail", args=[cat.pk]))
        else:
            messages.error(request, "Category could not updated")
            return HttpResponseRedirect(reverse("clients:cat_detail", args=[cat.pk]))
    else:
        form = ClientCategoryForm()

    return render(request, "clients/cat_detail.html", {"form": form})


@login_required
def cat_delete(request, pk):
    cat = get_object_or_404(ClientCategory, pk=pk)
    if request.method == "POST":
        log_deletion(request.user.pk, cat, "deleted a client category")
        cat.delete()
        messages.success(request, "Category has been deleted")
        return redirect("clients:cat_list")
    else:
        messages.error(request, "Category could not deleted")
        return HttpResponseRedirect(reverse("clients:cat_detail", args=[cat.pk]))

    return render(request, "clients/cat_detail.html")


@login_required
def client_cat(request, pk):
    cat = get_object_or_404(ClientCategory, pk=pk)
    client = Client.objects.filter(category=cat)

    context = {"client_list": client}

    return render(request, "clients/client_list.html", context)


@login_required
def add_case(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        form = ClientCaseForm(request.POST or None)
        if form.is_valid():
            form.instance.client = client
            form.instance.added_by = request.user
            x = form.save()

            add_log(request.user.pk, x, "added a case")
            messages.success(
                request, "a new case hase been added for {}".format(client.name)
            )
            return HttpResponseRedirect(
                reverse("clients:client_detail", args=[client.pk])
            )

        else:
            messages.error(
                request,
                "Failed To Add A New Case For  {},Please Check Your Form".format(
                    client.name
                ),
            )
            return HttpResponseRedirect(
                reverse("clients:client_detail", args=[client.pk])
            )
    else:
        form = ClientCaseForm()

    return render(request, "clients/client_detail", {"case_form": form})


def get_lawyer(user):
    qs = Lawyer.objects.get(user=user)

    return qs


@login_required
def add_will(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        form = ClientWillForm(request.POST or None)
        if form.is_valid():
            form.instance.client = client
            x = form.save()

            add_log(request.user.pk, x, "added a new will")

            messages.success(
                request, "New will has been added for {}".format(client.name)
            )
            return redirect("wills:will_list")

        else:
            messages.error(request, "failed to add new will for {}".format(client.name))
            return HttpResponseRedirect(
                reverse("clients:client_detail", args=[client.pk])
            )

    else:
        form = ClientWillForm()

    return render(request, "clients/client_detail.html", {"will_form": form})


@login_required
def add_engagement(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        form = EngagementForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.instance.client = client
            form.instance.added_by = request.user
            case_id = int(request.POST.get("case"))
            case = get_object_or_404(Case, pk=case_id)

            form.instance.case = case

            x = form.save()
            add_log(request.user.pk, x, "added an engagement terms")

            messages.success(request, "Engagement Terms have been added")
            return HttpResponseRedirect(
                reverse("clients:client_detail", args=[client.pk])
            )
        else:
            messages.error(request, "Engagement Terms could not be added added")
            return HttpResponseRedirect(
                reverse("clients:client_detail", args=[client.pk])
            )
    else:
        form = EngagementForm()

    return render(request, "clients/client_detail.html", {"terms_form": form})


@login_required
def update_terms(request, pk):
    terms = get_object_or_404(EngagementTerm, pk=pk)
    client = terms.client
    client_cases = Case.objects.filter(client=client)

    if request.method == "POST":
        files = request.FILES.get("upload_file")
        the_case = request.POST["case"]
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        if files:
            case = Case.objects.get(id=the_case)
            print(case)
            print(case.pk)
            print(case.id)
            print(terms.id)
            x = EngagementTerm.objects.filter(id=terms.id).update(case=case.id)
            x.file = files
            x.save()
            print("files involved")
        else:
            case = Case.objects.get(id=the_case)
            print(case)
            print(case.pk)
            print(case.id)

            EngagementTerm.objects.filter(id=terms.id).update(case=case.id)
            print("files not involved")

        # log_change(request.user.pk,x,"changed an engagement terms")

        messages.success(request, "Engagement Terms have been updated")
        return redirect(request.META["HTTP_REFERER"])

    #     form=EngagementForm(request.POST or None, request.FILES or None , instance=terms)
    #     if form.is_valid():
    #         case_id=int(request.POST.get("case"))
    #         case=get_object_or_404(Case,pk=case_id)

    #         form.instance.case=case
    #         x = form.save()

    #         log_change(request.user.pk,x,"changed an engagement terms")

    #         messages.success(request,'Engagement Terms have been updated')
    #         return HttpResponseRedirect(reverse('clients:terms_detail', args=[terms.pk]))
    #     else:
    #         messages.error(request,'Engagement Terms could not be updated')
    #         return HttpResponseRedirect(reverse('clients:terms_detail', args=[terms.pk]))
    # else:
    #     form=EngagementForm()

    return render(
        request,
        "clients/client_detail.html",
        {"terms_form": form, "client_cases": client_cases},
    )


@login_required
def delete_terms(request, pk):
    terms = get_object_or_404(EngagementTerm, pk=pk)
    if terms:
        log_deletion(request.user.pk, terms, "deleted an engagement terms")
        terms.delete()
        messages.success(request, "Engagement Terms have been added")
        return HttpResponseRedirect(
            reverse("clients:client_detail", args=[terms.client.pk])
        )
    else:
        messages.error(request, "Engagement Terms could not be updated")
        return HttpResponseRedirect(
            reverse("clients:client_detail", args=[terms.client.pk])
        )

    return render(request, "clients/client_detail.html")


# ----------------------------- Client types ----------------------


@login_required
def type_list(request):
    client_types = ClientType.objects.all()
    form = ClientTypeForm

    context = {"client_types": client_types, "form": form}
    return render(request, "clients/type_list.html", context)


@login_required
def type_detail(request, pk):
    client_types = get_object_or_404(ClientType, pk=pk)

    # log_change(request.user.pk,client_types,'viewed a client types')

    context = {
        "client_types": client_types,
        "form": ClientTypeForm(request.POST or None, instance=client_types),
    }

    return render(request, "clients/type_details.html", context)


@login_required
def add_types(request):
    if request.method == "POST":
        form = ClientTypeForm(request.POST or None)

        if form.is_valid():
            cat = form.save()
            add_log(request.user.pk, cat, "added a new client type")
            messages.success(request, "Type has been added")
            return redirect("clients:type_list")
    else:
        form = ClientTypeForm()

    return render(request, "clients/type_list.html", {"form": form})


@login_required
def update_type(request, pk):
    client_type = get_object_or_404(ClientType, pk=pk)

    if request.method == "POST":
        form = ClientTypeForm(request.POST or None, instance=client_type)
        if form.is_valid():
            form.save()
            log_change(request.user.pk, client_type, "updated a client type")

            messages.success(request, "Type has been updated")
            return HttpResponseRedirect(
                reverse("clients:type_detail", args=[client_type.pk])
            )
        else:
            messages.error(request, "Type could not updated")
            return HttpResponseRedirect(
                reverse("clients:type_detail", args=[client_type.pk])
            )
    else:
        form = ClientTypeForm()

    return render(request, "clients/type_detail.html", {"form": form})


@login_required
def type_delete(request, pk):
    client_type = get_object_or_404(ClientType, pk=pk)
    if request.method == "POST":
        log_deletion(request.user.pk, client_type, "deleted a client type")
        client_type.delete()
        messages.success(request, "Type has been deleted")
        return redirect("clients:type_list")
    else:
        messages.error(request, "Type could not deleted")
        return HttpResponseRedirect(
            reverse("clients:type_detail", args=[client_type.pk])
        )

    return render(request, "clients/type_details.html")


def client_type(request, pk):
    client_types = get_object_or_404(ClientType, pk=pk)
    client = ClientType.objects.filter(category=client_types)

    context = {"client_list": client}

    return render(request, "clients/type_list.html", context)


# ------------------------------ end of client types---------------------------


# @group_required(('Lawyer','Staff'))
@login_required
def term_detail(request, pk):
    term = get_object_or_404(EngagementTerm, pk=pk)
    client = term.client
    client_cases = Case.objects.filter(client=client)
    context = {
        "term": term,
        "form": EngagementForm(
            request.POST or None, request.FILES or None, instance=term
        ),
        "client_cases": client_cases,
    }
    return render(request, "clients/term_detail.html", context)


# @group_required('staff')
@login_required
def add_payment(request):
    if request.method == "POST":
        form = PaymentForm(request.POST or None)
        if form.is_valid():
            form.instance.added_by = request.user
            payment = form.save()

            log_log(request.user.pk, payment, "added a payment")
            subject = f"Client Payment Update"
            body = f"Dear {payment.client.lead_professional} , this email is to inform you that your client ,{payment.client}, has made payment"
            f_email = request.user.email
            t_email = payment.client.lead_professional.user.email
            send_mail(
                subject,
                body,
                f_email,
                [t_email],
                fail_silently=True,
            )
            messages.success(request, "Payment of has been added")
            return redirect("clients:add_payment")
        else:
            messages.error(request, "Payment couln't be added")
            return redirect("clients:add_payment")
    else:
        form = PaymentForm
    return render(request, "acc_dash/payments.html", {"form": form})


# @group_required('staff')
@login_required
def payment_detail(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    client = payment.client
    context = {
        "pay": payment,
        "form": PaymentForm(request.POST or None, instance=payment),
    }
    return render(request, "acc_dash/payment_detail.html", context)


# @group_required('Staff')
@login_required
def update_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)

    if request.method == "POST":
        form = PaymentForm(request.POST or None, instance=payment)
        if form.is_valid():
            x = form.save()
            log_change(request.user.pk, x, "changed a payment")
            messages.success(request, "payment has been updated")
            return HttpResponseRedirect(
                reverse("clients:payment_detail", args=[payment.pk])
            )
        else:
            messages.error(request, "payment couldnt be updated updated")
            return HttpResponseRedirect(
                reverse("clients:payment_detail", args=[payment.pk])
            )
    else:
        form = PaymentForm()
    return render(request, "acc_dash/payment_detail.html", {"form": form})


# @group_required('Staff')
@login_required
def delete_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)

    if payment:
        log_deletion(request.user.pk, payment, "deleted payment")
        payment.delete()
        messages.success(request, "payment has been deleted")
        return redirect("clients:payment_list")
    else:
        messages.error(request, "payment could not be deleted")
        return HttpResponseRedirect(
            reverse("clients:payment_detail", args=[payment.pk])
        )

    return render(request, "account_dash/payment_detail.html")


# @group_required('Staff')
@login_required
def payment_list(request):
    payment_list = Payment.objects.all()
    form = PaymentForm(request.POST or None)
    print(Payment.objects.all())

    return render(
        request,
        "acc_dash/payments.html",
        {
            form: "form",
            "payments": Payment.objects.all(),
        },
    )
