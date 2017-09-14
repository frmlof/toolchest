#!/usr/bin/env python

import os
import sys
import boto3

#
REGIONS = ('us-east-1',
           'us-east-2',
           'us-west-1',
           'us-west-2')

SSH_STR = 'ssh -i ~/.ssh/magicKey.pem'

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
    if len(sys.argv) > 1:
        # try to connect
        for region in REGIONS:
            get_host_name = setServiceConnection(region, sys.argv[1])
            cmd = ('%s hadoop@%s' % (SSH_STR, get_host_name))
        os.system(cmd)
        #print(cmd)
    else:
        sys.exit('You must specify EMR cluster id to connect to Master node')
