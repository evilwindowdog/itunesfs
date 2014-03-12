# -*- coding: utf-8 -*-
from __future__ import print_function
import sys

def warning(objs):
    print("WARNING: ", objs, file=sys.stdout)
def myexit(objs):
    print("EXITING: ", objs, file=sys.stderr)
    sys.exit(1)
