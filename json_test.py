import json

with open('instances.json') as jsonInstancesFile:
    instancesJson = json.load(jsonInstancesFile)
    print(instancesJson)