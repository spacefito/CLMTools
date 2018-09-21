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

    def set_value_by_key(self, key, new_value):
        CLMModel.replace_by_key(self._model, key, new_value)

    def replace_value(self, old_value, new_value):
        CLMModel.replace_item_by_value(self._model, old_value, new_value)

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

    def __str__(self):
        _dict = {self._root: self._model} if self._root else self._model
        return yaml.dump(_dict, default_flow_style=False)
