#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (c) Copyright 2018 SUSE LLC
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import re
import yaml


class CLMModel(object):

    def __init__(self, file_name=None, root=None):
        self._root = root
        if not file_name:
            return
        with open(file_name, "r") as f:
            if self._root:
                self._model = yaml.load(f)[self._root]
            else:
                self._model = yaml.load(f)

    def append_to_file(self, file_name):
        _dict = {self._root: self._model} if self._root else self._model
        with open(file_name, 'a+') as f:
            yaml.dump(_dict, f, default_flow_style=False)

    def replace_values(self, old_value, new_value):
        CLMModel.replace_item_by_value(self._model, old_value, new_value)

    def replace_keys(self, old_key, new_key):
        CLMModel.replace_key(self._model, old_key, new_key)

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        self._root = value

    @staticmethod
    def replace_item_by_value(data_structure, old_value, new_value):
        if isinstance(data_structure, dict):
            for key, item in data_structure.items():
                if isinstance(item, dict) or isinstance(item, list):
                    CLMModel.replace_item_by_value(item, old_value, new_value)
                elif isinstance(item, bool):
                    pass
                else:
                    if isinstance(item, str) and old_value in item:
                        data_structure[key] = new_value
        elif isinstance(data_structure, list):
            for item in data_structure:
                if isinstance(item, dict) or isinstance(item, list):
                    CLMModel.replace_item_by_value(item, old_value, new_value)
                elif isinstance(item, str) and old_value in item:
                    data_structure[data_structure.index(item)] = new_value

    @staticmethod
    def replace_key(data_structure, old_key, new_key):
        if isinstance(data_structure, dict):
            for key, item in data_structure.items():
                if isinstance(item, dict) or isinstance(item, list):
                    CLMModel.replace_key(item, old_key, new_key)
                if isinstance(key, str) and old_key in key:
                    data_structure[new_key] = data_structure.pop(key)

    @staticmethod
    def replace_ipv4_funct(ipv4):
        #TODO (spacefito): at some point this function should
        #                  probably return a more meaningful value
        #                  It would be great to use a class scope
        #                  dictionary to add ips into so the same
        #                  value maybe used to replace the ip everywhere
        return "X" * len(ipv4)

    @staticmethod
    def replace_regexvalue(data_structure, regexvalue, replace_function):
        if isinstance(data_structure, dict):
            for key, item in data_structure.items():
                if isinstance(item, dict) or isinstance(item, list):
                    CLMModel.replace_regexkey(item, regexvalue, replace_function)
                elif isinstance(item, bool):
                    pass
                else:
                    if isinstance(item, str):
                        m = regexvalue.match(item)
                        if m:
                            data_structure[key] = replace_function(item)

    @staticmethod
    def replace_regexkey(data_structure, regexkey, replace_function):
        if isinstance(data_structure, dict):
            for key, item in data_structure.items():
                if isinstance(item, dict) or isinstance(item, list):
                    CLMModel.replace_regexvalue(item, regexkey,
                                                replace_function)
                if isinstance(key, str):
                    m = regexkey.match(key)
                    if m:
                        data_structure[
                            replace_function(key)] = data_structure.pop(key)

    def obfuscate_ipv4_addresses(self):
        ipv4regex = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
        CLMModel.replace_regexkey(self._model, ipv4regex,
                                  CLMModel.replace_ipv4_funct)
        CLMModel.replace_regexvalue(self._model, ipv4regex,
                                  CLMModel.replace_ipv4_funct)

    def __str__(self):
        _dict = {self._root: self._model} if self._root else self._model
        return yaml.dump(_dict, default_flow_style=False)
