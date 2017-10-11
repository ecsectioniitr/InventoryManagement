from models import *
from table import Table
from table.columns import *
from django.core.urlresolvers import reverse_lazy
from django.utils.html import format_html
from django.core.urlresolvers import reverse

class IssueColumn(Column):
    def render(self, value):
        if not value.is_available:
            value = reverse('main:request')
            return format_html('<a href = "{}">Request</a>', value)

class AdmColumn(Column):
    def render(self, value):
        if value.is_available:
            value = reverse('main:issue')
            return format_html('<a href = "{}">Issue</a>', value)
        else:
            value = reverse('main:return')
            return format_html('<a href = "{}">Return</a>', value)
                
         


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
