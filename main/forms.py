from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from dal import autocomplete
from django.urls import reverse


from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.conf import settings

class RelatedFieldWidgetCanAdd(widgets.Select):

    def __init__(self, related_model, related_url=None, *args, **kw):

        super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)

        if not related_url:
            rel_to = related_model
            info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
            related_url = 'admin:%s_%s_add' % info

        # Be careful that here "reverse" is not allowed
        self.related_url = related_url

    def render(self, name, value, *args, **kwargs):
        self.related_url = reverse(self.related_url)
        output = [super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs)]
        output.append('<a href="%s" target="_blank" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % \
            (self.related_url, name))
        output.append('<img src="%sadmin/img/icon-addlink.svg" width="10" height="10" alt="%s"/></a>' % (settings.STATIC_URL, 'Add Another'))
        return mark_safe(''.join(output))








class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    first_name = forms.CharField(required=True, label="First Name")
    last_name = forms.CharField(required=True, label="Last Name") 

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email already used")
        return data  


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name','members')
        widgets = {'members': autocomplete.ModelSelect2Multiple(url='user-autocomplete', attrs={'data-html': True})}


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['branch', 'enrollment_no', 'year'] 

class IssueanceForm(forms.ModelForm):   
    project = forms.ModelChoiceField(
       required=False,
       queryset=Project.objects.all(),
       widget=RelatedFieldWidgetCanAdd(Project, related_url="addproject")
                                )
    class Meta:
        model = Issueance
        fields = ['issued_by', 'project', 'year'] 
        widgets = {'project': autocomplete.ModelSelect2(url='project-autocomplete', attrs={'data-html': True}),
                    'issued_by' :autocomplete.ModelSelect2(url='user-autocomplete') }                        
          

class PostForm(forms.Form):
    project = forms.ModelChoiceField(
        label='Project',
        required=True,
       queryset=Project.objects.all(),
       widget=RelatedFieldWidgetCanAdd(Project, related_url="addproject"))
    time = forms.IntegerField(label='Time(days)')   
    equipments = forms.ModelMultipleChoiceField( label='Equipments',
        required=True,
        queryset=EquipmentInstance.objects.filter(is_available=True),
        widget=autocomplete.ModelSelect2Multiple(url='equipment-autocomplete', attrs={'data-html': True}),
    )

    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['project'].queryset = user.project_set.all()
    

