#!/usr/bin/python3
"""Module test_amenity

This Module contains a tests for Amenity Class
"""

import sys
import unittest
from datetime import datetime
from io import StringIO

import pycodestyle

from models import amenity
from tests.test_models.test_base_model import BaseModel

Amenity = amenity.Amenity


class TestAmenityDocsAndStyle(unittest.TestCase):
    """Tests Amenity class for documentation and style conformance"""

    def test_pycodestyle(self):
        """Tests compliance with pycodestyle"""
        style = pycodestyle.StyleGuide(quiet=False)
        result = style.check_files(
            ["models/amenity.py", "tests/test_models/test_amenity.py"])
        self.assertEqual(result.total_errors, 0)

    def test_module_docstring(self):
        """Tests whether the module is documented"""
        self.assertTrue(len(amenity.__doc__) >= 1)

    def test_class_docstring(self):
        """Tests whether the class is documented"""
        self.assertTrue(len(Amenity.__doc__) >= 1)

    def test_class_name(self):
        """Test whether the class name is correct"""
        self.assertEqual(Amenity.__name__, "Amenity")


class TestAmenity(unittest.TestCase):
    """Test cases for Amenity Class"""

    def setUp(self):
        """creates a test object for other tests"""
        self.test_obj = Amenity()
        self.test_obj.name = "example"

    def test_amenity_is_subclass_of_base_model(self):
        self.assertTrue(issubclass(Amenity, BaseModel))

    def test_public_attributes_exist(self):
        """tests wether the public instance attributes exist."""
        req_att = ["id", "created_at", "updated_at", "name"]
        for attrib in req_att:
            self.assertTrue(hasattr(self.test_obj, attrib))

    def test_public_attributes_have_correct_type(self):
        """tests wether the public instance attributes exist."""
        req_att = ["name"]
        for attrib in req_att:
            self.assertTrue(type(getattr(self.test_obj, attrib)), str)

    def test_bas_str_should_print_formatted_output(self):
        """__str__ should print [<class name>] (<self.id>) <self.__dict__>"""
        self.test_obj.my_number = 89
        cls_name = Amenity.__name__
        id = self.test_obj.id
        expected = "[{}] ({}) {}".format(cls_name, id, self.test_obj.to_dict())
        output = StringIO()
        sys.stdout = output
        print(self.test_obj)
        sys.stdout = sys.__stdout__
        self.assertEqual(output.getvalue().strip("\n"), expected)

    def test_to_dict_returns_a_dictionary_of_attributes(self):
        """to_dict should return a dictionary containing all key/value of
        self.__dict__
        """
        temp_dict = self.test_obj.to_dict()
        self.assertIsInstance(temp_dict, dict)
        keys = temp_dict.keys()

        for k, v in self.test_obj.__dict__.items():
            if k == "_sa_instance_state":
                continue
            self.assertIn(k, keys)
            if not isinstance(self.test_obj.__dict__[k], datetime):
                self.assertEqual(temp_dict[k], v)

    def test_to_dict_has_a_key_with_the_class_name(self):
        """to_dict must have a key of __class__ with a value of the classes
        name
        """
        temp_dict = self.test_obj.to_dict()
        self.assertIn("__class__", temp_dict.keys())
        self.assertEqual(temp_dict["__class__"], Amenity.__name__)


if __name__ == "__main__":
    unittest.main()
