#!/bin/bash
# This script requires "pup" https://github.com/ericchiang/pup
# binaries for pup here: https://github.com/EricChiang/pup/releases
#  just unzip and put under ~/bin or a directory
# under $PATH

set -euo pipefail

name=$1
echo "looking for $name"
links=($(curl --silent "https://ark.intel.com/search?q=$name" | pup '.result-title a attr{href}'))

results=${#links[@]}
if [[ $results == 0 ]]; then
    echo "No results found" >&2
    exit 1
fi

link=${links[0]}
if [[ $results != 1 ]]; then
    echo "Warning: $results results found" >&2
    echo "Using: $link" >&2
fi

url="https://ark.intel.com$link"
codename=$(curl --silent "$url" | pup '.CodeNameText .value text{}' | xargs | sed 's/Products formerly //')

echo "$codename"
