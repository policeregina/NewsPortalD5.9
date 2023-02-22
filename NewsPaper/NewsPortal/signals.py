from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post, PostCategory, SubscribersCAT, User


@receiver(post_save, sender=[Post, PostCategory])
def notify_new_post(sender, instance, created, **kwargs):
    subject = f'Новая статья в любимой категории!'
    html_content = render_to_string('email_about_creating.html', {
        'news':instance
    })

    post_id = Post.objects.get(post_name=instance.post_name, post_text=instance.post_text).id
    cat = PostCategory.objects.get(rel_post=post_id).rel_category
    list_of_sub = SubscribersCAT.objects.filter(rel_cat=cat).values('rel_user')
    sub = []
    for i in list_of_sub:
        user_email = User.objects.get(id=i['rel_user']).email
        sub.append(user_email)

    msg = EmailMultiAlternatives(
       subject=subject,
       body=instance.post_name,
       from_email='p.seregina2015@yandex.ru',
       to=sub)

    msg.attach_alternative (html_content, "text/html")
    msg.send()

