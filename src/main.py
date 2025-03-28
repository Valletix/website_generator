import os
import shutil

def main():
    pass


def del_and_copy_all():
    shutil.rmtree("public/", True)
    print("Deleted all files from public-directory")
    public_path = "public/"
    static_path = "static/"
    stc_files = os.listdir("static/")
    print(stc_files)
    path_list = []

del_and_copy_all()


main()