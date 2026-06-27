import unittest
from app import app
from Backend.utils.db import get_db_connection


class PortfolioAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_admin_login_page_loads(self):
        response = self.client.get('/admin/login')
        self.assertEqual(response.status_code, 200)

    def test_default_admin_can_login(self):
        response = self.client.post('/admin/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'dashboard', response.data.lower())

    def test_can_edit_existing_skill(self):
        with self.client.session_transaction() as session:
            session['logged_in'] = True
            session['admin_id'] = 1
            session['admin_username'] = 'admin'

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO skills (nama_skill, tingkat_keahlian) VALUES (%s, %s)", ('Test Skill', 'Beginner'))
                conn.commit()
                skill_id = cursor.lastrowid
        finally:
            conn.close()

        response = self.client.post(f'/admin/skills/edit/{skill_id}', data={
            'nama_skill': 'Updated Skill',
            'tingkat_keahlian': 'Advanced'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated Skill', response.data)


if __name__ == '__main__':
    unittest.main()
