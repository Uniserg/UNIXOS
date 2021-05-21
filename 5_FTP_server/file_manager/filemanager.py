import os
import shutil
from sys import platform

from datetime import datetime
from shutil import rmtree, copy, move
import re


class Sequence(object):
    def __init__(self, init_value=0, allocation_size=1):
        self.__cur_value = init_value
        self.__allocation_size = allocation_size

    def get_next(self):
        res = self.__cur_value
        self.__cur_value += self.__allocation_size
        return res

    def reset(self, with_value=0):
        self.__cur_value = with_value

    def __get_cur_value(self):
        return self.__cur_value

    def __get_allocation_size(self):
        return self.__allocation_size

    def __set_allocation_size(self, allocation_size):
        self.__allocation_size = allocation_size

    allocation_size = property(__get_allocation_size, __set_allocation_size)


class Expression(object):
    def __init__(self, command=None, params=None, time=datetime.now()):
        self.__command = command
        self.__params: list = params
        self.__time: datetime = time

    def __get_command(self):
        return self.__command

    def __get_params(self):
        return self.__params

    def __get_time(self):
        return self.__time

    def __str__(self) -> str:
        return "Expression{" + f"command={self.command}, params={self.params}, time={self.time}"

    def __repr__(self) -> str:
        return self.__str__()

    params = property(__get_params)
    time = property(__get_time)
    command = property(__get_command)


class FileManager(object):
    def __init__(self, client_path, max_len_history=1000):
        self.home_dir = rf"C:\Users\Serg\Documents\MEGA\MEGAsync\PycharmProjects\UNIXOS\5_FTP_server\file_manager\home\{client_path}"
        self.cur_position = self.home_dir
        self.__commands = {
            "mkdir": self.mkdir,
            "history": lambda: self.history,
            "help": lambda: self.__commands.keys(),
            "rmdir": self.rmdir,
            "ls": self.ls,
            "cd": self.cd,
            'touch': self.touch,
            'rm': self.rm,
            'exit': exit,
            'echo': self.echo,
            'cat': self.cat,
            'mv': self.mv,
            'cp': self.cp,
            'rename': self.rename
        }

        self.__spec_ch = [
            lambda x: str(x).replace('../', self.cur_position[:self.cur_position.rfind('\\') + 1]),
            lambda x: str(x).replace('./', self.cur_position),
            lambda x: str(x).replace('/', "\\")
        ]
        self.max_len_history = max_len_history
        self.__seq = Sequence()
        self.__history = {}
        self.sh = '/'
        if 'win' in platform.lower():
            self.sh = '\\'

    def __check_errors(fn):
        def wrapper(self, *params):
            try:
                return fn(self, *params)
            except (IndexError, TypeError):
                return "Указаны не все параметры!"
            except FileExistsError:
                return "Файл с таким именем уже существует!"
            except FileNotFoundError as e:
                return(e)
            except NotADirectoryError:
                return 'Нет такой папки! Это файл. '
            except shutil.Error as e:
                return e

        return wrapper

    def trans_f(self, func, file, path):
        file = self.__get_path(file)
        path = self.__get_path(path)
        func(file, path)

    def rename(self, old_file, new_file, dir=None):
        path = self.cur_position
        if dir is not None:
            path = self.__get_path(dir)

        old_file = path + self.sh + old_file
        new_file = path + self.sh + new_file

        os.rename(old_file, new_file)

    def cp(self, file, path):
        self.trans_f(copy, file, path)

    def mv(self, file, path):
        self.trans_f(move, file, path)

    def rm(self, *params):
        exe = os.remove
        params = list(params)
        params_f = {
            '-r': lambda x: rmtree(x)
        }
        while params and str(params[0]).startswith('-'):
            if params[0] in params_f:
                exe = params_f[params.pop(0)]

        path = params[0]
        path = self.__get_path(path)
        exe(path)

    def touch(self, path):
        path = self.__get_path(path)

        if os.path.isdir(path):
            return f"{path} - это папка!"
        elif os.path.isfile(path):
            return f"{path} - файл с таким именем уже существует"

        dir = path[:path.rfind(self.sh)]
        if not os.path.isdir(dir):
            self.mkdir(dir)

        file_obj = open(f"{path}", 'w')
        file_obj.write(f"Created at: {datetime.now()}")
        file_obj.close()

    def echo(self, msg=None, file=None):
        if file is not None:
            file = self.__get_path(file)
            with open(file, 'w') as f:
                f.write(msg)
        else:
            return msg

    def cat(self, file):
        file = self.__get_path(file)
        with open(file) as f:
            for i in f:
                return i

    def mkdir(self, path):
        path = self.__get_path(path)
        os.mkdir(path)

    def rmdir(self, path):
        exe = os.rmdir
        path = self.__get_path(path)
        exe(path)

    def __get_path(self, path=None):
        if 'win' in platform.lower():
            for f in self.__spec_ch:
                path = f(path)

        if self.home_dir not in path:
            path = self.cur_position + self.sh + path
        return path.rstrip(self.sh)

    def ls(self, path=None):
        if path is None:
            path = self.cur_position

        path = self.__get_path(path)
        return os.listdir(path)

    def __to_story(self, exe_cmd):
        if len(self.history) >= self.max_len_history:
            self.__seq.reset()

        self.history[self.__seq.get_next()] = exe_cmd

    def __get_history(self):
        return self.__history

    def cd(self, path=None):
        if path is None:
            raise TypeError

        path = self.__get_path(path)

        if os.path.isdir(path):
            self.cur_position = self.__get_path(path)
        elif os.path.isfile(path):
            return(f"{path} - Это файл")
        else:
            return "Нет такого каталога!"

    @__check_errors
    def take_cmd(self, cmd: str):
        cmd = list(filter(lambda x: x and x != ' ' and x is not None,
                          re.split("[\"\'](.*?)[\"\']|([^\\s]+)", cmd)))
        exe_cmd = Expression(cmd.pop(0), cmd)

        self.__to_story(exe_cmd)

        if exe_cmd.command in self.__commands:
            exe = self.__commands[exe_cmd.command]
        else:
            return "Нет такой команды!"

        return str(exe(*exe_cmd.params))

    history = property(__get_history)
