# lrbd
Simplifies iSCSI configuration of Ceph RBD images.

## Quickstart

For the impatient, follow the instructions for the simplest configuration of one initiator to one gateway to one image.  A working Ceph installation is required.

### From gateway
1. Install lrbd  
`# zypper in lrbd`
2. Create a pool  
`# ceph osd pool create swimming 256 256`
* Create an RBD image  
`# rbd -p swimming create raft --size 2048`
* Create an initial configuration  
`# lrbd -e`
* Replace *archive* with *raft* and *rbd* with *swimming*.  Replace the initiator value with your client's setting. (See /etc/iscsi/initiatorname.iscsi on Linux.) Save the file.  Run lrbd.  
`# lrbd`
* Inspect with targetcli  
`# targetcli ls`

### From client
1. Discover the target.  
`# iscsiadm -m discovery -t st -p `*gateway_address*
* Login  
`# iscsiadm -m mode -p `*gateway_address*` --login`
* Find device   
* Format, write data, read data
* Logout  
`# iscsiadm -m mode -p `*gateway_address*` --logout`

### From gateway
1. From the gateway, clear the configuration  
`# lrbd -C`
* Unmap the RBD images  
`# lrbd -u`
* Wipe the configuration from Ceph  
`# lrbd -W`

## Manual

See [Wiki](https://github.com/swiftgist/lrbd/wiki)
