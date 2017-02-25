#!/usr/bin/env python

"""
    Author: Nazim Aliyev (nazim.b.aliyev AT gmail DOT com)
    Version: 0.0.1a / 02-24-2017

    The myenv.py is part of toolchest.

    toolchest is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toolchest is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toolchest.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import boto3
import argparse

REGIONS = ('us-east-1',
           'us-east-2',
           'us-west-1',
           'us-west-2')

def envUp(region):
    region_inst = []
    session = boto3.Session(region_name = region)
    ec2 = session.resource('ec2')
    for instance in ec2.instances.all():
        for tags in instance.tags:
            if tags['Key'] == 'Name' and tags['Value'] == 'workhorse' and instance.state['Name'] == 'stopped':
                instance.start()
#                instance.wait_until_running()
                region_inst.append("Bringing up %s in a %s" % (instance.instance_id,region))
    return region_inst

def envDown(region):
    region_inst = []
    session = boto3.Session(region_name = region)
    ec2 = session.resource('ec2')
    for instance in ec2.instances.all():
        if instance.state['Code'] == 16:
            for tags in instance.tags:
                if tags['Key'] == 'OS' or tags['Value'] == 'workhorse' or tags['Value'] == 'keepalive':
                    instance.stop()
#                    instance.wait_until_stopped()
                    region_inst.append('Stopping %s in %s' % (instance.instance_id,region))
                else:
                    instance.terminate()
#                    instance.wait_until_terminated()
                    region_inst.append('Terminating %s in %s' % (instance.instance_id,region))
    return region_inst

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--up', dest = 'up', action='store_true', help = 'Bring all instances with "worhorse" tag up')
    parser.add_argument('--down', dest = 'down', action='store_true', help = 'Stop all instances with "worhorse" and "donoterm" down, terminate all other instance(s)')
    args = parser.parse_args()

    if args.up:
        for region in REGIONS:
            bringItUp = envUp(region)
            for line in bringItUp:
                print(line)
    elif args.down:
        for region in REGIONS:
            tearItDown = envDown(region)
            for line in tearItDown:
                print(line)
    else:
        sys.exit('Usage: myenv --up|--down')
