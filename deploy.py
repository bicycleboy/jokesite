import random
import string
import sys
import argparse
import base64
import os

def randomPassword(length):
    randomSource = string.ascii_letters + string.digits + string.punctuation
    password = random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
    password += random.choice(string.punctuation)

    for i in range(length):
        password += random.choice(randomSource)

    passwordList = list(password)
    random.SystemRandom().shuffle(passwordList)
    password = ''.join(passwordList)
    return password

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deploy Jokesite to OpenSHift')
    parser.add_argument('ProjectName', metavar='projectname', type=str, help='The name of the OpenShift Project')
    parser.add_argument('APIEndpoint', metavar='apiendpoint', type=str, help='The name of the OpenShift API Endpoint')
    parser.add_argument('-s', '--source', action="store_true", help='Build from local source (default is Quay')
    args = parser.parse_args()
    project_name = args.ProjectName
    api_endpoint = args.APIEndpoint
else:
    sys.exit(1)

data =randomPassword(10)
encodedBytes = base64.b64encode(data.encode("utf-8"))
database_password = str(encodedBytes, "utf-8")
data = randomPassword(8)
encodedBytes = base64.b64encode(data.encode("utf-8"))
database_user = str(encodedBytes, "utf-8")
data = randomPassword(20)
encodedBytes = base64.b64encode(data.encode("utf-8"))
django_secret_key = str(encodedBytes, "utf-8")

secretFileName = 'yaml/' + project_name + "-secret.yaml"
secretFile = open(secretFileName, "w")
secretFile.write('\
kind: Secret\n\
apiVersion: v1\n\
metadata:\n\
  name: ' + project_name + '\n\
  namespace: ' + project_name + '\n\
  labels:\n\
    app: jokesite\n\
data:\n\
  database-password: ' + database_password + '\n\
  database-user: ' + database_user + '\n\
  django-secret-key: ' + django_secret_key + '\n\
type: Opaque\n\
')
secretFile.close()


cmd = "oc new-project " + project_name
print(cmd)
if os.system(cmd): sys.exit(1)

if args.source:
    # from git 
    #cmd = "oc new-app https://github.com/bicycleboy/jokesite"
    # from local source
    cmd = "oc new app ./jokesite"
    print(cmd)
    if os.system(cmd): sys.exit(1)
else:
    # assumes files in ./yaml refer to pre built container on Quay (which has a rebuild trigger on push to git)
    cmd = 'oc apply -f yaml'
    print(cmd)
    if os.system(cmd): sys.exit(1)
    cmd = 'oc expose svc/' + project_name
    print(cmd)
    if os.system(cmd): sys.exit(1)