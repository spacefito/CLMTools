usage: clm-control-plane.py [-h] [-o OUTPUT] [-b] [-at] [-ct] [-rt] [-nt]
                            [-st] [-sl] [-si] [-d SOURCE_DIRECTORY]
                            [--show-network NETWORK_NAME] [--list-nics]
                            [--debug]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output filename. output is redirectedto the specified
                        file.
  -b, --obfuscate       Obfuscate output. Removes sensible informationfrom the
                        output, like hostnames, ips, etc...
  -at, --all-topologies
                        Include all topologies
  -ct, --control-plane-topology
                        output control-plane topology
  -rt, --region-topology
                        output region topology
  -nt, --network-topology
                        output network topology
  -st, --service-topology
                        output service topology
  -sl, --service-list   List all services running in control-plane
  -si, --show-server-info
                        show server information
  -d SOURCE_DIRECTORY, --source-directory SOURCE_DIRECTORY
                        path to directory where yml inputmodels are stored
  --show-network NETWORK_NAME
                        displays list of servers attached to the given network
                        along with their ip addresses.
  --list-nics           displays network cards by server inthe format:
                        server:nic_name
  --debug               debug flag for developing
