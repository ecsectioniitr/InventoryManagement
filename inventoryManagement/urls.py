"""inventoryManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from main.views import UserAutocomplete , ProjectAutocomplete
from main.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^table/', include('table.urls')),
    url(r'^', include('main.urls')),
    url(
        r'^user-autocomplete/$',
        UserAutocomplete.as_view(),
        name='user-autocomplete',
    ),
    url(
        r'^user-autocomplete/$',
        ProjectAutocomplete.as_view(),
        name='project-autocomplete',
    ),
    url(r'^addproject/$', add_project, name='addproject'),
    url(r'^table/data/$', MyDataView.as_view(), name='table_data'),
    url(r'^table/admdata/$', MyAdmDataView.as_view(), name='admtable_data'),
    
]

