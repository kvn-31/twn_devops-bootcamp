import boto3

client = boto3.client('eks', region_name='eu-central-1')
clusters = client.list_clusters()['clusters']

for cluster in clusters:
    response = client.describe_cluster(name=cluster)
    cluster_info = response['cluster']
    cluster_status = cluster_info['status']
    cluster_endpoint = cluster_info['endpoint']
    cluster_version = cluster_info['version']

    print(f"Cluster {cluster} has status {cluster_status}")
    print(f"Cluster endpoint is {cluster_endpoint}")
    print(f"Cluster version is {cluster_version}")

