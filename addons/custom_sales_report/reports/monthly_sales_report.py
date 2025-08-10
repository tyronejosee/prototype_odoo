from odoo import models, fields, api


class MonthlySalesReport(models.TransientModel):
    _name = "monthly.sales.report"
    _description = "Monthly Sales Report"

    date_from = fields.Date("From Date", required=True)
    date_to = fields.Date("To Date", required=True)

    @api.model
    def get_sales_data(self, date_from, date_to) -> dict:
        """Get sales data for the specified period"""
        domain = [
            ("state", "=", "sale"),
            ("date_order", ">=", date_from),
            ("date_order", "<=", date_to),
        ]

        orders = self.env["sale.order"].search(domain)

        # Calculate totals
        total_orders = len(orders)
        total_revenue = sum(orders.mapped("amount_total"))

        # Group by product
        product_sales = {}
        for order in orders:
            for line in order.order_line:
                product_name = line.product_id.name
                if product_name in product_sales:
                    product_sales[product_name]["qty"] += line.product_uom_qty
                    product_sales[product_name]["amount"] += line.price_subtotal
                else:
                    product_sales[product_name] = {
                        "qty": line.product_uom_qty,
                        "amount": line.price_subtotal,
                        "brand": line.product_id.brand or "N/A",
                    }

        # Sort by amount
        top_products: list[tuple] = sorted(
            product_sales.items(), key=lambda x: x[1]["amount"], reverse=True
        )[:10]

        return {
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "top_products": top_products,
            "date_from": date_from,
            "date_to": date_to,
        }
