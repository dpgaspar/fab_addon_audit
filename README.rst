F.A.B. AddOn for Auditing 
-------------------------

Will add audit views to F.A.B's security menu. Enables audit for insert, update and delete operations
on any ModelView you choose.

- Install it::

	pip install fab_addon_audit

- Use it:

On your application change your views.py file to import::


    from fab_addon_audit.views import AuditedModelView


Then subclass the ModelView's you want to audit from AuditedModelView::



    class ContactModelView(AuditedModelView):
        datamodel = SQLAInterface(Contact)
