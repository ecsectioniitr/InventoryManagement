from models import *
from table import Table
from table.columns import *
from django.core.urlresolvers import reverse_lazy

class EquipmentInstanceTable(Table):
	id = Column(field='id', header=u'id')
	equipment = Column(field='equipment.name', header=u'Equipment Type')
	uid = Column(field='uid', header=u'UID')
	remark = Column(field='remark', header=u'Remark')
	is_available = CheckboxColumn(field='is_available', sortable=True, header=u'Availability')


	class Meta:
		model = EquipmentInstance
		ajax = True
		search = True
		ajax_source = reverse_lazy('table_data')
		sort = [(4, 'desc')]
