from flask import Blueprint, render_template, redirect, url_for, session, flash
from Backend.utils.db import get_db_connection

# Membuat Blueprint untuk Dashboard Admin
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/admin/dashboard')
def admin_dashboard():
    """Rute untuk menampilkan halaman dashboard utama admin"""
    
    # PROTEKSI: Jika admin belum login, tendang kembali ke halaman login
    if not session.get('logged_in'):
        flash('Silakan login terlebih dahulu!', 'danger')
        return redirect(url_for('login.admin_login'))

    # Ambil koneksi database untuk menghitung ringkasan data (opsional/statistik)
    connection = get_db_connection()
    stats = {'skills': 0, 'projects': 0, 'messages': 0}
    
    try:
        with connection.cursor() as cursor:
            # Hitung jumlah total skill
            cursor.execute("SELECT COUNT(*) AS total FROM skills")
            stats['skills'] = cursor.fetchone()['total']

            # Hitung jumlah total proyek
            cursor.execute("SELECT COUNT(*) AS total FROM projects")
            stats['projects'] = cursor.fetchone()['total']

            # Hitung jumlah total pesan masuk
            cursor.execute("SELECT COUNT(*) AS total FROM messages")
            stats['messages'] = cursor.fetchone()['total']
            
    except Exception as e:
        print(f"Error saat mengambil statistik dashboard: {e}")
    finally:
        connection.close()

    # Mengarah ke file dashboard.html milikmu di folder Frontend/admin/
    return render_template('admin/dashboard.html', stats=stats)