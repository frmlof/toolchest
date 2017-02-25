# toolchest

## Why?
I was testing different flavor of Linux instance in AWS, and come accross problem when I needed to access instance running Debian and I spent sometime trying to figure out which one is the right one.

I am running this code on daily basis on my Mac and Fedora.

That's how I come accross [AWS Tags](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html) and [Boto3](https://aws.amazon.com/sdk-for-python/).

## Prerequisites
You have to have boto3 installed on your system. Follow guide listed in [Boto3 home page on GitHub](https://github.com/boto/boto3#user-content-quick-start).

## Tag convension
These are tags I have setup for easy access, you free to update or change code provided based on your needs.

| Key           | Value           |
| ------------- |:---------------:|
| Name          | workhorse       |
| OS            | key word        |

Instances with tags above I stop-start on daily basis. I also add *special* tag

| Key           | Value           |
| ------------- |:---------------:|
| Name          | keepalive       |

with myenv --down any instance that does not have tags listed above will get terminated. Same script can bring instances back up, but it will ignore instances with "keepalive" tag.

These are list of pre-defined keywords

| Word          | Distro           |
| ------------- |:----------------:|
| amazon        | Amazon Linux     |
| debian        | Debian Linux     |
| ubuntu14      | Ubuntu LTS 14.04 |
| ubuntu16      | Ubuntu LTS 16.04 |
| rhel6         | RHEL 6           |
| rhel7         | RHEL 7           |
| suse11        | SLES 11          |
| suse12        | SLES 12          |
*feel free to play with this list as you wish*
