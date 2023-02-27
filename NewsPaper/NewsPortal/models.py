import datetime

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.get_username()}'
    def update_rating(self):
        set_post = Post.objects.filter(post_author_id=self.id).values('post_rating')
        sum_post = 0
        for i in set_post:
            val = i.get('post_rating')
            sum_post += val

        set_self_comment = Comment.objects.filter(comment_user_id=self.user_id).values('comment_rating')
        sum_self_comment = 0
        for i in set_self_comment:
            val = i.get('comment_rating')
            sum_self_comment += val

        set_self_post = Post.objects.filter(post_author_id=self.id).values('id')  # все посты автора
        sum_comment_post = 0
        for i in set_self_post:
            self_post_id = i.get('id')
            set_comment_post = Comment.objects.filter(comment_post_id=self_post_id).values('comment_rating')
            for k in set_comment_post:
                val = k.get('comment_rating')
                sum_comment_post += val

        self.rating = sum_post * 3 + sum_self_comment + sum_comment_post
        self.save()
    rating = models.IntegerField(default=0)


class Category(models.Model):
   name_cat = models.CharField(max_length = 255, unique = True)
   subscribers = models.ManyToManyField(User, through = 'SubscribersCAT')

   def __str__(self):
       return f'{self.name_cat.title()}'


post = 'PT'
article = 'AR'
TYPE = [
    (post, 'Пост'),
    (article,'Статья')
]

class Post(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2,choices=TYPE, default=post)
    post_cat = models.ManyToManyField(Category, through='PostCategory')
    post_name = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.post_name.title()}'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -=1
        self.save()

    def preview(self):
        return (f'{self.post_text[0:124]}...' )




class PostCategory(models.Model):
    rel_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    rel_category = models.ForeignKey(Category, on_delete=models.CASCADE)

class SubscribersCAT(models.Model):
    rel_cat = models.ForeignKey(Category,on_delete=models.CASCADE)
    rel_user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add = True)
    comment_rating = models.IntegerField(default = 0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -=1
        self.save()


