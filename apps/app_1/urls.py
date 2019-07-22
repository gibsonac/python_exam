from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^user/input$', views.user_input),
    url(r'^user/login$', views.user_login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^trips/new$', views.new_trip),
    url(r'^trips/new/request$', views.submit_new_trip),
    url(r'^trips/delete/(?P<my_val>\d+)$', views.delete_trips),
    url(r'^trips/edit/(?P<my_val>\d+)$', views.edit_trips),
    url(r'^trips/edit/(?P<my_val>\d+)/request$', views.edit_trip_submit),
    url(r'^trips/(?P<my_val>\d+)$', views.trip_details),
    url(r'^trips/(?P<my_val>\d+)/add$', views.add_trip),
    url(r'^trips/giveup/(?P<my_val>\d+)$', views.give_up),
    
]