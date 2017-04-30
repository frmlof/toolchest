import boto3

# Connect
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    trashFleet = [{
            "Name": "instance-state-name",
            "Values": ["running"]
        }
    ]
    # Collect my fleet info
    instances = ec2.instances.filter(Filters=trashFleet)

    # and select only stopped instance id's
    trashInstances = [instance.id for instance in instances]

    if trashInstances:
        bringThemUp = ec2.instances.filter(InstanceIds=trashInstances).terminate()
    else:
        print("Nothing to do here"):


