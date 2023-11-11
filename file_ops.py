import os


class FileOperations:
    @staticmethod
    def delete_file(file_path):
        # Delete the specified file
        if os.path.exists(file_path):
            os.remove(file_path)

    # You can add more file operations here as needed
