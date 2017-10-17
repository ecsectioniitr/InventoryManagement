from models import *
from table import Table
from table.columns import *
from django.core.urlresolvers import reverse_lazy
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from table.utils import A


class IssueColumn(Column):
    def render(self, value):
        return value.eqins.filter(is_available=False, decommisioned=False).count() 


class FollowColumn(Column):
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

class ReturnColumn(Column):
    def render(self, value):
            return format_html('<input type="button" id="{}-return" name="{}" value="Return" onclick="returnequip(this.name)" />', value.id, value.id)

class ProfileColumn(Column):
    def render(self, value):
            f = value.issued_by.id
            name = value.issued_by.username
            value = reverse('main:profile', kwargs={'id':f})
            return format_html('<a target="_blank" href = "{}">{}</a>', value, name )

class ProfileColumn1(Column):
    def render(self, value):
            if not value.is_available :
                qs=value.issueance_set.filter(returned=False)
                f = qs[0].issued_by
                value = reverse('main:profile', kwargs={'id':f.id})
                return format_html('<a target="_blank" href = "{}">{}</a>', value, f.username )            

class AvailableColumn(Column):
    def render(self, value):
        return value.eqins.filter(is_available=True, decommisioned=False).count() 

class IsAvailableColumn(Column):
    def render(self, value):
        if value.is_available:
            return "Yes"
        else :
            return "No"    




class UnfollowColumn(Column):
    def render(self, value):
        return format_html('<input type="button" id="{}-unfollow" name="{}" value="Unfollow" onclick="cancelfollow(this.name)" />', value.equipment.id , value.equipment.id )          

 





class MyFollowTable(Table):
    equipment = Column(field='equipment.name', header=u'Equipment')
    created_on =DatetimeColumn(field='created_on', header=u'Followed On') 
    unfollow = UnfollowColumn(field='', header=u'Project', searchable=False, sortable=False)

    class Meta:
        model = Follow
        ajax = True
        search = True
        ajax_source = reverse_lazy('myfollowtable_data')
        sort = [(1, 'desc')]

class MyIssueanceTable(Table):
    equipmentInstance = Column(field='equipmentInstance.equipment.name', header=u'Equipment Type')
    equipmentInstanceuid =Column(field='equipmentInstance.uid', header=u'Equipment Uid') 
    project = Column(field='project.name', header=u'Project')
    issued_on = DatetimeColumn(field='issued_on', header=u'Issued On')
    year = Column(field='year', header=u'Time(weeks)')
    returned = Column(field='returned', header=u'Returned')

    class Meta:
        model = Issueance
        ajax = True
        search = True
        ajax_source = reverse_lazy('issuetable_data')
        sort = [(3, 'desc')] 

class IssueanceAdmTable(Table):
    equipmentInstance = Column(field='equipmentInstance.equipment.name', header=u'Equipment Type')
    equipmentInstanceuid =Column(field='equipmentInstance.uid', header=u'Equipment Uid') 
    project = Column(field='project.name', header=u'Project')
    issued_by = ProfileColumn(field='id', header=u'Issued By', searchable=False, sortable=False)
    issued_on = DatetimeColumn(field='issued_on', header=u'Issued On')
    year = Column(field='year', header=u'Time(weeks)')
    issue = ReturnColumn(field='id', header=u'Return', searchable=False, sortable=False)

    class Meta:
        model = Issueance
        search = True       








class EquipmentTable(Table):
    equipment = LinkColumn(header=u'Equipment', links=[Link(text=A('name'), viewname='main:instancesearch', args=(A('id'),)),])
    no_available = AvailableColumn(header=u'Available', searchable=False, sortable=False)
    follow = FollowColumn(field='id', header=u'Follow/Unfollow', searchable=False, sortable=False)
    class Meta:
        model = Equipment
        search = True 

class EquipmentAdmTable(Table):
    equipment = LinkColumn(header=u'Equipment', links=[Link(text=A('name'), viewname='main:instancesearch', args=(A('id'),)),])
    no_available = AvailableColumn(header=u'Available', searchable=False, sortable=False)
    class Meta:
        model = Equipment
        search = True  


class EquipmentInstanceTable(Table):
    uid = Column(field='uid', header=u'UID')
    remark = Column(field='remark', header=u'Remark')
    is_available = IsAvailableColumn(field='', sortable=True, header=u'Availability')
    issued_by  = ProfileColumn1( header=u'Issued By', searchable=True, sortable=True)
    
    class Meta:
        model = EquipmentInstance
        search = True
        sort = [(2, 'desc')]       





class EquipmentIssueTable(Table):
    equipment = LinkColumn(header=u'Equipment', links=[Link(text=A('name'), viewname='main:issueance', args=(A('id'),)),])
    no_available = AvailableColumn(header=u'Available', searchable=False, sortable=False)
    no_issued = IssueColumn(header=u'Issued', searchable=False, sortable=False)
    class Meta:
        model = Equipment
        search = True          


class IssueanceTable(Table):
    equipmentInstance = Column(field='equipmentInstance.equipment.name', header=u'Equipment Type')
    equipmentInstanceuid =Column(field='equipmentInstance.uid', header=u'Equipment Uid') 
    issued_by = ProfileColumn(field='id', header=u'Issued By', searchable=False, sortable=False)
    project = Column(field='project.name', header=u'Equipment')
    issued_on = DatetimeColumn(field='issued_on', header=u'Issued On')
    year = Column(field='year', header=u'Time(weeks)')

    class Meta:
        model = Issueance
        ajax = False
        search = True



     


class EquipmentInstanceAdmTable(Table):
    id = Column(field='id', header=u'id')
    equipment = Column(field='equipment.name', header=u'Equipment Type')
    uid = Column(field='uid', header=u'UID')
    remark = Column(field='remark', header=u'Remark')
    is_available = CheckboxColumn(field='is_available', sortable=True, header=u'Availability')
    issue = AdmColumn(field='id', header=u'Issue/Return', searchable=False, sortable=False)


    class Meta:
        model = EquipmentInstance
        ajax = True
        search = True
        ajax_source = reverse_lazy('admtable_data')
        sort = [(4, 'desc')]        








