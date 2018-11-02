"""gogabangla URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
import notifications.urls

from definitions import views as core_views

urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    path('admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    path('words/<str:word>',core_views.show_word, name='show_word'),
    path('words/word_by_id=<int:num>',core_views.show_id_word, name='show_id_word'),
    path('tags/<str:tag_name>',core_views.show_tag, name='show_tag'),
    path('letter/<str:let>',core_views.lettersearch, name='show_letter'),
    path('add/',core_views.add_word, name='adder'),
    path('profile/<str:name>',core_views.profile, name='profile'),
    #path('letters/<str:letter>',core_views.show_letter, name='show_letter'),
    #path('add',core_views.add_word, name='add_word'),
    #path('remove',core_views.remove_def, name='remove_def'),
    #path('goga_guy/<id>',core_views.goga_guy, name='goga_guy'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^select2/', include('django_select2.urls')),
    url('search/', core_views.auto_complete, name='search'),
    url('search_page/', core_views.search_page, name='search_page'),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),

    #    url(r'^settings/password/$', core_views.password, name='password'),
]
