from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app.models import Campaign, DailyMetric
from app import db
from datetime import datetime, timedelta
from sqlalchemy import func

main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    campaign_id = request.args.get('campaign_id', type=int)
    days = request.args.get('days', 30, type=int)

    campaigns = Campaign.query.order_by(Campaign.status.desc(), Campaign.name).all()

    if campaign_id:
        selected = Campaign.query.get_or_404(campaign_id)
        metrics_query = selected.metrics
    else:
        selected = None
        metrics_query = DailyMetric.query

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    metrics = metrics_query.filter(
        DailyMetric.date >= start_date,
        DailyMetric.date <= end_date
    ).order_by(DailyMetric.date).all()

    # Aggregate KPIs
    total_clicks = sum(m.clicks for m in metrics)
    total_conversions = sum(m.conversions for m in metrics)
    total_cost = round(sum(m.cost for m in metrics), 2)
    total_impressions = sum(m.impressions for m in metrics)
    avg_cpc = round(total_cost / total_clicks, 2) if total_clicks else 0
    conv_rate = round((total_conversions / total_clicks) * 100, 2) if total_clicks else 0

    # Simple ROI estimation
    value_per_conv = 1100
    revenue = total_conversions * value_per_conv
    roi = round(((revenue - total_cost) / total_cost) * 100, 1) if total_cost else 0

    # Chart data: group by date
    date_map = {}
    for m in metrics:
        d = m.date.isoformat()
        if d not in date_map:
            date_map[d] = {'clicks': 0, 'conversions': 0, 'cost': 0, 'impressions': 0}
        date_map[d]['clicks'] += m.clicks
        date_map[d]['conversions'] += m.conversions
        date_map[d]['cost'] += m.cost
        date_map[d]['impressions'] += m.impressions

    sorted_dates = sorted(date_map.keys())
    chart_labels = sorted_dates
    chart_clicks = [date_map[d]['clicks'] for d in sorted_dates]
    chart_conversions = [date_map[d]['conversions'] for d in sorted_dates]
    chart_cost = [round(date_map[d]['cost'], 2) for d in sorted_dates]
    chart_roi_proxy = []
    for d in sorted_dates:
        c = date_map[d]['cost']
        conv = date_map[d]['conversions']
        if c > 0:
            chart_roi_proxy.append(round(((conv * value_per_conv - c) / c) * 100, 1))
        else:
            chart_roi_proxy.append(0)

    # Platform / source breakdown (simulated from campaigns)
    platforms = {}
    for c in campaigns:
        p = c.platform or "Other"
        for part in p.split('+'):
            part = part.strip()
            if part not in platforms:
                platforms[part] = 0
            platforms[part] += c.total_clicks() // 3  # distribute

    return render_template(
        'dashboard.html',
        campaigns=campaigns,
        selected=selected,
        days=days,
        total_clicks=total_clicks,
        total_conversions=total_conversions,
        total_cost=total_cost,
        total_impressions=total_impressions,
        avg_cpc=avg_cpc,
        conv_rate=conv_rate,
        roi=roi,
        chart_labels=chart_labels,
        chart_clicks=chart_clicks,
        chart_conversions=chart_conversions,
        chart_cost=chart_cost,
        chart_roi=chart_roi_proxy,
        platforms=platforms
    )


@main.route('/campaigns')
def campaigns_list():
    status_filter = request.args.get('status', 'all')
    query = Campaign.query
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    campaigns = query.order_by(Campaign.created_at.desc()).all()
    return render_template('campaigns.html', campaigns=campaigns, status_filter=status_filter)


@main.route('/campaign/<int:campaign_id>')
def campaign_detail(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    days = request.args.get('days', 30, type=int)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    metrics = campaign.metrics.filter(
        DailyMetric.date >= start_date,
        DailyMetric.date <= end_date
    ).order_by(DailyMetric.date).all()

    chart_labels = [m.date.isoformat() for m in metrics]
    chart_clicks = [m.clicks for m in metrics]
    chart_conversions = [m.conversions for m in metrics]
    chart_cost = [m.cost for m in metrics]
    chart_cpc = [m.cpc for m in metrics]

    return render_template(
        'campaign_detail.html',
        campaign=campaign,
        metrics=metrics,
        days=days,
        chart_labels=chart_labels,
        chart_clicks=chart_clicks,
        chart_conversions=chart_conversions,
        chart_cost=chart_cost,
        chart_cpc=chart_cpc
    )


@main.route('/reports')
def reports():
    campaigns = Campaign.query.all()
    # Summary table data
    summary = []
    for c in campaigns:
        summary.append({
            'campaign': c,
            'clicks': c.total_clicks(),
            'conversions': c.total_conversions(),
            'cost': c.total_cost(),
            'cpc': c.avg_cpc(),
            'conv_rate': c.conversion_rate(),
            'roi': c.roi(),
            'budget_used': round((c.total_cost() / c.budget * 100) if c.budget else 0, 1)
        })
    return render_template('reports.html', summary=summary, campaigns=campaigns)


@main.route('/api/metrics/<int:campaign_id>')
def api_metrics(campaign_id):
    days = request.args.get('days', 30, type=int)
    campaign = Campaign.query.get_or_404(campaign_id)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    metrics = campaign.metrics.filter(
        DailyMetric.date >= start_date
    ).order_by(DailyMetric.date).all()
    return jsonify([m.to_dict() for m in metrics])


@main.route('/api/overview')
def api_overview():
    days = request.args.get('days', 30, type=int)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    metrics = DailyMetric.query.filter(DailyMetric.date >= start_date).all()
    return jsonify({
        'clicks': sum(m.clicks for m in metrics),
        'conversions': sum(m.conversions for m in metrics),
        'cost': round(sum(m.cost for m in metrics), 2),
    })


@main.route('/export/csv')
def export_csv():
    """Simple CSV export of campaign summary."""
    from flask import Response
    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Campaign', 'Status', 'Clicks', 'Conversions', 'Cost ($)', 'Avg CPC', 'Conv Rate %', 'ROI %', 'URL'])

    for c in Campaign.query.all():
        writer.writerow([
            c.name, c.status, c.total_clicks(), c.total_conversions(),
            c.total_cost(), c.avg_cpc(), c.conversion_rate(), c.roi(), c.url or ''
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=campaign_report.csv'}
    )


@main.route('/toggle-status/<int:campaign_id>', methods=['POST'])
def toggle_status(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.status == 'active':
        campaign.status = 'paused'
    elif campaign.status == 'paused':
        campaign.status = 'active'
    # completed stays completed
    db.session.commit()
    flash(f'Campaign "{campaign.name}" is now {campaign.status}.', 'success')
    return redirect(request.referrer or url_for('main.campaigns_list'))
