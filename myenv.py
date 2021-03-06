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
import time
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
        if instance.state['Code'] == 80:
            try:
                for tags in instance.tags:
                    if tags['Value'] == 'workhorse':
                        instance.start()
                        region_inst.append("Bringing up %s in a %s" % (instance.instance_id,region))
            except(TypeError):
                pass
    return region_inst

def envDown(region):
    region_inst = []
    session = boto3.Session(region_name = region)
    ec2 = session.resource('ec2')
    for instance in ec2.instances.all():
        if instance.state['Code'] == 16:
            try:
                for tags in instance.tags:
                    if tags['Key'] == 'OS' or tags['Value'] == 'workhorse' or tags['Value'] == 'keepalive':
                        instance.stop()
                        region_inst.append('Stopping %s in %s' % (instance.instance_id,region))
                    else:
                        instance.terminate()
                        region_inst.append('Terminating %s in %s' % (instance.instance_id,region))
            except(TypeError):
                pass
    return region_inst

def envList(region):
    region_inst = []
    session = boto3.Session(region_name = region)
    ec2 = session.resource('ec2')
    for instance in ec2.instances.all():
        if instance.state['Code'] == 16:
            try:
                for tag in instance.tags:
                    region_inst.append('%s in %s' % (instance.instance_id, region))
            except(TypeError):
                pass
    return region_inst

def envReplace(region,myos):
    session = boto3.Session(region_name = region)
    ec2 = session.resource('ec2')
    filter = [{
            'Name': 'tag:Name',
            'Values': ['workhorse']
        },
        {
            'Name': 'tag:OS',
            'Values': [myos]
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ]
    instances = ec2.instances.filter(Filters=filter)
    my_image = [instance.image_id for instance in instances]
    my_sid = [instance.subnet_id for instance in instances]
    return my_image,my_sid


if __name__ == '__main__':
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--up', dest = 'up', action = 'store_true', help = 'Bring all instances with "worhorse" tag up')
    parser.add_argument('--down', dest = 'down', action = 'store_true', help = 'Stop all instances with "worhorse" and "donoterm" down, terminate all other instance(s)')
    parser.add_argument('--list', dest = 'list', action = 'store_true', help = 'List runing instances in regions of my interest')
    parser.add_argument('--replace', dest = 'replace', help = 'Replace one of your existing. ')
    args = parser.parse_args()

    if args.up:
        for region in REGIONS:
            bringItUp = envUp(region)
            for line in bringItUp:
                print(line)
    elif args.down:
        for region in REGIONS:
            tearItDown = envDown(region)
            for line in set(tearItDown):
                print(line)
    elif args.list:
        for region in REGIONS:
            listItAll = envList(region)
            for line in set(listItAll):
                print(line)
    elif args.replace:
        for region in REGIONS:
            #replaceIt = envReplace(region, args.replace)
            my_ami, my_sid = envReplace(region, args.replace)
            #if replaceIt:
            #    my_ami = ''.join(replaceIt)
            target_ami = ''.join(my_ami)
        print(target_ami)
        #print(replaceIt)

    else:
        sys.exit('Usage: myenv --up || --down || --list')

    end = time.time()
    print('--\nI run in four regions in %.4f seconds' % (end-start))
