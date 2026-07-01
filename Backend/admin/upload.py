from flask import Blueprint, request, jsonify, session
import cloudinary
import cloudinary.uploader

try:
    import resend
except ImportError:  # pragma: no cover - optional dependency
    resend = None

from config import Config


upload_bp = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import jsonify, request

@upload_bp.route('/api/kirim-pesan', methods=['POST'])
def api_kirim_pesan():
    try:
        # GANTI CARA AMBIL DATA DARI request.get_json() MENJADI FORM:
        nama = request.form.get('nama')
        email_pengirim = request.form.get('email')
        pesan = request.form.get('pesan')

        # === KODE SMTP GMAIL KAMU YANG KEMARIN ===
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        gmail_user = "meilianaelisabeth4@gmail.com" 
        gmail_password = "qbjn yirt deuw cwwt" 
        
        msg = MIMEMultipart()
        msg['From'] = f"Kontak Portofolio <{gmail_user}>"
        msg['To'] = gmail_user
        msg['Subject'] = f"Pesan Portofolio Baru dari {nama}"

        html_content = f"""
        <h3>Ada pesan baru dari website portofolio Anda!</h3>
        <p><strong>Nama Pengirim:</strong> {nama}</p>
        <p><strong>Email Pengirim:</strong> {email_pengirim}</p>
        <p><strong>Isi Pesan:</strong></p>
        <p>{pesan}</p>
        """
        msg.attach(MIMEText(html_content, 'html'))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, gmail_user, msg.as_string())
        server.quit()

        # Biar setelah kirim email, halaman otomatis balik lagi ke portofolio kamu:
        from flask import redirect
        return redirect('/')

    except Exception as e:
        print("Error detail SMTP:", str(e))
        return f"Terjadi kesalahan: {str(e)}", 500
