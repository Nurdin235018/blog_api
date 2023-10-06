from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model



User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=40, unique=True)
    slug = models.CharField(max_length=40, primary_key=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=40, unique=True)
    slug = models.CharField(max_length=40, primary_key=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')
    title = models.CharField(max_length=40, verbose_name='Заголовок')
    body = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} {self.title}'
