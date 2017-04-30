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
            "Values": ["running"]
        }
    ]
    # Collect my fleet info
    instances = ec2.instances.filter(Filters=myfleet)

    # and select only stopped instance id's
    runningInstances = [instance.id for instance in instances]

    if runningInstances:
        bringThemDown = ec2.instances.filter(InstanceIds=stoppedInstances).stop()
    else:
        print("Nothing to do here"):


