from django.core import validators
from django.db import models
from django.db import models

from admin_panel.models import SeoBlock


class TopCarousel(models.Model):
    img = models.ImageField(verbose_name='', upload_to='photos/%Y/%m/%d/', max_length=100, unique=True, null=True,
                            validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])
    link = models.URLField(verbose_name='', default='',
                           validators=[validators.URLValidator(),
                                       validators.RegexValidator(
                                           '\w*:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b([-a-zA-Z0-9@:%_\+.~#?&\/=]*)',message='Неверный url' )],
                           )
    title = models.CharField(verbose_name='', max_length=50, default='',
                             validators=[
                                 validators.MaxLengthValidator(50),
                                 validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                           message='Заголовок должен начинаться с заглавной буквы'),
                                 validators.ProhibitNullCharactersValidator(),
                             ]
                             )

    interval = 5

    class Meta:
        db_table = 'top_carousel'


class BackImg(models.Model):
    img = models.ImageField(verbose_name='', upload_to='photos/%Y/%m/%d/', max_length=100, unique=True, null=True,
                            validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])

    class Meta:
        db_table = 'back_img'


class BottomCarousel(models.Model):
    img = models.ImageField(verbose_name='', upload_to='photos/%Y/%m/%d/', max_length=100, unique=True, null=True,
                            validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])
    link = models.URLField(verbose_name='', default='',
                           validators=[validators.URLValidator(),
                                       validators.RegexValidator(
                                           '\w*:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b([-a-zA-Z0-9@:%_\+.~#?&\/=]*)',message='Неверный url' )],
                           )

    interval = 5

    class Meta:
        db_table = 'bottom_carousel'


class MainPage(models.Model):
    number = models.CharField(max_length=19, unique=True,
                              validators=[
                                  validators.MaxLengthValidator(19),
                                  validators.MinLengthValidator(19),
                                  validators.ProhibitNullCharactersValidator(),
                                  validators.RegexValidator('^\(\d{3}\) \d{3}-?\d{2}-?\d{2}$',
                                                            message='Неверно введён номер телефона.Пример ввода: (098) 567-81-23')
                              ]
                              )
    number2 = models.CharField(max_length=19, unique=True,
                               validators=[
                                   validators.MaxLengthValidator(19),
                                   validators.MinLengthValidator(19),
                                   validators.ProhibitNullCharactersValidator(),
                                   validators.RegexValidator('^\(\d{3}\) \d{3}-?\d{2}-?\d{2}$',
                                                             message='Неверно введён номер телефона.Пример ввода: (098) 567-81-23')
                               ]
                               )
    seo_text = models.TextField(max_length=500,
                                validators=[
                                    validators.MaxLengthValidator(500),
                                    validators.RegexValidator('^[A-ZА-Я]{1}.*',message='Описание должно начинаться с заглавной буквы.'),
                                    validators.ProhibitNullCharactersValidator(),

                                ]
                                )
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'main_page'
