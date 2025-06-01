import re

class EmailAgent:
    def __init__(self, shared_memory):
        self.memory = shared_memory

    def extract_sender(self, content):
        # Very simple regex to extract email sender in "From:" line
        match = re.search(r'^From:\s*(.+)$', content, re.MULTILINE | re.IGNORECASE)
        return match.group(1).strip() if match else 'unknown'

    def detect_urgency(self, content):
        urgent_words = ['urgent', 'asap', 'immediately', 'priority']
        if any(word in content.lower() for word in urgent_words):
            return True
        return False

    def process(self, email_path, conversation_id):
        with open(email_path, 'r', encoding='utf-8') as f:
            content = f.read()

        sender = self.extract_sender(content)
        urgency = self.detect_urgency(content)

      
        intent = 'rfq' if 'request for quotation' in content.lower() else 'general'

        context = {
            'sender': sender,
            'urgency': urgency,
            'intent': intent,
        }

        self.memory.set_context(conversation_id, context)

        return context
