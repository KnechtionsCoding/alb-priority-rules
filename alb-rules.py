#!/user/bin/env python3

import boto3
import click
import time
import json
from botocore.exceptions import ClientError

def describe_albs(alb_name):
    elb = boto3.client('elbv2')
    response = elb.describe_load_balancers(
        Names = [
            alb_name
    ])

    alb_arn = response['LoadBalancers'][0]['LoadBalancerArn']
    return alb_arn

def describe_listeners(alb_arn):
    listener = boto3.client('elbv2')
    response = listener.describe_listeners(
        LoadBalancerArn = alb_arn
    )
    listener_arn = response["Listeners"][0]["ListenersArn"]

    return listener_arn

def get_alb_rules(listener_arn):
    listener = boto3.client('elbv2')
    response = listener.describe_listeners(
        LoadBalancerArn = listener_arn
    )
    for Rule in response["Rules"]:
        try:
            data = {}
            data['path-pattern'] = Rule['Conditions'][0]['Values']
            data['host-header'] = Rule['Conditions'][1]['Values']
            data['priority'] = Rule['Priority']
            print(json.dumps(data, indent=4))
        except:
            print('Reached end of Rules')
    return data

@click.command()
@click.option(
    "--loadbalancer", "-alb", 
    default='', 
    help="Enter loadbalancer name: ", 
    required=True, 
    prompt='Please enter the loadbalancer name you would like to get rules for',
)
def show_priority(loadbalancer):

    product = product.lower()
        
    alb_arn = describe_albs(loadbalancer)
    listener_arn = describe_listeners(alb_arn)
    rules = get_alb_rules(listener_arn)

if __name__ == '__main__':
    intro_text = "This tool assumes that you have AWS credentials stored somewhere Boto3 can access. See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html for more information"
    print(intro_text)
    time.sleep(2)
    show_priority()