"""
Helpful util for starting bot
"""

from sys import platform, prefix
from os import chdir, mkdir, system as sc
from os.path import exists


list_libs = ""


def create_env():
    sc('@title = "Rupy -v:0.3.2a --update:creating venv"')
    chdir("..\\..\\")
    sc("python -m venv .\\rupy_env")
    chdir(".\\tools\\")
    sc("start .\\update.bat")


def install_libs():
    sc('@title = "Rupy -v:0.0.1a --update:installing libs"')
    libs_name = list_libs.replace(",", "").split(" ")
    for lib_name in libs_name:
        sc(f"pip install {lib_name}")


def run_main_script():
    chdir("..\\..\\tools\\")
    sc("start .\\run.bat")


def test_env_func():
    path_env = prefix.split("\\")
    if path_env[len(path_env) - 1] == "rupy_env":
        return True
    return False


def test_lib_func():
    try:
        import rustplus
        import PIL
        import selenium
        import webdriver_manager
        import disnake
    except ImportError:
        return False
    else:
        return True


def main():
    attempts = 0

    while attempts < 6:

        attempts += 1
        test_env, test_lib = test_env_func(), test_lib_func()

        print(f'''[*] TEST RESULT
Env test        : {"Successful" if test_env else "Failed("}
Lib import test : {"Successful" if test_lib else "Failed("}
        ''')

        if not test_env:
            create_env()
            quit()

        if not test_lib:
            install_libs()
            continue

        if not exists("..\\configs"):
            mkdir("..\\configs")

        if not exists("..\\meta"):
            mkdir("..\\meta")

        break


if __name__ == "__main__":
    print("[*] Start plugin > update.py")
    print(f"[*] {platform=}")
    if platform != ("win32" or "linux"):
        raise OSError(f"{platform=}\nPlease, rerun this program on Windows or Linux distribute")

    main()
    run_main_script()
    quit()
