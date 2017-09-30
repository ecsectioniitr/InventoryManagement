from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	enrollment_no = models.IntegerField(default=00000000,blank=True )
	branch = models.CharField(max_length=20, blank=True)
	year = models.IntegerField(blank=True)
	is_admin = models.BooleanField(default=False)
	def __str__(self):
		return self.user.username

class Project(models.Model):
	name = models.CharField(max_length=50)
	members =models.ManyToManyField(User)
	def __str__(self):
		return self.name

class Equipment(models.Model):
	name = models.CharField(max_length=100)
	price =  models.FloatField()
	def __str__(self):
		return self.name

class EquipmentInstance(models.Model):
	equipment = models.ForeignKey(Equipment, on_delete = models.CASCADE)
	buying_time = models.DateTimeField(blank=True)
	is_available = models.BooleanField(default=True)
	remark = models.CharField(max_length=200, blank=True)
	decommisioned = models.BooleanField(default=False)
	uid = models.CharField(max_length=50, unique=True)
	def __str__(self):
		return self.equipment.name+" "+self.uid

class Issueance(models.Model):
	issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
	project = models.ForeignKey(Project, on_delete=models.SET_NULL, null = True)
	equipmentInstance = models.ForeignKey(EquipmentInstance, on_delete=models.CASCADE)
	year = models.IntegerField()
	issued_on = models.DateTimeField(auto_now_add=True)
	returned  = models.BooleanField(default = False)
	def __str__(self):
		return self.equipmentInstance.equipment.name+" "+self.equipment.uid+" for "+self.project.name

class IssueRequest(models.Model):
	equipment = models.ForeignKey(Equipment, on_delete = models.CASCADE)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	created_on = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	def __str__(self):
		return self.equipment.name+" by "+self.user.username




