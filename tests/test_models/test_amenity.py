#!/usr/bin/python3
"""Defines unittests for models/amenity.py.

Unittest classes:
    TestAmenity_instantiation
    TestAmenity_save
    TestAmenity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Amenity class."""

    def test_for_no_args_init(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_for_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_for_is_id_public_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_for_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_for_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_for_name_is_public_class_attribute(self):
        a = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", a.__dict__)

    def test_for_two_amenities_unique_ids(self):
        am1 = Amenity()
        am2 = Amenity()
        self.assertNotEqual(am1.id, am2.id)

    def test_for_two_amenities_different_created_at(self):
        a1 = Amenity()
        sleep(0.04)
        a2 = Amenity()
        self.assertLess(a1.created_at, a2.created_at)

    def test_for_two_amenities_different_updated_at(self):
        am1 = Amenity()
        sleep(0.04)
        am2 = Amenity()
        self.assertLess(am1.updated_at, am2.updated_at)

    def test_for_str_rep(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        am = Amenity()
        am.id = "1234567890"
        am.created_at = am.updated_at = dt
        amstr = am.__str__()
        self.assertIn("[Amenity] (1234567890)", amstr)
        self.assertIn("'id': '1234567890'", amstr)
        self.assertIn("'created_at': " + dt_repr, amstr)
        self.assertIn("'updated_at': " + dt_repr, amstr)

    def test_for_args_unused(self):
        am = Amenity(None)
        self.assertNotIn(None, am.__dict__.values())

    def test_for_instantiation_with_kwargs(self):
        """instantiation with kwargs test_for method"""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        am = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(am.id, "345")
        self.assertEqual(am.created_at, dt)
        self.assertEqual(am.updated_at, dt)

    def test_for_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
    """Unittests for testing save method of the Amenity class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("storage.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("storage.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "storage.json")
        except IOError:
            pass

    def test_for_one_save(self):
        am = Amenity()
        sleep(0.04)
        first_updated_at = am.updated_at
        am.save()
        self.assertLess(first_updated_at, am.updated_at)

    def test_for_two_saves(self):
        am = Amenity()
        sleep(0.04)
        first_updated_at = am.updated_at
        am.save()
        second_updated_at = am.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.04)
        am.save()
        self.assertLess(second_updated_at, am.updated_at)

    def test_for_save_with_arg(self):
        am = Amenity()
        with self.assertRaises(TypeError):
            am.save(None)

    def test_for_save_updates_file(self):
        am = Amenity()
        am.save()
        amid = "Amenity." + am.id
        with open("storage.json", "r") as f:
            self.assertIn(amid, f.read())


class TestAmenity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Amenity class."""

    def test_for_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_for_to_dict_contains_correct_keys(self):
        am = Amenity()
        self.assertIn("id", am.to_dict())
        self.assertIn("created_at", am.to_dict())
        self.assertIn("updated_at", am.to_dict())
        self.assertIn("__class__", am.to_dict())

    def test_for_to_dict_contains_added_attributes(self):
        am = Amenity()
        am.middle_name = "Holberton"
        am.my_number = 98
        self.assertEqual("Holberton", am.middle_name)
        self.assertIn("my_number", am.to_dict())

    def test_for_to_dict_datetime_attributes_are_strs(self):
        am = Amenity()
        am_dict = am.to_dict()
        self.assertEqual(str, type(am_dict["id"]))
        self.assertEqual(str, type(am_dict["created_at"]))
        self.assertEqual(str, type(am_dict["updated_at"]))

    def test_for_to_dict_output(self):
        dt = datetime.today()
        am = Amenity()
        am.id = "1253456"
        am.created_at = am.updated_at = dt
        tdict = {
            "id": "1253456",
            "__class__": "Amenity",
            "created_at": dt.isoformat(),
            "updated_at": dt.isoformat(),
        }
        self.assertDictEqual(am.to_dict(), tdict)

    def test_for_contrast_to_dict_dunder_dict(self):
        am = Amenity()
        self.assertNotEqual(am.to_dict(), am.__dict__)

    def test_for_to_dict_with_arg(self):
        am = Amenity()
        with self.assertRaises(TypeError):
            am.to_dict(None)


if __name__ == "__main__":
    unittest.main()
