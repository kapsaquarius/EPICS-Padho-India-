from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
# Create your views here.

from .models import donor
from school.models import school



from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
import logging, traceback
import hashlib
import requests
from random import randint
from django.views.decorators.csrf import csrf_exempt

global FIRST_NAME
global PHONE
global PAID_FEE_AMOUNT
global EMAIL
SALT = 'eCwWELxi'
KEY = 'gtKFFx'
PAID_FEE_AMOUNT = 10000
PAID_FEE_PRODUCT_INFO = "Donation for School"
PAYMENT_URL_TEST = 'https://test.payu.in/_payment'
SERVICE_PROVIDER = "payu_paisa"
FIRST_NAME = "Kapil"
EMAIL = "kapilrathod1234@gmail.com"
PHONE = "9167448253"

DT = {}

def home_page(request):
	return render(request,'donor_home_page.html')


def listdonors(request):

	all_donors = donor.objects.all()

	print(all_donors)
	context = {
		"donors":all_donors,
	}
	return render(request,'donor_list.html',context)

def donation_form(request):
	if request.method == "POST":

		donor_name = request.POST.get("full_name")
		pnum = request.POST.get("phone_number")
		amount = request.POST.get("amount")
		email = request.POST.get("email")

		DT["name"]=donor_name
		DT["pnum"]=pnum
		DT["amount"]=amount
		DT["email"]=email

		return HttpResponseRedirect('http://127.0.0.1:8000/payment/')	
			

	else:
		return render(request,"donor_form.html")


def payment(request):   


	data = {}
	txnid = get_transaction_id()
	hash_ = generate_hash(request, txnid)
	hash_string = get_hash_string(request, txnid)
	# use constants file to store constant values.
	# use test URL for testing
	data["action"] = PAYMENT_URL_TEST
	data["amount"] = float(DT["amount"])
	data["productinfo"]  = PAID_FEE_PRODUCT_INFO
	data["key"] = KEY
	data["txnid"] = txnid
	data["hash"] = hash_
	data["hash_string"] = hash_string
	data["firstname"] = DT["name"]
	data["email"] = DT["email"]
	data["phone"] = DT["pnum"]
	data["surl"] = "http://127.0.0.1:8000/payment_success/"
	data["furl"] = "http://127.0.0.1:8000/payment_failure/"

	return render(request, "donor_payment.html", data)        
	
# generate the hash
def generate_hash(request, txnid):
	try:
		# get keys and SALT from dashboard once account is created.
		hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
		hash_string = get_hash_string(request,txnid)
		generated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
		return generated_hash
	except Exception as e:
		# log the error here.
		logging.getLogger("error_logger").error(traceback.format_exc())
		return None

# create hash string using all the fields
def get_hash_string(request, txnid):

	hash_string = KEY+"|"+txnid+"|"+str(float(DT["amount"]))+"|"+PAID_FEE_PRODUCT_INFO+"|"
	hash_string += str(DT["name"])+"|"+str(DT["email"])+"|"
	hash_string += "||||||||||"+SALT

	return hash_string
# generate a random transaction Id.
def get_transaction_id():
	hash_object = hashlib.sha256(str(randint(0,9999)).encode("utf-8"))
	# take approprite length
	txnid = hash_object.hexdigest().lower()[0:32]
	return txnid


@csrf_exempt
def payment_success(request):
	data = {}
	return render(request, "success.html", data)

# no csrf token require to go to Failure page. This page displays the message and reason of failure.
@csrf_exempt
def payment_failure(request):
	data = {}
	return render(request, "failure.html", data)

def register_donor(request):

	donor_name = request.POST.get("donor_name")
	pnum = request.POST.get("phone_number")
	d = donor(name=donor_name,phone_number=pnum)
	d.save()

	
	return render(request,'donor_home_page.html',context)

		
