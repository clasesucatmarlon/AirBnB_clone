#/usr/bin/env python3

"""

    HBNBdata - data line tool for Airbnb clone
    Autors:
    - Andres Camilo Tobon Mejia : github @Deepzirox
    - Pon tu informacion plis xd

"""
import re
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
def pre_parse(arg, quoating=False):
    method, value = "", ""
    flag = False
    
    if not arg:
        return (False, False)
    if arg[-1] == ')':
        for char in arg:
            if char == '(' or char == ')':
                flag = True
                continue
            if flag is True:
                if not quoating:
                    if char == '"':
                        continue
                value += char
            if flag is False:
                method += char

    return (method, value)

def pre_method(arg):
    method = ""
    if "count()" not in arg and "all()" not in arg:
        method = pre_parse(arg[1])
        if method[0] not in actions:
            return False
        else:
            return True
    else:
        return True

def pre_all(parsed):
    jsonList = []
    store = models.storage.all()
    for values in store.values():
        if  values.to_dict()['__class__'] in parsed:
            jsonList.append(values)
    else:
        if jsonList == []:
            print("** no instance found **")
        else:
            print(jsonList)

def pre_count(parsed):
    instances = 0
    store = models.storage.all()
    for values in store.values():
        if  values.to_dict()['__class__'] in parsed:
            instances += 1
    else:
        if instances == 0:
            print("** no instance found **")
        else:
            print(instances)

def pre_show(classname, method_value):
    if classname not in classes:
        pass
    else:
        store = models.storage.all()
        try:
            key = "{}.{}".format(classname, method_value[1])
            print(str(store[key]))
        except KeyError:
            print("** no instance found **")

def pre_destroy(classname, method_value):
    if classname not in classes:
        print("** class doesn't exist **")
    else:
        store = models.storage.all()
        keys = list(store.keys())
        key = "{}.{}".format(classname, method_value[1])
        if key not in keys:
            print('** no instance found **')
        else:
            del store[key]
            models.storage.save()

# Update handler functions -----------

def check(idx_args, data):
    '''
    tuple (
        [0] Key correct: True else False
        [1] Is a dict: True else False
    )
    '''
    check_results = [True, True]
    valid_data = [0, 0]
    keys = list(models.storage.all().keys())
    id_obj = data[0][0:idx_args[0]]
    if id_obj[0] == '"' and id_obj[-1] == '"':
        id_obj = id_obj[1:-1]

    key = "{}.{}".format(data[1], id_obj)
    if key not in keys:
        check_results[0] = False
    
    # check if works for key/value or dictionary mode
    if len(idx_args) == 1:
        hi_dict = data[0][idx_args[0] + 1:].strip()
        try:
            hi_dict = eval(hi_dict)
            if type(hi_dict) not in [dict]:
                raise TypeError
            valid_data[0] = hi_dict
            valid_data[1] = key
            return (check_results, valid_data)
        except:
            check_results[1] = False
            return (check_results, None)
    elif len(idx_args) == 2:
        d_key = data[0][idx_args[0] + 1:idx_args[1]].strip()
        d_value = data[0][idx_args[1] + 1:].strip()
        if d_key[0] in ["'", '"']:
            if d_key[-1] in ["'", '"']:
                d_key = d_key[1:-1]
        if d_value[0] in ["'", '"']:
            if d_value[-1] in ["'", '"']:
                d_value = d_value[1:-1]
        return (check_results, ({d_key:d_value}, key))
        

def args_data(string):
    commas, index = 0, []
    flag = False
    for c in range(len(string)):
        if string[c] == "{":
            flag = True
        if string[c] == ',' and not flag:
            commas += 1
            index.append(c)
    else:
        return (commas, index)


def save_data(data):
    store = models.storage.all()
    store[data[1]].__dict__.update(data[0])
    models.storage.save()
 
def pre_update(classname, method_value):
    n_args, idx_args = args_data(method_value[1])

    if classname not in classes:
            print("** class doesn't exists **")
            return 0

    if n_args == 1:
        ifvalid, valid_args = check(idx_args, (method_value[1], classname))
        if ifvalid[0] == False:
            print("** no instance found **")
            return 0
        elif ifvalid[1] == False:
            print("** Invalid dictionary **")
            return 0
        else:
            save_data(valid_args)
    elif n_args == 2:
        ifvalid, valid_args = check(idx_args, (method_value[1], classname))
        if ifvalid[0] == False:
            print("** no instance found **")
            return 0
        else:
            save_data(valid_args)
    else:
        print("** Invalid number of arguments **")
        return 0

    

# --------------------------

class HBNBdata(cmd.Cmd):
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
        Preproccesor of the data Line, all arguments will be here after executing
        so we can validate if there's any ocurrence with <class> . <method> of the existing
        classes
        '''
        if '.' in line and line.split(' ')[0] not in actions:
            parsed = line.split('.')
            if pre_method(parsed):
                if parsed[1] == "all()":
                    pre_all(parsed)
                elif parsed[1] == "count()":
                    pre_count(parsed)
                elif pre_parse(parsed[1])[0] == "show":
                    if pre_parse(parsed[1])[1] == '':
                        return cmd.Cmd.default(self, line)
                    else:
                        pre_show(parsed[0], pre_parse(parsed[1]))
                elif pre_parse(parsed[1])[0] == "destroy":
                    if pre_parse(parsed[1])[1] == '':
                        return cmd.Cmd.default(self, line)
                    else:
                        pre_destroy(parsed[0], pre_parse(parsed[1]))
                elif pre_parse(parsed[1])[0] == "update":
                    if pre_parse(parsed[1])[1] == '':
                        return cmd.Cmd.default(self, line)
                    else:
                        pre_update(parsed[0], pre_parse(parsed[1], True))
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
        @ usage - > <data> <model> {ex: create BaseModel}

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
        @ usage - > <data> <model> <id> {ex: show BaseModel 123asd1272bn28dn}
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
        @ usage - > <data> <model> {ex: all BaseModel}
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
            tmp_keys = list(tmp_dictionary.keys())
            key = instancia + '.' + instance_id
            if instancia not in classes:
                print("** class doesn't exist **")
                return 0
            # !! aca se debe encontrar una nueva forma de validar instancia
            if key not in tmp_keys:
                print('** not instance found')
                return 0
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
        Quit data to exit the program
        """
        return True
    
    def do_EOF(self, args):
        """
        Quit data to exit the program
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
    interprete = HBNBdata()
    interprete.cmdloop()