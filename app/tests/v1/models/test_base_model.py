# """
# This module contains tests for the base model
# """

# # 3rd party imports
# import unittest
# import os

# # local imports
# from app.api.v1.models.base_model import BaseModel
# from app.database import InitializeDb

# class TestBaseModel(unittest.TestCase):

#     def setUp(self):
#         self.base_model = BaseModel('users', os.getenv('TEST_DATABASE_URI'))
#         self.base_model.database.create_tables()

#         self.user_item = dict(
#             first_name="David",
#             last_name="Mwangi",
#             email="dave@demo.com",
#             username="dave",
#             password="abc123@1A"
#         )


#     def test_encode_auth_token(self):
#         """ Test the encode token method works correctly """

#         auth_token = self.base_model.encode_auth_token(1)
#         self.assertTrue(isinstance(auth_token, bytes))


#     def test_decode_auth_token(self):
#         """ Test the decode token method works correctly """

#         auth_token = self.base_model.encode_auth_token(1)
#         self.assertTrue(isinstance(auth_token, bytes))
#         self.assertTrue(self.base_model.decode_auth_token(auth_token) == 1)


#     def test_add_item(self):
#         """ Test the add item method works correctly """

#         keys = ", ".join(self.user_item.keys())
#         values = tuple(self.user_item.values())
#         self.base_model.add_item(keys, values)

#         self.assertTrue(self.base_model.grab_items_by_name('username', "username = 'dave'"))


#     # def test_grab_all_items(self):
#     #     """ Test the grab all items method works correctly """
        
#     #     users = self.base_model.grab_all_items('username', "True = True")
#     #     print(users)
#     #     # test with no items
#     #     self.assertFalse(users)

#     #     # test with one item
#     #     keys = ", ".join(self.user_item.keys())
#     #     values = tuple(self.user_item.values())
#     #     self.base_model.add_item(keys, values)
#     #     users2 = self.base_model.grab_all_items('username', "True = True")
#     #     self.assertEqual(len(users2), 1)


#     def test_grab_items_by_name(self):
#         """ Test the grab items by name works correctly """

#         keys = ", ".join(self.user_item.keys())
#         values = tuple(self.user_item.values())
#         self.base_model.add_item(keys, values)
#         users = self.base_model.grab_items_by_name('username', "username = 'dave'")[0]
#         self.assertEqual(users, 'dave')

#     def test_delete_item(self):
#         """ Test the grab items by name method works correctly """

#         # add item
#         keys = ", ".join(self.user_item.keys())
#         values = tuple(self.user_item.values())
#         self.base_model.add_item(keys, values)
#         users = self.base_model.grab_items_by_name('username', "username = 'dave'")
#         self.assertTrue(users)

#         # delete item
#         self.base_model.delete_item("id = 1")
#         users = self.base_model.grab_items_by_name('username', "username = 'dave'")
#         self.assertFalse(users)
        

#     def test_update_item(self):
#         """ Test update items method works correctly """

#         # add item
#         keys = ", ".join(self.user_item.keys())
#         values = tuple(self.user_item.values())
#         self.base_model.add_item(keys, values)
#         users = self.base_model.grab_items_by_name('username', "username = 'dave'")
#         self.assertTrue(users)

#         # update item
#         self.base_model.update_item("username = 'Davee'", "id = 1")
#         self.assertTrue(self.base_model.grab_items_by_name('username', "username = 'Davee'"))


#     def tearDown(self):
#         """ This method destroys the test tables """

#         self.base_model.database.drop_tables()


# if __name__ == "__main__":
#     unittest.main()