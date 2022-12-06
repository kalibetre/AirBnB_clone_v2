#!/usr/bin/python3
"""Module test_amenity

This Module contains a tests for Amenity Class
"""

import inspect
import os
import unittest
from io import StringIO
from unittest.mock import patch

import pep8
import pycodestyle

import console

HBNBCommand = console.HBNBCommand


class TestConsoleStyle(unittest.TestCase):
    def test_pep8_console(self):
        """Pep8 console.py"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["console.py"])
        self.assertEqual(p.total_errors, 0, 'fix Pep8')

    def test_pycodestyle(self):
        """Tests compliance with pycodestyle"""
        style = pycodestyle.StyleGuide(quiet=False)
        result = style.check_files(
            ["console.py", "tests/test_console.py"])
        self.assertEqual(result.total_errors, 0)


class TestBaseModelDocsAndStyle(unittest.TestCase):
    """Tests Base class for documentation and style conformance"""

    def test_module_docstring(self):
        """Tests whether the module is documented"""
        self.assertTrue(len(console.__doc__) >= 1)

    def test_class_docstring(self):
        """Tests whether the class is documented"""
        self.assertTrue(len(console.__doc__) >= 1)

    def test_methods_docstring(self):
        """Tests whether the class methods are documented"""
        funcs = inspect.getmembers(console, inspect.isfunction)
        for func in funcs:
            self.assertTrue(len(func[1].__doc__) >= 1)

    def test_class_name(self):
        """Test whether the class name is correct"""
        self.assertEqual(HBNBCommand.__name__, "HBNBCommand")


class TestConsoleBasic(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """sets up the test console"""
        cls.cmd = HBNBCommand()

    @classmethod
    def tearDownClass(cls) -> None:
        """removes the cmd object"""
        del cls.cmd

    def tearDown(cls):
        """removes the file.json temporary file"""
        if os.path.exists('file.json'):
            os.remove('file.json')

    def test_emptyline(self):
        """Test empty line input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cmd.onecmd("\n")
            self.assertEqual('', f.getvalue())

    def test_quit(self):
        """Test quit command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cmd.onecmd("quit")
            self.assertEqual('', f.getvalue())

    def test_show_prints_class_name_error(self):
        """tests the show command class name error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('show')
            self.assertEqual("** class name missing **\n",
                             output.getvalue())

    def test_show_prints_class_does_not_exist(self):
        """tests the show command class not found error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('show BModel')
            self.assertEqual("** class doesn't exist **\n",
                             output.getvalue())

    def test_show_displays_an_object(self):
        """tests the show shows an instance"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'show BaseModel {id}')
            self.assertIn("BaseModel", output.getvalue())

    def test_show_prints_instance_not_found(self):
        """tests the show command displays instance not found error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('show BaseModel testid')
            self.assertEqual("** no instance found **\n",
                             output.getvalue())

    def test_destroy_prints_class_name_error(self):
        """tests the destroy command class name error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('destroy')
            self.assertEqual("** class name missing **\n",
                             output.getvalue())

    def test_destroy_prints_class_does_not_exist(self):
        """tests the destroy command class not found error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('destroy BModel')
            self.assertEqual("** class doesn't exist **\n",
                             output.getvalue())

    def test_destroy_prints_instance_id_missing(self):
        """tests the destroy command prints instance id missing error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('destroy BaseModel')
            self.assertIn("** instance id missing **\n", output.getvalue())

    def test_destroy_prints_instance_not_found(self):
        """tests the destroy command prints instance not found error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('destroy BaseModel adfadfadf')
            self.assertIn("** no instance found **", output.getvalue())

    def test_destroy_deletes_an_object(self):
        """tests the destroy deletes a instance"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'destroy BaseModel {id}')
            self.cmd.onecmd(f'show BaseModel {id}')
            self.assertIn("** no instance found **", output.getvalue())

    def test_all_displays_instance_objects(self):
        """tests the all shows instance objects"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            self.cmd.onecmd('create BaseModel')
            self.cmd.onecmd(f'all')
            self.assertIn("BaseModel", output.getvalue())
            self.assertGreaterEqual(output.getvalue().count("BaseModel"), 2)

    def test_all_displays_class_instance_objects(self):
        """tests the all shows instance objects"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            self.cmd.onecmd('create User')
            self.cmd.onecmd(f'all User')
            self.assertIn("User", output.getvalue())
            self.assertNotIn("BaseModel", output.getvalue())


class TestConsoleCreate(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """sets up the test console"""
        cls.cmd = HBNBCommand()

    @classmethod
    def tearDownClass(cls) -> None:
        """removes the cmd object"""
        del cls.cmd

    def tearDown(cls):
        """removes the file.json temporary file"""
        if os.path.exists('file.json'):
            os.remove('file.json')

    def test_create_prints_class_name_error(self):
        """tests the create command class name error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create')
            self.assertEqual("** class name missing **\n",
                             output.getvalue())

    def test_create_prints_class_does_not_exist(self):
        """tests the create command class not found error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BModel')
            self.assertEqual("** class doesn't exist **\n",
                             output.getvalue())

    def test_create_creates_an_object(self):
        """tests the create creates an instance"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            id = output.getvalue()
            self.assertNotIn(id, [None, ""])

        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd(f'show BaseModel {id}')
            self.assertIn(id.strip('\n'), output.getvalue())

    def test_create_creates_an_obj_with_args(self):
        """tests the create cmd accepts args"""
        with patch("sys.stdout", new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel name="test"')
            id = output.getvalue
            self.assertNotIn(id, [None, ""])

    def test_create_creates_an_obj_with_args_check_arg(self):
        """tests the create cmd accepts args and sets them correctly"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create Review text="Good Review"')
            id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'show Review {id}')
            self.assertIn("Review", output.getvalue())
            self.assertIn("Good Review", output.getvalue())

    def test_create_creates_an_obj_skips_invalid_args(self):
        """tests the create cmd accepts args and sets them correctly"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create Review text=Good')
            id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'show Review {id}')
            self.assertIn("Review", output.getvalue())
            self.assertNotIn("Good", output.getvalue())

    def test_create_creates_an_obj_reads_int(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create Place number_rooms=1234')
            id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'show Place {id}')
            self.assertIn("Place", output.getvalue())
            self.assertIn("1234", output.getvalue())

    def test_create_creates_an_obj_reads_float(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd(
                'create Place latitude=37.773972 longitude=-122.431297')
            id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'show Place {id}')
            self.assertIn("Place", output.getvalue())
            self.assertIn("37.773972", output.getvalue())
            self.assertIn("-122.431297", output.getvalue())


class TestConsoleUpdate(unittest.TestCase):
    """Tests the console app"""
    @classmethod
    def setUpClass(cls) -> None:
        """sets up the test console"""
        cls.cmd = HBNBCommand()

    @classmethod
    def tearDownClass(cls) -> None:
        """removes the cmd object"""
        del cls.cmd

    def tearDown(cls):
        """removes the file.json temporary file"""
        if os.path.exists('file.json'):
            os.remove('file.json')

    def test_update_prints_class_name_error(self):
        """tests the update command class name error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('update')
            self.assertEqual("** class name missing **\n",
                             output.getvalue())

    def test_update_prints_class_does_not_exist(self):
        """tests the update command class not found error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('update BModel')
            self.assertEqual("** class doesn't exist **\n",
                             output.getvalue())

    def test_update_prints_instance_id_missing(self):
        """tests the update command prints instance id missing error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('update BaseModel')
            self.assertIn("** instance id missing **\n", output.getvalue())

    def test_update_prints_instance_not_found(self):
        """tests the update command prints instance not found error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('update BaseModel adfadfadf')
            self.assertIn("** no instance found **", output.getvalue())

    def test_update_attr_name_missing_error(self):
        """test update command shows attr name missing error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'update BaseModel {id}')
            self.assertIn("** attribute name missing **", output.getvalue())

    def test_update_attr_value_missing_error(self):
        """test update command shows attr val missing error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'update BaseModel {id} fname')
            self.assertIn("** value missing **", output.getvalue())

    def test_update_updates_instance(self):
        """test update command shows attr val missing error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create State')
            id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'update State {id} name example_state')
            self.cmd.onecmd(f'show State {id}')
            self.assertIn('name', output.getvalue())
            self.assertIn('example_state', output.getvalue())


class TestConsoleAdvancedShowDestroy(unittest.TestCase):
    """Tests the console app"""
    @classmethod
    def setUpClass(cls) -> None:
        """sets up the test console"""
        cls.cmd = HBNBCommand()

    @classmethod
    def tearDownClass(cls) -> None:
        """removes the cmd object"""
        del cls.cmd

    def tearDown(cls):
        """removes the file.json temporary file"""
        if os.path.exists('file.json'):
            os.remove('file.json')

    def test_classname_all_prints_class_does_not_exist(self):
        """tests the update command class not found error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('BModel.all()')
            self.assertEqual("** class doesn't exist **\n",
                             output.getvalue())

    def test_classname_all_displays_instance_objects(self):
        """tests the all shows instance objects"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            self.cmd.onecmd('create BaseModel')
            self.cmd.onecmd('BaseModel.all()')
            self.assertIn("BaseModel", output.getvalue())
            self.assertGreaterEqual(output.getvalue().count("BaseModel"), 2)

    def test_classname_count_prints_class_does_not_exist(self):
        """tests the update command class not found error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('BModel.count()')
            self.assertEqual("** class doesn't exist **\n",
                             output.getvalue())

    def test_classname_count_displays_instance_objects(self):
        """tests the all shows instance objects"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create Place')
            self.cmd.onecmd('create Place')
            self.cmd.onecmd('create Place')
            self.cmd.onecmd('create Place')
            self.cmd.onecmd('create Place')
            self.cmd.onecmd('Place.count()')
            self.assertIn('5', output.getvalue())

    def test_classname_show_prints_class_does_not_exist(self):
        """tests the update command class not found error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('BModel.show()')
            self.assertEqual("** class doesn't exist **\n",
                             output.getvalue())

    def test_classname_show_displays_an_object(self):
        """tests the show shows an instance"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'BaseModel.show("{id}")')
            self.assertIn("BaseModel", output.getvalue())

    def test_classname_destroy_prints_class_does_not_exist(self):
        """tests the update command class not found error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('BModel.destroy()')
            self.assertEqual("** class doesn't exist **\n",
                             output.getvalue())

    def test_classname_destroy_deletes_an_object(self):
        """tests the destroy deletes a instance"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'BaseModel.destroy("{id}")')
            self.cmd.onecmd(f'show BaseModel {id}')
            self.assertIn("** no instance found **", output.getvalue())


class TestConsoleAdvancedUpdate(unittest.TestCase):
    """Tests the console app"""
    @classmethod
    def setUpClass(cls) -> None:
        """sets up the test console"""
        cls.cmd = HBNBCommand()

    @classmethod
    def tearDownClass(cls) -> None:
        """removes the cmd object"""
        del cls.cmd

    def tearDown(cls):
        """removes the file.json temporary file"""
        if os.path.exists('file.json'):
            os.remove('file.json')

    def test_classname_update_prints_class_does_not_exist(self):
        """tests the update command class not found error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('BModel.update()')
            self.assertEqual("** class doesn't exist **\n",
                             output.getvalue())

    def test_classname_update_prints_no_instance_found(self):
        """tests the update command instance not found error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('BaseModel.update("123")')
            self.assertEqual("** no instance found **\n",
                             output.getvalue())

    def test_classname_update_prints_att_missing(self):
        """test update command shows attr name missing error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'BaseModel.update("{id}")')
            self.assertIn("** attribute name missing **", output.getvalue())

    def test_update_attr_value_missing_error(self):
        """test update command shows attr val missing error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'BaseModel.update("{id}", "fname")')
            self.assertIn("** value missing **", output.getvalue())

    def test_classname_update_updates_instance(self):
        """test update command shows attr val missing error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create Review')
            id = output.getvalue().strip('\n')
            self.cmd.onecmd(f'Review.update("{id}", "rev_k", "rev_v")')
            self.cmd.onecmd(f'show Review {id}')
            self.assertIn('rev_k', output.getvalue())
            self.assertIn('rev_v', output.getvalue())

    def test_classname_update_updates_instance_with_dict(self):
        """test update command shows attr val missing error"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create Amenity')
            id = output.getvalue().strip('\n')
            dict_att = "{ 'name' : 'amne', 'rev_k' : 'rev_v' }"
            self.cmd.onecmd(f'Amenity.update("{id}", {dict_att})')
            self.cmd.onecmd(f'show Amenity {id}')
            self.assertIn('name', output.getvalue())
            self.assertIn('amne', output.getvalue())
            self.assertIn('rev_k', output.getvalue())
            self.assertIn('rev_v', output.getvalue())
