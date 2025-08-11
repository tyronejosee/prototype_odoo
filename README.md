<div align="center">
  <a href="https://github.com/tyronejosee/marketly" target="_blank">
    <img src="logo.svg" alt="logo" width="80">
  </a>
</div>
<div align="center">
  <h1><strong>Prototype Odoo</strong></h1>
</div>
<br>
<p align="center">
Complete, functional Odoo 17 eCommerce environment with critical modules, custom extensions, and API integration examples.
<p>
<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/python-3.12-blue" alt="python-version">
  </a>
  <a href="https://flask.palletsprojects.com/en/stable/">
    <img src="https://img.shields.io/badge/flask-2.3.3-black" alt="flask-version">
  </a>
  <a href="https://hub.docker.com/_/odoo">
    <img src="https://img.shields.io/badge/odoo-18.0-875A7B" alt="odoo-version">
  </a>
</p>

## 📁 Project Structure

```bash
prototype_odoo/
├── docker-compose.yml
├── config/
│   └── odoo.conf
├── addons/
│   ├── custom_product_fields/
│   │   ├── __manifest__.py
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── product.py
│   │   ├── views/
│   │   │   └── product_views.xml
│   │   └── security/
│   │       └── ir.model.access.csv
│   └── custom_sales_report/
│       ├── __manifest__.py
│       ├── __init__.py
│       ├── reports/
│       │   ├── __init__.py
│       │   ├── monthly_sales_report.py
│       │   └── monthly_sales_template.xml
│       └── wizard/
│           ├── __init__.py
│           ├── sales_report_wizard.py
│           └── sales_report_wizard_view.xml
├── api_examples/
│   ├── odoorpc_example.py
│   ├── webhook_example.py
│   └── requirements.txt
└── README.md
```

## 📋 Prerequisites

- Docker and Docker Compose installed
- Python 3.12+ (for API examples)
- 4GB+ RAM available for containers

## 🚀 Quick Start

Start Odoo and PostgreSQL

```bash
docker-compose up -d
```

Wait for services to be ready (about 2-3 minutes)

```bash
docker-compose logs -f odoo
```

Access the System

- **Frontend (Website)**: <http://localhost:8069>
- **Backend (Admin)**: <http://localhost:8069/web>
  - Email: `admin`
  - Password: `admin`

Verify modules are installed

- Go to Apps menu
- Check that "Custom Product Fields" and "Custom Sales Report" are installed

Configure demo data

- Go to Products menu
- Edit existing products to add brand and warranty information
- Go to Website > eCommerce to see the frontend

## ⚖️ License

This project is under the [MIT License](LICENSE).

Enjoy! 🎉
