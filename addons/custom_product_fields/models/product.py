from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    brand = fields.Char(
        string="Brand",
        help="Product brand or manufacturer",
    )
    warranty_months = fields.Integer(
        string="Warranty (Months)",
        help="Number of warranty months",
        default=12,
    )
    warranty_description = fields.Text(
        string="Warranty Description",
        help="Detailed warranty information",
    )

    @api.depends("brand", "name")
    def _compute_display_name(self) -> None:
        """Override display name to include brand"""
        for record in self:
            name = record.name or ""
            if record.brand:
                name: str = f"[{record.brand}] {name}"
            record.display_name = name


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.depends("product_tmpl_id.brand", "name")
    def _compute_display_name(self) -> None:
        """Override display name to include brand"""
        for record in self:
            name = record.name or ""
            if record.product_tmpl_id.brand:
                name: str = f"[{record.product_tmpl_id.brand}] {name}"
            record.display_name = name
