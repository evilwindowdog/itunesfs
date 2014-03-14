# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from xtermcolor import colorize

def printsuccess(objs):
    print(colorize(objs, ansi=2), file=sys.stdout)
def printwarning(objs):
    print(colorize("WARNING: "+objs, ansi=9), file=sys.stdout)
def myexit(objs):
    print(colorize("EXITING: "+objs, ansi=1),file=sys.stderr)
    sys.exit(1)
