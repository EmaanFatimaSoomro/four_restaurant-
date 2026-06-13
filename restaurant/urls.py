from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('',                    views.home,               name='home'),
    path('menu/',               views.menu,               name='menu'),
    path('about/',              views.about,              name='about'),
    path('chef/',               views.chef,               name='chef'),
    path('events/',             views.events,             name='events'),
    path('events/<slug:slug>/', views.event_detail,       name='event_detail'),
    path('gallery/',            views.gallery,            name='gallery'),
    path('reservation/',        views.reservation,        name='reservation'),
    path('reservation/success/',views.reservation_success,name='reservation_success'),
    path('contact/',            views.contact,            name='contact'),

    # AJAX / API
    path('api/menu/',           views.api_menu,           name='api_menu'),
    path('api/newsletter/',     views.api_newsletter,     name='api_newsletter'),
]
