import cmd
from json import loads, dumps
from models.base_model import BaseModel
from models import class_names

class HBNBCommand(cmd.Cmd):
    """Interprete de comandos"""
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


if __name__ == '__main__':
    interprete = HBNBCommand()
    interprete.cmdloop()
