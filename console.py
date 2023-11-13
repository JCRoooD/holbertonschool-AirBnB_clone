#!/usr/bin/python3
"""entry point of the command interpreter
def do_quit = exit the program
def do_EOF = exit the program
def emptyline = do nothing when emptyline + ENTER
def do_create = create a new instance of BaseModel
def do_show = print the string representation of an instance
def do_destroy = delete an instance based on the class name and id
def do_all = print all string representation of all instances
def do_update = update an instance based on the class name and id
"""

import cmd
from models.base_model import BaseModel
from models import storage
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """defines the class HBNBCommand"""
    prompt = '(hbnb) '

    def do_quit(self, arg):
        """Exit the program with quit"""
        return True

    def help_quit(self):
        """help quit function"""
        print("Quit command to exit the program")

    def do_EOF(self, arg):
        """Exit the program"""
        return True

    def help_EOF(self):
        """help enf of file function"""
        print("EOF command to exit the program")

    def emptyline(self):
        """do nothing when receiving an empty line followed by ENTER"""
        pass

    def do_create(self, arg):
        """create a new instance of BaseModel"""
        if not arg:
            print("** class name missing **")
            return
        arg_list = arg.split()
        if arg_list[0] not in FileStorage.CLASS_DICT:
            print("** class doesn't exist **")
            return
        new_instance = FileStorage.CLASS_DICT[arg_list[0]]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """print the string representation of an instance"""
        arg = arg.split()
        class_name = arg[0] if arg else None
        new_instance_id = arg[1] if len(arg) > 1 else None
        if class_name is None:
            print("** class name missing **")
            return
        if class_name not in FileStorage.CLASS_DICT:
            print("** class doesn't exist **")
            return
        if new_instance_id is None:
            print("** instance id missing **")
            return
        key = "{}.{}".format(class_name, new_instance_id)
        if key not in storage._FileStorage__objects:
            print("** no instance found **")
            return
        print(storage._FileStorage__objects[key])

    def do_destroy(self, arg):
        """delete an instance based on the class name and id"""
        arg = arg.split()
        class_name = arg[0] if arg else None
        new_instance_id = arg[1] if len(arg) > 1 else None
        if class_name is None:
            print("** class name missing **")
            return
        if class_name not in FileStorage.CLASS_DICT:
            print("** class doesn't exist **")
            return
        if new_instance_id is None:
            print("** instance id missing **")
            return
        key = "{}.{}".format(class_name, str(new_instance_id))
        if key in storage._FileStorage__objects:
            del storage._FileStorage__objects[key]
            storage.save()
        else:
            print("** no instance found **")
            return

    def do_all(self, arg):
        """print all string representation of all instances"""
        arg = arg.split()
        class_name = arg[0] if arg else None
        objs_to_print = []
        if class_name and class_name not in FileStorage.CLASS_DICT:
            print("** class doesn't exist **")
            return
        for key, value in storage._FileStorage__objects.items():
            if not class_name or key.split(".")[0] == class_name:
                objs_to_print.append(str(value))
        print(objs_to_print)

    def do_update(self, arg):
        """update an instance based on the class name and id"""
        arg_list = arg.split()
        if len(arg_list) == 0:
            print("** class name missing **")
            return
        if arg_list[0] not in FileStorage.CLASS_DICT:
            print("** class doesn't exist **")
            return
        if len(arg_list) == 1:
            print("** instance id missing **")
            return
        key = "{}.{}".format(arg_list[0], arg_list[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(arg_list) == 2:
            print("** attribute name missing **")
            return
        if len(arg_list) == 3:
            print("** value missing **")
            return
        setattr(storage.all()[key], arg_list[2], arg_list[3])
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
