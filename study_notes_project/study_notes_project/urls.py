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
from flash_cards import views as flash_cards
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete

urlpatterns = [
	
	url(r'^$', landing.Home),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', user_profile.Login),
    url(r'^accounts/logout/$', user_profile.Logout),
    url(r'^accounts/signup/$', user_profile.Signup),
    url(r'^accounts/profile/$', user_profile.Profile),
    url(r'^accounts/change_password/$', user_profile.Change_Password),
    url(r'^accounts/reset/password_reset/$', password_reset, name='reset_password_reset1'),
    url(r'^accounts/password_reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^accounts/reset/done/$', password_reset_complete, name='password_reset_complete'),
    url(r'^cards/new_deck/$', flash_cards.New_Deck),
    url(r'^cards/upload_file/$', flash_cards.Upload_File),
    url(r'^cards/clone/$', flash_cards.Clone),
    url(r'^cards/edit_deck/$', flash_cards.Edit_Deck),
    url(r'^cards/delete_deck/$', flash_cards.Delete_Deck),
    url(r'^cards/new_card/$', flash_cards.New_Card),
    url(r'^cards/edit_card/$', flash_cards.Edit_Card),
    url(r'^cards/delete_card/$', flash_cards.Delete_Card),
    url(r'^cards/search/$', flash_cards.Search),
    url(r'^cards/view_shared_deck/$', flash_cards.View_Shared_Deck),
    url(r'^cards/shared_decks/$', flash_cards.Shared_Decks),
    url(r'^cards/study/$',flash_cards.Study),
    url(r'^cards/', flash_cards.View_Deck),
    
]
