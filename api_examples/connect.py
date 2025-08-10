import os

from dotenv import load_dotenv
import odoorpc

load_dotenv()


def connect_to_odoo() -> odoorpc.ODOO:
    """Establish connection to Odoo"""
    odoo = odoorpc.ODOO(
        os.getenv("ODOO_HOST", "localhost"),
        port=int(os.getenv("ODOO_PORT", 8069)),
    )
    odoo.login(
        os.getenv("ODOO_DB", "odoo"),
        os.getenv("ODOO_USER", "admin"),
        os.getenv("ODOO_PASSWORD", "admin"),
    )
    return odoo
