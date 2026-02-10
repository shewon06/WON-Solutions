from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, CompanyMaster, Director, Shareholder
from datetime import datetime

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def manage_settings():
    settings = CompanyMaster.objects().first()
    if not settings:
        settings = CompanyMaster(company_name='WON SOLUTIONS (PVT) LTD')
        settings.save()

    if request.method == 'POST':
        settings.company_name = request.form.get('company_name')
        settings.tagline = request.form.get('tagline')
        settings.roc_number = request.form.get('roc_number')
        settings.tin_number = request.form.get('tin_number')
        settings.vat_number = request.form.get('vat_number')
        settings.is_vat_registered = 'is_vat_registered' in request.form
        settings.nature_of_business = request.form.get('nature_of_business')
        settings.registered_address = request.form.get('address')
        settings.contact_phone = request.form.get('phone')
        settings.contact_email = request.form.get('email')
        settings.country = request.form.get('country')
        settings.currency = request.form.get('currency')
        settings.website_domain = request.form.get('website_domain')
        settings.receipt_footer = request.form.get('receipt_footer')
        settings.financial_year_end = request.form.get('financial_year_end', 'March')
        
        settings.save()
        flash('Company Master updated successfully!', 'success')
        return redirect(url_for('settings.manage_settings'))
    
    return render_template('settings.html', settings=settings)

@settings_bp.route('/settings/directors', methods=['GET', 'POST'])
@login_required
def manage_directors():
    company = CompanyMaster.objects().first()
    if not company:
        flash('Please configure Company Information first.', 'warning')
        return redirect(url_for('settings.manage_settings'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        nic = request.form.get('nic')
        address = request.form.get('address')
        appoint_date_str = request.form.get('appointment_date')
        
        from datetime import datetime as dt
        appoint_date = None
        if appoint_date_str:
            appoint_date = dt.strptime(appoint_date_str, '%Y-%m-%d').date()
            
        new_director = Director(
            company=company,
            name=name,
            nic_or_passport=nic,
            address=address,
            appointment_date=dt.combine(appoint_date, dt.min.time()) if appoint_date else None
        )
        new_director.save()
        flash('Director added successfully!', 'success')
        return redirect(url_for('settings.manage_directors'))
    
    directors = Director.objects(company=company)
    return render_template('settings/directors.html', directors=directors)

@settings_bp.route('/settings/shareholders', methods=['GET', 'POST'])
@login_required
def manage_shareholders():
    company = CompanyMaster.objects().first()
    if not company:
        flash('Please configure Company Information first.', 'warning')
        return redirect(url_for('settings.manage_settings'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        shares = int(request.form.get('shares', 0))
        share_class = request.form.get('share_class', 'Ordinary')
        
        new_shareholder = Shareholder(
            company=company,
            name=name,
            shares_count=shares,
            share_class=share_class
        )
        new_shareholder.save()
        flash('Shareholder added successfully!', 'success')
        return redirect(url_for('settings.manage_shareholders'))
    
    shareholders = Shareholder.objects(company=company)
    return render_template('settings/shareholders.html', shareholders=shareholders)
