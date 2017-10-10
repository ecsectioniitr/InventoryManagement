
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
from dal import autocomplete
from django.db.models import Q
try:
    from django.utils import simplejson as json
except ImportError:
    import json

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
            mail_subject = 'Activate your Inventory management account.'
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
    form = IssueanceForm()
    if request.method == "POST":
        if UserProfile.objects.get(user=request.user.username).is_admin == True:
            form = IssueanceForm(request.POST)
            if form.is_valid():
                issue = form.save()
                notification = issue.equipment + " has been issued to " + issue.issued_by
        else:
            HttpResponse('You dont have required permissions to issue the equipment')        
    return render(request, "main/issue.html", {'form': form})                    
        

def return_equipment(request):
    if request.method == "POST" :
        Issueance_pk = request.POST.get('Issueance_pk')
        if UserProfile.objects.get(user=request.user.username).is_admin == True:
            Issueance.objects.get(pk = Issueance_pk).update(returned = True)
            notification = "equipment returned"
            ctx = { 'noti' : True,}
            return HttpResponse(json.dumps(ctx), content_type='application/json')
    ctx = { 'noti' : False,}
    return HttpResponse(json.dumps(ctx), content_type='application/json')            


def issue_request(request):
    """ generate a issue request for items unavailable """
    if request.method == "POST":
        equip = request.POST.get('id')
        equipment = get_object_or_404(EquipmentInstance, pk=equip)
        if equipment.is_available == False and equipment.decommisioned == False :
            try:
                issue_request = IssueRequest(equipment = equipment, user = request.user, is_active=True)
                issue_request.save()
                ctx = { 'noti' : True,}
                return HttpResponse(json.dumps(ctx), content_type='application/json')
            except IntegrityError:
                ctx = { 'noti' : False,}
                return HttpResponse(json.dumps(ctx), content_type='application/json')

def cancel_issue_request(request):
    """cancel the issue request"""
    if request.method == "POST":
            issue_request_pk = request.POST.get('request_pk')
            issue_request = IssueRequest.objects.filter(pk=issue_request_pk)
            if issue_request.user == request.user :
                issue_request.delete()
                ctx = { 'noti' : True,}
                return HttpResponse(json.dumps(ctx), content_type='application/json')
            else :
                ctx = { 'noti' : False,}
                return HttpResponse(json.dumps(ctx), content_type='application/json')

def update_profile(request):
    """update the userprofile"""
    if request.method == 'POST':
        user = request.user
        profile = UserProfile.objects.get(user=user)
        userform = UserForm(request.POST, instance=user)
        profileform = UserProfileForm(request.POST, instance=profile)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            f = profileform.save(commit=False)
            f.user = request.user
            f.save()
            context = {
            'userform'  : userform,
            'profileform': profileform
            }   
            return HttpResponseRedirect(reverse('main:editprofile'), context)
        else :
            context = {
            'userform'  : userform,
            'profileform': profileform
            } 
            return HttpResponseRedirect(reverse('main:editprofile'), context)
    else:    
        profile = UserProfile.objects.get(user = request.user)
        userform = UserForm(instance=request.user)
        profileform = UserProfileForm(instance=profile)
        context = {
            'userform'  : userform,
            'profileform': profileform
        }
        return render(request, 'main/editProfile.html', context)


def view_issue_request(request):
    """view all the issue request from newest to oldest"""
    if request.method == "POST":
        if UserProfile.objects.get(user=request.user.username).is_admin == True:
            issue_requests = IssueRequest.objects.all.order_by('-pk')
            #return render(request,'main/view_issue_request.html',{'issue_requests'=issue_requests})

def add_project(request):
    """ add a project name and its members, permissions to be decided"""
    return handlePopAdd(request, ProjectForm)        

    


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

class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        query = UserProfile.objects.all()
        qs = []
        for userp in query:
            qs.append(userp.user)

        if self.q:
            qs = qs.filter( Q(first_name__icontains = term) | Q(last_name__icontains = term)  | Q(username__icontains = term))
        return qs


class ProjectAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Project.objects.all()

        if self.q:
            qs = qs.filter( Q(name__icontains = term) | Q(name__contains = term))
        return qs



from django.utils.html import escape
def handlePopAdd(request, addForm):
    if request.method == "POST":
        form = addForm(request.POST)
        if form.is_valid():
            try:
                newObject = form.save()
            except forms.ValidationError, error:
                newObject = None
            if newObject:
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script><script type="text/javascript">self.close();</script>' % \
                    (escape(newObject._get_pk_val()), escape(newObject)))
    else:
        form = addForm()
        context = {'form': form}
        #return render_to_response("main/addProject.html", pageContext)
        return render(request, 'main/addProject.html', context)