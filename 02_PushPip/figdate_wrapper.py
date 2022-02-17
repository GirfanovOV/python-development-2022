import subprocess
import sys
import os
from tempfile import TemporaryDirectory
import venv

with TemporaryDirectory() as tmpdirname:
    venv.create(tmpdirname, with_pip=True)
    pip_exec = os.path.join(tmpdirname, "bin", "pip")
    subprocess.run([pip_exec, "install", "pyfiglet", "--disable-pip-version-check", "--quiet"])
    py_exec = os.path.join(tmpdirname, "bin", "python3")
    subprocess.run([py_exec, "-m", "figdate", *map(str, sys.argv[1:3])])
