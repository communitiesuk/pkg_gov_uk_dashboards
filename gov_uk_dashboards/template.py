import os
import inspect
from . import colours




def read_template():
    with open(inspect.getfile(colours).replace('colours.py','template.html'), encoding="utf-8") as f:
        template = f.read()
        return template
        