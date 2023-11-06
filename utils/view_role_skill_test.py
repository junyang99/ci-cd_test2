import unittest
from view_role_skill import app  # Import your Flask app from view_role_skill.py
from flask_testing import TestCase

class RoleSkillTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_get_role_skills(self):
        role_name = 'Developer'  # Use the provided role name
        response = self.client.get(f'/Role_Skill/{role_name}')
        data = response.json

        self.assertEqual(response.status_code, 200)  # Check the HTTP status code
        self.assertIn('data', data)
        self.assertIn('Role-Skill', data['data'])
        role_skills = data['data']['Role-Skill']

        # Check if the number of returned role skills matches the expected count
        expected_skill_count = 22  # Update this count based on your expected output
        self.assertEqual(len(role_skills), expected_skill_count)

        # Check if the role name in the response matches the expected role name
        self.assertEqual(role_name, role_skills[0]['Role_Name'])

    def test_get_role_skills_invalid_role(self):
        role_name = 'invalid_role'  # Use an invalid role name
        response = self.client.get(f'/Role_Skill/{role_name}')
        data = response.json

        self.assertEqual(data['code'], 400)  # Check the HTTP status code
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Roleinvalid_role does not exist.')

if __name__ == '__main__':
    unittest.main()
