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

import argparse
import os
import re

from clm_models import CLMModel


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output',
                        help='output filename. If present, output is redirected'
                             'to the specified file.'
                        )

    parser.add_argument('-b', '--obfuscate', action='store_true',
                        help='Obfuscate output. Removes sensible information'
                             'from the output, like hostnames, ips, etc...'
                        )

    parser.add_argument('-at','--all-topologies', action='store_true',
                        help="Include all topologies")

    parser.add_argument('-ct', '--control-plane-topology', action='store_true',
                        help='output control-plane topology')

    parser.add_argument('-rt', '--region-topology', action='store_true',
                        help='output region topology')

    parser.add_argument('-nt', '--network-topology', action='store_true',
                        help='output network topology ')

    parser.add_argument('-st', '--service-topology', action='store_true',
                        help='output service topology ')

    parser.add_argument('-sl', '--service-list', action='store_true',
                        help='List all services running in control-plane')

    parser.add_argument('-si', '--show-server-info', action='store_true',
                        help='show server information')

    default_dir = os.path.join(os.path.expanduser('~'), 'openstack','my_cloud', 'info')
    parser.add_argument('-d', '--source-directory',
                        help='path to directory where yml input'
                             'models are stored',
                        default=default_dir)

    parser.add_argument('--show-network', dest='network_name',
                        help='displays list of servers attached to the '
                             'given network along with their ip addresses.')

    parser.add_argument('--list-nics', action='store_true',
                        help='displays network cards by server in'
                             'the format: server:nic_name')

    parser.add_argument('--debug', action='store_true',
                        help='debug flag for developing')

    args = parser.parse_args()

    # tuples: (file_name, rooth_node)
    sub_model_list = [('control_plane_topology', 'control_planes'),
                      ('region_topology', 'regions'),
                      ('network_topology', 'network_groups'),
                      ('service_topology', 'services'),
                      ('server_info', None)]

    mdl = {k: CLMModel(
        os.path.join(args.source_directory, k+'.yml'), root)
        for (k, root) in sub_model_list} if not args.debug else {}

    output = {}

    if args.network_name:
        output['show_network'] = '-this should be the list of servers attached to the named network, with their ips'
        raise NotImplementedError(output['show_network'])

    if args.list_nics:
        output['nic_list'] = CLMModel(root='nic_list')
        output['nic_list'].model = [
            ':'.join([server, nic])
            for server in mdl['server_info'].model
            for nic in mdl['server_info'].model[server]['net_data']
        ]

    if args.show_server_info:
        output['server_info'] = mdl['server_info']

    if args.control_plane_topology or args.all_topologies:
        output['control_plane_topology'] = mdl['control_plane_topology']

    if args.region_topology or args.all_topologies:
        output['region_topology'] = mdl['region_topology']

    if args.network_topology or args.all_topologies:
        output['network_topology'] = mdl['network_topology']

    if args.service_topology or args.all_topologies:
        output['service_topology'] = mdl['service_topology']

    if args.service_list:
        output['service_list'] = CLMModel(root='service_list')
        output['service_list'].model = mdl['service_topology'].model.keys()

    if args.obfuscate:
        # create a mapping of hostnames to simple servers

        hm = {}
        # we want only the xxx-xx-xx- part of the real nodes (xxx-xx-xx)
        # and we need to create the endpoint names (xxx-xx-vip)
        regexp = re.compile('\A\w+\-\w+\-\w+\-')
        regexv = re.compile('\A\w+\-\w+\-')
        for server in mdl['server_info'].model:
            hostname = mdl['server_info'].model[server]['hostname']
            m = regexp.match(hostname)
            if m:
                hm[m.group(0)] = server
                v = regexv.match(m.group(0))
                if v:
                    vip_name = v.group(0)+'vip'
                    hm[vip_name] = server+'-vip'

        for hostname in hm:
            for model in output.values():
                model.replace_values(hostname, hm[hostname])
                model.replace_keys(hostname, hm[hostname])

    for model in output.values():
        if args.output:
            model.append_to_file(args.output)
        else:
            print(model)


if __name__ == '__main__':
    main()
