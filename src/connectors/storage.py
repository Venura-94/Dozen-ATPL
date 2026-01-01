import os
from pathlib import Path


class LocalStorage:
    
    MAIN_FOLDERPATH = "storage"
    os.makedirs("storage", exist_ok=True)

    @classmethod
    def list_files(cls) -> list[str]:
        """View all files in the storage system.

        e.g. : [
          'a.txt',
          'fol1/b.txt',
          'fol2/c.txt'
        ]

        Returns:
            list[str]: Avalable files (filepaths)
        """

        outputs: list[str] = []
        root = Path(cls.MAIN_FOLDERPATH)        

        for path in root.rglob("*"):
            if path.is_file():
                path_object = path.relative_to(root)
                outputs.append(path_object.as_posix())

        return outputs
    
    @classmethod
    def upload_file(cls, filepath: str, file_contents: bytes, can_overwrite = True):
        """Upload a file to the storage system.

        Args:
            filepath (str): Filepath to save the file. Use alphanumeric characters and hyphens ('-') only, in case of use with cloud storage systems like Azure storage.
            file_contents (bytes): _description_
            can_overwrite (bool, optional): _description_. Defaults to True.

        Raises:
            FileExistsError: if file already exists (if can_overwrite = False)
        """
        final_filepath = os.path.join(cls.MAIN_FOLDERPATH, filepath)
        if not can_overwrite and os.path.exists(final_filepath):
            raise FileExistsError

        os.makedirs(os.path.dirname(final_filepath), exist_ok=True)
        with open(final_filepath, "wb") as f:
            f.write(file_contents)

    @classmethod
    def download_file(cls, filepath: str) -> bytes:
        """Download a file from the storage system.

        Args:
            filepath (str): _description_

        Raises:
            FileNotFoundError: if filepath does not exist

        Returns:
            bytes: The file.
        """
        final_filepath = os.path.join(cls.MAIN_FOLDERPATH, filepath)
        with open(final_filepath, "rb") as f:
            file_contents = f.read()
        return file_contents
