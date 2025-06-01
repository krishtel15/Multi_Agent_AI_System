# Multi-Agent AI Document Processor

## Objective
A Python-based multi-agent system to classify and process inputs in PDF, JSON, and Email formats. It detects format and intent, routes data to specialized agents, and maintains shared context for traceability.

## Features
- Classifier Agent detects format & intent
- JSON Agent validates and extracts structured data
- Email Agent extracts sender, urgency, and intent
- PDF Agent extracts text and identifies key intents
- Shared context stored in Redis for session traceability
- Dark-themed Flask UI for easy uploads and visualization

## Setup
1. Install Redis (ensure running on port 6380)
2. Install dependencies:

```bash
pip install -r requirements.txt

