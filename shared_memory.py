import redis
import json
from datetime import datetime

class SharedMemory:
    def __init__(self, host='localhost', port=6380):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)

    def set_context(self, conversation_id, data):
        """Save a dict as JSON string keyed by conversation ID"""
        data['timestamp'] = datetime.utcnow().isoformat()
        self.client.set(conversation_id, json.dumps(data))

    def get_context(self, conversation_id):
        """Retrieve and parse JSON context by conversation ID"""
        raw = self.client.get(conversation_id)
        if raw:
            return json.loads(raw)
        return {}

    def log_format_intent(self, conversation_id, format_, intent):
        """Keep a simple log entry of classification"""
        entry = {
            'format': format_,
            'intent': intent,
            'timestamp': datetime.utcnow().isoformat()
        }
        self.client.set(f"{conversation_id}_log", json.dumps(entry))
