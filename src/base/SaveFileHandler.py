from pathlib import Path
import warnings

class SaveFileHandler:
    def __init__(self):
            self._save_files = {}

    @property
    def save_files(self):
        return self._save_files

    def add_save_file(self, save_id, path):
        save_file_path = Path(path)
        print(save_id)

        if save_file_path.exists() and save_file_path.is_dir() and save_id not in self._save_files.keys() and path not in self._save_files.values():
            self._save_files[save_id] = path
        elif not save_file_path.exists():
            raise FileExistsError
        elif not save_file_path.is_dir():
            raise NotADirectoryError
        elif save_id in self._save_files.keys():
            warnings.warn(f"{save_id} already exists as a key!")
        elif path in self._save_files.values():
            warnings.warn(f"{path} already exists as a value!")

        print(self._save_files)

    def reset_save_file(self, save_id):
        if save_id in self._save_files.keys():
            pass