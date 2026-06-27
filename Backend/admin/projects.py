from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from Backend.utils.db import get_db_connection
import cloudinary
import cloudinary.uploader

# Membuat Blueprint untuk Pengelolaan Projects Admin
projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/admin/projects', methods=['GET', 'POST'])
def admin_projects():
    """Rute untuk menampilkan daftar proyek dan menambah proyek baru dengan gambar"""

    if not session.get('logged_in'):
        flash('Silakan login terlebih dahulu!', 'danger')
        return redirect(url_for('login.admin_login'))

    connection = get_db_connection()

    if request.method == 'POST':
        nama_proyek = request.form.get('nama_proyek')
        deskripsi = request.form.get('deskripsi')
        link_proyek = request.form.get('link_proyek')
        file_gambar = request.files.get('gambar_proyek')

        gambar_url = ""

        if file_gambar and file_gambar.filename != '':
            try:
                upload_result = cloudinary.uploader.upload(file_gambar, folder="portofolio/projects")
                gambar_url = upload_result.get('secure_url')
            except Exception as e:
                print(f"Gagal upload gambar proyek ke Cloudinary: {e}")
                flash('Gagal mengunggah gambar proyek.', 'danger')

        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO projects (nama_proyek, deskripsi, gambar_url, link_proyek) 
                         VALUES (%s, %s, %s, %s)"""
                cursor.execute(sql, (nama_proyek, deskripsi, gambar_url, link_proyek))
                connection.commit()
                flash('Proyek baru berhasil ditambahkan!', 'success')
        except Exception as e:
            print(f"Error saat menambah proyek: {e}")
            flash('Gagal menyimpan proyek baru ke database.', 'danger')
        finally:
            connection.close()

        return redirect(url_for('projects.admin_projects'))

    projects_data = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM projects ORDER BY id DESC")
            projects_data = cursor.fetchall()
    except Exception as e:
        print(f"Error saat mengambil data proyek: {e}")
    finally:
        connection.close()

    return render_template('admin/projects.html', projects=projects_data, editing_project=None)


@projects_bp.route('/admin/projects/edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    """Rute untuk mengubah proyek yang sudah ada"""

    if not session.get('logged_in'):
        flash('Silakan login terlebih dahulu!', 'danger')
        return redirect(url_for('login.admin_login'))

    connection = get_db_connection()

    if request.method == 'POST':
        nama_proyek = request.form.get('nama_proyek')
        deskripsi = request.form.get('deskripsi')
        link_proyek = request.form.get('link_proyek')
        file_gambar = request.files.get('gambar_proyek')

        gambar_url = request.form.get('old_gambar_url', '')
        if file_gambar and file_gambar.filename != '':
            try:
                upload_result = cloudinary.uploader.upload(file_gambar, folder="portofolio/projects")
                gambar_url = upload_result.get('secure_url')
            except Exception as e:
                print(f"Gagal upload gambar proyek ke Cloudinary: {e}")
                flash('Gagal mengunggah gambar proyek.', 'danger')

        try:
            with connection.cursor() as cursor:
                sql = "UPDATE projects SET nama_proyek = %s, deskripsi = %s, link_proyek = %s, gambar_url = %s WHERE id = %s"
                cursor.execute(sql, (nama_proyek, deskripsi, link_proyek, gambar_url, id))
                connection.commit()
                flash('Proyek berhasil diperbarui!', 'success')
        except Exception as e:
            print(f"Error saat mengubah proyek: {e}")
            flash('Gagal memperbarui proyek.', 'danger')
        finally:
            connection.close()

        return redirect(url_for('projects.admin_projects'))

    project = None
    projects_data = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM projects WHERE id = %s", (id,))
            project = cursor.fetchone()
            cursor.execute("SELECT * FROM projects ORDER BY id DESC")
            projects_data = cursor.fetchall()
    except Exception as e:
        print(f"Error saat mengambil data proyek: {e}")
    finally:
        connection.close()

    if not project:
        flash('Proyek tidak ditemukan.', 'danger')
        return redirect(url_for('projects.admin_projects'))

    return render_template('admin/projects.html', projects=projects_data, editing_project=project)


@projects_bp.route('/admin/projects/delete/<int:id>')
def delete_project(id):
    """Rute untuk menghapus proyek berdasarkan ID"""

    if not session.get('logged_in'):
        return redirect(url_for('login.admin_login'))

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM projects WHERE id = %s"
            cursor.execute(sql, (id,))
            connection.commit()
            flash('Proyek berhasil dihapus!', 'success')
    except Exception as e:
        print(f"Error saat menghapus proyek: {e}")
        flash('Gagal menghapus proyek.', 'danger')
    finally:
        connection.close()

    return redirect(url_for('projects.admin_projects'))