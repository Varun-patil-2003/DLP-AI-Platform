"""
Google Gemini AI Client
Handles all interactions with Gemini API
"""

# import google.generativeai as genai     # ❌ OLD
from groq import Groq                     # [GROQ-ADD]

# from config_ai import GEMINI_API_KEY, GEMINI_MODEL
from config_ai import GROQ_API_KEY, GROQ_MODEL, AI_PROVIDER  # [GROQ-ADD]
import time

class GeminiClient:
    """Client for Google Gemini AI"""
    
    # def __init__(self):
    #     """Initialize Gemini client"""
    #     try:
    #         genai.configure(api_key=GEMINI_API_KEY)
    #         self.model = genai.GenerativeModel(GEMINI_MODEL)
    #         self.enabled = True
    #         print("[OK] Google Gemini AI initialized successfully")
    #     except Exception as e:
    #         print(f"[WARNING] Could not initialize Gemini AI: {str(e)}")
    #         self.enabled = False
    
    def __init__(self):
        try:
            if AI_PROVIDER != "GROQ":                      # [GROQ-ADD]
                self.enabled = False
                return

            self.client = Groq(api_key=GROQ_API_KEY)      # [GROQ-ADD]
            self.model = GROQ_MODEL                        # [GROQ-ADD]
            self.enabled = True
            print("[OK] Groq AI initialized successfully") # [GROQ-ADD]

        except Exception as e:
            print(f"[WARNING] Could not initialize Groq AI: {str(e)}")
            self.enabled = False

    # def generate_text(self, prompt, max_retries=3):
    #     """
    #     Generate text using Gemini
        
    #     Args:
    #         prompt (str): The prompt to send to Gemini
    #         max_retries (int): Number of retries on failure
            
    #     Returns:
    #         str: Generated text or fallback message
    #     """
    #     if not self.enabled:
    #         return self._get_fallback_message()
        
    #     for attempt in range(max_retries):
    #         try:
    #             response = self.model.generate_content(prompt)
                
    #             # Handle safety blocks
    #             if not response.text:
    #                 if response.prompt_feedback:
    #                     print(f"[WARNING] Gemini blocked prompt: {response.prompt_feedback}")
    #                 return self._get_fallback_message()
                
    #             return response.text.strip()
                
    #         except Exception as e:
    #             print(f"[ERROR] Gemini API error (attempt {attempt + 1}): {str(e)}")
    #             if attempt < max_retries - 1:
    #                 time.sleep(1)  # Wait before retry
    #             else:
    #                 return self._get_fallback_message()

    def generate_text(self, prompt, max_retries=3):
        if not self.enabled:
            return self._get_fallback_message()

        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(  # [GROQ-ADD]
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                )

                return response.choices[0].message.content.strip()  # [GROQ-ADD]

            except Exception as e:
                print(f"[ERROR] Groq API error (attempt {attempt + 1}): {str(e)}")
                time.sleep(1)

        return self._get_fallback_message()
    
    # def generate_with_safety(self, prompt):
    #     """
    #     Generate text with safety settings
        
    #     Args:
    #         prompt (str): The prompt to send
            
    #     Returns:
    #         str: Generated text
    #     """
    #     if not self.enabled:
    #         return self._get_fallback_message()
        
    #     try:
    #         # Configure safety settings for security content
    #         safety_settings = [
    #             {
    #                 "category": "HARM_CATEGORY_HARASSMENT",
    #                 "threshold": "BLOCK_NONE"
    #             },
    #             {
    #                 "category": "HARM_CATEGORY_HATE_SPEECH",
    #                 "threshold": "BLOCK_NONE"
    #             },
    #             {
    #                 "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    #                 "threshold": "BLOCK_NONE"
    #             },
    #             {
    #                 "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    #                 "threshold": "BLOCK_NONE"
    #             }
    #         ]
            
    #         response = self.model.generate_content(
    #             prompt,
    #             safety_settings=safety_settings
    #         )
            
    #         return response.text.strip() if response.text else self._get_fallback_message()
            
    #     except Exception as e:
    #         print(f"[ERROR] Gemini generation failed: {str(e)}")
    #         return self._get_fallback_message()

    def generate_with_safety(self, prompt):
        return self.generate_text(prompt)  # [GROQ-ADD]
    
    def _get_fallback_message(self):
        """Return a fallback message when AI is unavailable"""
        return "Security event detected. AI analysis temporarily unavailable. Review recommended."
    
    def is_available(self):
        """Check if Gemini AI is available"""
        return self.enabled


# Global client instance
_gemini_client = None

def get_gemini_client():
    """Get or create global Gemini client instance"""
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    return _gemini_client
