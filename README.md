# lrbd
Simplifies iSCSI management of Ceph RBD images.  

The lrbd utility centrally stores the configuration in Ceph objects and executes the necessary rbd and targetcli commands to apply the stored configuration.

The tool depends on targetcli which depends on python-rtslib.  The original purpose is to support the rbd backstore and is the default option.  If your distribution is lacking kernel support or updated packages for targetcli and python-rtslib, the iblock backstore can be used for many configurations.

## Quickstart

For the impatient, follow the instructions for the simplest configuration of one initiator to one gateway to one image.  A working Ceph installation is required.

### From gateway
1. Install lrbd  
   * On SUSE: `# zypper in lrbd`
   * On Fedora: `# dnf install lrbd`
   * On RHEL 7: `# yum install lrbd`
2. Create a pool  
`# ceph osd pool create swimming 256 256`
* Create an RBD image  
`# rbd -p swimming create raft --size 2048`
* Create an initial configuration  
`# lrbd -e`
* Replace *archive* with *raft* and *rbd* with *swimming*.  Remove the initiator (and the comma from the previous line).  Replace the host *igw1* with the result of **uname -n**. Save the file.  Run lrbd using an iblock backstore.  
`# lrbd -I`
* Inspect with targetcli  
`# targetcli ls`

### From client
1. Discover the target.  
`# iscsiadm -m discovery -t st -p `*gateway_address*
* Login  
`# iscsiadm -m node -p `*gateway_address*` --login`
* Find device   
`# multipath -ll`
* Format, write data, read data
* Logout  
`# iscsiadm -m node -p `*gateway_address*` --logout`
* Delete discovery cache  
`# iscsiadm -m node -o delete`

### From gateway
1. From the gateway, clear the configuration  
`# lrbd -C`
* Unmap the RBD images  
`# lrbd -u`
* Wipe the configuration from Ceph  
`# lrbd -W`

## Manual

See [Wiki](https://github.com/swiftgist/lrbd/wiki)

## FAQ

* What is a gateway?

The gateway is simply a Linux host that supports iSCSI.  This host is providing iSCSI access to another host, a client or initiator, and is mapping Ceph RBD images locally.  Any client that cannot use Ceph directly (lack of library support), but supports iSCSI can still use Ceph storage.

One gateway can support multiple iSCSI targets which is primarily the reason for the distinction.

* Where should lrbd run?

For creating or editing the configuration, lrbd can run on any ceph client with proper credentials (e.g. ceph.client.admin.keyring).  For applying the configuration, lrbd runs on the host intended to be a gateway.

* What about configuring multipath?

Lrbd does not configure multipath on an initiator.  See **multipathd**. 
