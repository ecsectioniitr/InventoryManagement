from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from main.views import *

app_name = 'main'
urlpatterns = [
    # ex: /polls
    url(r'^login/$', auth_views.login, {'template_name': 'main/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,{'next_page': '/'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^search/$', views.search, name='search'),
    url(r'^addproject/$', views.add_project, name='addproject'),
    url(r'^editprofile/$', views.update_profile, name='editprofile'),
    url(r'^request/$', views.issue_request, name='request'),
    url(r'^issue/(?P<issue_id>[0-9]+)/$', views.issue, name='issue'),
    url(r'^return/$', views.return_equipment, name='return'),
    url(r'^cancelrequest/$', views.cancel_issue_request, name='cancelrequest'),
    url(r'^viewrequest/$', views.view_issue_request, name='viewrequest'),
    
]
