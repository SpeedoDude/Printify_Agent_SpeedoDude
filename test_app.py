import unittest
import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_ad_generator(self):
        response = self.app.get('/ad_generator')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
