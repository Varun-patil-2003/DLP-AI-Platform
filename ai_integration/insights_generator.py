"""
AI-Powered Dashboard Insights
Generates intelligent summaries and trend analysis
"""

from .gemini_client import get_gemini_client
from config_ai import INSIGHT_GENERATION_PROMPT, ENABLE_AI_INSIGHTS


def generate_dashboard_insights(alert_history):
    """
    Generate AI-powered dashboard insights
    
    Args:
        alert_history (list): List of recent alerts
        
    Returns:
        dict: Insights including summary, trends, and recommendations
    """
    if not ENABLE_AI_INSIGHTS or not alert_history:
        return get_default_insights(alert_history)
    
    try:
        # Prepare summary of recent alerts
        alerts_summary = prepare_alerts_summary(alert_history)
        
        # Generate insights prompt
        prompt = INSIGHT_GENERATION_PROMPT.format(
            alerts_summary=alerts_summary
        )
        
        # Get Gemini client
        client = get_gemini_client()
        
        if not client.is_available():
            return get_default_insights(alert_history)
        
        # Generate AI insights
        ai_summary = client.generate_text(prompt)
        
        # Analyze trends
        trends = analyze_trends(alert_history)
        
        return {
            'summary': ai_summary,
            'trends': trends,
            'total_alerts': len(alert_history),
            'critical_count': sum(1 for a in alert_history if a.get('risk_level') == 'CRITICAL'),
            'high_count': sum(1 for a in alert_history if a.get('risk_level') == 'HIGH'),
            'medium_count': sum(1 for a in alert_history if a.get('risk_level') == 'MEDIUM')
        }
        
    except Exception as e:
        print(f"[ERROR] Insight generation failed: {str(e)}")
        return get_default_insights(alert_history)


def prepare_alerts_summary(alert_history):
    """Prepare a concise summary of alerts for AI analysis"""
    recent_alerts = alert_history[-10:]  # Last 10 alerts
    
    summary_lines = []
    for alert in recent_alerts:
        risk = alert.get('risk_level', 'UNKNOWN')
        user = alert.get('user', 'Unknown')
        msg = alert.get('message', 'Security event')
        summary_lines.append(f"- {risk}: {user} - {msg[:80]}")
    
    return '\n'.join(summary_lines)


def analyze_trends(alert_history):
    """Analyze alert trends"""
    if not alert_history:
        return []
    
    trends = []
    
    # Count by risk level
    critical = sum(1 for a in alert_history if a.get('risk_level') == 'CRITICAL')
    high = sum(1 for a in alert_history if a.get('risk_level') == 'HIGH')
    medium = sum(1 for a in alert_history if a.get('risk_level') == 'MEDIUM')
    
    if critical > 0:
        trends.append(f"🔴 {critical} critical threat(s) require immediate attention")
    if high > 2:
        trends.append(f"🟠 {high} high-risk events detected - review urgently")
    if medium > 5:
        trends.append(f"🟡 {medium} medium-risk events - monitor closely")
    
    # Identify common users
    user_alerts = {}
    for alert in alert_history:
        user = alert.get('user', 'Unknown')
        user_alerts[user] = user_alerts.get(user, 0) + 1
    
    repeat_offenders = [user for user, count in user_alerts.items() if count > 2]
    if repeat_offenders:
        trends.append(f"👥 Repeat violations from: {', '.join(repeat_offenders[:3])}")
    
    return trends


def get_default_insights(alert_history):
    """Fallback insights when AI is unavailable"""
    if not alert_history:
        return {
            'summary': "No security alerts to analyze. System is operating normally.",
            'trends': ["✅ No significant security events detected"],
            'total_alerts': 0,
            'critical_count': 0,
            'high_count': 0,
            'medium_count': 0
        }
    
    critical = sum(1 for a in alert_history if a.get('risk_level') == 'CRITICAL')
    high = sum(1 for a in alert_history if a.get('risk_level') == 'HIGH')
    medium = sum(1 for a in alert_history if a.get('risk_level') == 'MEDIUM')
    
    summary = f"Security system has detected {len(alert_history)} alert(s) including "
    summary += f"{critical} critical, {high} high-risk, and {medium} medium-risk events. "
    
    if critical > 0:
        summary += "Immediate investigation of critical threats recommended."
    elif high > 0:
        summary += "Review high-risk events as soon as possible."
    else:
        summary += "Monitor medium-risk events and maintain vigilance."
    
    return {
        'summary': summary,
        'trends': analyze_trends(alert_history),
        'total_alerts': len(alert_history),
        'critical_count': critical,
        'high_count': high,
        'medium_count': medium
    }
