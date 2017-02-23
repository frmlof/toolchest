#!/usr/bin/env python

#    connect.py version 0.0.1
#    connect.py is part of tool chest I am developing for my own needs
#    For now code will released under GPLv3
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>



import os
import boto3
import argparse

REGIONS = ('us-east-1',
           'us-east-2',
           'us-west-1',
           'us-west-2')

class ConnectToHost:
    def __init__(self,myregion, myos):
        self.region = myregion
        self.this_session = boto3.Session(region_name = self.region)
        self.ec2 = self.this_session.resource('ec2')
        self.os = myos

    def discoverHost(self):
        host_id = ''
        for instance in self.ec2.instances.all():
            if instance.state['Name'] == 'running':
                for tags in instance.tags:
                    if tags['Key'] == 'OS' and tags['Value'] == self.os:
                        host_id = instance.public_dns_name
        return host_id

SSHSTR = 'ssh -i ~/.ssh/<key_name>'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--os', dest='os', help='Specify distribution')
    args = parser.parse_args()

    if args.os:
        for region in REGIONS:
            gethost = ConnectToHost(region,args.os)
            myhost = gethost.discoverHost()
            if myhost:
                if args.os == 'rhel7' or args.os == 'suse' or args.os == 'amazon':
                    user = 'ec2-user'
                elif args.os == 'centos':
                    user = 'centos'
                elif args.os == 'debian':
                    user = 'admin'
                elif args.os == 'ubuntu':
                    user = 'ubuntu'
                cmd = ("%s %s@%s" % (SSHSTR,user,myhost))
                os.system(cmd)
