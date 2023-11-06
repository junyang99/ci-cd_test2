import unittest
from view_staff import app  # Import your Flask app from view_staff.py
from flask_testing import TestCase

class StaffTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_get_staff_by_id(self):
        staff_id = 140001  # Use the provided staff_id
        response = self.client.get(f'/Staff/{staff_id}')
        data = response.json

        # check that the status code is 200 in data['code']
        self.assertStatus(response, 200)

        self.assertEqual(data['data']['Staff_ID'], staff_id)
        self.assertEqual(data['data']['Staff_FName'], "Derek")
        self.assertEqual(data['data']['Staff_LName'], "Tan")
        self.assertEqual(data['data']['Dept'], "Sales")
        self.assertEqual(data['data']['Country'], "Singapore")
        self.assertEqual(data['data']['Email'], "Derek.Tan@allinone.com.sg")

    def test_get_staff_by_id_not_found(self):
        staff_id = 999  # Replace with a non-existing Staff_ID
        response = self.client.get(f'/Staff/{staff_id}')
        data = response.json

        self.assertEqual(data['code'], 404)
        self.assertEqual(data['message'], 'Staff not found.')

if __name__ == '__main__':
    unittest.main()
