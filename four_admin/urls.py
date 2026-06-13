from django.urls import path
from . import views

app_name = 'four_admin'

urlpatterns = [
    # Auth
    path('login/',  views.admin_login,  name='login'),
    path('logout/', views.admin_logout, name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Menu
    path('menu/',               views.menu_list,   name='menu_list'),
    path('menu/add/',           views.menu_add,    name='menu_add'),
    path('menu/<int:pk>/edit/', views.menu_edit,   name='menu_edit'),
    path('menu/<int:pk>/delete/', views.menu_delete, name='menu_delete'),

    # Reservations
    path('reservations/',                        views.reservations,        name='reservations'),
    path('reservations/<int:pk>/',               views.reservation_detail,  name='reservation_detail'),
    path('reservations/<int:pk>/status/',        views.reservation_status,  name='reservation_status'),
    path('reservations/<int:pk>/delete/',        views.reservation_delete,  name='reservation_delete'),

    # Events
    path('events/',                  views.events,         name='events'),
    path('events/add/',              views.events_add,     name='events_add'),
    path('events/<int:pk>/edit/',    views.events_edit,    name='events_edit'),
    path('events/<int:pk>/delete/',  views.events_delete,  name='events_delete'),

    # Gallery
    path('gallery/',                  views.gallery,        name='gallery'),
    path('gallery/add/',              views.gallery_add,    name='gallery_add'),
    path('gallery/<int:pk>/delete/',  views.gallery_delete, name='gallery_delete'),

    # Staff
    path('staff/',                  views.staff,        name='staff'),
    path('staff/add/',              views.staff_add,    name='staff_add'),
    path('staff/<int:pk>/edit/',    views.staff_edit,   name='staff_edit'),
    path('staff/<int:pk>/delete/',  views.staff_delete, name='staff_delete'),

    # Reviews
    path('reviews/',                       views.reviews,        name='reviews'),
    path('reviews/<int:pk>/toggle/',       views.review_toggle,  name='review_toggle'),
    path('reviews/<int:pk>/delete/',       views.review_delete,  name='review_delete'),

    # Newsletter
    path('newsletter/', views.newsletter, name='newsletter'),

    # Messages
    path('messages/',                   views.messages_list,   name='messages_list'),
    path('messages/<int:pk>/',          views.message_detail,  name='message_detail'),
    path('messages/<int:pk>/delete/',   views.message_delete,  name='message_delete'),
]
