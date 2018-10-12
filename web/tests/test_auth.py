# import json
# import unittest
#
# from tests.base import BaseTestCase
# from app.auth.models import User
#
# from app import create_app, db
# app = create_app()
#
#
# class TestAuthService(BaseTestCase):
#     """
#     Tests for the Users Service.
#     """
#     def create_app(self):
#         app.config.from_object('config.DevelopmentConfig')
#         return app
#
#     def test_users(self):
#         """
#         Ensure the /ping route behaves correctly.
#         """
#         response = self.client.get('/users/ping')
#         data = json.loads(response.data.decode())
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('pong!', data['message'])
#         self.assertIn('success', data['status'])
#
#     def test_add_user(self):
#         """
#         Test add new user to the database
#         """
#         response = self.client.post('/users',
#                                     data=json.dumps({'name': 'Elena',
#                                                      'email': 'anelka.dmytriieva@gmail.com'}),
#                                     content_type='application/json')
#         data = json.loads(response.data.decode())
#         self.assertEqual(response.status_code, 201)
#         self.assertIn('anelka.dmytriieva@gmail.com', data['message'])
#         self.assertIn('success', data['status'])
#
#     def test_add_family(self):
#         response = self.client.post('families',
#                                     data=json.dumps({'last_name': 'Dmytriieva'}),
#                                     content_type='application/json')
#         data = json.loads(response.data.decode())
#         self.assertEqual(response.status_code, 201)
#         self.assertIn('Dmytriieva', data['message'])
#         self.assertIn('success', data['status'])
#
#     def test_add_user_invalid_json(self):
#         response = self.client.post('/users',
#                                     data=json.dumps({}),
#                                     content_type='application/json')
#         data = json.loads(response.data.decode())
#         self.assertEqual(response.status_code, 400)
#         self.assertIn('Invalid json', data['message'])
#         self.assertIn('fail', data['status'])
#
#     def test_add_user_invalid_json_keys(self):
#         response = self.client.post('/users',
#                                     data=json.dumps({'email': 'fvbuhaeb'}),
#                                     content_type='application/json')
#         data = json.loads(response.data.decode())
#         self.assertEqual(response.status_code, 400)
#         self.assertIn('Invalid json', data['message'])
#         self.assertIn('fail', data['status'])
#
#     def test_add_user_duplicate_email(self):
#         with self.client:
#             self.client.post(
#                 '/users',
#                 data=json.dumps({
#                     'name': 'michael',
#                     'email': 'michael@mherman.org'
#                 }),
#                 content_type='application/json',
#             )
#             response = self.client.post(
#                 '/users',
#                 data=json.dumps({
#                     'name': 'michael',
#                     'email': 'michael@mherman.org'
#                 }),
#                 content_type='application/json',
#             )
#             data = json.loads(response.data.decode())
#             self.assertEqual(response.status_code, 400)
#             self.assertIn('Sorry. That email already exists.', data['message'])
#             self.assertIn('fail', data['status'])
#
#     # def test_single_user(self):
#     #     user = User(username='michael', email='michael@mherman.org')
#     #     db.session.add(user)
#     #     db.session.commit()
#     #     with self.client:
#     #         response = self.client.get(f'/users/{user.id}')
#     #         data = json.loads(response.data.decode())
#     #         self.assertEqual(response.status_code, 200)
#     #         self.assertIn('michael', data['data']['name'])
#     #         self.assertIn('michael@mherman.org', data['data']['email'])
#     #         self.assertIn('success', data['status'])
#
#
# if __name__ == '__main__':
#     unittest.main()
