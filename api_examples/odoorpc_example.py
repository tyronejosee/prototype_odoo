#!/usr/bin/env python3
"""
Odoo RPC API Examples
Demonstrates how to use the Odoo RPC API to perform common tasks.
"""

from datetime import datetime
import logging

import odoorpc

from .connect import connect_to_odoo


def create_customer(
    odoo: odoorpc.ODOO,
    name: str,
    email: str,
    phone: str | None = None,
) -> int:
    """Create a new customer"""
    customer_data = {
        "name": name,
        "email": email,
        "is_company": False,
        "customer_rank": 1,
    }
    if phone:
        customer_data["phone"] = phone

    customer_id = odoo.env["res.partner"].create(customer_data)
    logging.info(f"Customer created with ID: {customer_id}")
    return customer_id


def create_product(
    odoo: odoorpc.ODOO,
    name: str,
    price: float,
    brand: str | None = None,
    warranty_months: int = 12,
) -> int:
    """Create a new product"""
    product_data = {
        "name": name,
        "list_price": price,
        "type": "product",
        "website_published": True,
    }

    if brand:
        if "brand" in odoo.env["product.template"].fields_get():
            product_data["brand"] = brand
        else:
            logging.warning(
                "Warning: field 'brand' does not exist in product.template, skipping",
            )

    if warranty_months:
        if "warranty_months" in odoo.env["product.template"].fields_get():
            product_data["warranty_months"] = warranty_months
        else:
            logging.warning(
                "Warning: field 'warranty_months' does not exist in product.template, skipping",
            )

    product_id = odoo.env["product.template"].create(product_data)
    logging.info(f"Product created with ID: {product_id}")
    return product_id


def create_sale_order(
    odoo: odoorpc.ODOO,
    customer_id: int,
    product_lines: list,
) -> int:
    """
    Create a sale order
    product_lines: list of dicts with 'product_id' and 'quantity'
    """
    order_data = {
        "partner_id": customer_id,
        "state": "draft",
    }
    order_id = odoo.env["sale.order"].create(order_data)

    # Add order lines
    lines_data = []
    for line in product_lines:
        lines_data.append(
            {
                "order_id": order_id,
                "product_id": line["product_id"],
                "product_uom_qty": line["quantity"],
            }
        )
    odoo.env["sale.order.line"].create(lines_data)

    order = odoo.env["sale.order"].browse(order_id)
    try:
        order.action_confirm()
    except Exception as e:
        logging.error(f"Error confirmando pedido: {e}")

    logging.info(f"Sale order created and confirmed with ID: {order_id}")
    return order_id


def get_sales_report(
    odoo: odoorpc.ODOO,
    date_from: str | None = None,
    date_to: str | None = None,
) -> list:
    if not date_from:
        date_from = datetime.now().replace(day=1).strftime("%Y-%m-%d")
    if not date_to:
        date_to = datetime.now().strftime("%Y-%m-%d")

    domain = [
        ("state", "=", "sale"),
        ("date_order", ">=", date_from),
        ("date_order", "<=", date_to),
    ]

    orders = odoo.env["sale.order"].search_read(
        domain, ["name", "partner_id", "date_order", "amount_total"]
    )
    total_revenue = sum(order["amount_total"] for order in orders)

    logging.info(f"Sales Report ({date_from} to {date_to}):")
    logging.info(f"Total Orders: {len(orders)}")
    logging.info(f"Total Revenue: ${total_revenue:,.2f}")

    for order in orders[-5:]:
        logging.info(f"  {order['name']}: ${order['amount_total']:,.2f}")

    return orders


def main() -> None:
    try:
        odoo = connect_to_odoo()
        logging.info("Connected to Odoo successfully")

        customer_id = create_customer(
            odoo, "John Doe API", "john.api@example.com", "+1-555-0123"
        )
        product_id = create_product(
            odoo,
            "API Test Product",
            99.99,
            brand="TechCorp",
            warranty_months=24,
        )

        product_template = odoo.env["product.template"].browse(product_id)
        if product_template.product_variant_ids:
            product_variant_id = product_template.product_variant_ids[0].id
        else:
            logging.error(
                "Product does not have variants, aborting order creation",
            )
            return

        _ = create_sale_order(
            odoo,
            customer_id,
            [{"product_id": product_variant_id, "quantity": 2}],
        )
        get_sales_report(odoo)

        logging.info("API examples completed successfully")

    except Exception as e:
        logging.error(f"Error: {e}")


if __name__ == "__main__":
    main()
