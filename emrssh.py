#!/usr/bin/env python

import os
import sys
import boto3

#
REGIONS = ('us-east-1',
           'us-east-2',
           'us-west-1',
           'us-west-2')

SSH_STR = 'ssh -i ~/.ssh/magicKey.pem -o TCPKeepAlive=yes -o ServerAliveInterval=120'

def setServiceConnection(region, cluster):
    # Establish service connection
    session = boto3.Session(region_name=region)
    ec2 = session.resource('ec2')

    # Set filter
    filter = [{
            'Name':'tag:aws:elasticmapreduce:instance-group-role',
            'Values':['MASTER']
        },
        {
            'Name':'tag:aws:elasticmapreduce:job-flow-id',
            'Values':[cluster]
    }]

    # Filter out EC2 instances with required tag
    instances = ec2.instances.filter(Filters = filter)
    the_dude = [instance.public_ip_address for instance in instances]
    host_id = ''.join(the_dude)
    return host_id


if __name__ == '__main__':
    #if len(sys.argv) > 1:
    if sys.argv[1]:
        # try to connect
        for region in REGIONS:
            get_host_name = setServiceConnection(region, sys.argv[1])
            if get_host_name:
                print(get_host_name)
                cmd = ('%s hadoop@%s' % (SSH_STR, str(get_host_name)))
                print(cmd)
               # os.system(cmd)
        """
        get_host_name = [setServiceConnection(region, sys.argv[1]) for region in REGIONS]
        filter(None, get_host_name)
        if get_host_name:
            print(get_host_name)
        """
    else:
        sys.exit('You must specify EMR cluster id to connect to Master node')
