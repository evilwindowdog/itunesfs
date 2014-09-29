#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import os
import subprocess
import argparse
import shutil
from itunesfslib import converter
from itunesfslib.helpers import *



def main():
    parser = argparse.ArgumentParser(
        description='Generates a YAML file or an iTunes Store Transporter package (.itmsp) from a folder\'s assets',
        epilog="Author: Petros Douvantzis @ Evil Window Dod")
    parser.add_argument('inputpath',
                        help='path to the asset folder')
    parser.add_argument('-o', metavar='outputpath', dest='outputpath',
                        help='path to output folder')
##    parser.add_argument('--package', metavar='package', action='store_const', const=True, default=False,
##                        help='Generate .itmsp package (default: generate YAML file)')
    parser.add_argument('-t', metavar='type', dest='type', choices=["YAML","itmsp"], default="itmsp",
                        help="the type of the output: [YAML, itmsp]. (default is itmsp)")
    
    #sys.argv = [sys.argv[0]] + '../Horizon -out la'.split()#overide input from command line

    # parse arguments
    try:
        args = parser.parse_args()
    except:
        print("****************")
        parser.print_help()
        print("****************")
        sys.exit(1)
        
    inputpath = os.path.normpath(args.inputpath)
    if not args.outputpath:
        outputpath = None
        savepath = inputpath
    else:
        outputpath = os.path.normpath(args.outputpath)
        savepath = outputpath
        if os.path.abspath(inputpath) == os.path.abspath(outputpath):
            myexit('Input path can not be the same as output path')

    # parse folder and generate "output.yaml"
    converter.convert(inputpath, outputpath)
    printsuccess("Succesfully created \"output.yaml\" file at {}".format(os.path.abspath(savepath)))
    if args.type == 'YAML':
        return
    
    # convert "output.yaml" to a .itmsp package
    executable_path = shutil.which('itmsp')
    if not executable_path:
        myexit("""\"itmsp\" is not installed. \n\n"""
               "In order to convert the generated YAML file to .itmsp package,"
               """you have to install itmsp from https://github.com/colinhumber/itunes_transporter_generator.\n\n"""
               """If you have ruby installed, run:\n   \"$ gem install itunes_transporter_generator\"""")
    os.chdir(savepath)
    success = not subprocess.call([executable_path, 'package', '-i', 'output.yaml','--prefix-image'])
    if not success:
        myexit('Failed to convert output.yaml to .itmsp package')

if __name__ == '__main__':
    main()

