from django.db import models


class Contact(models.Model):
    """ Подписка по Email """
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Подписка по Email"
        verbose_name_plural = "Подписка по Email"
