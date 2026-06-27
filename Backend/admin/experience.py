from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from Backend.utils.db import get_db_connection

# Membuat Blueprint untuk Pengelolaan Pengalaman Admin
experience_bp = Blueprint('experience', __name__)

@experience_bp.route('/admin/experience', methods=['GET', 'POST'])
def admin_experience():
    """Rute untuk menampilkan daftar pengalaman dan menambahkan data baru"""

    if not session.get('logged_in'):
        flash('Silakan login terlebih dahulu!', 'danger')
        return redirect(url_for('login.admin_login'))

    connection = get_db_connection()

    if request.method == 'POST':
        perusahaan = request.form.get('perusahaan')
        posisi = request.form.get('posisi')
        tahun = request.form.get('tahun')
        deskripsi = request.form.get('deskripsi')

        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO experience (perusahaan, posisi, tahun, deskripsi) 
                         VALUES (%s, %s, %s, %s)"""
                cursor.execute(sql, (perusahaan, posisi, tahun, deskripsi))
                connection.commit()
                flash('Pengalaman baru berhasil ditambahkan!', 'success')
        except Exception as e:
            print(f"Error saat menambah pengalaman: {e}")
            flash('Gagal menambahkan pengalaman baru ke database.', 'danger')
        finally:
            connection.close()

        return redirect(url_for('experience.admin_experience'))

    experience_data = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM experience ORDER BY id DESC")
            experience_data = cursor.fetchall()
    except Exception as e:
        print(f"Error saat mengambil data pengalaman: {e}")
    finally:
        connection.close()

    return render_template('admin/experience.html', experiences=experience_data, editing_experience=None)


@experience_bp.route('/admin/experience/edit/<int:id>', methods=['GET', 'POST'])
def edit_experience(id):
    """Rute untuk mengubah data pengalaman yang sudah ada"""

    if not session.get('logged_in'):
        flash('Silakan login terlebih dahulu!', 'danger')
        return redirect(url_for('login.admin_login'))

    connection = get_db_connection()

    if request.method == 'POST':
        perusahaan = request.form.get('perusahaan')
        posisi = request.form.get('posisi')
        tahun = request.form.get('tahun')
        deskripsi = request.form.get('deskripsi')

        try:
            with connection.cursor() as cursor:
                sql = "UPDATE experience SET perusahaan = %s, posisi = %s, tahun = %s, deskripsi = %s WHERE id = %s"
                cursor.execute(sql, (perusahaan, posisi, tahun, deskripsi, id))
                connection.commit()
                flash('Data pengalaman berhasil diperbarui!', 'success')
        except Exception as e:
            print(f"Error saat mengubah pengalaman: {e}")
            flash('Gagal memperbarui data pengalaman.', 'danger')
        finally:
            connection.close()

        return redirect(url_for('experience.admin_experience'))

    experience = None
    experience_data = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM experience WHERE id = %s", (id,))
            experience = cursor.fetchone()
            cursor.execute("SELECT * FROM experience ORDER BY id DESC")
            experience_data = cursor.fetchall()
    except Exception as e:
        print(f"Error saat mengambil data pengalaman: {e}")
    finally:
        connection.close()

    if not experience:
        flash('Data pengalaman tidak ditemukan.', 'danger')
        return redirect(url_for('experience.admin_experience'))

    return render_template('admin/experience.html', experiences=experience_data, editing_experience=experience)


@experience_bp.route('/admin/experience/delete/<int:id>')
def delete_experience(id):
    """Rute untuk menghapus data pengalaman berdasarkan ID"""

    if not session.get('logged_in'):
        return redirect(url_for('login.admin_login'))

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM experience WHERE id = %s"
            cursor.execute(sql, (id,))
            connection.commit()
            flash('Data pengalaman berhasil dihapus!', 'success')
    except Exception as e:
        print(f"Error saat menghapus pengalaman: {e}")
        flash('Gagal menghapus data pengalaman.', 'danger')
    finally:
        connection.close()

    return redirect(url_for('experience.admin_experience'))