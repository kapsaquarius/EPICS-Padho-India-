from django.urls import path

from . import views

urlpatterns = [
	path('donor/',views.home_page,name="donor_home_page"),
	path('donor/',views.register_donor,name='register_donor'),
	path('payment/', views.payment),
	path('donation_form/', views.donation_form),
	path('payment_success/', views.payment_success),
	path('payment_failure/', views.payment_failure),
	path('listdonors/', views.listdonors,name="donors"),

]