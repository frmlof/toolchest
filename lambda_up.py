import boto3

# Connect
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    myfleet = [{
            "Name": "tag:Name",
            "Values": ['workhorse']
        },
        {
            "Name": "instance-state-name",
            "Values": ["stopped"]
        }
    ]
    # Collect my fleet info
    instances = ec2.instances.filter(Filters=myfleet)

    # and select only stopped instance id's
    stoppedInstances = [instance.id for instance in instances]

    if stoppedInstances:
        bringThemUp = ec2.instances.filter(InstanceIds=stoppedInstances).start()
    else:
        print("Nothing to do here"):


