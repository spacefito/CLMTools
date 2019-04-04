#!/bin/bash -xe

# before we need
# neutron net-create ext-net --router:external
# neutron subnet-create ext-net 192.172.0.0/24 --disable-dhcp --allocation-pool start=192.172.0.100,end=192.172.0.200 --gateway_ip 192.172.0.1
# openstack image create cirros --file cirros-0.4.0-x86_64-disk.img --disk-format qcow2  --container-format bare --public

DISTRIBUTED=True
HA=True
EXT_NET_NAME='ext-net'
BASE_NAME='n'
i=1
NET_NAME=${BASE_NAME}$i
SUBNET_NAME=${BASE_NAME}$i
VM_NAME=${BASE_NAME}$i
ROUTER_NAME="r${i}"
IMAGE_NAME='cirros'

NET_ID=$(neutron net-create ${NET_NAME} | grep ' id ' | awk '{print $4}')
SUBNET_ID=$(neutron subnet-create ${NET_NAME} 101.${i}.0.0/24 --name $SUBNET_NAME |grep ' id '| awk {'print $4'})
ROUTER_ID=$(neutron router-create ${ROUTER_NAME} --distributed=${DISTRIBUTED} --ha=${HA} |grep ' id '| awk {'print $4'})
neutron router-gateway-set ${ROUTER_NAME} ${EXT_NET_NAME}
neutron router-interface-add ${ROUTER_NAME} ${SUBNET_NAME}
