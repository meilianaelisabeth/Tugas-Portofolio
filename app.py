import os
from flask import Flask
from config import Config


def _normalize_cloudinary_url():
    raw_url = os.environ.get('CLOUDINARY_URL', '').strip()
    if raw_url.startswith('CLOUDINARY_URL='):
        raw_url = raw_url.split('=', 1)[1]

    if not raw_url:
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', '').strip()
        api_key = os.environ.get('CLOUDINARY_API_KEY', '').strip()
        api_secret = os.environ.get('CLOUDINARY_API_SECRET', '').strip()
        if cloud_name and api_key and api_secret:
            raw_url = f'cloudinary://{api_key}:{api_secret}@{cloud_name}'
        else:
            raw_url = 'cloudinary://demo:demo@demo'

    if raw_url.startswith('cloudinary://'):
        os.environ['CLOUDINARY_URL'] = raw_url
    else:
        os.environ['CLOUDINARY_URL'] = 'cloudinary://demo:demo@demo'


_normalize_cloudinary_url()
import cloudinary


# GANTI BARIS INISIALISASI FLASK DI APP.PY MENJADI SEPERTI INI:
app = Flask(__name__, static_folder='Frontend', template_folder='Frontend')


app.config.from_object(Config)

cloudinary.config(cloudinary_url=os.environ.get('CLOUDINARY_URL'))

from Backend.utama.utama import utama_bp
from Backend.admin.login import login_bp
from Backend.admin.dashboard import dashboard_bp
from Backend.admin.profiles import profiles_bp
from Backend.admin.skills import skills_bp
from Backend.admin.experience import experience_bp
from Backend.admin.projects import projects_bp
from Backend.admin.upload import upload_bp

app.register_blueprint(utama_bp)
app.register_blueprint(login_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(profiles_bp)
app.register_blueprint(skills_bp)
app.register_blueprint(experience_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(upload_bp)


if __name__ == '__main__':
    print('Aplikasi Portofolio Flask berhasil berjalan!')
    app.run(debug=True, host='0.0.0.0', port=5000)