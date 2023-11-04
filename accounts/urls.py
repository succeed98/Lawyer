from django.urls import path
from .views import (accounts, update_lawyers_profile, staff_detail_view,
                    lawyer_profile_view, lawyer_detail, lawyer_list,
                    lawyer_profile, other_staff, update_lawyer_profile,
                    change_password, add_staff, staff_details,
                    update_staff, update_staff_profile, delete_lawyer, delete_staff,
                    client_dashboard,get_case_details ,team_list_view,add_team,
                    update_team,team_detail,team_update,delete_team,
                    add_role,role_detail,role_list,update_role,delete_role,
                    status_list,add_status,delete_status,update_status,status_detail,case_detail_acc,get_case_expenses,AccountExpense, account_expense,
                    invoice_list,invoice_detail,approve_invoice





                    )


app_name = "accounts"


urlpatterns = [

    path("accounts/signup", accounts, name="signup"),
    path("accounts/lawyer/signup", lawyer_profile_view, name='lawyer-signup'),
    path("accounts/lawyers/lawyer-list", lawyer_list, name="lawyer_list"),
    path("accounts/lawyers/<int:pk>/lawyer-detail",
         lawyer_detail, name="lawyer_detail"),


    path("accounts/lawyers/<int:pk>/lawyer-profile",
         lawyer_profile, name="lawyer_profile"),

    path("accounts/front-desk/staff-list", other_staff, name="staff_list"),
    path("accounts/password", change_password, name="change_password"),
    path("accounts/users/add-staff", add_staff, name="add_staff"),
    path("accounts/users/<int:pk>/staff-detail",
         staff_details, name='staff_detail'),
    path("accounts/users/<int:pk>/update-staff",
         update_staff, name='update_staff'),

    path("accounts/lawyers/<int:pk>/lawyers-profile",
         update_lawyers_profile, name="lawyers_profile"),







    path("accounts/profile/<int:pk>/update-profile",
         update_lawyer_profile, name="update_profile"),
    path("accounts/<int:pk>/profile/staff-profile",
         staff_detail_view, name="staff_profile"),


    path("accounts/profile/<int:pk>/update-staff-profile",
         update_staff_profile, name="staff_profileupdate"),

    path("accounts/lawyers/<int:pk>/delete",
         delete_lawyer, name="delete_lawyer"),
    path("accounts/staff/<int:pk>/delete", delete_staff, name="delete_staff"),

    ######################### CLIENTS ###############################################


    path("accounts/clients/<int:pk>/client-dashboard",client_dashboard,name="client_dashboard"),
    path("accounts/clients/<int:pk>/case-detail",get_case_details, name="case_details"),

    ############################################ TEAMS ##################################################

    path("accounts/teams/team-list",team_list_view,name='teams'),
    path("accounts/teams/add-team",add_team,name="add_team"),
    path("accounts/teams/<int:pk>/team/detail",team_detail,name="team_detail"),
    path("accounts/teams/<int:pk>/team/delete",delete_team, name="team_delete"),
    path("accounts/teams/<int:pk>/team/update",team_update,name="team_update"),
    path("accounts/teams/<int:pk>/team/update",update_team,name="update_team"),


    ############################# ROLES #######################################
    path("accounts/roles/roles-list",role_list,name='role_list'),
    path("accounts/roles/add-role",add_role,name='add_role'),

    path("accounts/roles/<int:pk>/role-details",role_detail,name="role_detail"),
    path("accounts/roles/<int:pk>/update-role",update_role,name="update_role"),
    path("accounts/roles/<int:pk>/delete-role",delete_role,name="delete_role"),


    ############################ Lawyer Status ###############################

    path("accounts/status/status-list",status_list,name='status_list'),
    path("accounts/expenses",account_expense,name='expenses'),
    path("accounts/status/add-status",add_status,name='add_status'),
    path("accounts/status/<int:pk>/status-details",status_detail,name="status_detail"),
    path("accounts/status/<int:pk>/update-status",update_status,name="update_status"),
    path("accounts/status/<int:pk>/delete-status",delete_status,name="delete_status"),
    path("accounts/cases/<int:pk>/detail",case_detail_acc,name='case_detail_acc'),
    path("accounts/cases/<int:pk>/case-expenses",get_case_expenses,name='case_expenses'),



     # invoice
     
    path("accounts/invoice_list/",invoice_list,name='invoice_list'),
    path("accounts/invoice_detail/<int:pk>",invoice_detail,name='invoice_detail'),
    path("accounts/approve_invoice/<int:pk>",approve_invoice,name='approve_invoice'),







]
