
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import index, FirmChart,user_path,my_notifications,my_custom_page_not_found_view,mark_as_deleted,mark_as_read,mark_as_unread,user_logs,all_read,all_unread,account_dash,go_to_target, view_team_logs
# from ajax_select import urls
# from ajax_select import urls as ajax_select_url
from ajax_select import urls as ajax_select_urls


admin.autodiscover()

handler404 = 'firm.views.my_custom_page_not_found_view'

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", index, name="index"),
    path('sentry-debug/', trigger_error),
    path('accounts/', include('django.contrib.auth.urls')),
    path("api/chart/data", FirmChart.as_view(), name="api-data"),
    path("user_path/redirect/", user_path, name="user_path"),
    path("user-notifications/", my_notifications, name="user_notifications"),
    path("go_to_target/<int:pk>", go_to_target, name="go_to_target"),
    path("", include('accounts.urls')),
    path("", include('cases.urls')),
    path("", include('documents.urls')),
    path("", include('principles.urls')),
    path("", include('clients.urls')),
    path("", include('schedules.urls')),
    path("", include('visitors.urls')),
    path("", include('wills.urls')),
    path("", include('correspondents.urls')),
    path('comment/', include('comment.urls')),
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('notifications/', include('notify.urls', 'notifications')),
    path("resources/", include('resources.urls')),
    path("activity/<int:pk>/user-logs",user_logs,name='user-logs'),
    path('ajax_select/', include(ajax_select_urls)),
    path('user-notifications/<int:pk>/read',mark_as_read,name="read"),
    path('user-notifications/<int:pk>/unread',mark_as_unread,name="unread"),
    path('user-notifications/all-read',all_read,name="all_read"),
    path('user-notifications/all-unread',all_unread,name="all_unread"),
    path("account_dash/",account_dash,name='account_dash'),
    path("view_team_logs/",view_team_logs,name='view_team_logs'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('tinymce/', include('tinymce.urls')),







]
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
