from app import create_app, db
from app.models import Campaign, DailyMetric
from datetime import datetime, timedelta
import random

app = create_app()

def seed_data():
    """Seed sample campaigns and metrics if DB is empty."""
    with app.app_context():
        if Campaign.query.count() > 0:
            return

        campaigns = [
            Campaign(
                name="Digital Marketing Training - Noida",
                description="Comprehensive digital marketing training course covering SEO, SEM, Social Media Marketing, Content Marketing, Email Marketing and Analytics. Hands-on training with live projects.",
                url="https://uncodemy.com/course/digital-marketing-training-course-in-noida",
                budget=25000.00,
                start_date=datetime.now().date() - timedelta(days=45),
                end_date=datetime.now().date() + timedelta(days=15),
                status="active",
                target_audience="Aspiring digital marketers, entrepreneurs, students in Noida/Delhi NCR",
                platform="Google Ads + Meta Ads + LinkedIn"
            ),
            Campaign(
                name="Machine Learning Training - Delhi",
                description="Industry-ready Machine Learning course covering Python, Statistics, Supervised & Unsupervised Learning, Deep Learning, NLP and real-world projects. Placement assistance included.",
                url="https://uncodemy.com/course/machine-learning-training-course-in-delhi",
                budget=35000.00,
                start_date=datetime.now().date() - timedelta(days=60),
                end_date=datetime.now().date() + timedelta(days=30),
                status="active",
                target_audience="Software engineers, data enthusiasts, students looking for ML careers in Delhi",
                platform="Google Ads + YouTube + LinkedIn"
            ),
            Campaign(
                name="Full Stack Web Development - Weekend",
                description="Weekend batch for Full Stack Development with MERN stack. Ideal for working professionals.",
                url="https://uncodemy.com/",
                budget=18000.00,
                start_date=datetime.now().date() - timedelta(days=20),
                end_date=datetime.now().date() + timedelta(days=40),
                status="active",
                target_audience="Working professionals, career switchers",
                platform="Meta Ads + Google Ads"
            ),
            Campaign(
                name="Data Science Bootcamp - Online",
                description="Intensive online Data Science bootcamp with Python, SQL, Tableau, ML and Capstone project.",
                url="https://uncodemy.com/",
                budget=22000.00,
                start_date=datetime.now().date() - timedelta(days=90),
                end_date=datetime.now().date() - timedelta(days=5),
                status="completed",
                target_audience="Graduates and professionals seeking data science roles",
                platform="Google Ads + Email + Webinars"
            ),
        ]

        for c in campaigns:
            db.session.add(c)
        db.session.commit()

        # Generate daily metrics for last 60 days
        for campaign in Campaign.query.all():
            days = 60 if campaign.status == "completed" else 45
            base_clicks = random.randint(200, 500)
            base_conv = random.randint(8, 25)
            base_cost = random.uniform(0.15, 0.45)

            for i in range(days):
                day = datetime.now().date() - timedelta(days=days - i)
                # Some variation + weekly pattern
                factor = 1 + 0.3 * random.random() + 0.2 * (1 if day.weekday() < 5 else 0.6)
                clicks = int(base_clicks * factor + random.randint(-50, 80))
                conversions = max(1, int(base_conv * factor * random.uniform(0.7, 1.3)))
                cpc = round(base_cost * random.uniform(0.85, 1.2), 2)
                cost = round(clicks * cpc, 2)
                impressions = clicks * random.randint(8, 18)

                metric = DailyMetric(
                    campaign_id=campaign.id,
                    date=day,
                    clicks=clicks,
                    conversions=conversions,
                    cost=cost,
                    impressions=impressions,
                    cpc=cpc
                )
                db.session.add(metric)

        db.session.commit()
        print("Database seeded successfully with sample campaigns and metrics.")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_data()
app.run(host="0.0.0.0", port=5001, debug=True)
