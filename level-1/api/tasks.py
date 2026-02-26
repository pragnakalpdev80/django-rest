import datetime
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import Post, Task_3B, Analytics

@shared_task
def send_post_notification(post_id):
    # print("hello 2")
    post = Post.objects.get(id=post_id)
    # print(post)
    user = User.objects.filter(id=post.author_id).first()
    # print(user)
    send_mail(
        subject=f'New Post: {post.title}',
        message=post.content,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list= [user.email],
    )

@shared_task
def generate_weekly_analytics_report(user_id=None):    
    total = Task_3B.objects.count()
    completed = Task_3B.objects.filter(completed=True).count()
    
    report_data = {
        "total": total,
        "completed": completed
    }
    
    user = User.objects.filter(id=user_id).first() if user_id else None
    
    report = Analytics.objects.create(
        date=datetime.date.today(),
        completed_tasks=completed
    )
    return f"Report {report} generated successfully."