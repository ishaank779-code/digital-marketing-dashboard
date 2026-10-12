# Digital Marketing Analytics Dashboard

A complete, full-stack **Digital Marketing Analytics Dashboard** built with **Python (Flask)** + **MySQL**.

Inspired by modern marketing analytics UIs, this project provides real-time style campaign performance tracking, interactive charts, filtering, detailed campaign views, reports, and CSV export.

## Features

- **Dashboard Overview**
  - KPI cards: Conversions, Clicks, Cost per Click (CPC), ROI
  - Interactive charts (Chart.js): Trend (Clicks + Conversions), Platform distribution, Donuts, Cost & ROI
  - Filter by Campaign and Date range (7/14/30/60 days)
  - Quick view of active campaigns

- **Campaigns**
  - List all campaigns with status filter (Active / Paused / Completed)
  - Toggle Active ↔ Paused
  - Budget progress bars
  - Direct links to landing pages (including Uncodemy courses)

- **Campaign Detail**
  - Full performance metrics
  - Daily trend charts
  - Daily metrics table
  - Link to original course/landing page

- **Reports**
  - Summary table of all campaigns
  - Budget utilization
  - One-click CSV export

- **Working Navigation**
  - Every menu item, filter, button, and link is functional
  - Responsive design (mobile-friendly sidebar)

## Tech Stack

| Layer     | Technology              |
|-----------|-------------------------|
| Backend   | Python 3, Flask         |
| Database  | MySQL 8                 |
| ORM       | Flask-SQLAlchemy + PyMySQL |
| Frontend  | Bootstrap 5, Chart.js, custom CSS |
| Charts    | Chart.js 4              |

## Sample Data

Two real Uncodemy courses are included as campaigns:

1. **Digital Marketing Training - Noida**  
   → https://uncodemy.com/course/digital-marketing-training-course-in-noida

2. **Machine Learning Training - Delhi**  
   → https://uncodemy.com/course/machine-learning-training-course-in-delhi

Plus two additional demo campaigns with realistic daily metrics (clicks, conversions, cost, impressions) for the last 45–60 days.

## Project Structure

```
digital-marketing-dashboard/
├── app/
│   ├── __init__.py          # App factory
│   ├── models.py            # Campaign & DailyMetric models
│   ├── routes.py            # All routes & API endpoints
│   ├── templates/           # Jinja2 templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── campaigns.html
│   │   ├── campaign_detail.html
│   │   └── reports.html
│   └── static/
│       └── css/style.css
├── run.py                   # Entry point + seed data
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Prerequisites

- Python 3.10+
- MySQL 8.x running
- pip

### 2. Create Database & User

```sql
CREATE DATABASE marketing_dashboard CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'dashboard'@'localhost' IDENTIFIED BY 'dashboard123';
GRANT ALL PRIVILEGES ON marketing_dashboard.* TO 'dashboard'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Install Dependencies

```bash
cd digital-marketing-dashboard
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python run.py
```

This will:
- Create all tables
- Seed sample campaigns + daily metrics (only if empty)
- Start the server at **http://0.0.0.0:5000**

Open your browser: **http://localhost:5000**

## Configuration

Database URI is set in `app/__init__.py`:

```python
'mysql+pymysql://dashboard:dashboard123@localhost/marketing_dashboard'
```

Change username/password/host as needed.

## API Endpoints (JSON)

- `GET /api/overview?days=30` – Aggregate KPIs
- `GET /api/metrics/<campaign_id>?days=30` – Daily metrics for a campaign

## Screenshots / UI Feel

- Dark sidebar with logo
- Clean white content area
- KPI cards with icons
- Multiple interactive charts
- Campaign cards with status badges and budget bars
- Fully clickable navigation and filters

## License

MIT – free to use and modify.

---

Built as a complete working project ready for GitHub.
