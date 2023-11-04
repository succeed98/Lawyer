from django.urls import path

from .views import (case_detail, add_case, update_case,
                    delete_case, add_task,upload_files,
                    new_case,  pending_list, completed_list, CaseList, CaseCreateView, CategoryListView,
                    delete_cat, cat_update, cat_add, add_argument, cat_detail, file_list,
                    delete_files, task_view, task_list_view, completed, delete_task, argument_list, argument_detail, arg_update, arg_delete, case_filter, complete_case,
                    court_list, add_court, court_detail, update_court, court_delete,

                    add_session, update_session, detail_session, delete_session,bill_case,

                    add_process, edit_task,generate_process,generate_process1,list_processes,process_detail,update_process,delete_process,add_to_archives,
                    upload_archives,update_archive,archive_detail,
                    add_action_report,list_action_reports,update_action,post_action_detail,delete_action,
                    add_rep,rep_detail,update_rep,delete_rep,rep_list,
                    case_history,
                    request_file,request_list,approve_request,make_request,all_files,start_timer,case_hours,
                    add_expense,ExpenseDetailView,ExpenseListView,update_expense,delete_expense,
                    RenumerationList,approve_renumeration,request_renumeration,
                    request_client_payment,update_client_payment,client_payment_list,client_payment_detail,edit_start_timer, addpercharge, PendingExpenseListView, accept_expense, 
                    decline_expense,resend_expense,generate_invoice_total, generate_invoice_total_save,calendar,all_user_logs,all_user_logs_per_case,upload_terms_files,terms_files_list,terms_edit

                    )


app_name = "cases"


urlpatterns = [

    path('cases/list/', CaseList.as_view(), name='case_list'),
    path('calendar/', calendar, name='calendar'),
    path('cases/list/filter-cases', case_filter, name='case_filter'),




    path("cases/pending-list", pending_list, name="pending_list"),

    path("cases/completed-list", completed_list, name="completed_list"),
    ############################### ARCHIVED CASES #####################################################
    path("cases/archived_cases", add_to_archives, name="add_archive"),
    path("cases/archives/<int:pk>/archive-details", archive_detail, name="archive_detail"),
    path("cases/archives/<int:pk>/update-archive",update_archive, name="archive_update"),
    path("cases/archives/<int:pk>/upload-files",upload_archives, name="archive_upload"),

    path("cases/<int:pk>/case-detail", case_detail, name="case_detail"),
    path("cases/add-case", add_case, name="add_case"),



    path("cases/<int:pk>/case-update", update_case, name="case_update"),
    path("cases/<int:pk>/case-delete", delete_case, name="case_delete"),
    path("cases/tasks/<int:pk>/add-task", add_task, name="add_task"),
    path("cases/files/<int:pk>/add-files", upload_files, name="upload_files"),




    ############################### TERMS OF ENGAGEMENT ########################################################
    path("cases/termsofengagement/<int:pk>/add-files", upload_terms_files, name="upload_terms_files"),
    path("cases/termsofengagement/<int:pk>/list-files", terms_files_list, name="terms_files_list"),
    path("cases/termsofengagement/terms_edit", terms_edit, name="terms_edit"),



    ############################### CATEGORY ########################################################
    path("cases/category/list", CategoryListView.as_view(), name="cat_list"),
    path("cases/category/<int:pk>/update",
         cat_update, name="cat_update"),
    path("cases/category/<int:pk>/delete", delete_cat, name="cat_delete"),
    path("cases/category/add", cat_add, name="cat_add"),
    path("cases/argument/<int:pk>/add", add_argument, name="add_arg"),
    path("cases/category/<int:pk>/detail", cat_detail, name="cat_detail"),
    path("cases/<int:pk>/case-files", file_list, name="file_list"),
    path("cases/<int:pk>/delete_file", delete_files, name="delete_file"),
    path("cases/tasks/<int:pk>/list", task_view, name="task_list"),
    path("cases/tasks/<int:pk>/list-tasks", task_list_view, name="list_tasks"),
    path("cases/tasks/<int:pk>/completed", completed, name="completed"),
    path("cases/tasks/<int:pk>/delete", delete_task, name="delete_task"),
    path("cases/<int:pk>/legal_arguments/list",
         argument_list, name="argument_list"),
    path("cases/<int:pk>/legal_arguments/detail",
         argument_detail, name="argument_detail"),
    path("cases/<int:pk>/legal_arguments/update",
         arg_update, name="argument_update"),
    path("cases/<int:pk>/legal_arguments/delete",
         arg_delete, name="argument_delete"),

    path("cases/<int:pk>/case-update-status",
         complete_case, name="complete_case"),
    ########################################################## COURT ######################################################################
    path('cases/courts/list', court_list, name='court_list'),
    path('cases/courts/<int:pk>/court-detail',
         court_detail, name="court_detail"),
    path('cases/courts/<int:pk>/court-update',
         update_court, name="court_update"),
    path('cases/courts/add', add_court, name="court_add"),
    path('cases/courts/<int:pk>/court-delete',
         court_delete, name="court_delete"),

    #################################################### COURT SESSIONS #################################################################


    path('cases/court-sessions/<int:pk>/add', add_session, name="session_add"),
    path('cases/court-sessions/<int:pk>/details',
         detail_session, name="session_detail"),
    path('cases/court-sessions/<int:pk>/update',
         update_session, name="session_update"),
    path('cases/court-sessions/<int:pk>/delete',
         delete_session, name="session_delete"),


    ############################################### PROCESSES ####################################
    path('cases/processes/add', add_process, name="process_add"),
    path('cases/processes/list', list_processes, name="list_process"),

    path('cases/processes/<int:pk>/generate-process', generate_process1, name="generate_process"),
    path('cases/processes/<int:pk>/process-detail', process_detail, name="process_detail"),
    path('cases/processes/<int:pk>/process-update', update_process, name="process_update"),
    path('cases/processes/<int:pk>/delete-process', delete_process, name="process_delete"),



    ############################################### BILL CASE ####################################
    path('cases/<int:pk>/bill-case',bill_case,name='bill_case'),

    path('cases/tasks/<int:pk>/edit-task',edit_task,name='edit_task'),

    ############################################### POST ACTION REPORT ##########################
    path('cases/post-action-report/<int:pk>/add-new',add_action_report,name="add_action"),
    path('cases/post-action-report/<int:pk>/report-list',list_action_reports,name='list_report'),
    path('cases/post-action-report/<int:pk>/report-detail',post_action_detail,name="action_detail"),
    path('cases/post-action-report/<int:pk>/update-report',update_action,name='action_update'),
    path('cases/post-action-report/<int:pk>/delete-report',delete_action,name='action_delete'),

##################################### REPRESENTATION ############################################
    path('cases/representation/add',add_rep,name="add_rep"),
    path('cases/representation/list',rep_list,name="rep_list"),
    path('cases/representation/<int:pk>/details',rep_detail,name="rep_detail"),
    path('cases/representation/<int:pk>/update',update_rep,name="update_rep"),
    path('cases/representation/<int:pk>/delete',delete_rep,name="delete_rep"),
    path("cases/<int:pk>/case-history",case_history,name='case_history'),



    ################################### ARCHIVE REQUESTS #########################################
    path('cases/archives/request',request_file,name='request_file'),
    path('cases/archives/requests/list',request_list,name='request_list'),
    path('cases/archives/<int:pk>/request',make_request,name='make_request'),
    path('cases/archives/<int:pk>/request/approve',approve_request,name='approve_request'),

    ################################### CASE FILES ###############################################
    path('cases/files/all-files',all_files,name="all_files"),
    path('cases/start-timer',start_timer,name="start_timers"),
    path('cases/edit_start_timer',edit_start_timer,name="edit_start_timer"),
    path('cases/<int:pk>/timer/elapsed-time',case_hours,name="case_hours"),
    path('cases/addpercharge',addpercharge,name="addpercharge"),
    path('cases/delete_case/<int:pk>',delete_case,name="delete_case"),


     ################################## EXPENSES #################################################
    path('cases/expenses/', ExpenseListView.as_view(), name='expenses'),
    path('cases/pending_expenses/', PendingExpenseListView.as_view(), name='pending_expenses'),
    path('cases/expenses/<int:pk>/detail', ExpenseDetailView.as_view(), name='expense_detail'),
    path('cases/expenses/<int:pk>/update', update_expense, name='update_expense'),
    path('cases/expenses/<int:pk>/delete', delete_expense, name='delete_expense'),
    path('cases/expenses/add-expense',add_expense,name='add_expense'),
    path('cases/accept_expense/<int:pk>',accept_expense,name='accept_expense'),
    path('cases/decline_expense/<int:pk>',decline_expense,name='decline_expense'),
    path('cases/resend_expense/<int:pk>',resend_expense,name='resend_expense'),

    ################################### Renumeration #############################################
    path('case/renumeration/list',RenumerationList.as_view(),name='renumerations'),
    path('case/renumeration/<int:pk>/approve',approve_renumeration,name='approve_renumeration'),
    path('case/renumeration/<int:pk>/request',request_renumeration,name='request_renumeration'),

    ################################## REQUEST CLIENT PAYMENT INFORMATION ########################
    path('cases/<int:pk>/client-payment',request_client_payment,name='request_payment_info'),
    path('cases/<int:pk>/update-client-payment',update_client_payment,name='update_payment_info'),
    path('cases/client-payment',client_payment_list,name='client_payment_list'),
    path('cases/<int:pk>/client-payment-details',client_payment_detail,name='client_payment_detail'),



    ################################## INVOICE ########################
    path('cases/generate_invoice_total/<int:pk>',generate_invoice_total,name='generate_invoice_total'),
    path('cases/generate_invoice_total_save/<int:pk>',generate_invoice_total_save,name='generate_invoice_total_save'),


    ############################################### USERLOGS ####################################


    path('userlogs/', all_user_logs, name='all_user_logs'),
    path('caselogs/<int:pk>', all_user_logs_per_case, name='all_user_logs_per_case'),


    ]
