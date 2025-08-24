from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from jinja2 import Template

class EmailGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
        
    def generate_initial_email(self, prospect_data):
        """Generate personalized initial outreach email"""
        
        prompt = ChatPromptTemplate.from_template("""
        Write a personalized sales email for:
        
        Prospect: {name}
        Company: {company}
        Title: {title}
        Industry: {industry}
        Pain Points: {pain_points}
        
        Email should be:
        - Personalized and relevant
        - Professional but friendly tone
        - Clear value proposition
        - Include soft call-to-action
        - 100-150 words max
        
        Return JSON with 'subject' and 'content' fields.
        """)
        
        chain = prompt | self.llm
        result = chain.invoke(prospect_data)
        
        try:
            import json
            email_data = json.loads(result.content)
            return email_data
        except:
            return {
                "subject": f"Quick question about {prospect_data['company']}'s sales process",
                "content": f"Hi {prospect_data['name']},\n\nI noticed {prospect_data['company']} is doing great work in {prospect_data['industry']}. I'm curious - how are you currently handling your lead generation and sales outreach?\n\nWe've helped similar companies increase their sales efficiency by 35%. Would love to share a quick insight that might be relevant.\n\nWorth a brief chat?\n\nBest,\nAI SDR"
            }
    
    def generate_follow_up(self, prospect_data, follow_up_number):
        """Generate follow-up emails based on sequence number"""
        
        follow_up_templates = {
            1: "Following up on my previous email about {company}'s sales process...",
            2: "Sharing a relevant case study that might interest {company}...",
            3: "Quick question - what's your biggest challenge with lead generation?",
            4: "Should I assume this isn't a priority for {company} right now?",
            5: "Last follow-up - would love to help {company} grow sales by 35%..."
        }
        
        template_text = follow_up_templates.get(follow_up_number, follow_up_templates[1])
        
        prompt = ChatPromptTemplate.from_template(f"""
        Write a follow-up email (#{follow_up_number}) using this template idea:
        {template_text}
        
        For prospect:
        Name: {{name}}
        Company: {{company}}
        Industry: {{industry}}
        
        Keep it short, valuable, and respectful.
        Return JSON with 'subject' and 'content'.
        """)
        
        chain = prompt | self.llm
        result = chain.invoke(prospect_data)
        
        try:
            import json
            return json.loads(result.content)
        except:
            return {
                "subject": f"Re: {prospect_data['company']} sales process",
                "content": f"Hi {prospect_data['name']},\n\nJust following up on my previous email. Would love to help {prospect_data['company']} improve sales efficiency.\n\nBest,\nAI SDR"
            }
