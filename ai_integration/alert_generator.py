"""
AI-Powered Alert Generation
Uses Google Gemini to generate intelligent, contextual security alerts
"""

from .gemini_client import get_gemini_client
from config_ai import ALERT_GENERATION_PROMPT, RECOMMENDATION_PROMPT, ENABLE_AI_ALERTS


def generate_ai_alert(user_data, prediction, risk_level, confidence):
    """
    Generate intelligent alert message using AI
    
    Args:
        user_data (dict): User activity data
        prediction (int): Model prediction (0=normal, 1=leakage)
        risk_level (str): Risk level (LOW/MEDIUM/HIGH/CRITICAL)
        confidence (float): Prediction confidence
        
    Returns:
        str: AI-generated alert message
    """
    if not ENABLE_AI_ALERTS:
        return get_default_message(prediction, risk_level)
    
    try:
        prompt = ALERT_GENERATION_PROMPT.format(
            user=user_data.get('user', 'Unknown'),
            pc=user_data.get('pc', 'Unknown'),
            authority=user_data.get('Authority', 'user'),
            pwd=user_data.get('Through_pwd', 0),
            pin=user_data.get('Through_pin', 0),
            mfa=user_data.get('Through_MFA', 0),
            data_mod=user_data.get('Data Modification', 0),
            conf_access=user_data.get('Confidential Data Access', 0),
            file_transfer=user_data.get('Confidential File Transfer', 0),
            external=user_data.get('External Destination', 'no'),
            file_op=user_data.get('File Operation', 'unknown'),
            sensitivity=user_data.get('Data Sensitivity Level', 'unknown'),
            prediction='Data Leakage' if prediction == 1 else 'Normal Activity',
            risk_level=risk_level,
            confidence=round(confidence * 100, 1)
        )
        
        # Get Gemini client
        client = get_gemini_client()
        
        if not client.is_available():
            return get_default_message(prediction, risk_level)
        
        # Generate AI response
        ai_message = client.generate_with_safety(prompt)
        
        return ai_message
        
    except Exception as e:
        print(f"[ERROR] AI alert generation failed: {str(e)}")
        return get_default_message(prediction, risk_level)


def generate_recommendations(user_data, risk_level, issue_description):
    """
    Generate AI-powered security recommendations
    
    Args:
        user_data (dict): User activity data
        risk_level (str): Risk level
        issue_description (str): Description of the security issue
        
    Returns:
        list: List of recommendations
    """
    try:
        prompt = RECOMMENDATION_PROMPT.format(
            user=user_data.get('user', 'Unknown'),
            risk_level=risk_level,
            issue_description=issue_description
        )
        
        client = get_gemini_client()
        
        if not client.is_available():
            return get_default_recommendations(risk_level)
        
        ai_recommendations = client.generate_text(prompt)
        
        # Parse recommendations into list
        recommendations = []
        for line in ai_recommendations.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                # Remove numbering and bullet points
                clean_line = line.lstrip('0123456789.-•* ').strip()
                if clean_line:
                    recommendations.append(clean_line)
        
        return recommendations[:5]  # Limit to top 5
        
    except Exception as e:
        print(f"[ERROR] Recommendation generation failed: {str(e)}")
        return get_default_recommendations(risk_level)


def get_default_message(prediction, risk_level):
    """Fallback message when AI is unavailable"""
    if prediction == 1:
        if risk_level == 'CRITICAL':
            return "CRITICAL: Potential data leakage detected. Immediate investigation required. High-risk activity patterns identified."
        elif risk_level == 'HIGH':
            return "HIGH RISK: Suspicious data access detected. Unusual activity patterns suggest potential security breach. Review immediately."
        elif risk_level == 'MEDIUM':
            return "MEDIUM RISK: Potentially suspicious activity detected. Monitor user behavior and review access logs."
        else:
            return "Data leakage indicators detected. Further monitoring recommended."
    else:
        return "Normal activity detected. No immediate security concerns identified."


def get_default_recommendations(risk_level):
    """Fallback recommendations when AI is unavailable"""
    if risk_level in ['CRITICAL', 'HIGH']:
        return [
            "Immediately review user access logs and recent activities",
            "Enable mandatory MFA for all elevated privilege accounts",
            "Restrict external file transfers pending investigation",
            "Alert security team and user's supervisor",
            "Conduct thorough audit of data accessed in past 48 hours"
        ]
    elif risk_level == 'MEDIUM':
        return [
            "Monitor user activity for next 24-48 hours",
            "Review authentication methods and enable MFA if not active",
            "Verify legitimacy of data access with user's manager",
            "Check for similar patterns from other users"
        ]
    else:
        return [
            "Continue routine monitoring",
            "Ensure security policies are up to date",
            "Maintain regular security awareness training"
        ]
