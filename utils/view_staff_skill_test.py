import unittest
from view_staff_skill import app  # Import your Flask app from view_staff_skill.py
from flask_testing import TestCase

class StaffSkillTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_get_staff_skills(self):
        staff_id = 140001  # Use the provided staff_id
        response = self.client.get(f'/Staff_Skill/{staff_id}')
        data = response.json

        self.assertStatus(response, 200)  # Assuming you return 200 for successful requests
        self.assertIn('data', data)
        self.assertIn('Staff-Skill', data['data'])
        staff_skills = data['data']['Staff-Skill']

        # Check if the number of returned skills matches the expected count
        expected_skill_count = 8  # Update this count based on your expected output
        self.assertEqual(len(staff_skills), expected_skill_count)

        # Check if the staff ID in the response matches the expected staff ID
        self.assertEqual(staff_id, staff_skills[0]['Staff_ID'])

    def test_get_staff_skills_invalid_id(self):
        staff_id = 999  # Use an invalid staff_id
        response = self.client.get(f'/Staff_Skill/{staff_id}')
        data = response.json

        self.assertEqual(data['code'], 400)  # Assuming you return 400 for an invalid request
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Invalid Staff ID')

if __name__ == '__main__':
    unittest.main()
