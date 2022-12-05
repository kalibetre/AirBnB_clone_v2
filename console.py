#!/usr/bin/python3
""" Console Module """
import cmd
import importlib
import json
import re
import sys
from typing import cast

from models.__init__ import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    prompt = "(hbnb) "

    def do_quit(self, command):
        """Exists to the HBNB console"""
        return True

    def do_EOF(self, arg):
        """Exist the console using Ctrl + D or end of file"""
        print()
        return True

    def emptyline(self):
        """prevents default behavior of cmd to ignore running command on
        empty line plus enter
        """
        pass

    def do_create(self, line):
        """Creates a class of any type
        [Usage]: create <className>"""
        obj_cls = self.get_class_from_input(line)
        if obj_cls is not None:
            new_obj = obj_cls(self.read_params(line))
            new_obj.save()
            print(new_obj.id)

    def do_show(self, line):
        """Shows an individual instance of a class
        [Usage]: show <className> <objectId>\n"""
        key = self.get_obj_key_from_input(line)
        if key is None:
            return

        saved_obj = storage.all().get(key, None)
        if saved_obj is None:
            print("** no instance found **")
        else:
            print(saved_obj)

    def do_destroy(self, line):
        """Destroys an individual instance of a class
        [Usage]: destroy < className > <objectId >\n"""
        key = self.get_obj_key_from_input(line)
        if key is None:
            return

        saved_obj = storage.all().pop(key, None)
        if saved_obj is None:
            print("** no instance found **")
        else:
            storage.save()

    def do_all(self, line):
        """Shows all objects, or all of a class
        print("[Usage]: all <className>\n"""
        if len(line.split()) == 0:
            result = storage.all().values()
        else:
            obj_cls = self.get_class_from_input(line)
            if obj_cls is None:
                return
            result = list(filter(lambda item: isinstance(
                item, obj_cls), storage.all().values()))

        print([str(item) for item in result])

    def do_count(self, line):
        """Count current number of class instances
        Usage: count <class_name>"""
        obj_cls = self.get_class_from_input(line)
        if obj_cls is None:
            return
        result = list(filter(lambda item: isinstance(
            item, obj_cls), storage.all().values()))

        print(len(result))

    def do_update(self, line):
        """ Updates a certain object with new info
        Usage: update <className> <id> <attName> <attVal>\n"""
        key = self.get_obj_key_from_input(line)
        if key is None:
            return

        saved_obj = storage.all().get(key, None)
        if saved_obj is None:
            print("** no instance found **")
        else:
            attr_name, attr_val = self.get_attribute_name_value_pair(line)
            if attr_name is None or attr_val is None:
                return

            if hasattr(saved_obj, attr_name):
                attr_type = type(getattr(saved_obj, attr_name))
                attr_val = cast(attr_type, attr_val)
            setattr(saved_obj, attr_name, attr_val)
            saved_obj.save()

    def default(self, line):
        if '.' not in line:
            return super().default(line)

        cls_name, func_name, id, args = self.parse_input(line)

        if cls_name is None:
            print("** class name missing **")
            return

        if func_name is None:
            print(
                "** incorrect function (all, count, show, destroy & update) **"
            )
            return

        id = id if id is not None else ""

        if func_name == "count":
            self.do_count(cls_name)
        elif func_name == "all":
            self.do_all(cls_name)
        elif func_name == "show":
            self.do_show(f"{cls_name} {id}")
        elif func_name == "destroy":
            self.do_destroy(f"{cls_name} {id}")
        elif func_name == "update":
            if isinstance(args, str):
                args = " ".join([id, args])
                self.do_update(f"{cls_name} {args}")
            elif isinstance(args, dict):
                for k, v in args.items():
                    self.do_update(f"{cls_name} {id} {k} {v}")
            else:
                self.do_update(f"{cls_name}")

    def parse_input(self, input):
        args = input.split('.')
        if len(args) != 2:
            return None, None, None, None

        cls_name = args[0]
        valid_commands = ["all", "count", "show", "destroy", "update"]
        if '(' not in args[1] or ')' not in args[1]:
            return cls_name, None, None, None

        func_w_args = args[1].split("(")
        if len(func_w_args) == 0 or func_w_args[0] not in valid_commands:
            return cls_name, None, None, None
        func_name = func_w_args[0]
        f_args = func_w_args[1].strip(')')

        id_match = re.match(r'(^\"[\w-]+\")', f_args)
        if len(f_args) == 0 or id_match is None:
            return cls_name, func_name, None, None

        id = id_match.group()
        f_args = f_args.replace(id, "")
        id = id.strip('"')

        if len(f_args) == 0:
            return cls_name, func_name, id, ''

        dict_match = re.match(r'(\{.*\})', f_args.strip(", "))
        if dict_match is not None:
            dict_str = dict_match.group().replace("'", '"')
            return (
                cls_name, func_name, id, dict(json.loads(dict_str))
            )

        f_args = f_args.replace(',', ' ')
        return cls_name, func_name, id, str(f_args)

    def get_class_from_input(self, line):
        """parses and returns class from input"""
        if line is None or len(line.strip()) == 0:
            print("** class name missing **")
            return None

        return self.get_class(line.split()[0])

    def get_class(self, name):
        """ returns a class from models module using its name"""
        try:
            sub_module = re.sub('(?!^)([A-Z]+)', r'_\1', name).lower()
            module = importlib.import_module(f"models.{sub_module}")
            return getattr(module, name)
        except Exception:
            print("** class doesn't exist **")
            return None

    def get_obj_key_from_input(self, line):
        """parses and returns object key from input"""
        obj_cls = self.get_class_from_input(line)
        if obj_cls is None:
            return None
        id = self.get_id_from_input(line)
        if id is None:
            return None
        return f"{obj_cls.__name__}.{id}"

    def get_id_from_input(self, line):
        """parses and returns id from input"""
        cmds = line.split()
        if len(cmds) < 2:
            print("** instance id missing **")
            return None
        return cmds[1]

    def get_attribute_name_value_pair(self, line):
        """parses and returns a tuple of attribute name and value"""
        cmds = line.split()

        attr_name = None if len(cmds) < 3 else cmds[2].strip('"')
        if attr_name is None:
            print("** attribute name missing **")
            return None, None

        attr_val = None if len(cmds) < 4 else cmds[3].strip('"')
        if attr_val is None:
            print("** value missing **")
            return attr_name, None

        return attr_name, attr_val

    def to_number(self, value):
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            return None

    def read_params(self, args: str):
        params = {}
        raw_params = args.split()
        if (len(raw_params) <= 1):
            return None

        for param in raw_params:
            if ("=" in param):
                key, value = tuple(param.split("="))
                if None in [key, value]:
                    continue
                value = value.replace('"', '') if value.startswith(
                    '"') else to_number(value)
                if value is None:
                    continue
                params[key] = value

        return params


if __name__ == "__main__":
    HBNBCommand().cmdloop()
