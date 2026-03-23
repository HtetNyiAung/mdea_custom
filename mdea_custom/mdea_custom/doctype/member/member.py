import frappe
from frappe.model.document import Document


class Member(Document):
    def before_save(self):
        """Validate and clean data before saving."""
        if self.full_name:
            self.full_name = self.full_name.strip().title()

    def after_insert(self):
        """Called after a new Member is created."""
        frappe.msgprint(
            f"Welcome! Member <b>{self.full_name}</b> (ID: {self.name}) has been created.",
            title="Member Created",
            indicator="green",
        )

    def on_update(self):
        """Called every time the document is saved/updated."""
        pass

    @frappe.whitelist()
    def get_active_subscriptions(self):
        """Return all active subscriptions for this member."""
        return frappe.get_all(
            "Member Subscription",
            filters={"member": self.name, "status": "Active"},
            fields=["name", "plan_name", "start_date", "end_date", "amount"],
        )
