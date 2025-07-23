import openai
from openai import OpenAI
from typing import Dict, List
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
    
    async def generate_billing_summary(self, email_data: Dict) -> Dict:
        """Generate a billing summary from email content using OpenAI"""
        try:
            prompt = self._create_billing_prompt(email_data)
            
            # Use the new OpenAI client
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a legal billing assistant. Generate professional billing summaries from email communications. Always include estimated time and a concise description. Format your response with clear sections for Time, Description, and Activities."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            summary_text = response.choices[0].message.content
            logger.info(f"Generated summary: {summary_text[:100]}...")
            
            # Parse the summary to extract billing information
            billing_info = self._parse_billing_summary(summary_text)
            
            return {
                'summary': summary_text,
                'billing_hours': billing_info.get('hours', '0.25'),
                'billing_description': billing_info.get('description', summary_text[:200]),
                'client_matter': billing_info.get('client_matter', 'General')
            }
            
        except Exception as e:
            logger.error(f"Error generating summary with OpenAI: {e}")
            # Fallback to simple rule-based summary
            return self._generate_fallback_summary(email_data)
    
    def _create_billing_prompt(self, email_data: Dict) -> str:
        """Create a prompt for billing summary generation"""
        return f"""
        Please analyze the following email and create a professional billing summary for legal time tracking:
        
        Subject: {email_data.get('subject', 'No Subject')}
        From: {email_data.get('sender', 'Unknown')}
        To: {email_data.get('recipient', 'Unknown')}
        Date: {email_data.get('date_sent', 'Unknown')}
        
        Email Content:
        {email_data.get('body', '')[:2000]}
        
        Please provide a structured response with:
        
        Time: [Estimated hours in decimal format, e.g., 0.25, 0.5, 1.0]
        Description: [Brief professional billing description suitable for client invoicing]
        Activities: [List of key legal activities performed]
        
        Consider these factors for time estimation:
        - Simple email responses: 0.25 hours
        - Document review/drafting: 0.5-1.0 hours  
        - Client meetings/calls: 0.5-2.0 hours
        - Research and analysis: 1.0+ hours
        """
    
    def _parse_billing_summary(self, summary: str) -> Dict:
        """Parse the AI-generated summary to extract billing components"""
        lines = summary.split('\n')
        
        billing_info = {
            'hours': '0.25',  # default
            'description': '',
            'client_matter': 'General'
        }
        
        # Look for structured response
        for line in lines:
            line = line.strip()
            if line.lower().startswith('time:'):
                # Extract numeric values
                import re
                time_match = re.search(r'(\d+\.?\d*)', line)
                if time_match:
                    billing_info['hours'] = time_match.group(1)
            
            elif line.lower().startswith('description:'):
                desc = line.split(':', 1)[1].strip()
                if desc:
                    billing_info['description'] = desc[:200]
        
        # If no structured description found, use first meaningful sentence
        if not billing_info['description']:
            sentences = summary.split('.')
            for sentence in sentences:
                if len(sentence.strip()) > 20 and not sentence.strip().lower().startswith('time'):
                    billing_info['description'] = sentence.strip()[:200]
                    break
            
            # Final fallback
            if not billing_info['description']:
                billing_info['description'] = summary[:200]
        
        return billing_info
    
    def _generate_fallback_summary(self, email_data: Dict) -> Dict:
        """Generate a simple rule-based summary as fallback"""
        subject = email_data.get('subject', 'Email Communication')
        body = email_data.get('body', '')
        
        # Enhanced keyword-based time estimation
        time_estimate = '0.25'  # default 15 minutes
        
        subject_lower = subject.lower()
        body_lower = body.lower()
        
        # Meeting/call related
        if any(word in subject_lower for word in ['meeting', 'call', 'conference', 'zoom', 'teams']):
            time_estimate = '1.0'
        # Document work
        elif any(word in subject_lower for word in ['review', 'draft', 'contract', 'agreement', 'document']):
            time_estimate = '0.5'
        # Research/analysis
        elif any(word in subject_lower for word in ['research', 'analysis', 'memo', 'brief']):
            time_estimate = '1.0'
        # Long emails get more time
        elif len(body) > 1000:
            time_estimate = '0.5'
        elif len(body) > 2000:
            time_estimate = '1.0'
        
        # Generate description based on content
        if 'meeting' in subject_lower:
            description = f"Email correspondence regarding meeting: {subject}"
        elif 'contract' in subject_lower or 'agreement' in subject_lower:
            description = f"Contract/agreement related communication: {subject}"
        elif 'review' in subject_lower:
            description = f"Document review and correspondence: {subject}"
        else:
            description = f"Client communication regarding: {subject}"
        
        return {
            'summary': f"Email correspondence: {subject}. {body[:300]}..." if body else f"Email correspondence: {subject}",
            'billing_hours': time_estimate,
            'billing_description': description[:200],
            'client_matter': 'General'
        }
