from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from Backend.utils.db import get_db_connection
import cloudinary
import cloudinary.uploader

# Membuat Blueprint untuk Pengelolaan Profil Admin
profiles_bp = Blueprint('profiles', __name__)

@profiles_bp.route('/admin/profile', methods=['GET', 'POST'])
def admin_profile():
    """Rute untuk melihat dan memperbarui data profil diri"""
    
    # PROTEKSI: Jika belum login, kembalikan ke halaman login
    if not session.get('logged_in'):
        flash('Silakan login terlebih dahulu!', 'danger')
        return redirect(url_for('login.admin_login'))

    connection = get_db_connection()
    
    if request.method == 'POST':
        nama = request.form.get('nama')
        judul_profesi = request.form.get('judul_profesi')
        deskripsi = request.form.get('deskripsi')
        file_foto = request.files.get('foto')
        
        foto_url = request.form.get('old_foto_url') # Simpan URL foto lama sebagai cadangan

        # Proses upload foto ke Cloudinary jika ada file baru yang dimasukkan
        if file_foto and file_foto.filename != '':
            try:
                upload_result = cloudinary.uploader.upload(file_foto, folder="portofolio/profile")
                foto_url = upload_result.get('secure_url')
            except Exception as e:
                print(f"Gagal upload ke Cloudinary: {e}")
                flash('Gagal mengunggah foto baru.', 'danger')

        # Update data ke TiDB Cloud
        try:
            with connection.cursor() as cursor:
                # Cek apakah sudah ada data profil sebelumnya
                cursor.execute("SELECT id FROM profil ORDER BY id DESC LIMIT 1")
                profil_row = cursor.fetchone()

                if profil_row:
                    # Jika sudah ada, lakukan UPDATE pada baris profil yang ada
                    profil_id = profil_row['id']
                    sql = """UPDATE profil SET nama=%s, judul_profesi=%s, deskripsi=%s, foto_url=%s WHERE id=%s"""
                    cursor.execute(sql, (nama, judul_profesi, deskripsi, foto_url, profil_id))
                else:
                    # Jika masih kosong, lakukan INSERT baru
                    sql = """INSERT INTO profil (nama, judul_profesi, deskripsi, foto_url) VALUES (%s, %s, %s, %s)"""
                    cursor.execute(sql, (nama, judul_profesi, deskripsi, foto_url))
                
                connection.commit()
                flash('Profil berhasil diperbarui!', 'success')
        except Exception as e:
            print(f"Error database saat simpan profil: {e}")
            flash('Gagal menyimpan perubahan ke database.', 'danger')
        finally:
            connection.close()
            
        return redirect(url_for('profiles.admin_profile'))

    # Metode GET: Ambil data profil saat ini untuk ditampilkan di form HTML
    profil_data = None
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM profil ORDER BY id DESC LIMIT 1")
            profil_data = cursor.fetchone()
    except Exception as e:
        print(f"Error ambil data profil: {e}")
    finally:
        connection.close()

    # Mengarah ke file profiles.html di folder Frontend/admin/
    return render_template('admin/profiles.html', profil=profil_data)