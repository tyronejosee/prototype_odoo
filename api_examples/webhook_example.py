#!/usr/bin/env python3
"""
Webhook Integration Example
Simulates a payment gateway webhook integration
"""

import logging

from flask import Flask, request, jsonify, Response

from .connect import connect_to_odoo

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/webhook/payment", methods=["POST"])
def handle_payment_webhook() -> tuple[Response, int]:
    """Handle incoming payment webhook"""
    try:
        data = request.get_json()

        # Extract payment information
        order_reference = data.get("order_reference")
        payment_status = data.get("status")  # 'completed', 'failed', 'pending'
        payment_amount = data.get("amount")
        transaction_id = data.get("transaction_id")

        logging.info(
            f"Received payment webhook: {order_reference} - {payment_status}",
        )

        # Connect to Odoo
        odoo = connect_to_odoo()

        # Find the sale order
        orders = odoo.env["sale.order"].search(
            [("name", "=", order_reference)],
        )

        if not orders:
            logging.error(f"Order not found: {order_reference}")
            return (
                jsonify({"status": "error", "message": "Order not found"}),
                404,
            )
        communication_msg = f"Payment for {order_reference} - {transaction_id}"
        order = odoo.env["sale.order"].browse(orders[0])

        if payment_status == "completed":
            # Create payment record
            payment_vals = {
                "payment_type": "inbound",
                "partner_type": "customer",
                "partner_id": order.partner_id.id,
                "amount": payment_amount,
                "currency_id": order.currency_id.id,
                "payment_method_id": 1,  # Manual payment method
                "journal_id": 1,  # Default journal
                "communication": communication_msg,
            }

            payment = odoo.env["account.payment"].create(payment_vals)
            payment.action_post()

            # Add note to sale order
            body = f"Payment conf via webhook. TX_ID: {transaction_id}"
            order.message_post(body=body, message_type="comment")

            logging.info(f"Payment recorded for order {order_reference}")

        elif payment_status == "failed":
            # Add failure note
            order.message_post(
                body=f"Payment failed. Transaction ID: {transaction_id}",
                message_type="comment",
            )
            logging.info(f"Payment failed for order {order_reference}")

        return jsonify({"status": "success"}), 200

    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/orders", methods=["GET"])
def get_orders() -> tuple[Response, int]:
    """API endpoint to get orders"""
    try:
        odoo = connect_to_odoo()

        # Get recent orders
        orders = odoo.env["sale.order"].search_read(
            [("state", "=", "sale")],
            ["name", "partner_id", "date_order", "amount_total"],
            limit=10,
        )

        return jsonify({"orders": orders}), 200

    except Exception as e:
        logging.error(f"API error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/products", methods=["POST"])
def create_product_api() -> tuple[Response, int]:
    """API endpoint to create products"""
    try:
        data = request.get_json()
        odoo = connect_to_odoo()

        product_data = {
            "name": data.get("name"),
            "list_price": data.get("price", 0),
            "type": "product",
            "website_published": data.get("published", True),
        }

        if data.get("brand"):
            product_data["brand"] = data["brand"]

        if data.get("warranty_months"):
            product_data["warranty_months"] = data["warranty_months"]

        product_id = odoo.env["product.template"].create(product_data)

        return jsonify({"status": "success", "product_id": product_id}), 201

    except Exception as e:
        logging.error(f"Product creation error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    logging.info("🚀 Starting webhook server...")
    logging.info("Endpoints:")
    logging.info("  POST /webhook/payment - Payment webhook")
    logging.info("  GET  /api/orders - Get orders")
    logging.info("  POST /api/products - Create product")

    app.run(host="0.0.0.0", port=5000, debug=True)
