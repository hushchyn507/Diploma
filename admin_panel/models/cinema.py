import datetime
import uuid

import django.utils.timezone
from django.core import validators
from django.db import models

from admin_panel.models.film import Film, TechnologyType, SeoBlock
from admin_panel.models.user import Account


class Contact(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            validators=[
                                validators.MaxLengthValidator(100,
                                                              'Длина названия должна быть не более 100 символов.'),
                                validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                          'Название должно начинаться с заглавной буквы'),
                                validators.ProhibitNullCharactersValidator(),
                            ]
                            )
    address = models.TextField()
    coordinate = models.TextField(max_length=10000)
    logo = models.ImageField(upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True,
                             validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])
    cinema = models.ForeignKey("Cinema", on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'contacts'


class Cinema(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100, unique=True,
                            validators=[
                                validators.MaxLengthValidator(100),
                                validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                          message='Название кинотеатра должно начинаться с заглавной буквы'),
                                validators.ProhibitNullCharactersValidator(),
                            ]
                            )
    description = models.TextField(verbose_name='Описание', max_length=500,
                                   validators=[
                                       validators.MaxLengthValidator(500),
                                       validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                 message='Описание должно начинаться с заглавной буквы.'),
                                       validators.ProhibitNullCharactersValidator(),

                                   ]
                                   )
    banner = models.ImageField(verbose_name='Баннер', upload_to="photos/%Y/%m/%d/", max_length=100, unique=True,
                               null=True,
                               validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])
    logo = models.ImageField(verbose_name='Логотип', upload_to="photos/%Y/%m/%d/", max_length=100, unique=True,
                             null=True,
                             validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'cinema'


class CinemaImg(models.Model):
    img = models.ImageField(upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True,
                            validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'cinema_imgs'


class Page(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, default=1)
    name = models.CharField(verbose_name="Название", max_length=100, unique=True,
                            validators=[
                                validators.MaxLengthValidator(100,
                                                              'Длина названия страницы должна быть не более 100 символов.'),
                                validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                          'Название страницы должно начинаться с заглавной буквы'),
                                validators.ProhibitNullCharactersValidator(),
                            ]
                            )
    description = models.TextField(verbose_name="Описание", max_length=500,
                                   validators=[
                                       validators.MaxLengthValidator(500),
                                       validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                 message='Описание должно начинаться с заглавной буквы.'),
                                       validators.ProhibitNullCharactersValidator(),

                                   ]
                                   )
    banner = models.ImageField(verbose_name="Баннер", upload_to="photos/%Y/%m/%d/", max_length=100, unique=True,
                               null=True,
                               validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])
    first_pic = models.ImageField(verbose_name="Первая картинка", upload_to="photos/%Y/%m/%d/", max_length=100,
                                  unique=True, null=True,
                                  validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])
    second_pic = models.ImageField(verbose_name="Вторая картинка", upload_to="photos/%Y/%m/%d/", max_length=100,
                                   unique=True, null=True,
                                   validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])
    third_pic = models.ImageField(verbose_name="Третья картинка", upload_to="photos/%Y/%m/%d/", max_length=100,
                                  unique=True, null=True,
                                  validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])
    description2 = models.TextField(verbose_name="Второе описание", max_length=500,
                                    validators=[
                                        validators.MaxLengthValidator(500),
                                        validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                  message='Описание должно начинаться с заглавной буквы.'),
                                        validators.ProhibitNullCharactersValidator(),

                                    ]
                                    )
    turn_on = models.BooleanField(verbose_name="ВКЛ/ВЫКЛ", default=False)
    creation_date = models.DateField(verbose_name="Дата создания", auto_now_add=True, null=True)
    able_to_del = models.BooleanField(default=True)
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'pages'


class PageImg(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    img = models.ImageField(verbose_name="", upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True,
                            validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])

    class Meta:
        db_table = 'pages_imgs'


class Hall(models.Model):
    number = models.PositiveSmallIntegerField(verbose_name="Номер зала", unique=True,
                                              validators=[
                                                  validators.MinValueValidator(0)
                                              ]
                                              )
    banner = models.ImageField(verbose_name="Баннер", upload_to="photos/%Y/%m/%d/", max_length=100, unique=True,
                               null=True,
                               validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])
    description = models.TextField(verbose_name="Описание", max_length=500,
                                   validators=[
                                       validators.MaxLengthValidator(500),
                                       validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                 message='Описание должно начинаться с заглавной буквы.'),
                                       validators.ProhibitNullCharactersValidator(),

                                   ]
                                   )
    num_tickets = models.PositiveSmallIntegerField(verbose_name="Кол-во биллетов", )
    scheme = models.ImageField(verbose_name="Cхема зала", upload_to="photos/%Y/%m/%d/", max_length=100, unique=True,
                               null=True,
                               validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])
    creation_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, default=1)
    scheme_html = models.TextField(blank=True, null=True)
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.number)

    class Meta:
        ordering = ['number']
        db_table = 'halls'


class HallImg(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    img = models.ImageField(verbose_name='', upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True,
                            validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])

    class Meta:
        db_table = 'halls_imgs'


class Seance(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, verbose_name='Зал')
    date = models.DateField(verbose_name='Дата')
    price = models.PositiveSmallIntegerField(default=0, verbose_name='Цена',
                                             validators=[validators.MinValueValidator(0)])
    time = models.TimeField(verbose_name='Время')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, null=False, verbose_name='Фильм')
    tech_type = models.ForeignKey(TechnologyType, on_delete=models.CASCADE, null=True, verbose_name='Технология')

    class Meta:
        db_table = 'seances'


class Ticket(models.Model):
    second_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False)
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, null=False)
    row = models.PositiveSmallIntegerField()
    seat = models.PositiveSmallIntegerField()
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'tickets'


class Stock(models.Model):
    name = models.CharField(verbose_name="Название", max_length=30, null=False,
                            validators=[
                                validators.MaxLengthValidator(30,
                                                              'Длина названия акции должна быть не более 30ти символов.'),
                                validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                          'Название акции должно начинаться с заглавной буквы'),
                                validators.ProhibitNullCharactersValidator(),
                            ]
                            )
    short_description = models.TextField(verbose_name="Краткое описание", max_length=50,
                                         validators=[
                                             validators.MaxLengthValidator(50),
                                             validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                       message='Описание должно начинаться с заглавной буквы.'),
                                             validators.ProhibitNullCharactersValidator(),

                                         ]
                                         )
    description = models.TextField(verbose_name="Описание", max_length=500,
                                   validators=[
                                       validators.MaxLengthValidator(500),
                                       validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                 message='Описание должно начинаться с заглавной буквы.'),
                                       validators.ProhibitNullCharactersValidator(),

                                   ]
                                   )
    creation_date = models.DateField(verbose_name="Дата создания", auto_now_add=True, null=True)
    turn_on = models.BooleanField(verbose_name="ВКЛ/ВЫКЛ", default=False)
    video_link = models.URLField(verbose_name="Ссылка на видео",
                                 validators=[validators.URLValidator(),
                                             validators.RegexValidator(
                                                 '\w*:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b([-a-zA-Z0-9@:%_\+.~#?&\/=]*)', )],
                                 )
    banner = models.ImageField(verbose_name="Баннер", upload_to="photos/%Y/%m/%d/", max_length=100, unique=True,
                               null=True,
                               validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])
    card_img = models.ImageField(verbose_name="Картинка карточки", upload_to="photos/%Y/%m/%d/", max_length=100,
                                 unique=True, null=True,
                                 validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'stocks'


class StockImg(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True,
                            validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])

    class Meta:
        db_table = 'stock_imgs'


class News(models.Model):
    name = models.CharField(verbose_name="Название", max_length=30, null=False,
                            validators=[
                                validators.MaxLengthValidator(30,
                                                              'Длина названия новости должна быть не более 30ти символов.'),
                                validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                          'Название новости должно начинаться с заглавной буквы'),
                                validators.ProhibitNullCharactersValidator(),
                            ]
                            )
    short_description = models.TextField(verbose_name="Краткое описание", max_length=50,
                                         validators=[
                                             validators.MaxLengthValidator(50),
                                             validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                       message='Описание должно начинаться с заглавной буквы.'),
                                             validators.ProhibitNullCharactersValidator(),

                                         ]
                                         )
    description = models.TextField(verbose_name="Описание", max_length=500,
                                   validators=[
                                       validators.MaxLengthValidator(500),
                                       validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                 message='Описание должно начинаться с заглавной буквы.'),
                                       validators.ProhibitNullCharactersValidator(),

                                   ]
                                   )
    creation_date = models.DateField(verbose_name="Дата создания", auto_now_add=True, null=True)
    turn_on = models.BooleanField(verbose_name="ВКЛ/ВЫКЛ", default=False)
    video_link = models.URLField(verbose_name="Ссылка на видео",
                                 validators=[validators.URLValidator(),
                                             validators.RegexValidator(
                                                 '\w*:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b([-a-zA-Z0-9@:%_\+.~#?&\/=]*)', )],
                                 )
    banner = models.ImageField(verbose_name="Баннер", upload_to="photos/%Y/%m/%d/", max_length=100, unique=True,
                               null=True,
                               validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])
    card_img = models.ImageField(upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True,
                                 verbose_name="Картинка карточки",
                                 validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'news'


class NewsImg(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    img = models.ImageField(verbose_name='', upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True,
                            validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])

    class Meta:
        db_table = 'news_imgs'


class CafeBarMenu(models.Model):
    name = models.CharField(max_length=150,
                            validators=[
                                validators.MaxLengthValidator(150),
                                validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                          message='Название блюда должно начинаться с заглавной буквы'),
                                validators.ProhibitNullCharactersValidator(),
                            ]
                            )
    weight = models.PositiveSmallIntegerField(null=True, verbose_name='Вес(грамм)',
                                              validators=[
                                                  validators.MinValueValidator(0)
                                              ]
                                              )
    price = models.FloatField(null=True, verbose_name='Цена',
                              validators=[
                                  validators.MinValueValidator(0.0)
                              ]
                              )

    class Meta:
        db_table = 'cafe_bar_menu'
