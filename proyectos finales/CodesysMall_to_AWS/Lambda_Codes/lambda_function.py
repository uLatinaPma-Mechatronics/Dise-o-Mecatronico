import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('dynamodb')
    
    update_expressions = []
    expression_attribute_values = {}

    
    for attribute_name in ['AC_OnOff', 'Lights_OnOff', 'AutoCleaning_OnOff', 'Escalator_Speed_F12', 'Escalator_Speed_F23']:
        if attribute_name in event:
            update_expressions.append(f"{attribute_name} = :{attribute_name.lower()}")
            expression_attribute_values[f":{attribute_name.lower()}"] = {'N': str(event[attribute_name])}
    
    update_expression_str = 'SET ' + ', '.join(update_expressions)
    
    response = client.update_item(
        TableName='CodesysMall_Status',
        Key={'HOUR': {'N': str(event['HOUR'])}},
        UpdateExpression=update_expression_str,
        ExpressionAttributeValues=expression_attribute_values,
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }