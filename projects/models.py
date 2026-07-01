from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    author = models.CharField(max_length=100, verbose_name="Автор(ы)")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    github_link = models.URLField(blank=True, verbose_name="Ссылка на GitHub")

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.title

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.score for r in ratings) / len(ratings), 1)
        return 0

class Rating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Оценка")
    session_key = models.CharField(max_length=40, blank=True, null=True) # Защита от накруток по сессии

    class Meta:
        unique_together = ('project', 'session_key') # Один голос с одной сессии

    def __str__(self):
        return f"{self.project.title} - {self.score}"