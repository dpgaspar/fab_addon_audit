import copy
from flask import render_template, g
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder.widgets import ListLinkWidget
from flask.ext.appbuilder import ModelView
from flask.ext.appbuilder.charts.views import DirectByChartView, GroupByChartView
from flask.ext.appbuilder.models.group import aggregate_count, aggregate_avg, aggregate_sum
from .models import AuditLog, Operation


class AuditedModelView(ModelView):
    

    def update_operation(self):
        return self.appbuilder.get_session.query(Operation).filter(Operation.name == 'UPDATE').first()

    def insert_operation(self):
        return self.appbuilder.get_session.query(Operation).filter(Operation.name == 'INSERT').first()

    def delete_operation(self):
        return self.appbuilder.get_session.query(Operation).filter(Operation.name == 'DELETE').first()

    def add_log_event(self, message, operation):
        auditlog = AuditLog(message=message, username=g.user.username, operation=operation, target=self.__class__.__name__)
        try:
            self.appbuilder.get_session.add(auditlog)
            self.appbuilder.get_session.commit()
        except Exception as e:
            log.error("Unable to write audit log for post_update")
            self.appbuilder.get_session.rollback()

    def post_update(self, item):
        operation = self.update_operation()
        self.add_log_event(str(item), operation)

    def post_add(self, item):
        operation = self.insert_operation()
        self.add_log_event(str(item), operation)

    def post_delete(self, item):
        operation = self.delete_operation()
        self.add_log_event(str(item), operation)

class AuditLogView(ModelView):
    datamodel = SQLAInterface(AuditLog)
    list_widget = ListLinkWidget
    list_columns = ['created_on', 'username', 'operation.name', 'target', 'message']
    base_permissions = ['can_list','can_show']


class AuditLogChartView(GroupByChartView):
    datamodel = SQLAInterface(AuditLog)

    chart_title = 'Grouped Audit Logs'
    chart_type = 'BarChart'
    definitions = [
        {
            'group' : 'operation',
            'formatter': str,
            'series': [(aggregate_count,'operation')]
        },
        {
            'group' : 'username',
            'formatter': str,
            'series': [(aggregate_count,'username')]
        }
    ]

