from models import *
from table import Table
from table.columns import *

class EquipmentInstanceTable(Table):
	id = Column(field='id', header=u'id')
	equipment = Column(field='equipment.name', header=u'Equipment Type')
	uid = Column(field='uid', header=u'UID')
	remark = Column(field='remark', header=u'Remark')
	is_available = CheckboxColumn(field='is_available', header=u'Availability')
	decommisioned = CheckboxColumn(field='decommisioned', header=u'Decommisioned')


	class Meta:
		model = EquipmentInstance
		ajax = True
		search = True
