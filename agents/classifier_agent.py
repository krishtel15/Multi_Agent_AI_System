import json
import os

from shared_memory import SharedMemory

class ClassifierAgent:
    def __init__(self):
        self.memory = SharedMemory()

    def classify_format(self, input_path):
        ext = os.path.splitext(input_path)[1].lower()
        if ext == '.pdf':
            return 'PDF'
        elif ext == '.json':
            return 'JSON'
        elif ext in ['.eml', '.txt']:
            return 'Email'
        else:
            return 'Unknown'

    def classify_intent(self, content_text):
       
        keywords = {
            'invoice': ['invoice', 'amount due', 'bill'],
            'rfq': ['request for quotation', 'rfq', 'quote'],
            'complaint': ['complaint', 'issue', 'problem'],
            'regulation': ['regulation', 'compliance', 'law']
        }
        content_lower = content_text.lower()
        for intent, keys in keywords.items():
            if any(k in content_lower for k in keys):
                return intent
        return 'general'

    def route(self, input_path, conversation_id):
        format_ = self.classify_format(input_path)

        if format_ == 'Unknown':
            raise ValueError("Unsupported file format")

     
        content_text = ''
        if format_ == 'PDF':
            import fitz 
            doc = fitz.open(input_path)
            content_text = "\n".join(page.get_text() for page in doc)
        elif format_ == 'JSON':
            with open(input_path, 'r') as f:
                data = json.load(f)
            content_text = json.dumps(data)
       
        else:  
            with open(input_path, 'r', encoding='utf-8') as f:
                content_text = f.read()

        intent = self.classify_intent(content_text)

        # Log classification in shared memory
        self.memory.log_format_intent(conversation_id, format_, intent)

        # Route to appropriate agent
        if format_ == 'JSON':
            from agents.json_agent import JSONAgent
            agent = JSONAgent(self.memory)
        elif format_ == 'Email':
            from agents.email_agent import EmailAgent
            agent = EmailAgent(self.memory)
        elif format_ == 'PDF':
            from agents.pdf_agent import PDFAgent
            agent = PDFAgent(self.memory)

        else:
            raise NotImplementedError("PDF Agent not implemented yet")

        result = agent.process(input_path, conversation_id)

        return result
