{
    "name": "Custom Sales Report",
    "version": "1.0.0",
    "category": "Sales",
    "summary": "Custom monthly sales reports",
    "description": """
        Custom sales reporting module with:
        - Monthly sales summary
        - Product performance analysis
        - Customer insights
    """,
    "author": "Tyrone Jose",
    "depends": ["base", "sale", "product"],
    "data": [
        "wizard/sales_report_wizard_view.xml",
        "reports/monthly_sales_template.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
}
