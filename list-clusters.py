import boto3

def main():
    client = boto3.client('emr')
    response = client.list_clusters(ClusterStates=['STARTING','BOOTSTRAPPING','RUNNING','WAITING'])
    print(response['Id'])

if __name__ == '__main__':
    main()
