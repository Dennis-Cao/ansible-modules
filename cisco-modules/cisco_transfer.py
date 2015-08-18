#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2015, Dennis Cao <DennisCao@gmail.com>
#
# This file is module for Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
'''
Ansible module to transfer files to Cisco IOS devices.
'''
import time
from ansible.module_utils.basic import *
from netmiko import ConnectHandler, FileTransfer
DOCUMENTATION = '''
---
module: cisco_transfer
short_description: Copies files to Cisco IOS devices
description:
    - The M(cisco_transfer) module copies a file on a host server to a Cisco IOS device using commands sent over SSH.
options:
  host:
    description:
      - The ip address of the ansible control laptop. Used in establishing the SSH connection.
    required: true
    default: null
  port:
    description:
      - The port that will be used by SSH. Used in establishing the SSH connection.
    required: false
    default: 22
  username:
    description:
      - The account name you will be connecting to on the remote device. Used in establishing
        the SSH connection.
    required: true
    default: null
  password:
    description:
      - The password to the account you will be connecting to on the remote device. Used in
        establishing the SSH connection.
    required: true
    default: null
  source_file:
    description:
      - The path to the file on the sending server that you wish to transfer.
    required: true
    default: null
  target_dir:
    description:
      - The remote file system you want to transfer your files to.
    required: false
    default: flash
  target_name:
    description:
      - What you wish to name the transfered file on the remote server.
    required: false
    default: The value of the "source_file" parameter
  protocol:
    description:
      - The transfer protocol to be utilized. If using "http" or "https", you must specify
        a port number after the url seperated by a colon. Example: 192.168.2.1:8000
    required: true
    default: null
    choices: [ "http","https","tftp","ftp","scp","rcp"]
  host_url:
    description:
      - The URL of the server from which you will SEND the file to the cisco ios device.
      required: true
      default: null
author: Dennis Cao (DennisCao@live.com)
notes:
  - The Cisco IOS device must be SSH enabled. On the Cisco IOS device, the following options
    must be set in the configuration: "aaa new-model", "aaa authorization exec default local",
    "aaa authentication login default local". The account you are connecting to via SSH must
    have the appropriate permissions to copy over files.
'''
EXAMPLES = '''
# Transfer a new IOS image from an http server at 192.168.1.1 to a Cisco router with ip 192.168.1.5
- cisco_transfer:
    host=192.168.1.5
    username=cisco
    password=cisco
    source_file=c180x-adventerprisek9-mz.124-24.T7.bin
    host_url=192.168.1.1
    target_name=c180x-adventerprisek9-mz.124-24.T7.bin
    protocol=http:8000

# Transfer a configuration file from a tftp server at 10.22.66.71 to the slot0 filesystem of a Cisco router with ip 192.168.1.5
- cisco_transfer:
    host=10.22.66.71
    username=cisco
    password=cisco
    source_file=new_configuration_file.txt
    host_url=192.168.1.1
    target_name=config
    target_dir=slot0
    protocol=tftp
'''
def main():

    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=True),
            port=dict(default=22, required=False),
            username=dict(required=True),
            password=dict(required=True),
            source_file=dict(required=True),
            target_dir=dict(required=False, default="flash"),
            target_name=dict(required=False, default=False),
            protocol=dict(required=True),
            host_url=dict(required=True)
        ),
        supports_check_mode=False
    )

    source_file = module.params['source_file']
    target_name = module.params['target_name']
    if(not target_name):
        target_name=source_file
    target_dir = module.params['target_dir']
    host_url = module.params['host_url']
    protocol = module.params['protocol'] + "://"
    net_device = {
        'device_type': 'cisco_ios',
        'ip': module.params['host'],
        'username': module.params['username'],
        'password': module.params['password'],
        'port': int(module.params['port']),
        'verbose': False,
    }
    ssh_conn = ConnectHandler(**net_device)
    output=ssh_conn.enable()
    output = ssh_conn.send_command_expect("copy " + protocol+host_url + "/" + source_file+" " + target_dir + ":" + target_name,"filename")
    if("No such file or directory" in output):
        module.fail_json(msg="Note enough space on device",changed=False)
    output = ssh_conn.send_command(target_name)
    if("Not enough space on device" in output):
        module.fail_json(msg="Note enough space on device",changed=False)
    while(True):
        newoutput = ssh_conn.find_prompt()
        if "!" not in newoutput:
            break
        time.sleep(5)


    module.exit_json(msg=output,changed=True)


if __name__ == "__main__":
    main()
