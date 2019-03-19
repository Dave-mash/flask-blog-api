# import os
# import unittest
# from app import create_app

# class TestDevelopmentConfig(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app('development')

#     def test_app_is_development(self):
#         self.assertTrue(self.app.config['DEBUG'] is True)
#         self.assertFalse(self.app.config['SECRET_KEY'] is 'thisismykey')

# class TestTestingConfig(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app('testing')

#     def test_app_is_testing(self):
#         self.assertTrue(self.app.config['DEBUG'] is True)
#         self.assertTrue(self.app.config['TESTING'] is True)
#         self.assertFalse(self.app.config['SECRET_KEY'] is 'thisismykey')

# class TestProductionConfig(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app('production')

#     def test_is_production(self):
#         self.assertTrue(self.app.config['DEBUG'] is False)
#         self.assertTrue(self.app.config['TESTING'] is False)