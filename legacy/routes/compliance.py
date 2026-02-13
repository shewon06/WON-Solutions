from flask import Blueprint, render_template, request, send_file, flash, redirect, url_for
from flask_login import login_required
from models import db, CompanyMaster, Director, Shareholder, Sale, Expense, DocumentLog, Customer
from utils.doc_engine import DocumentEngine, log_document
from datetime import datetime, date
import os

compliance_bp = Blueprint('compliance', __name__)

@compliance_bp.route('/compliance')
@login_required
def dashboard():
    company = CompanyMaster.objects().first()
    logs = DocumentLog.objects().order_by('-generated_at').limit(10)
    return render_template('compliance/dashboard.html', company=company, logs=logs)

@compliance_bp.route('/compliance/generate/form18/<director_id>')
@login_required
def generate_form18(director_id):
    company = CompanyMaster.objects().first()
    director = Director.objects.get_or_404(pk=director_id)
    
    context = {
        'company': company,
        'director': director,
        'today': date.today(),
        'system_gen_msg': "Prepared by System – Subject to Auditor Verification"
    }
    
    filename = f"Form18_{director.name.replace(' ', '_')}_{date.today().isoformat()}.pdf"
    filepath = os.path.join('static', 'generated_docs', filename)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    pdf_content = DocumentEngine.generate_pdf('compliance/templates/form18.html', context, output_path=filepath)
    
    if pdf_content:
        log_document('ROC_FORM_18', filename, filepath)
        return send_file(filepath, as_attachment=True)
    else:
        flash("Error generating PDF", "danger")
        return redirect(url_for('compliance.dashboard'))

@compliance_bp.route('/compliance/generate/tax-form20')
@login_required
def generate_tax_form20():
    company = CompanyMaster.objects().first()
    year = int(request.args.get('year', datetime.now().year))
    
    from datetime import datetime as dt
    year_start = dt(year, 1, 1)
    year_end = dt(year, 12, 31, 23, 59, 59)
    
    # Simple logic for NIL detection
    sales_count = Sale.objects(created_at__gte=year_start, created_at__lte=year_end).count()
    is_nil = sales_count == 0
    
    context = {
        'company': company,
        'year': year,
        'is_nil': is_nil,
        'sales_total': Sale.objects(created_at__gte=year_start, created_at__lte=year_end).sum('total_amount'),
        'system_gen_msg': "Prepared by System – Subject to Auditor Verification"
    }
    
    filename = f"Form20_{year}_{'NIL' if is_nil else 'REG'}.pdf"
    filepath = os.path.join('static', 'generated_docs', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    pdf_content = DocumentEngine.generate_pdf('compliance/templates/form20.html', context, output_path=filepath)
    
    if pdf_content:
        log_document('IRD_FORM_20', filename, filepath)
        return send_file(filepath, as_attachment=True)
    
    flash("Error generating Tax Return", "danger")
    return redirect(url_for('compliance.dashboard'))

@compliance_bp.route('/compliance/audit-pack')
@login_required
def download_audit_pack():
    # Implementation for ZIP export
    import zipfile
    from io import BytesIO
    
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        # Add Sales Register (Excel)
        sales = Sale.objects()
        sales_data = [{'ID': str(s.id), 'Date': s.created_at, 'Amount': s.total_amount, 'VAT': s.vat_amount} for s in sales]
        sales_path = 'static/generated_docs/sales_register.xlsx'
        DocumentEngine.generate_excel(sales_data, ['ID', 'Date', 'Amount', 'VAT'], sales_path)
        zf.write(sales_path, 'Sales_Register.xlsx')
        
        # Add Expense Register (Excel)
        exps = Expense.objects()
        exp_data = [{'ID': str(e.id), 'Date': e.expense_date, 'Desc': e.description, 'Amount': e.amount} for e in exps]
        exp_path = 'static/generated_docs/expense_register.xlsx'
        DocumentEngine.generate_excel(exp_data, ['ID', 'Date', 'Desc', 'Amount'], exp_path)
        zf.write(exp_path, 'Expense_Register.xlsx')
        
    memory_file.seek(0)
    return send_file(memory_file, download_name=f"AuditPack_{date.today().isoformat()}.zip", as_attachment=True)

@compliance_bp.route('/compliance/generate/all-shares', methods=['POST'])
@login_required
def generate_all_shares():
    company = CompanyMaster.objects().first()
    shareholders = Shareholder.objects()
    
    if not shareholders:
        flash("No shareholders found to generate certificates.", "warning")
        return redirect(url_for('compliance.dashboard'))
    
    count = 0
    for sh in shareholders:
        context = {
            'company': company,
            'shareholder': sh,
            'today': date.today()
        }
        
        filename = f"ShareCert_{sh.name.replace(' ', '_')}_{date.today().isoformat()}.pdf"
        filepath = os.path.join('static', 'generated_docs', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        pdf_content = DocumentEngine.generate_pdf('compliance/templates/share_certificate.html', context, output_path=filepath)
        if pdf_content:
            log_document('SHARE_CERT', filename, filepath)
            count += 1
            
    flash(f"Successfully generated {count} share certificates!", "success")
    return redirect(url_for('compliance.dashboard'))
