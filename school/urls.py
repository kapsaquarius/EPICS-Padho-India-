from django.urls import path

from . import views

urlpatterns = [
	path('school/',views.home_page,name="school_home_page"),
	path('map/',views.plot_map,name="map"),
	path('',views.register,name="register"),
	path('about/',views.about,name="about"),
]