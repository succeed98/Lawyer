from django.urls import path
from .views import (client_create_view, client_delete,
                    client_detail, client_list,
                    client_detail, client_update,
                    cat_delete, cat_detail,
                    category_list, add_cat,
                    update_cat,
                    client_cat,add_case,
                    add_will,
                    add_engagement,update_terms,
                    delete_terms,term_detail,payment_detail,
                    add_payment,update_payment,delete_payment,payment_list,
                    type_list,type_detail,add_types,update_type,type_delete,client_type

                    )


app_name = 'clients'

urlpatterns = [

    path("clients/client_list", client_list, name='client_list'),
    path("clients/<int:pk>/client-detail", client_detail, name="client_detail"),
    path("clients/<int:pk>/client-update", client_update, name="client_update"),
    path("clients/<int:pk>/client-delete", client_delete, name="client_delete"),
    path("clients/add-client", client_create_view, name="client_add"),

    path("clients/categroy/<int:pk>/category-details",
         cat_detail, name="cat_detail"),
    path("clients/categroy/<int:pk>/category-update",
         update_cat, name="cat_update"),
    path("clients/categroy/<int:pk>/category-delete",
         cat_delete, name="cat_delete"),
    path("clients/categroy/add-category", add_cat, name="cat_add"),
    path("clients/categroy/list", category_list, name="cat_list"),
    path("clients/clients/categroy/<int:pk>/list",
         client_cat, name="client_cat"),

    #case
    path('clients/<int:pk>/add-new-case',add_case,name='add-case'),
    #will
    path('clients/<int:pk>/add-new-will',add_will,name='add-will'),


    # client types
    path("clients/type/list", type_list, name="type_list"),
    path("clients/type/<int:pk>/type-details",
         type_detail, name="type_detail"),
    path("clients/type/<int:pk>/type-update",
         update_type, name="update_type"),
    path("clients/type/<int:pk>/type-delete",
         type_delete, name="type_delete"),
    path("clients/type/add-type", add_types, name="add_types"),

    path("clients/clients/type/<int:pk>/list",
         client_type, name="client_type"),



    ####################################TERMS OF ENGAGEMENT ###############################################
    path('client/add/<int:pk>/terms-of-engagement',add_engagement,name='add_terms'),
    path('client/update/<int:pk>/terms-of-engagement',update_terms,name='update_terms'),
    path('client/details/<int:pk>/terms-of-engagement',term_detail,name='terms_detail'),
    path('client/delete/<int:pk>/terms-of-engagement',delete_terms,name='delete_terms'),


    ########################################## PAYMENTS ###################################################
    path('client/payments/list',payment_list, name='payment_list'),
    path('client/payments/add/new-payment',add_payment, name='add_payment'),
    path('client/payments/<int:pk>/details',payment_detail, name='payment_detail'),
    path('client/payments/<int:pk>/update',update_payment, name='update_payment'),
    path('client/payments/<int:pk>/delete',delete_payment, name='delete_payment'),




]
