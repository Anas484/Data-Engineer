import json
import boto3

sns = boto3.client('sns')

def lambda_handler(event, context):
    data = event
    patient_id = data['patient_id']
    heartbeat = data['heartbeat']
    blood_SPO2 = data['blood_SPO2']
    blood_ps = data['blood_ps']
    respiration_rate = data['respiration_rate']

    TOPIC_ARN = 'arn:aws:sns:ap-south-1:420550168880:patient_alert'

    message = {
        "patient_id": patient_id,
        "status": "Critical --- Needs Attention !!!",
        "data" : data
    }

    if (heartbeat > 140) or (blood_SPO2 < 93) or (blood_ps > 180) or (blood_ps < 50) or (respiration_rate < 15) :

        response = sns.publish(
        TopicArn=TOPIC_ARN,
        Message=json.dumps(message),
        Subject='🚨 Patient Alert')

        return {
            "patient_id": patient_id,
            "status": "Critical --- Needs Attention !!!",
            "alert": "Notification sent succesfully"}
    else:
        return {
            'status' : 'Normal --- No Attention Needed'
        }        
