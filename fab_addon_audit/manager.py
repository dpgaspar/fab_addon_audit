import logging
from flask.ext.appbuilder.basemanager import BaseManager
from .views import AuditLogView, AuditLogChartView
from flask_babelpkg import lazy_gettext as _
from .models import Operation

log = logging.getLogger(__name__)


class AuditAddOnManager(BaseManager):

    operations = ['INSERT','UPDATE','DELETE']

    def __init__(self, appbuilder):
        """
             Use the constructor to setup any config keys specific for your app. 
        """
        super(AuditAddOnManager, self).__init__(appbuilder)

    def register_views(self):
        """
            This method is called by AppBuilder when initializing, use it to add you views
        """
        self.appbuilder.add_separator("Security")
        self.appbuilder.add_view(AuditLogView, "Audit Events",icon = "fa-user-secret",category = "Security")
        self.appbuilder.add_view(AuditLogChartView, "Chart Events",icon = "fa-area-chart",category = "Security")

    def pre_process(self):
        for operation in self.operations:
            if not self.appbuilder.get_session.query(Operation).filter(Operation.name == operation).first():
                _operation = Operation(name = operation)
                self.appbuilder.get_session.add(_operation)
                self.appbuilder.get_session.commit()

    def post_process(self):
        pass

