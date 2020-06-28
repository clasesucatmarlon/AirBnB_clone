import cmd
from json import loads, dumps
from models.base_model import BaseModel
from models import classes
import models
import shlex

class HBNBCommand(cmd.Cmd):
    """Interprete de comandos"""
    classDict = {
            "BaseModel": BaseModel,
        }
    prompt = "(hbnb) "

    def do_create(self, args):
        """
        Create new model of a class 'Base model'
        """
        if len(args) < 2:
            print('** class name missing **')
        else:
            try:
                new = eval(args)()
                new.save()
                print(new.id)
            except NameError:
                print("** class doesn't exist **")
                pass
    
    def do_show(self, args):
        """
        Print the string representation of the instance in Json File
        """
        tmp_dictionary = {}
        parsed = args.split(' ')
        if parsed == ['']:
            print('** class name missing **')
        elif len(parsed) == 1:
            print('** instance id missing *')
        if len(parsed) == 2:
            instancia, instance_id = parsed[0], parsed[1]
            with open('file.json', 'r') as jsonfile:
                tmp_dictionary = loads(jsonfile.read())
            key = instancia + '.' + instance_id
            try:
                new_ins = eval(instancia)
            except:
                print("** class doesn't exist **")
                return 0
            try:
                new_ins = eval(instancia)(**tmp_dictionary[key])
                print(new_ins)
            except:
                print('** no instance found **')
                return 0
        else:
            pass

    def do_destroy(self, arg):
        'Deletes an instance based on the class name and id'
        args = parse(arg)
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classDict:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            objects = models.storage.all()
            for k, v in objects.items():
                obj_id = objects[k].id
                obj_class = objects[k].__class__.__name__
                if obj_id == args[1] and args[0] == obj_class:
                    del objects[k]
                    models.storage.save()
                    break
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """
        Print all string representation of all instances in Json File
        """
        aux_list = []
        with open('file.json', 'r') as jsonfile:
            tmp_dictionary = loads(jsonfile.read())
        for key, value in tmp_dictionary.items():
            tmp_str = str(key + ' ' + str(value))
            aux_list.append(tmp_str)
        if len(arg) == 0:
            print(aux_list)
        else:
            if arg not in class_names:
                print("** class doesn't exist **")
                return 0
            else:
                print(aux_list)
    
    def do_destroy(self, args):
        tmp_dictionary = {}
        parsed = args.split(' ')
        if parsed == ['']:
            print('** class name missing **')
        elif len(parsed) == 1:
            print('** instance id missing *')
        if len(parsed) == 2:
            instancia, instance_id = parsed[0], parsed[1]
            tmp_dictionary = models.storage.all()
            key = instancia + '.' + instance_id
            if instancia not in class_names:
                print("** class doesn't exist **")
                return 0
            try:
                eval(instancia)(**tmp_dictionary[key])
            except:
                print('** no instance found **')
                return 0
            if key in tmp_dictionary:
                print("Encontrado")
                del tmp_dictionary[key]
                models.storage.save()

    def do_update(self, args):
        parsed = args.split(' ')

        if parsed == ['']:
            print("** class name missing **")
            return 0

        if len(parsed) < 2:
            print("** instance id missing **")
            return 0

        if parsed[0] not in class_names:
            print("** class doesn't exist **")
            return 0

        # test instance
        instance_dict = models.storage.all()
        key = "{}.{}".format(parsed[0], parsed[1])
        if key not in instance_dict:
            print("** no instance found **")
            return 0

        if len(parsed) < 3:
            print('** attribute name missing **')
            return 0
        elif len(parsed) < 4:
            print('** value missing **')
        else:
            parsed = parsed[0:4]
            with open('file.json', 'r+') as file:
                tmp_d = loads(file.read())
                tmp_d[key].update({parsed[2] : parsed[3]})
            with open('file.json', 'w') as file:
                file.write(dumps(tmp_d))
                models.storage.save()

    def do_update(self, arg):
        'Updates an instance based on the class name and id'
        args = parse(arg)
        objects = models.storage.all()
        if not args:
            print("** class name missing **")
            return 0
        elif args[0] not in classes:
            print("** class doesn't exist **")
            return 0
        elif len(args) < 2:
            print("** instance id missing **")
            return 0
        elif len(args) < 3:
            print("** attribute name missing **")
            return 0
        elif len(args) < 4:
            print("** value missing **")
            return 0
        else:
            found = False
        
        key = "{}.{}".format(args[0], args[1])
        try:
            objects[key].__dict__[args[2]] = args[3]
            models.storage.save()
        except:
            print("** no instance found **")
            return 0
        """
            for k, v in objects.items():
                obj_id = objects[k].id
                if obj_id == args[1]:
                    found = True
                    obj_dict = objects[k].__dict__
                    input_value = args[3]
                    obj_dict[args[2]] = input_value
                    models.storage.save()
            if not found:
                print("** no instance found **")
        """

    def do_quit(self, args):
        """
        Quit command to exit the program
        """
        return True
    
    def do_EOF(self, args):
        """
        Quit command to exit the program
        """
        return True
    
    def emptyline(self):
        """
        Dont do any action
        """
        pass

def parse(arg):
        """
        Parse arguments and split by space
        """
        return tuple(shlex.split(arg))

if __name__ == '__main__':
    interprete = HBNBCommand()
    interprete.cmdloop()
