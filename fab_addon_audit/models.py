import datetime
from flask.ext.appbuilder import Model
from flask.ext.appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy import event


class Operation(Model):
    id = Column(Integer, Sequence('audit_log_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return self.name

class AuditLog(Model):
    id = Column(Integer, Sequence('audit_log_id_seq'), primary_key=True)
    message = Column(String(300), nullable=False)
    username = Column(String(64),  nullable=False)
    created_on = Column(DateTime, default=datetime.datetime.now, nullable=True)
    operation_id = Column(Integer, ForeignKey('operation.id'), nullable=False)
    operation = relationship("Operation")
    target = Column(String(150), nullable=False)


