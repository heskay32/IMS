import cx_Freeze
import sys
from cx_Freeze import setup, Executable
import os

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
#build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

os.environ['TCL_LIBRARY'] = r"C:\Users\SK\AppData\Local\Programs\Python\Python39\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\SK\AppData\Local\Programs\Python\Python39\tcl\tk8.6"


executables = [cx_Freeze.Executable("login.py", base=base,icon="icon.ico")]



setup(
    name = "KingsPower",
    version = "0.1",
    description = "Management System | by Olasunkanmi",
    options = {"build_exe": {"packages":["tkinter","os","sys"], "include_files":['tcl86t.dll','tk86t.dll','billing.py','category.py','create_db.py','credit.py','dashboard.py','employee.py','product.py','sales.py','supplier.py','images','bill','icon.ico']}},
    executables = executables
)