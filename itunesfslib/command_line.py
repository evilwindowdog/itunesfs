#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import os
import argparse
from itunesfslib import converter
from itunesfslib import helpers


def main():
    parser = argparse.ArgumentParser(
        description='Generates a .yamp configuration file from the assets of a folder',
        epilog="Author: Petros Douvantzis @ Evil Window Dod")
    parser.add_argument('i', metavar='input', help='Relative path to the input folder')
    parser.add_argument('-out', metavar='output', help='Relative path to the output folder')

    #sys.argv = [sys.argv[0]] + '../Horizon -out la'.split(" ")#overide input from command line
    try:
        args = parser.parse_args()
    except:
        print("****************")
        parser.print_help()
        print("****************")
        sys.exit(1)   

    inputpath = os.path.normpath(args.i)
    if not args.out:
        outputpath = None
    else:
        outputpath = os.path.normpath(args.out)
        if inputpath == outputpath:
            helpers.myexit('Input path can not be the same as output path')

    converter.convert(inputpath, outputpath)

if __name__ == '__main__':
    main()

