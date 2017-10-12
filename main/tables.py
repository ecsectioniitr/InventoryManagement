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
                
         


class EquipmentInstanceTable(Table):
    id = Column(field='id', header=u'id')
    equipment = Column(field='equipment.name', header=u'Equipment Type')
    uid = Column(field='uid', header=u'UID')
    remark = Column(field='remark', header=u'Remark')
    is_available = CheckboxColumn(field='is_available', sortable=True, header=u'Availability')
    issue = IssueColumn(field='id', header=u'Issue/Request', searchable=False, sortable=False)


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
    issue = AdmColumn(field='id', header=u'Issue/Request', searchable=False, sortable=False)


    class Meta:
        model = EquipmentInstance
        ajax = True
        search = True
        ajax_source = reverse_lazy('admtable_data')
        sort = [(4, 'desc')]        
