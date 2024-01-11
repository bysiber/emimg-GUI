
import os
def compatible_path(path):
    """
    -> This function takes a path as input and converts it to the appropriate format for the current OS.
    -> This function returns path which is compatible with the OS. (Windows, Linux...)
    -> \\ windows
    -> / linux
    """

    if os.name == 'nt' and '/' in path:
        # If the OS is Windows and the path uses Unix-style slashes, convert to Windows style
        return os.path.normpath(path).replace("/", "\\")
    elif os.name != 'nt' and '\\' in path:
        # If the OS is not Windows and the path uses Windows-style backslashes, convert to Unix style
        return os.path.normpath(path).replace("\\", "/")
    else:
        # If the path is already in the correct format for the OS, return it as is
        return path

#example
#print(compatible_path("Users\\user\\Desktop\\stegano\\resources\\test.txt"))
