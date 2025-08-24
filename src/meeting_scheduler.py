from datetime import datetime, timedelta
import json
from langchain_openai import ChatOpenAI

class MeetingScheduler:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo")
    
    def propose_meeting_times(self, prospect_timezone="EST"):
        """Generate available meeting slots"""
        now = datetime.now()
        available_slots = []
        
        # Generate next 5 business days
        for i in range(1, 8):
            next_day = now + timedelta(days=i)
            if next_day.weekday() < 5:  # Monday to Friday
                # Morning slots
                morning_slot = next_day.replace(hour=10, minute=0, second=0, microsecond=0)
                afternoon_slot = next_day.replace(hour=14, minute=0, second=0, microsecond=0)
                
                available_slots.extend([morning_slot, afternoon_slot])
        
        return available_slots[:6]  # Return 6 options
    
    def generate_scheduling_email(self, prospect_data):
        """Generate email with meeting scheduling options"""
        available_times = self.propose_meeting_times()
        
        time_options = []
        for i, time in enumerate(available_times, 1):
            formatted_time = time.strftime("%A, %B %d at %I:%M %p")
            time_options.append(f"{i}. {formatted_time}")
        
        prompt = f"""
        Write an email to schedule a meeting with {prospect_data['name']} from {prospect_data['company']}.
        
        Available times:
        {chr(10).join(time_options)}
        
        Email should:
        - Be professional and friendly
        - Mention the value of the meeting
        - Ask them to pick a time
        - Include calendar link placeholder
        
        Return JSON with 'subject' and 'content'.
        """
        
        result = self.llm.invoke(prompt)
        
        try:
            return json.loads(result.content)
        except:
            return {
                "subject": f"Meeting with {prospect_data['company']} - {prospect_data['name']}",
                "content": f"Hi {prospect_data['name']},\n\nThanks for your interest! I'd love to show you how we can help {prospect_data['company']} increase sales efficiency.\n\nWhich of these times work for a 30-minute call?\n\n{chr(10).join(time_options)}\n\nLooking forward to our conversation!\n\nBest,\nAI SDR"
            }
    
    def transcribe_meeting(self, meeting_audio):
        """Transcribe meeting audio and extract action items"""
        # Placeholder for meeting transcription
        # In production, integrate with speech-to-text services
        
        sample_transcript = """
        AI SDR: Thanks for joining today. Can you tell me about your current sales process?
        
        Prospect: We're struggling with lead generation. Our team spends too much time on manual research.
        
        AI SDR: That's a common challenge. Our AI system can automate 80% of prospect research. Would you like to see a demo?
        
        Prospect: Yes, that sounds interesting. Can we schedule a follow-up next week?
        """
        
        # Extract action items using AI
        action_items_prompt = f"""
        Extract action items from this meeting transcript:
        
        {sample_transcript}
        
        Return a JSON list of action items.
        """
        
        result = self.llm.invoke(action_items_prompt)
        
        try:
            action_items = json.loads(result.content)
        except:
            action_items = [
                "Schedule demo for next week",
                "Send case studies",
                "Follow up with pricing information"
            ]
        
        return {
            "transcript": sample_transcript,
            "action_items": action_items
        }
