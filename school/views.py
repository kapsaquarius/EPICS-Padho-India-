from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

import geopy
from geopy.geocoders import Nominatim
import folium
from googlegeocoder import GoogleGeocoder
locator = Nominatim(user_agent="myGeocoder")

# Create your views here.

from .models import school

def home_page(request):
	return render(request,'school_home_page.html')

def about(request):
	return render(request,'about.html')

def register(request):
	try:
		school_name = request.POST.get("school_name")
		location = request.POST.get("location")
		requirements = request.POST.get("requirements")
	except school.DoesNotExist:
		return HttpResponse("School name not found")

	s = school(school_name=school_name,location=location,requirements=requirements)
	s.save()

	return render(request,'success_page.html')
	

def plot_map(request):

	schools = school.objects.all()
	location1 = locator.geocode("nitw",timeout=10)
	m = folium.Map(location = [location1.latitude,location1.longitude],title='loc',zoom_start=12)
	folium.Marker(
			location=[location1.latitude,location1.longitude],
    		popup="nitw"+ " : "+ "50 blackboards",
    		icon=folium.Icon(icon='cloud')
	).add_to(m)

	m = folium.Map(location = [20.5937,78.9629],title='loc',zoom_start=5)
	for s in schools:
		school_name = s.school_name
		location = s.location
		requirements = s.requirements
		geolocation = ""
		try:
			#timeout=None
			location = school_name + " " + location
			geolocation = locator.geocode(location,timeout=20)               
		except ValueError as error_message:
			print("Error: geocode failed on input %s with message %s"%(a, error_message))

		#return HttpResponse(geolocation)
		lat = geolocation.latitude
		lon = geolocation.longitude
		

		pp= folium.Html('<a href="'+ 'http://127.0.0.1:8000/donation_form/'+'"target="_blank">'+ school_name + '<br>' + requirements + '</a>', script=True)
		popup = folium.Popup(pp, max_width=2650)
		folium.Marker(
			location=[lat,lon],
    		popup=popup,

    		icon=folium.Icon(icon='cloud')
		).add_to(m)
		m._repr_html_()
	m.save('school/templates/map.html')
	return render(request,'map.html')