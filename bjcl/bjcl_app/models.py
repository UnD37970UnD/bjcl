from django.db import models

class searchers(models.Model):
    search = models.CharField(max_length=200)
    ip = models.CharField(max_length=200)
    browser_info = models.CharField(max_length=200)
    device_info = models.CharField(max_length=500)
    os_info = models.CharField(max_length=200)

    def __str__(self):
        return self.ip

class result(models.Model):
    book_title = models.CharField(max_length=200)
    book_author = models.CharField(max_length=200)
    book_image = models.CharField(max_length=2000)
    book_disponibility = models.CharField(max_length=200)
    disp_color = models.CharField(max_length=100, default="orange")

    def __str__(self):
        return self.book_title


