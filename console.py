#/usr/bin/env python3

"""

    HBNBCommand - command Line tool for Airbnb clone
    Autors:
    - Andres Camilo Tobon Mejia : github @Deepzirox
    - Pon tu informacion plis xd

"""

import cmd
import models
import shlex
from json import loads, dumps
from models import classes, actions
from models.base_model import BaseModel
from models.city import City
from models.user import User
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.place import Place

# Preprocessor (onecmd) functions
def pre_method_validator(arg):
    if "count()" not in arg and "all()" not in arg:
        return False
    else:
        return True

def pre_all_handler(parsed):
    jsonList = []
    store = models.storage.all()
    for values in store.values():
        if  values.to_dict()['__class__'] in parsed:
            jsonList.append(values)
    else:
        if jsonList == []:
            print('** No such model: {}'.format(parsed[0]))
        else:
            print(jsonList)

def pre_count_handler(parsed):
    instances = 0
    store = models.storage.all()
    for values in store.values():
        if  values.to_dict()['__class__'] in parsed:
            instances += 1
    else:
        if instances == 0:
            print('** No such instance: {}'.format(parsed[0]))
        else:
            print(instances)

# --------------------------


class HBNBCommand(cmd.Cmd):
    """Interprete de comandos"""
    prompt = "(hbnb) "
    classDict = {
        "BaseModel": BaseModel,
        "User" : User,
        "City" : City,
        "State" : State,
        "Review" : Review,
        "Amenity" : Amenity,
        "Place" : Place
    }
    def default(self, line):
        #print('default({})'.format(line))
        '''
            Method that checks if the input contains dot, if false
            print the message error
        '''
        
        if '.' not in line:
            return cmd.Cmd.default(self, line)

    def onecmd(self, line):
        '''
        # advanced lol
        Preproccesor of the command Line, all arguments will be here after executing
        so we can validate if there's any ocurrence with <class> . <method> of the existing
        classes
        '''
        if '.' in line and line.split(' ')[0] not in actions:
            parsed = line.split('.')
            if pre_method_validator(parsed):
                if parsed[1] == "all()":
                    pre_all_handler(parsed)
                elif parsed[1] == "count()":
                    pre_count_handler(parsed)
            else:
                return cmd.Cmd.default(self, line)

        return cmd.Cmd.onecmd(self, line)

    def do_create(self, args):
        """
        Create - Create new model of a class
        -----------------------------------------------------
        available models:
        - BaseModel
        - Amenity
        - City
        - Place
        - Review
        - User
        - State
        -----------------------------------------------------
        @ usage - > <command> <model> {ex: create BaseModel}

        """
        if len(args) < 2:
            print('** class name missing **')
        else:
            try:
                new = eval(args)()
                new.save()
                print(new.id)
            except (NameError, SyntaxError):
                print("** class doesn't exist **")
                pass
    
    def do_show(self, args):
        """
        show - show Python object representation of json object
        -----------------------------------------------------
        available models:
        - BaseModel
        - Amenity
        - City
        - Place
        - Review
        - User
        - State
        -----------------------------------------------------
        @ usage - > <command> <model> <id> {ex: show BaseModel 123asd1272bn28dn}
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


    def do_all(self, arg):
        """
        all - show all list of json objects
        -----------------------------------------------------
        available models:
        - BaseModel
        - Amenity
        - City
        - Place
        - Review
        - User
        - State
        -----------------------------------------------------
        @ usage - > <command> <model> {ex: all BaseModel}
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
            if arg not in classes:
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
            if instancia not in classes:
                print("** class doesn't exist **")
                return 0
            # !! aca se debe encontrar una nueva forma de validar instancia
            if key in tmp_dictionary:
                del tmp_dictionary[key]
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

        key = "{}.{}".format(args[0], args[1])
        try:
            objects[key].__dict__[args[2]] = args[3]
            models.storage.save()
        except:
            print("** no instance found **")
            return 0


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
