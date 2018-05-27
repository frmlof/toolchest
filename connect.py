lust

"""
    Version: 0.1.0 / 05-06-2017

    The connect.py is part of toolchest.

    Copyright (c) 2017 Nazim Aliyev

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

"""

import os
import sys
import argparse
import ConfigParser

REGIONS = ('us-east-1',
           'us-east-2',
           'us-west-1',
           'us-west-2')

# Check if boto3 present
try:
    import boto3
except ImportError:
    sys.exit("To run this script please install boto3: pip install boto3")

# path to configuration file
configFile = '~/.aws/config'


# retiring in favor of config variable
#SHSTR = 'ssh -i ~/.ssh/<YOUR_KEY>'

def discoverHost(region,myos):
    mysession = boto3.Session(region_name = region)
    ec2 = mysession.resource('ec2')
    filter = [{
            'Name':'tag: OS',
            'Values': [myos]
        },
        {
            'Name':'instance-state-name',
            'Values': ['running']

    }]

    instances = ec2.instances.filter(Filter=filter)
    my_pal = [instance.public_ip_address for instance in instances]
    host_ip = ''.join(my_pal)
    return host_ip

def pathToPem:
    #
    path = ConfigParser.ConfigParser()
    if os.path.isfile(configFile):
        # read content
        # check if path really exist
        config.read(configFile)
        keyPath = config.get('KeyPath','PEM')
    else:
        # ask to add path to pem file
        # check if path really exist
        sys.exit('The connect was not setup yet. Please run script with "--init"')
    return keyPath

def getkeypath():
    if os.path.isfile('~/.aws/credentials'):
        # credentials file exist
        # check if key is not empty
    else:
        sys.exit('Connect requires CLI-like credentials in place.')



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
