import time
import boto3
from typing import List, Dict
from db_adapter import DatabaseAdapter

class DynamoDBAdapter(DatabaseAdapter):
    def __init__(self, table_name: str):
        self.table = boto3.resource("dynamodb").Table(table_name)

    def save_message(self, chat_id: int, username: str, message: str) -> None:
        self.table.put_item(Item={
            "conversation_id": str(chat_id),
            "timestamp": int(time.time()),
            "type": "user",
            "username": username,
            "message": message
        })

    def save_response(self, chat_id: int, response: str) -> None:
        self.table.put_item(Item={
            "conversation_id": str(chat_id),
            "timestamp": int(time.time()),
            "type": "bot",
            "message": response
        })

    def get_conversation(self, chat_id: int) -> List[Dict[str, str]]:
        response = self.table.query(
            KeyConditionExpression="conversation_id = :cid",
            ExpressionAttributeValues={":cid": str(chat_id)}
        )
        items = response.get("Items", [])
        return [
            {
                "sender": item.get("type", "user"),
                "message": item.get("message", "")
            }
            for item in sorted(items, key=lambda x: x["timestamp"])
        ]

    def reset_conversation(self, chat_id: int) -> None:
        # Suppression manuelle : scan + delete (non optimal mais fonctionne pour des petits volumes)
        response = self.table.query(
            KeyConditionExpression="conversation_id = :cid",
            ExpressionAttributeValues={":cid": str(chat_id)}
        )
        for item in response.get("Items", []):
            self.table.delete_item(
                Key={
                    "conversation_id": item["conversation_id"],
                    "timestamp": item["timestamp"]
                }
            )
