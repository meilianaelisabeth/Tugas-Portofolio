from flask import Blueprint, render_template, request, redirect, url_for, flash
from Backend.utils.db import get_db_connection
import os
import smtplib
import json
import urllib.request
from email.message import EmailMessage

utama_bp = Blueprint('utama', __name__)

def send_notification_email(nama, email, pesan):
    mail_host = os.environ.get('MAIL_HOST')
    mail_port = int(os.environ.get('MAIL_PORT') or 0)
    mail_user = os.environ.get('MAIL_USER')
    mail_password = os.environ.get('MAIL_PASSWORD')
    mail_from = os.environ.get('MAIL_FROM') or mail_user
    mail_to = os.environ.get('MAIL_TO')
    use_tls = os.environ.get('MAIL_USE_TLS', '1').lower() in ('1', 'true', 'yes')

    if mail_host and mail_port and mail_to:
        msg = EmailMessage()
        msg['Subject'] = f'Pesan baru dari {nama}'
        msg['From'] = mail_from or mail_user
        msg['To'] = mail_to
        msg.set_content(f"Nama: {nama}\nEmail: {email}\n\nPesan:\n{pesan}")

        smtp = smtplib.SMTP(mail_host, mail_port, timeout=10)
        if use_tls:
            smtp.starttls()
        if mail_user and mail_password:
            smtp.login(mail_user, mail_password)
        smtp.send_message(msg)
        smtp.quit()
        return True

    resend_api_key = os.environ.get('RESEND_API_KEY')
    resend_from = os.environ.get('RESEND_FROM_EMAIL')
    resend_to = os.environ.get('RESEND_TO_EMAIL')
    if resend_api_key and resend_from and resend_to:
        payload = {
            'from': resend_from,
            'to': [resend_to],
            'subject': f'Pesan baru dari {nama}',
            'text': f'Nama: {nama}\nEmail: {email}\n\nPesan:\n{pesan}'
        }
        req = urllib.request.Request(
            'https://api.resend.com/emails',
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {resend_api_key}'
            },
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            if getattr(response, 'status', None) not in (200, 202):
                raise RuntimeError(f'Resend API gagal dengan status {getattr(response, "status", None)}')
        return True

    raise RuntimeError('Tidak ada konfigurasi email (SMTP atau Resend) yang valid.')


def _fetch_portfolio_data():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM profil ORDER BY id DESC LIMIT 1")
            profil_data = cursor.fetchone()

            cursor.execute("SELECT * FROM skills ORDER BY id DESC")
            skills_data = cursor.fetchall()

            cursor.execute("SELECT * FROM experience ORDER BY id DESC")
            experience_data = cursor.fetchall()

            cursor.execute("SELECT * FROM projects ORDER BY id DESC")
            projects_data = cursor.fetchall()
    except Exception as exc:
        print(f'Terjadi kesalahan database: {exc}')
        profil_data = None
        skills_data = []
        experience_data = []
        projects_data = []
    finally:
        connection.close()

    return profil_data, skills_data, experience_data, projects_data


@utama_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nama = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        pesan = request.form.get('message', '').strip()

        if not all([nama, email, pesan]):
            flash('Silakan isi semua kolom pesan.', 'danger')
            profil_data, skills_data, experience_data, projects_data = _fetch_portfolio_data()
            return render_template(
                'utama/index.html',
                profil=profil_data,
                skills=skills_data,
                experiences=experience_data,
                projects=projects_data
            )

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO messages (nama_pengirim, email_pengirim, isi_pesan) VALUES (%s, %s, %s)",
                    (nama, email, pesan)
                )
                connection.commit()
                flash('Pesan Anda berhasil dikirim. Terima kasih!', 'success')

                try:
                    send_notification_email(nama, email, pesan)
                except Exception as exc_mail:
                    print(f'Peringatan: gagal mengirim email notifikasi: {exc_mail}')
                    flash('Pesan tersimpan, tetapi notifikasi email gagal dikirim.', 'warning')
        except Exception as exc:
            print(f'Terjadi kesalahan saat mengirim pesan: {exc}')
            flash('Pesan gagal dikirim. Coba lagi nanti.', 'danger')
        finally:
            connection.close()

        profil_data, skills_data, experience_data, projects_data = _fetch_portfolio_data()
        return render_template(
            'utama/index.html',
            profil=profil_data,
            skills=skills_data,
            experiences=experience_data,
            projects=projects_data
        )

    profil_data, skills_data, experience_data, projects_data = _fetch_portfolio_data()
    return render_template(
        'utama/index.html',
        profil=profil_data,
        skills=skills_data,
        experiences=experience_data,
        projects=projects_data
    )