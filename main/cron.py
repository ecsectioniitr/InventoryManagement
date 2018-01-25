from .models import *
from django.utils import timezone
from notify.signals import notify
from django_cron import CronJobBase, Schedule
from datetime import datetime, timedelta

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5 # every 5 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'main.cron_job'    # a unique code

    def do(self):
        issues = Issueance.objects.filter(returned=False)
        for issue in issues:
            day  = issue.year 
            returndate = issue.issued_on + timedelta(days=day)
            if timezone.now() >= returndate:
                notify.send(issue.issued_by, recipient=issue.issued_by, actor=issue.equipmentInstance,
                        verb='your issuance period has exceeded, please return the equipment!',)
            elif timezone.now() >= returndate - timedelta(days=1) : 
                notify.send(issue.issued_by, recipient=issue.issued_by, actor=issue.equipmentInstance,
                        verb='Your returning time is approaching!',)