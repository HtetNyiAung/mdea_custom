import frappe
from frappe.model.document import Document
from frappe.utils import add_months, add_years, getdate, nowdate


class MemberSubscription(Document):
    def validate(self):
        """Validate subscription data before saving."""
        self.validate_dates()
        self.set_next_billing_date()

    def validate_dates(self):
        """Ensure end_date is after start_date."""
        if self.end_date and self.start_date:
            if getdate(self.end_date) < getdate(self.start_date):
                frappe.throw("End Date cannot be before Start Date.")

    def set_next_billing_date(self):
        """Auto-calculate next billing date based on billing cycle."""
        if self.start_date and self.status == "Active":
            if self.billing_cycle == "Monthly":
                self.next_billing_date = add_months(self.start_date, 1)
            elif self.billing_cycle == "Quarterly":
                self.next_billing_date = add_months(self.start_date, 3)
            elif self.billing_cycle == "Yearly":
                self.next_billing_date = add_years(self.start_date, 1)

    def on_submit(self):
        pass

    def before_save(self):
        """Auto-expire if past end date."""
        if self.end_date and self.status == "Active":
            if getdate(self.end_date) < getdate(nowdate()):
                self.status = "Expired"
                frappe.msgprint(
                    f"Subscription {self.name} has been marked as Expired (past end date).",
                    indicator="orange",
                )

    def after_insert(self):
        """Notify after new subscription is created."""
        frappe.msgprint(
            f"Subscription <b>{self.name}</b> created for member <b>{self.member}</b>.",
            title="Subscription Created",
            indicator="green",
        )
