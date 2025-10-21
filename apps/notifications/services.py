import logging
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
from django.conf import settings
from django.template import Template, Context
from .models import SMSTemplate, EmailTemplate, NotificationLog

logger = logging.getLogger(__name__)

class NotificationProvider(ABC):
    """Base class for notification providers"""
    
    @abstractmethod
    def send(self, to: str, content: str, **kwargs) -> tuple[bool, Optional[str], Optional[str]]:
        """
        Send notification
        Returns: (success, provider_message_id, error_message)
        """
        pass


class SMSProvider(NotificationProvider):
    """SMS provider implementation"""
    
    def send(self, to: str, content: str, **kwargs) -> tuple[bool, Optional[str], Optional[str]]:
        # TODO: Implement actual SMS provider (Twilio, MessageBird, etc)
        if settings.DEBUG:
            logger.info(f"DEBUG SMS to {to}: {content}")
            return True, "debug_message_id", None
            
        # Mock implementation
        try:
            # Add actual SMS provider implementation here
            return True, "mock_message_id", None
        except Exception as e:
            logger.error(f"SMS sending failed: {str(e)}")
            return False, None, str(e)


class EmailProvider(NotificationProvider):
    """Email provider implementation"""
    
    def send(self, to: str, content: str, **kwargs) -> tuple[bool, Optional[str], Optional[str]]:
        subject = kwargs.get('subject', 'Notification')
        from_email = kwargs.get('from_email', settings.DEFAULT_FROM_EMAIL)
        html_content = kwargs.get('html_content')

        # TODO: Implement actual email provider (SendGrid, Amazon SES, etc)
        if settings.DEBUG:
            logger.info(f"DEBUG Email to {to}:\nSubject: {subject}\nContent: {content}")
            return True, "debug_message_id", None

        try:
            # Add actual email provider implementation here
            return True, "mock_message_id", None
        except Exception as e:
            logger.error(f"Email sending failed: {str(e)}")
            return False, None, str(e)


class NotificationService:
    """Main service for sending notifications"""

    def __init__(self):
        self.sms_provider = SMSProvider()
        self.email_provider = EmailProvider()

    def render_template(self, template_content: str, context_data: Dict[str, Any]) -> str:
        """Render a template with given context"""
        template = Template(template_content)
        context = Context(context_data)
        return template.render(context)

    def send_sms(self, 
                 phone_number: str,
                 template_key: str,
                 context_data: Dict[str, Any],
                 user=None) -> NotificationLog:
        """Send SMS using template"""
        try:
            template = SMSTemplate.objects.get(template_key=template_key, is_active=True)
            content = self.render_template(template.content, context_data)

            # Create notification log
            notification = NotificationLog.objects.create(
                notification_type='sms',
                recipient=user,
                phone_number=phone_number,
                template_key=template_key,
                context_data=context_data,
                status='sending'
            )

            # Send SMS
            success, message_id, error = self.sms_provider.send(phone_number, content)

            # Update notification log
            if success:
                notification.status = 'sent'
                notification.provider_message_id = message_id
            else:
                notification.status = 'failed'
                notification.error_message = error

            notification.save()
            return notification

        except SMSTemplate.DoesNotExist:
            logger.error(f"SMS template not found: {template_key}")
            raise ValueError(f"SMS template not found: {template_key}")
        except Exception as e:
            logger.error(f"SMS sending failed: {str(e)}")
            raise

    def send_email(self,
                  email: str,
                  template_key: str,
                  context_data: Dict[str, Any],
                  user=None) -> NotificationLog:
        """Send email using template"""
        try:
            template = EmailTemplate.objects.get(template_key=template_key, is_active=True)
            subject = self.render_template(template.subject, context_data)
            html_content = self.render_template(template.html_content, context_data)
            text_content = self.render_template(template.text_content, context_data)

            # Create notification log
            notification = NotificationLog.objects.create(
                notification_type='email',
                recipient=user,
                email=email,
                template_key=template_key,
                context_data=context_data,
                status='sending'
            )

            # Send email
            success, message_id, error = self.email_provider.send(
                email,
                text_content,
                subject=subject,
                html_content=html_content
            )

            # Update notification log
            if success:
                notification.status = 'sent'
                notification.provider_message_id = message_id
            else:
                notification.status = 'failed'
                notification.error_message = error

            notification.save()
            return notification

        except EmailTemplate.DoesNotExist:
            logger.error(f"Email template not found: {template_key}")
            raise ValueError(f"Email template not found: {template_key}")
        except Exception as e:
            logger.error(f"Email sending failed: {str(e)}")
            raise

    def create_in_app_notification(self,
                                 user,
                                 title: str,
                                 message: str,
                                 notification_type: str = 'info',
                                 action_url: Optional[str] = None,
                                 related_object=None):
        """Create an in-app notification"""
        from .models import InAppNotification
        
        notification = InAppNotification.objects.create(
            recipient=user,
            title=title,
            message=message,
            notification_type=notification_type,
            action_url=action_url
        )

        if related_object:
            notification.content_object = related_object
            notification.save()

        return notification