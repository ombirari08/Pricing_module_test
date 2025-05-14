# Django Pricing Configuration Module

This project is a Django web application for configuring, calculating, modifying, and deleting dynamic pricing based on parameters like distance, time, waiting period, and day of the week — all through a responsive web interface.

---

## Features

- Add pricing configurations for each day of the week
- Modify or delete existing configurations
- Form-based price calculation (no API required)
- Prevents multiple active configurations for the same day
- User-friendly Bootstrap forms
- Log actions (Create, Update, Delete) via `PricingConfigLog`
- Admin panel to manage pricing models and logs

---

## Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** MYSQL
- **Admin Panel:** Django admin

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/pricing-config-django.git
cd Pricing_module_test
