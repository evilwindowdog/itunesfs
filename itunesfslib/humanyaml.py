# -*- coding: utf-8 -*-
from collections import OrderedDict
import yaml

class literal(str): pass

def literal_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
yaml.add_representer(literal, literal_presenter)

def ordered_dict_presenter(dumper, data):
    return dumper.represent_dict(data.items())
yaml.add_representer(OrderedDict, ordered_dict_presenter)

class MyDumper(yaml.Dumper):
    def ignore_aliases(self, _data):
        return True
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)

def dump_humanised(data):
    return yaml.dump(data, allow_unicode=True, default_flow_style=False, canonical=False, Dumper=MyDumper)
