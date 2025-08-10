{
    "name": "Custom Product Fields",
    "version": "1.0.0",
    "category": "Sales",
    "summary": "Adds brand and warranty fields to products",
    "description": """
        This module extends the product model with additional fields:
        - Brand: Manufacturer or brand name
        - Warranty Months: Number of warranty months
    """,
    "author": "Tyrone Jose",
    "depends": ["base", "product", "website_sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_views.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
}
