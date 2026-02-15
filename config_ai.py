"""
AI Configuration for Google Gemini Integration
Store your API key securely here
"""

import os

# Google Gemini API Configuration
# GEMINI_API_KEY = "AIzaSyADuHTi_NMQXTeiPymFpruFXiUpORoBNI8"  # Google AI
# GEMINI_MODEL = "gemini-2.5-pro"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # [GROQ-ADD]
GROQ_MODEL = "llama-3.1-8b-instant"          # [GROQ-ADD]

AI_PROVIDER = "GROQ"  # GEMINI | GROQ | OFF  # [GROQ-ADD]   

# AI Feature Flags
ENABLE_AI_ALERTS = True
ENABLE_AI_INSIGHTS = True
ENABLE_AI_RECOMMENDATIONS = True

# AI Prompt Templates
ALERT_GENERATION_PROMPT = """You are an expert cybersecurity analyst. Analyze this security event and generate a professional alert.

Event Details:
- User ID: {user}
- PC ID: {pc}
- Authority Level: {authority}
- Authentication: Password={pwd}, PIN={pin}, MFA={mfa}
- Data Operations: Modification={data_mod}, Confidential Access={conf_access}, File Transfer={file_transfer}
- Network: External Destination={external}, File Operation={file_op}
- Data Sensitivity: {sensitivity}
- ML Prediction: {prediction}
- Risk Level: {risk_level}
- Confidence: {confidence}%

Generate a concise alert message (2-3 sentences) that:
1. Describes what happened
2. Explains why it's suspicious
3. States the risk level

Keep it professional and actionable. Maximum 150 words.
"""

INSIGHT_GENERATION_PROMPT = """You are a cybersecurity analyst reviewing system alerts. 

Recent Alerts:
{alerts_summary}

Provide a brief security summary (3-4 sentences) covering:
1. Main security concerns
2. Common patterns
3. Top priority action

Keep it executive-friendly and under 100 words.
"""

RECOMMENDATION_PROMPT = """Based on this security incident:

User: {user}
Risk Level: {risk_level}
Issue: {issue_description}

Provide 2-3 specific, actionable security recommendations. Be concise and practical.
Format as a numbered list.
"""
