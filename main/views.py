
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
from .tables import *
from .models import *
import datetime
from notify.signals import notify
from dal import autocomplete
from django.db.models import Q
from django.utils import timezone
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


@login_required(login_url='/')
def index(request):
    if UserProfile.objects.get(user=request.user).is_admin == True:
        return render(request, 'main/index_admin.html')
    issuetable = MyIssueanceTable()
    followtable = MyFollowTable()
    return render(request, 'main/index.html', {'issuetable': issuetable, 'followtable': followtable})        

@login_required(login_url='/')
def search(request):
    """for searching different items available depending on get request,
    display all items available for no filters """ 
    equipments = Equipment.objects.all()
    if UserProfile.objects.get(user=request.user).is_admin == True:
        equipment = EquipmentAdmTable() 
    else:
        equipment = EquipmentTable()      
    return render(request, "main/search.html", {'equipment': equipment, 'equipments': equipments})


@login_required(login_url='/')
def instance_search(request, id):
    """for searching different items available depending on get request,
    display all items available for no filters """ 
    equipment=get_object_or_404(Equipment, pk=id)
    qs = equipment.eqins.filter(decommisioned=False)
    if UserProfile.objects.get(user=request.user).is_admin == True:
        equipmenttable = EquipmentInstanceTable(qs) 
    else:
        equipmenttable = EquipmentInstanceTable(qs)      
    return render(request, "main/searchinstance.html", {'equipment': equipment, 'equipmenttable': equipmenttable})    


@login_required(login_url='/')
def issues(request, id):
    equipment=get_object_or_404(Equipment, pk=id)
    qs = Issueance.objects.filter(equipmentInstance__equipment=equipment)
    issuetable = IssueanceTable(qs)
    if UserProfile.objects.get(user=request.user).is_admin == True:
        issuetable = IssueanceAdmTable(qs)
    return render(request, "main/issues.html", {'issuetable': issuetable})

def all_issues(request):
    equipments=Equipment.objects.all()
    qs = []
    for equipment in equipments :
        if equipment.eqins.filter(is_available=False, decommisioned=False).count() != 0:
            qs.append(equipment)
    issuetable = EquipmentIssueTable(qs)
    if UserProfile.objects.get(user=request.user).is_admin == True:
        issuetable = EquipmentIssueTable(qs)
    return render(request, "main/issues.html", {'issuetable': issuetable})    


@login_required(login_url='/')
def profile(request, id):
    user  = get_object_or_404(User, pk=id)
    userprofile = get_object_or_404(UserProfile, user=user)
    return render(request, "main/profile.html", {'userp': user, 'userprofile': userprofile})


@login_required(login_url='/')
def admprofile(request):
    if UserProfile.objects.get(user=request.user).is_admin == False:
        return HttpResponse('You cannot access this page')       
    userprofile  = get_object_or_404(UserProfile, enrollment_no=request.GET.get('enrollment_no'))
    user = userprofile.user
    qs = Issueance.objects.filter(issued_by=user, returned=False) 
    issuetable = IssueanceAdmTable(qs)
    form = PostForm(user)
    return render(request, "main/profile_adm.html", {'userp': user, 'userprofile': userprofile, 'issuetable':issuetable, 'form':form })    


@login_required(login_url='/')
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
            return HttpResponseRedirect(reverse('main:search'), context)
        else :
            context = {
            'userform'  : userform,
            'profileform': profileform
            } 
            return HttpResponseRedirect(reverse('main:search'), context)
    else:    
        profile = UserProfile.objects.get(user = request.user)
        userform = UserForm(instance=request.user)
        profileform = UserProfileForm(instance=profile)
        context = {
            'userform'  : userform,
            'profileform': profileform
        }
        return render(request, 'main/editProfile.html', context)


@login_required(login_url='/')
def issue(request, issue_id):
    if UserProfile.objects.get(user=request.user).is_admin == False:
        return HttpResponse('You dont have required permissions to issue the equipment') 
    user = get_object_or_404(User, pk=issue_id)
    form = PostForm(user)
    if request.method == "POST":
        if UserProfile.objects.get(user=request.user).is_admin == True:
            user = get_object_or_404(User, pk=issue_id)
            form = PostForm(user, request.POST)
            if form.is_valid():
                user = get_object_or_404(User, pk=issue_id)
                time = form.cleaned_data['time']
                project = form.cleaned_data['project']
                for equipment in form.cleaned_data['equipments']:
                    if  equipment.is_available:
                        Issueance.objects.create(issued_by=user, project=project, equipmentInstance=equipment, year=time,
                        enrollment_no = user.userprofile.enrollment_no )
                        equipment.is_available=False
                        equipment.save()
                response = redirect('main:admprofile')
                response['Location'] += '?enrollment_no=%d' % user.userprofile.enrollment_no
                return response    

        else:
            return HttpResponse('You dont have required permissions to issue the equipment') 
    return render(request, 'main/issue.html', {'form': form})
        

@login_required(login_url='/')
def return_equipment(request):
    if request.method == "POST" :
        Issueance_pk = request.POST.get('Issueance_pk')
        if UserProfile.objects.get(user=request.user).is_admin == True:
            issue = Issueance.objects.get(pk = Issueance_pk)
            equipment = issue.equipmentInstance
            issue.returned = True
            issue.save()
            issue.return_date = timezone.now()
            equipment.is_available=True
            issue.save()
            equipment.save()
            followers = list(equipment.equipment.followers.all())
            notify.send(request.user, recipient_list=followers, actor=equipment,
                        verb='is available now!.',)
            notification = "equipment returned"
            ctx = { 'noti' : True,}
            return HttpResponse(json.dumps(ctx), content_type='application/json')
    ctx = { 'noti' : False,}
    return HttpResponse(json.dumps(ctx), content_type='application/json')            


@login_required(login_url='/')
def follow(request):
    """ generate a issue request for items unavailable """
    if request.method == "POST":
        equip = request.POST.get('id')
        equipment = get_object_or_404(Equipment, pk=equip)
        try:
            follow = Follow(equipment = equipment, user = request.user, is_active=True)
            follow.save()
            ctx = { 'noti' : True,}
            return HttpResponse(json.dumps(ctx), content_type='application/json')
        except IntegrityError:
            ctx = { 'noti' : False,}
            return HttpResponse(json.dumps(ctx), content_type='application/json')



@login_required(login_url='/')
def cancel_follow(request):
    """cancel the issue request"""
    if request.method == "POST":
            follow_pk = request.POST.get('request_pk')
            equipment = get_object_or_404(Equipment, pk=follow_pk)
            follow = get_object_or_404(Follow, equipment=equipment, user =request.user )
            if follow.user == request.user :
                follow.delete()
                ctx = { 'noti' : True,}
                return HttpResponse(json.dumps(ctx), content_type='application/json')
            else :
                ctx = { 'noti' : False,}
                return HttpResponse(json.dumps(ctx), content_type='application/json')



@login_required(login_url='/')
def add_project(request):
    """ add a project name and its members, permissions to be decided"""
    return handlePopAdd(request, ProjectForm)        

    





class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.all()
        if self.q:
            qs = qs.filter( Q(first_name__icontains = self.q) | Q(last_name__icontains = self.q)  | Q(username__icontains = self.q))
        return qs


class ProjectAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Project.objects.all()

        if self.q:
            qs = qs.filter( Q(name__icontains = self.q) | Q(name__contains = self.q))
        return qs

class EquipmentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = EquipmentInstance.objects.filter(is_available=True)

        if self.q:
            qs = qs.filter( Q(uid__icontains = self.q) | Q(equipment__name__contains = self.q))
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




from table.views import FeedDataView


class MyDataView(FeedDataView):
    token = EquipmentInstanceTable.token
    def get_queryset(self):
        return super(MyDataView, self ).get_queryset().filter(decommisioned=False) 

class MyAdmDataView(FeedDataView):
    token = EquipmentInstanceAdmTable.token
    def get_queryset(self):
        return super(MyAdmDataView, self).get_queryset().filter(decommisioned=False)                             



class MyIssueView(FeedDataView):
    token = MyIssueanceTable.token
    def get_queryset(self):
        return super(MyIssueView, self).get_queryset().filter(issued_by=self.request.user)  

class MyAdmIssueView(FeedDataView):
    token = IssueanceAdmTable.token
    def get_queryset(self):
        return super(MyAdmIssueView, self).get_queryset().filter(returned=False) 


class MyFollowView(FeedDataView):
    token = MyFollowTable.token
    def get_queryset(self):
        return super(MyFollowView, self).get_queryset().filter(user=self.request.user)                       




