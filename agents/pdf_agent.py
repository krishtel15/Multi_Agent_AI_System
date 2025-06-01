import fitz
import re

class PDFAgent:
    def __init__(self, shared_memory):
        self.memory = shared_memory

    def extract_fields(self, text):
        # Very basic pattern extraction (expandable)
        invoice_id = re.search(r'Invoice\s*#?:?\s*(\w+)', text, re.IGNORECASE)
        amount = re.search(r'Amount\s*Due?:?\s*\$?(\d+(?:\.\d{2})?)', text, re.IGNORECASE)
        date = re.search(r'Date:? (\d{4}-\d{2}-\d{2})', text)
        customer = re.search(r'Customer:? ([\w\s&]+)', text)

        return {
            'invoice_id': invoice_id.group(1) if invoice_id else None,
            'amount': float(amount.group(1)) if amount else None,
            'date': date.group(1) if date else None,
            'customer': customer.group(1).strip() if customer else None
        }

    def process(self, pdf_path, conversation_id):
        doc = fitz.open(pdf_path)
        full_text = "\n".join(page.get_text() for page in doc)

        fields = self.extract_fields(full_text)
        anomalies = [k for k, v in fields.items() if v is None]

        context = {
            'extracted_fields': fields,
            'anomalies': anomalies
        }

        self.memory.set_context(conversation_id, context)
        return context
