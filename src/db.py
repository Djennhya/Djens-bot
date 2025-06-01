import boto3

# Création de la ressource DynamoDB et sélection de la table 'messages'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('messages')

def save_message(conversation_id, question, answer, timestamp):
    """
    Sauvegarde un message dans la table DynamoDB.

    """
    table.put_item(Item={
        'conversation_id': conversation_id,
        'timestamp': timestamp,
        'question': question,
        'answer': answer
    })

def get_messages(conversation_id):
    """
    Récupère tous les messages d'une conversation, triés par timestamp croissant.

    """
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('conversation_id').eq(conversation_id),
        ScanIndexForward=True  # Trie par timestamp croissant
    )
    return response.get('Items', [])

def delete_messages(conversation_id):
    """
    Supprime tous les messages d'une conversation spécifique.

    """
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('conversation_id').eq(conversation_id)
    )
    for item in response.get('Items', []):
        table.delete_item(
            Key={
                'conversation_id': item['conversation_id'],
                'timestamp': item['timestamp']
            }
        )
    return True

def delete_conversation(conversation_id):
    """
    Supprime une conversation (tous ses messages).

    """
    return delete_messages(conversation_id)

def get_conversations():
    """
    Récupère la liste de tous les identifiants de conversation.

    """
    response = table.scan(
        ProjectionExpression='conversation_id',
        Select='SPECIFIC_ATTRIBUTES'
    )
    conversations = set()
    for item in response.get('Items', []):
        conversations.add(item['conversation_id'])
    return list(conversations)

def get_conversation_messages(conversation_id):
    """
    Récupère tous les messages d'une conversation, triés par timestamp croissant.

    """
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('conversation_id').eq(conversation_id),
        ScanIndexForward=True  # Trie par timestamp croissant
    )
    return response.get('Items', [])

def get_all_messages():
    """
    Récupère tous les messages de toutes les conversations.

    """
    response = table.scan()
    return response.get('Items', [])

def delete_all_messages():
    """
    Supprime tous les messages de la table.
    
    """
    response = table.scan()
    for item in response.get('Items', []):
        table.delete_item(
            Key={
                'conversation_id': item['conversation_id'],
                'timestamp': item['timestamp']
            }
        )
    return True