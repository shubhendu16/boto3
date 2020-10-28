import boto3

def aws_session(role_arn=None, session_name='my_session'):
    client = boto3.client('sts')
    response = client.assume_role(RoleArn=role_arn, RoleSessionName=session_name)
    session = boto3.Session(
        aws_access_key_id=response['Credentials']['AccessKeyId'],
        aws_secret_access_key=response['Credentials']['SecretAccessKey'],
        aws_session_token=response['Credentials']['SessionToken'])
    return session

ec2 = session.resource('ec2')
volumes = ec2.volumes.all()

to_terminate=[]
for volume in volumes:
    print('Evaluating volume {0}'.format(volume.id))
    print('The number of attachments for this volume is {0}'.format(len(volume.attachments)))
    if len(volume.attachments) == 0:
        to_terminate.append(volume)

if len(to_terminate) == 0:
    print ("No volumes to terminate! Exiting.")
    exit()

for volume in to_terminate:
    print('Deleting volume {0}'.format(volume.id))
    volume.delete()