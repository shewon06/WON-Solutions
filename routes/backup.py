import shutil
import os
from datetime import datetime
from flask import Blueprint, flash, redirect, url_for
from flask_login import login_required

backup_bp = Blueprint('backup', __name__)

@backup_bp.route('/settings/backup')
@login_required
def run_backup():
    db_path = 'instance/system.db' # Flask-SQLAlchemy usually puts it here
    if not os.path.exists(db_path):
        db_path = 'system.db' # Fallback
        
    if not os.path.exists(db_path):
        flash('Database file not found!', 'danger')
        return redirect(url_for('settings.manage_settings'))
        
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f'backup_{timestamp}.db')
    
    try:
        shutil.copy2(db_path, backup_path)
        flash(f'Backup created: backup_{timestamp}.db', 'success')
    except Exception as e:
        flash(f'Backup failed: {str(e)}', 'danger')
        
    return redirect(url_for('settings.manage_settings'))
