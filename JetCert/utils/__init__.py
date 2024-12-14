import os
import shutil
import json


class Utils:
    @staticmethod
    def importer(modular_path, root_package=False, relative_globals=None, level=0):
        """We only import modules, functions can be looked up on the module.
        Usage:

        from foo.bar import baz
        >>> baz = importer('foo.bar.baz')

        import foo.bar.baz
        >>> foo = importer('foo.bar.baz', root_package=True)
        >>> foo.bar.baz

        from .. import baz (level = number of dots)
        >>> baz = importer('baz', relative_globals=globals(), level=2)
        """

        try:
            return __import__(
                modular_path,
                locals=None,
                globals=relative_globals,
                fromlist=[] if root_package else [None],
                level=level,
            )

        except:
            return None

    @staticmethod
    def is_json(input_obj):
        try:
            if type(input_obj) == str:
                json.loads(input_obj)

            else:
                json.dumps(input_obj)

            return True

        except:
            return False

    @staticmethod
    def is_valid_python_func_name(func_name):
        if not func_name:
            return False

        if type(func_name) != str:
            return False

        return func_name.isidentifier() and not func_name[0].isdigit()

    @staticmethod
    def is_valid_python_filename(filename):
        if not filename:
            return False

        if type(filename) != str:
            return False

        basename, extension = os.path.splitext(filename)

        if extension != ".py":
            return False

        return basename.isidentifier()

    @staticmethod
    def is_valid_c_filename(filename):
        if not filename:
            return False

        if type(filename) != str:
            return False

        basename, extension = os.path.splitext(filename)

        if extension != ".c":
            return False

        return basename.isidentifier()

    def get_base_file_path(file_path):
        directory, filename = os.path.split(file_path)
        basename, extension = os.path.splitext(filename)
        return os.path.join(directory, basename)

    @staticmethod
    def list_folders(folder_path):
        if not os.path.isdir(folder_path):
            return

        folders = []

        for item in os.listdir(folder_path):
            if os.path.isdir(os.path.join(folder_path, item)):
                folders.append(item)

        return folders

    @staticmethod
    def clear_folder(folder_path):
        if not os.path.exists(folder_path):
            return

        if not os.path.isdir(folder_path):
            return

        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                continue

            os.remove(item_path)
