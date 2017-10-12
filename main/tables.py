from models import *
from table import Table
from table.columns import *
from django.core.urlresolvers import reverse_lazy
from django.utils.html import format_html
from django.core.urlresolvers import reverse

class IssueColumn(Column):
    def render(self, value):
            return format_html('<span id = "{}-user"></span>', value.id)

class AdmColumn(Column):
    def render(self, value):
        if value.is_available:
            f = value.id
            value = reverse('main:issue', kwargs={'issue_id':f})
            return format_html('<a href = "{}">Issue</a>', value)
        else:
            issue = value.issueance_set.all()
            qs = issue.filter(returned=False)
            iss = qs[0]
            return format_html('<input type="button" id="{}-return" name="{}" value="Return" onclick="returnequip(this.name)" />', iss.id , iss.id )

class IssueanceAdmColumn(Column):
    def render(self, value):
            return format_html('<input type="button" id="{}-return" name="{}" value="Return" onclick="returnequip(this.name)" />', value.id, value.id)

class ProfileColumn(Column):
    def render(self, value):
            f = value.issued_by.id
            name = value.issued_by.username
            value = reverse('main:profile', kwargs={'id':f})
            return format_html('<a target="_blank" href = "{}">{}</a>', value, name )                
         


class EquipmentInstanceTable(Table):
    id = Column(field='id', header=u'id')
    equipment = Column(field='equipment.name', header=u'Equipment Type')
    uid = Column(field='uid', header=u'UID')
    remark = Column(field='remark', header=u'Remark')
    is_available = CheckboxColumn(field='is_available', sortable=True, header=u'Availability')
    issue = IssueColumn(field='id', header=u'Request', searchable=False, sortable=False)


    class Meta:
        model = EquipmentInstance
        ajax = True
        search = True
        ajax_source = reverse_lazy('table_data')
        sort = [(4, 'desc')]


class EquipmentInstanceAdmTable(Table):
    id = Column(field='id', header=u'id')
    equipment = Column(field='equipment.name', header=u'Equipment Type')
    uid = Column(field='uid', header=u'UID')
    remark = Column(field='remark', header=u'Remark')
    is_available = CheckboxColumn(field='is_available', sortable=True, header=u'Availability')
    issue = AdmColumn(field='id', header=u'Issue/Return', searchable=False, sortable=False)
    request = IssueColumn(field='id', header=u'Request', searchable=False, sortable=False)


    class Meta:
        model = EquipmentInstance
        ajax = True
        search = True
        ajax_source = reverse_lazy('admtable_data')
        sort = [(4, 'desc')]        


class IssueanceTable(Table):
    equipmentInstanceid = Column(field='equipmentInstance.id', header=u'Equipment Id')
    equipmentInstance = Column(field='equipmentInstance.equipment.name', header=u'Equipment Type')
    equipmentInstanceuid =Column(field='equipmentInstance.uid', header=u'Equipment Uid') 
    issued_by = ProfileColumn(field='id', header=u'Issued By', searchable=False, sortable=False)
    project = Column(field='project.name', header=u'Equipment')
    issued_on = DatetimeColumn(field='issued_on', header=u'Issued On')
    year = Column(field='year', header=u'Time(weeks)')

    class Meta:
        model = Issueance
        ajax = True
        search = True
        ajax_source = reverse_lazy('issuetable_data')


class IssueanceAdmTable(Table):
    equipmentInstanceid = Column(field='equipmentInstance.id', header=u'Equipment Id')
    equipmentInstance = Column(field='equipmentInstance.equipment.name', header=u'Equipment Type')
    equipmentInstanceuid =Column(field='equipmentInstance.uid', header=u'Equipment Uid') 
    issued_by = ProfileColumn(field='id', header=u'Issued By', searchable=False, sortable=False)
    project = Column(field='project.name', header=u'Equipment')
    issued_on = DatetimeColumn(field='issued_on', header=u'Issued On')
    year = Column(field='year', header=u'Time(weeks)')
    issue = IssueanceAdmColumn(field='id', header=u'Issue/Return', searchable=False, sortable=False)

    class Meta:
        model = Issueance
        ajax = True
        search = True
        ajax_source = reverse_lazy('admissuetable_data')        


