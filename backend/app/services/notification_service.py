import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from typing import Optional
import os

logger = logging.getLogger(__name__)

class NotificationService:
    """Service for sending SMS and Email notifications"""
    
    def __init__(self):
        self.email_enabled = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
        self.sms_enabled = os.getenv("SMS_ENABLED", "false").lower() == "true"
        
        # Email config
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@grievance.gov.in")
        
    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Send email notification"""
        if not self.email_enabled or not self.smtp_user:
            logger.warning(f"Email disabled or not configured. Would send to {to_email}: {subject}")
            return False
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    def send_sms(self, phone: str, message: str) -> bool:
        """Send SMS notification (using Twilio or similar)"""
        if not self.sms_enabled:
            logger.warning(f"SMS disabled. Would send to {phone}: {message}")
            return False
            
        try:
            # Twilio integration would go here
            # For demo, just log
            logger.info(f"SMS would be sent to {phone}: {message}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SMS to {phone}: {e}")
            return False
    
    def notify_complaint_submitted(self, complaint_data: dict, user_email: str, user_phone: Optional[str] = None):
        """Notify citizen that complaint was submitted"""
        complaint_id = complaint_data.get("complaint_id")
        category = complaint_data.get("category", "Unknown")
        urgency = complaint_data.get("urgency_level", "MEDIUM")
        
        # Email
        subject = f"Complaint Registered - {complaint_id}"
        body = f"""
        <html>
            <body>
                <h2>Your Complaint Has Been Registered</h2>
                <p>Thank you for submitting your complaint. Our AI system has analyzed it.</p>
                
                <table style="border: 1px solid #ddd; padding: 10px;">
                    <tr><td><strong>Complaint ID:</strong></td><td>{complaint_id}</td></tr>
                    <tr><td><strong>Category:</strong></td><td>{category}</td></tr>
                    <tr><td><strong>Urgency Level:</strong></td><td>{urgency}</td></tr>
                    <tr><td><strong>Status:</strong></td><td>Submitted</td></tr>
                </table>
                
                <p>You will receive updates as your complaint progresses.</p>
                <p>Track your complaint status at: <a href="http://localhost:5173/citizen">Dashboard</a></p>
                
                <p>Regards,<br>Grievance Redressal System</p>
            </body>
        </html>
        """
        self.send_email(user_email, subject, body)
        
        # SMS
        if user_phone:
            sms_body = f"Complaint {complaint_id} registered. Category: {category}, Urgency: {urgency}. Track at: grievance.gov.in"
            self.send_sms(user_phone, sms_body)
    
    def notify_complaint_assigned(self, complaint_data: dict, user_email: str, officer_name: str, user_phone: Optional[str] = None):
        """Notify citizen that complaint was assigned to officer"""
        complaint_id = complaint_data.get("complaint_id")
        
        # Email
        subject = f"Complaint Assigned - {complaint_id}"
        body = f"""
        <html>
            <body>
                <h2>Your Complaint Has Been Assigned</h2>
                <p>Your complaint has been assigned to an officer for resolution.</p>
                
                <table style="border: 1px solid #ddd; padding: 10px;">
                    <tr><td><strong>Complaint ID:</strong></td><td>{complaint_id}</td></tr>
                    <tr><td><strong>Assigned Officer:</strong></td><td>{officer_name}</td></tr>
                    <tr><td><strong>Status:</strong></td><td>Assigned</td></tr>
                </table>
                
                <p>The officer will review and take action soon.</p>
                
                <p>Regards,<br>Grievance Redressal System</p>
            </body>
        </html>
        """
        self.send_email(user_email, subject, body)
        
        # SMS
        if user_phone:
            sms_body = f"Complaint {complaint_id} assigned to {officer_name}. Status: In Progress."
            self.send_sms(user_phone, sms_body)
    
    def notify_status_updated(self, complaint_data: dict, user_email: str, new_status: str, note: Optional[str], user_phone: Optional[str] = None):
        """Notify citizen of status update"""
        complaint_id = complaint_data.get("complaint_id")
        
        # Email
        subject = f"Status Update - {complaint_id}"
        body = f"""
        <html>
            <body>
                <h2>Complaint Status Updated</h2>
                <p>Your complaint status has been updated.</p>
                
                <table style="border: 1px solid #ddd; padding: 10px;">
                    <tr><td><strong>Complaint ID:</strong></td><td>{complaint_id}</td></tr>
                    <tr><td><strong>New Status:</strong></td><td>{new_status}</td></tr>
                    {f'<tr><td><strong>Note:</strong></td><td>{note}</td></tr>' if note else ''}
                </table>
                
                <p>View full details at: <a href="http://localhost:5173/citizen">Dashboard</a></p>
                
                <p>Regards,<br>Grievance Redressal System</p>
            </body>
        </html>
        """
        self.send_email(user_email, subject, body)
        
        # SMS
        if user_phone:
            sms_body = f"Complaint {complaint_id} status: {new_status}. {note if note else ''}"
            self.send_sms(user_phone, sms_body[:160])
    
    def notify_complaint_resolved(self, complaint_data: dict, user_email: str, user_phone: Optional[str] = None):
        """Notify citizen that complaint is resolved"""
        complaint_id = complaint_data.get("complaint_id")
        
        # Email
        subject = f"Complaint Resolved - {complaint_id}"
        body = f"""
        <html>
            <body>
                <h2>Your Complaint Has Been Resolved</h2>
                <p>We are pleased to inform you that your complaint has been resolved.</p>
                
                <table style="border: 1px solid #ddd; padding: 10px;">
                    <tr><td><strong>Complaint ID:</strong></td><td>{complaint_id}</td></tr>
                    <tr><td><strong>Status:</strong></td><td>Resolved</td></tr>
                </table>
                
                <p>Please rate your experience to help us improve our service.</p>
                <p><a href="http://localhost:5173/citizen">Submit Feedback</a></p>
                
                <p>Thank you for using our service.</p>
                
                <p>Regards,<br>Grievance Redressal System</p>
            </body>
        </html>
        """
        self.send_email(user_email, subject, body)
        
        # SMS
        if user_phone:
            sms_body = f"Complaint {complaint_id} has been RESOLVED. Please provide feedback at: grievance.gov.in"
            self.send_sms(user_phone, sms_body)
    
    def notify_officer_assignment(self, complaint_data: dict, officer_email: str, officer_name: str):
        """Notify officer of new complaint assignment"""
        complaint_id = complaint_data.get("complaint_id")
        category = complaint_data.get("category")
        urgency = complaint_data.get("urgency_level")
        title = complaint_data.get("title")
        
        # Email
        subject = f"New Complaint Assigned - {complaint_id}"
        body = f"""
        <html>
            <body>
                <h2>New Complaint Assigned to You</h2>
                <p>Dear {officer_name},</p>
                <p>A new complaint has been assigned to you for resolution.</p>
                
                <table style="border: 1px solid #ddd; padding: 10px;">
                    <tr><td><strong>Complaint ID:</strong></td><td>{complaint_id}</td></tr>
                    <tr><td><strong>Title:</strong></td><td>{title}</td></tr>
                    <tr><td><strong>Category:</strong></td><td>{category}</td></tr>
                    <tr><td><strong>Urgency:</strong></td><td>{urgency}</td></tr>
                </table>
                
                <p>Please review and take action: <a href="http://localhost:5173/officer">Officer Dashboard</a></p>
                
                <p>Regards,<br>Grievance Redressal System</p>
            </body>
        </html>
        """
        self.send_email(officer_email, subject, body)

notification_service = NotificationService()
