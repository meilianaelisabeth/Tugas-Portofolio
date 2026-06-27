from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from Backend.utils.db import get_db_connection

# Membuat Blueprint untuk fitur admin login
login_bp = Blueprint('login', __name__)

@login_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Rute untuk menampilkan halaman login dan memproses data login"""
    
    # Jika admin sudah login sebelumnya, langsung lempar ke dashboard
    if session.get('logged_in'):
        return redirect(url_for('dashboard.admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Ambil koneksi database TiDB
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Periksa apakah username dan password cocok dengan di database
                sql = "SELECT * FROM admin WHERE username = %s AND password = %s"
                cursor.execute(sql, (username, password))
                admin = cursor.fetchone()

                if admin:
                    # Jika cocok, buat session login
                    session['logged_in'] = True
                    session['admin_id'] = admin['id']
                    session['admin_username'] = admin['username']
                    flash('Login berhasil! Selamat datang.', 'success')
                    return redirect(url_for('dashboard.admin_dashboard'))
                else:
                    flash('Username atau Password salah!', 'danger')
        except Exception as e:
            print(f"Error saat login: {e}")
            flash('Terjadi kesalahan pada server database.', 'danger')
        finally:
            connection.close()

    # Jika aksesnya GET, tampilkan halaman form login biasa
    # Mengarah ke folder Frontend/admin/login.html
    return render_template('admin/login.html')

@login_bp.route('/admin/logout')
def admin_logout():
    """Rute untuk logout dan menghapus session admin"""
    session.clear()
    flash('Anda telah berhasil keluar.', 'success')
    return redirect(url_for('login.admin_login'))