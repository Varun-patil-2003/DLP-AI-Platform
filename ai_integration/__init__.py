"""
AI Integration Package for Data Leakage Detection System
Powered by Google Gemini
AI Integration Package
Powered by Groq LLM
"""

# from .gemini_client import GeminiClient   # ❌ OLD
from .gemini_client import GeminiClient     # ✅ keep name to avoid refactors

from .alert_generator import generate_ai_alert, generate_recommendations
from .insights_generator import generate_dashboard_insights

__all__ = [
    'GeminiClient',
    'generate_ai_alert',
    'generate_recommendations',
    'generate_dashboard_insights'
]
