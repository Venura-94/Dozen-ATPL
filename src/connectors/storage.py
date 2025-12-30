import os
from pathlib import Path


class LocalStorage:
    
    MAIN_FOLDERPATH = "storage"
    os.makedirs("storage", exist_ok=True)

    @classmethod
    def list_files(cls) -> list[str]:

        outputs: list[str] = []
        root = Path(cls.MAIN_FOLDERPATH)        

        for path in root.rglob("*"):
            if path.is_file():
                path_object = path.relative_to(root)
                outputs.append(path_object.as_posix())

        return outputs
    
    @classmethod
    def upload_file(cls, filepath: str, file_contents: bytes, can_overwrite = True):
        # TODO: in docstring mention use of hyphen filepaths in case of azure stoareg, Raise
        final_filepath = os.path.join(cls.MAIN_FOLDERPATH, filepath)
        if not can_overwrite and os.path.exists(final_filepath):
            raise FileExistsError

        os.makedirs(os.path.dirname(final_filepath), exist_ok=True)
        with open(final_filepath, "wb") as f:
            f.write(file_contents)

    @classmethod
    def download_file(cls, filepath: str) -> bytes:
        # TODO: in docstring mention raises FileNotFoundError
        final_filepath = os.path.join(cls.MAIN_FOLDERPATH, filepath)
        with open(final_filepath, "rb") as f:
            file_contents = f.read()
        return file_contents
