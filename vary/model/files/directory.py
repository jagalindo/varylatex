import os
import shutil

def clear_directory(path):
    """
    Removes the content of a directory without removing the directory itself
    """
    for root, dirs, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def create_temporary_copy(path):
    """
    Creates a working directory with a copy of the project files, that can  be altered by the program
    and used for the compilations.
    """
    tmp_path = os.path.join(os.getcwd(), "vary/build/latex")
    try:
        shutil.copytree(path, tmp_path)
        macro_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "../macros.tex")
        macro_copy_path = os.path.join(tmp_path, "macros.tex")
        shutil.copyfile(macro_path, macro_copy_path)
    except shutil.Error:
        print("Error creating the temporary copy")

    return tmp_path
