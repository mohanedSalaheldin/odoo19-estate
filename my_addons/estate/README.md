# 🏡 Odoo Real Estate Module (`estate`)

[![Odoo Version](https://img.shields.io/badge/Odoo-19.0-875A7B?style=flat-square&logo=odoo&logoColor=white)](https://www.odoo.com/)
[![License](https://img.shields.io/badge/License-LGPL--3-blue.svg?style=flat-square)](https://www.gnu.org/licenses/lgpl-3.0)

A custom Odoo module designed to manage real estate property listings, pricing rules, offer negotiations, and sales workflows.

---

## 🚀 Key Highlights

- **Custom Models**: `real.estate`, `estate.offer`, `estate.property.type`, `property.tag`
- **Dynamic Computations**: Automated calculation of best offer, total area, and offer expiration deadline.
- **Constraints & Validations**: 
  - SQL constraints on prices (`expected_price > 0`, `selling_price >= 0`).
  - Python business constraints ensuring selling price is at least 90% of expected price.
  - Unique constraints on property types and tags.
- **UI Components**: Interactive statusbar, custom notebook tabs, search filters, and action buttons.
- **Security & ACL**: Group-based permissions (`Estate Manager` vs standard users).

---

## 📂 Structure

```text
estate/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── estate_offer.py
│   ├── estate_property_type.py
│   ├── models.py
│   └── property_tag.py
├── security/
│   ├── ir.model.access.csv
│   └── res_groups.xml
└── views/
    ├── estate_menus.xml
    ├── estate_offer_views.xml
    ├── estate_property_views.xml
    ├── property_tag_views.xml
    └── property_type_views.xml
```

---

## 🛠️ Usage
Add `my_addons` to your Odoo configuration file (`odoo.conf`) under `addons_path`, update the apps list in developer mode, and install `estate`.
