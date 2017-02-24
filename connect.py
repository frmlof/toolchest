#!/usr/bin/env python

"""
    Author: Nazim Aliyev (nazim.b.aliyev AT gmail DOT com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

import os
import sys
import boto3
import argparse

REGIONS = ('us-east-1',
           'us-east-2',
           'us-west-1',
           'us-west-2')

# Specify path to your ssh key pair or pem file here
SSHSTR = 'ssh -i ~/.ssh/<YOUR_KEY>'

def discoverHost(region,myos):
    mysession = boto3.Session(region_name = region)
    ec2 = mysession.resource('ec2')
    host_id = ''
    for instance in ec2.instances.all():
        if instance.state['Name'] == 'running':
            for tags in instance.tags:
                if tags['Key'] == 'OS' and tags['Value'] == myos:
                    host_id = instance.public_dns_name
    return host_id

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--os', dest = 'os', help = 'Specify target Operating System tag associated with your instance')
    args = parser.parse_args()

    if args.os:
        for region in REGIONS:
            myos = args.os
            getHost = discoverHost(region,myos)
            if getHost:
                if args.os == 'rhel6' or args.os == 'rhel7' or args.os == 'suse12' or args.os == 'suse11' or args.os == 'amazon':
                    user = 'ec2-user'
                elif args.os == 'centos6' or args.os == 'centos7':
                    user = 'centos'
                elif args.os == 'debian':
                    user = 'admin'
                elif args.os == 'ubuntu14' or args.os == 'ubuntu16':
                    user = 'ubuntu'
                cmd = ('%s %s@%s' % (SSHSTR,user,getHost))
                os.system(cmd)
    else:
        sys.exit('Usage: connect --os <target os>')
