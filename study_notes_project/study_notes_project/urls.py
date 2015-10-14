"""study_notes_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from user_profile import views as user_profile
from landing import views as landing

urlpatterns = [
	
	url(r'^$', landing.Home),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', user_profile.Login),
    url(r'^accounts/logout/$', user_profile.Logout),
    url(r'^accounts/signup/$', user_profile.Signup),
    url(r'^accounts/profile/$', user_profile.Profile),
    url(r'^accounts/change_password/$', user_profile.Change_Password),

    
]
