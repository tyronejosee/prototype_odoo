from odoo import models, fields


class SalesReportWizard(models.TransientModel):
    _name = "sales.report.wizard"
    _description = "Sales Report Wizard"

    date_from = fields.Date(
        "From Date",
        required=True,
        default=fields.Date.today().replace(day=1),
    )
    date_to = fields.Date(
        "To Date",
        required=True,
        default=fields.Date.today(),
    )

    def generate_report(self) -> dict:
        """Generate the sales report"""
        report = self.env["monthly.sales.report"].create(
            {
                "date_from": self.date_from,
                "date_to": self.date_to,
            }
        )

        data = report.get_sales_data(self.date_from, self.date_to)

        return {
            "type": "ir.actions.report",
            "report_name": "custom_sales_report.monthly_sales_report_template",
            "report_type": "qweb-pdf",
            "data": data,
            "context": self.env.context,
        }
