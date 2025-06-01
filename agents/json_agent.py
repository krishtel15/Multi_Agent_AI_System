import json

class JSONAgent:
    def __init__(self, shared_memory):
        self.memory = shared_memory

    def process(self, json_path, conversation_id):
        with open(json_path, 'r') as f:
            data = json.load(f)

        
        target_schema = ['invoice_id', 'amount', 'date', 'customer']

        anomalies = []
        for key in target_schema:
            if key not in data:
                anomalies.append(f"Missing field: {key}")

       
        context = {
            'extracted_fields': {k: data.get(k) for k in target_schema},
            'anomalies': anomalies
        }
        self.memory.set_context(conversation_id, context)

        return context
