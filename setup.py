from cx_Freeze import setup, Executable

base = None

executables = [Executable("src.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {
        'packages': packages,
    },
}

setup(
    name="TicTacToe",
    options=options,
    version="1.0",
    description='It does not contain any virus. I promise.',
    executables=executables
)
