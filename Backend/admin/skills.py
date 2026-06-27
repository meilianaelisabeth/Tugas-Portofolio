from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from Backend.utils.db import get_db_connection

# Membuat Blueprint untuk Pengelolaan Skills Admin
skills_bp = Blueprint('skills', __name__)

@skills_bp.route('/admin/skills', methods=['GET', 'POST'])
def admin_skills():
    """Rute untuk menampilkan daftar skill dan menambahkan skill baru"""

    if not session.get('logged_in'):
        flash('Silakan login terlebih dahulu!', 'danger')
        return redirect(url_for('login.admin_login'))

    connection = get_db_connection()

    if request.method == 'POST':
        nama_skill = request.form.get('nama_skill')
        tingkat_keahlian = request.form.get('tingkat_keahlian')

        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO skills (nama_skill, tingkat_keahlian) VALUES (%s, %s)"
                cursor.execute(sql, (nama_skill, tingkat_keahlian))
                connection.commit()
                flash('Skill baru berhasil ditambahkan!', 'success')
        except Exception as e:
            print(f"Error saat menambah skill: {e}")
            flash('Gagal menambahkan skill baru ke database.', 'danger')
        finally:
            connection.close()

        return redirect(url_for('skills.admin_skills'))

    skills_data = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM skills ORDER BY id DESC")
            skills_data = cursor.fetchall()
    except Exception as e:
        print(f"Error saat mengambil data skill: {e}")
    finally:
        connection.close()

    return render_template('admin/skills.html', skills=skills_data, editing_skill=None)


@skills_bp.route('/admin/skills/edit/<int:id>', methods=['GET', 'POST'])
def edit_skill(id):
    """Rute untuk mengubah skill yang sudah ada"""

    if not session.get('logged_in'):
        flash('Silakan login terlebih dahulu!', 'danger')
        return redirect(url_for('login.admin_login'))

    connection = get_db_connection()

    if request.method == 'POST':
        nama_skill = request.form.get('nama_skill')
        tingkat_keahlian = request.form.get('tingkat_keahlian')

        try:
            with connection.cursor() as cursor:
                sql = "UPDATE skills SET nama_skill = %s, tingkat_keahlian = %s WHERE id = %s"
                cursor.execute(sql, (nama_skill, tingkat_keahlian, id))
                connection.commit()
                flash('Skill berhasil diperbarui!', 'success')
        except Exception as e:
            print(f"Error saat mengubah skill: {e}")
            flash('Gagal memperbarui skill.', 'danger')
        finally:
            connection.close()

        return redirect(url_for('skills.admin_skills'))

    skill = None
    skills_data = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM skills WHERE id = %s", (id,))
            skill = cursor.fetchone()
            cursor.execute("SELECT * FROM skills ORDER BY id DESC")
            skills_data = cursor.fetchall()
    except Exception as e:
        print(f"Error saat mengambil data skill: {e}")
    finally:
        connection.close()

    if not skill:
        flash('Skill tidak ditemukan.', 'danger')
        return redirect(url_for('skills.admin_skills'))

    return render_template('admin/skills.html', skills=skills_data, editing_skill=skill)


@skills_bp.route('/admin/skills/delete/<int:id>')
def delete_skill(id):
    """Rute untuk menghapus skill berdasarkan ID"""

    if not session.get('logged_in'):
        return redirect(url_for('login.admin_login'))

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM skills WHERE id = %s"
            cursor.execute(sql, (id,))
            connection.commit()
            flash('Skill berhasil dihapus!', 'success')
    except Exception as e:
        print(f"Error saat menghapus skill: {e}")
        flash('Gagal menghapus skill.', 'danger')
    finally:
        connection.close()

    return redirect(url_for('skills.admin_skills'))