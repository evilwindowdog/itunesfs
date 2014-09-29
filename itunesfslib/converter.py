# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import OrderedDict
from shutil import copytree, ignore_patterns, rmtree
import sys, os, argparse, codecs, yaml, traceback

from itunesfslib.helpers import *
from itunesfslib.humanyaml import *

master_locale_name ='en-US'
chars_count_max = 100
filenames = {
    'config_app'            :'config_app.yaml',
    'config_local'          :'config-local.yaml',
    'description'           :'description.txt',
    'keywords'              :'keywords.txt',
    'version_whats_new'     :'whats_new.txt',
    'screenshots'           :'screenshots'
    }
required_asset_types = [
    'config_local',
    'description',
    'keywords'
    ]
# **************************************************
def convert(path, outpath=''):

    if not outpath:
        outpath     = path
        copyfiles   = False
    else:
        copyfiles   = True
    #open app configuration file
    filepath = os.path.join(path,filenames['config_app'])
    if not os.path.isfile(filepath):
        myexit('The app configuration was not found in location {}'.format(filepath))
    stream = open(filepath, "r", encoding='utf-8-sig').read()
    app_configuration = yaml.load(stream)  
    
    #find versions
    vdirs = []
    for vdir in next(os.walk(path))[1]:
        if vdir.endswith('.itmsp'):continue
        vdirs.append(vdir)
    if "versions" in app_configuration:
        vdirs_restricted_dict = app_configuration.pop('versions')
        try:
            vdirs_restricted = [item['name'] for item in vdirs_restricted_dict]
            dirs_not_found = set(vdirs_restricted) - set(vdirs)
            if dirs_not_found:
                myexit("The following folders were not found: {}".format(dirs_not_found))
            vdirs = vdirs_restricted
        except Exception as inst:
            traceback.print_exc(file=sys.stdout)
            myexit('Add one or more versions in "config_app.yaml"')
        
    versions = []                   
    for vdir in vdirs:
        #find locales
        master_locale = {}
        master_locale_config_local = {}
        locales = []
        ldirs = next(os.walk(os.path.join(path,vdir)))[1]
        if master_locale_name not in ldirs:
            myexit('No files found for the default locale ({}) of v{}'.format(master_locale_name, vdir))
        ldirs.insert(0, ldirs.pop(ldirs.index(master_locale_name))) 
        for ldir in ldirs:
            #find assets
            locale = OrderedDict();
            locale.update({'name': ldir})
            asset_types_copied = []
            for asset_type in ['config_local', 'description', 'keywords', 'version_whats_new', 'screenshots']:
                filepath = os.path.join(path,vdir,ldir,filenames[asset_type]);
                if not os.path.exists(filepath):
                    if ldir == master_locale_name:
                        if asset_type in required_asset_types:
                            myexit('The {} was not found in location {}'.format(asset_type, filepath))
                        else:
                            continue
                    else:                           
                        if asset_type in master_locale:
                            asset_types_copied.append(asset_type)
                            locale.update({asset_type : master_locale[asset_type]})
                        elif asset_type == 'config_local':
                            asset_types_copied.append(asset_type)
                            locale.update(master_locale_config_local)
                        continue

                if asset_type == 'config_local':
                    stream = codecs.open(filepath, 'r', encoding='utf-8-sig')
                    config_local_dic = yaml.load(stream)
                    locale.update(config_local_dic)
                    if ldir == master_locale_name:
                        master_locale_config_local = config_local_dic
                elif asset_type == 'keywords':
                    keywords_text = codecs.open(filepath, 'r', encoding="utf-8-sig").read()
                    keywords = [keyword.strip() for keyword in keywords_text.split(",")]
                    asset = keywords
                    chars_count = len(keywords)-1 + sum([len(keyword) for keyword in keywords])
                    if chars_count > chars_count_max:
                        printwarning('The maximum keyword character count was exceeded in {} locale of v{}'.format(ldir, vdir))
                    locale.update({asset_type : asset})
                elif asset_type == 'description':
                   asset = open(filepath, 'r', encoding='utf-8-sig').read()
                   locale.update({asset_type : literal(asset)})
                elif asset_type == 'version_whats_new':
                    asset = codecs.open(filepath, 'r', encoding='utf-8-sig').read()
                    locale.update({asset_type : literal(asset)})
                elif asset_type == 'screenshots':
                    devices_screenshots = {}
                    for device in ['iphone_3.5in', 'iphone_4in', 'iphone_4.7in', 'iphone_5.5in', 'ipad']:
                        device_filepath = os.path.join(filepath, device)
                        if not os.path.exists(device_filepath):
                            continue
                        screenshots = []
                        relative_path_to_output = os.path.relpath(device_filepath, path)
                        for screenshot in next(os.walk(device_filepath))[2]:
                            if not screenshot.startswith('.'):
                                screenshots.append(os.path.join(relative_path_to_output, screenshot))
                        devices_screenshots.update({device : screenshots})
                    if not devices_screenshots:
                        myexit("No screenshots were found for {} locale of v{}".format(ldir, vdir))
                    if copyfiles:
                        copypath = os.path.join(outpath, vdir, ldir, filenames[asset_type])
                        if os.path.exists(copypath):
                            rmtree(copypath)
                        copytree(filepath, copypath, ignore=ignore_patterns('.*'))
                    locale.update({asset_type : devices_screenshots})                             
            locales.append(locale)
            if ldir == master_locale_name:
                master_locale = locale
        version = OrderedDict();
        version.update({'name'       : vdir})
        version.update({'locales'    : locales})
        versions.append(version)

    app_configuration.update({'versions' : versions})


    #convert app_configuration Python object to YAML
    yaml_data = dump_humanised(app_configuration)
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    with open(os.path.join(outpath, 'output.yaml'), 'w', encoding='utf-8-sig') as outfile:
        outfile.write(yaml_data)
