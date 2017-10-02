from models import *
from table import Table
from table.columns import Column

class EquipmentInstanceTable(Table):
	id = Column(field='id')
	equipment = Column(field='equipment')
	uid = Column(field='uid')
	remark = Column(field='remark')
	is_available = Column(field='is_available', header=u'Avalability')
	decommisioned = Column(field='decommisioned', header=u'decommisioned')


	class Meta:
		model = EquipmentInstance
		ajax = True
		search = True