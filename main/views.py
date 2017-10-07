
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .forms import *
from .tables import EquipmentInstanceTable
from .models import *
from django_cron import CronJobBase, Schedule
import datetime

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('main/acc_active_email.html', {
                'user':user, 
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    
    else:
        form = SignupForm()
    
    return render(request, 'main/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def search(request):
	"""for searching different items available depending on get request,
	display all items available for no filters """ 
	equipment = EquipmentInstanceTable()	
	return render(request, "main/search.html", {'equipment': equipment})   

def issue(request):
	"""check availability of the item ,
	issuer should have admin access or isadmin=True """
    form = IssueanceForm()
    if request.method == "POST":
	if UserProfile.objects.get(user=request.user.username).is_admin == True:
            form = IssueanceForm(request.POST)
            if form.is_valid():
                issued_by = form.cleaned_data.get('issued_by')
                project = form.cleaned_data.get('project')
                equipment = form.cleaned_data('equipmentInstance')
		year = form.cleaned_date('year')
		return_date = form.cleaned_data('return_date')
		Issueance.objects.create(issued_by = issued_by, projecy = project, equipmentInstance = equipment, year = year, return_date = return_date)
		notification = equipment + " has been issued to " + issued_by    	
	    

def return_equipment(request):
	"""check if all the related paramenters are correct,
	return only by admin, 
	calculate fine if any (may need to add a new model field)"""
    if request.method == "POST":
        Issueance_pk = request.POST.get('Issueance_pk')
	Issueance.objects.get(pk = Issueance_pk).update(returned = True)
	notification = "equipment returned"

def issue_request(request):
	""" generate a issue request for items unavailable """
    if request.method == "POST":
        equipment = request.POST.get('equipment_name')
	equipment_queryset = EquipmentInstance.objects.get(equipment=equipment)
	if equipment_queryset.is_available == True:
            issue_request = IssueRequest(equipment = equipment, user = request.user.username, is_active=True)
            notification = "Your Request has been registered"
	else:
	    notification = "Sorry the Equiment is unavailable"

def cancel_issue_request(request):
	"""cancel the issue request"""
    if request.method == "POST":
	if UserProfile.objects.get(user=request.user.username).is_admin == True:
            issue_request_pk = request.POST.get('request_pk')
            issue_request = IssueRequest.objects.filter(pk=issue_request_pk)
            issue_request.delete()
            """ send cancencellation notification to the respective user"""
            notification = "Your request has been cancelled"

def update_profile(request):
	"""update the userprofile"""


def view_issue_request(request):
	"""view all the issue request from newest to oldest"""
    if request.method == "POST":
        if UserProfile.objects.get(user=request.user.username).is_admin == True:
            issue_requests = IssueRequest.objects.all.order_by('-pk')
            #return render(request,'main/view_issue_request.html',{'issue_requests'=issue_requests})

def add_project(request):
	""" add a project name and its members, permissions to be decided"""


"""
class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 720 #runs once every 12 hours
    schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
    code = "main.my_cron_job"
    def do(self):
        user = request.user.username
        issueance = Issueance.objects.filter(issued_by = user)
        if issueance.return_date <= datetime.datetime.now():
            message = "your issuance period has exceeded, please return the equipment"
        else:
            message = " ";
        pass

"""
