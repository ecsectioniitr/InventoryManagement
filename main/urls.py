from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from main.views import *

app_name = 'main'
urlpatterns = [
    # ex: /polls
    url(r'^$', auth_views.login, name='login', kwargs={'redirect_authenticated_user': True}),
    url(r'^logout/$', auth_views.logout,{'next_page': '/'}, name='logout'),
    url(r'^index/$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search/(?P<id>[0-9]+)/$', views.instance_search, name='instancesearch'),
    url(r'^addproject/$', views.add_project, name='addproject'),
    url(r'^profile/(?P<id>[0-9]+)/$', views.profile, name='profile'),
    url(r'^editprofile/$', views.update_profile, name='editprofile'),
    url(r'^follow/$', views.follow, name='follow'),
    url(r'^issue/(?P<issue_id>[0-9]+)/$', views.issue, name='issue'),
    url(r'^return/$', views.return_equipment, name='return'),
    url(r'^cancelfollow/$', views.cancel_follow, name='cancelfollow'),
    url(r'^issueances/(?P<id>[0-9]+)/$', views.issues, name='issueance'),
    url(r'^issueances/$', views.all_issues, name='allissueance'),
    url(r'^admprofile/$', views.admprofile, name='admprofile'),
    
]
