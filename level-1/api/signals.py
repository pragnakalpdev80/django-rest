from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Post
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .tasks import send_post_notification

@receiver(pre_save, sender=Post)
def pre_save_post(sender, instance, **kwargs):
    """Called before Post is saved"""
    if not instance.slug:
        instance.slug = slugify(instance.title)

# @receiver(post_save, sender=Post)
# def post_save_post(sender, instance, created, **kwargs):
#     """
#     Called after Post is saved.
#     created = True if this is a new object, False if it's an update
#     """
#     print(created)
#     if created:
#         # This is a new post (not an update)
#         # print(f"New post created: {instance.title}")
#         user = User.objects.filter(id=instance.author_id).first()
#         # print(user)
#         context = {}
#         subject = "post"
#         message = f"you have posted {instance.title} titled post."
#         sender = settings.EMAIL_HOST_USER
#         # print(sender)
#         to_mail = [user.email]
#         # print(to_mail)
#         try:
#             # print("hello")
#             # send_mail(subject, message, sender, to_mail)
#             context['result'] = 'Email sent successfully'
#         except Exception as e:
#             context['result'] = f'Error sending email: {e}'
@receiver(post_save, sender=Post)
def post_save_post(sender, instance, created, **kwargs):
    """
    Called after Post is saved.
    Triggers the Celery background task only for new posts.
    """
    print(created)
    if created:
        send_post_notification(instance.id)