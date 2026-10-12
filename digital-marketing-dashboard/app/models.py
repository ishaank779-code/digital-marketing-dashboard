from app import db
from datetime import datetime

class Campaign(db.Model):
    __tablename__ = 'campaigns'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(500))
    budget = db.Column(db.Float, default=0.0)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='active')  # active, paused, completed
    target_audience = db.Column(db.String(300))
    platform = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    metrics = db.relationship('DailyMetric', backref='campaign', lazy='dynamic', cascade='all, delete-orphan')

    def total_clicks(self):
        return sum(m.clicks for m in self.metrics) or 0

    def total_conversions(self):
        return sum(m.conversions for m in self.metrics) or 0

    def total_cost(self):
        return round(sum(m.cost for m in self.metrics) or 0, 2)

    def total_impressions(self):
        return sum(m.impressions for m in self.metrics) or 0

    def avg_cpc(self):
        clicks = self.total_clicks()
        if clicks == 0:
            return 0.0
        return round(self.total_cost() / clicks, 2)

    def conversion_rate(self):
        clicks = self.total_clicks()
        if clicks == 0:
            return 0.0
        return round((self.total_conversions() / clicks) * 100, 2)

    def roi(self):
        # Simplified ROI: assume each conversion worth ~ average course value relative to cost
        # For demo: value per conversion ~ 800-1500 depending on campaign
        value_per_conv = 1200 if "Machine Learning" in self.name else 900
        revenue = self.total_conversions() * value_per_conv
        cost = self.total_cost()
        if cost == 0:
            return 0.0
        return round(((revenue - cost) / cost) * 100, 1)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'url': self.url,
            'budget': self.budget,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'target_audience': self.target_audience,
            'platform': self.platform,
            'total_clicks': self.total_clicks(),
            'total_conversions': self.total_conversions(),
            'total_cost': self.total_cost(),
            'avg_cpc': self.avg_cpc(),
            'conversion_rate': self.conversion_rate(),
            'roi': self.roi(),
        }


class DailyMetric(db.Model):
    __tablename__ = 'daily_metrics'

    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    clicks = db.Column(db.Integer, default=0)
    conversions = db.Column(db.Integer, default=0)
    cost = db.Column(db.Float, default=0.0)
    impressions = db.Column(db.Integer, default=0)
    cpc = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {
            'date': self.date.isoformat(),
            'clicks': self.clicks,
            'conversions': self.conversions,
            'cost': self.cost,
            'impressions': self.impressions,
            'cpc': self.cpc,
        }
