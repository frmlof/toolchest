#!env python

import os
import sys
import boto3
import argparse
import ConfigParser

CONFIG_FILE = os.path.expanduser('~/.aws/config')

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
    parser = argparse.ArgumentParser()
    parser.add_argument('--cluster-id', dest='cluster', required=True, help='Connect to EMR cluster')
    parser.add_argument('--region', dest='region', required=False, help='Set region for the connection')
    args = parser.parse_args()

    if args.cluster:
        region = args.region

        # check region

        if not args.region:
            if os.path.isfile(CONFIG_FILE):
                # parse cofig
                config = ConfigParser.ConfigParser()
                config.read(CONFIG_FILE)
                #for profile in config.options('default'):
                region = config.get('default', 'region')
                get_host = setServiceConnection(region, args.cluster)
            else:
                sys.exit('Default region has not been setup yet. You must specify region name with --region and re-run this script')
        else:
            region = args.region
            get_host = setServiceConnection(region, args.cluster)
