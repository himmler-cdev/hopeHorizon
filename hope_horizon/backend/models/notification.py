from django.db import models
from django.conf import settings


class Notification(models.Model):
    # Fields
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # To track when the notification was created
    content = models.TextField()  # Stores the content of the notification

    # Relationships
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="notifications"
    )

    #TODO: Uncomment the following line after creating the Comment model
    #comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)  # Comment that the notification is about
