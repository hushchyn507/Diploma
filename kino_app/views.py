import datetime
import json

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import formset_factory
from django.http import FileResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DetailView

from admin_panel.models.film import *
from admin_panel.models.cinema import *
from admin_panel.models.main_page import *
from datetime import date, timedelta

from admin_panel.forms import BookingForm


def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


# Create your views here.
def page(request, page_id):
    page = Page.objects.get(pk=page_id)
    page_imgs = PageImg.objects.filter(page_id=page_id)

    data = {"page": page, 'page_imgs': page_imgs}

    return render(request, '../templates/kino_app/page2.html', context=data)


@method_decorator([login_required], name='dispatch')
class SeanceDetail(DetailView):
    model = Seance
    template_name = '../templates/kino_app/booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def getBookedTickets(request, seance_id):
    if is_ajax(request):
        tickets = Ticket.objects.filter(seance_id=seance_id)
        data = {}
        ticket_list = []
        for row in tickets.distinct('row'):
            for ticket in tickets.filter(row=row.row):
                ticket_list.append(ticket.seat)
            data[row.row] = ticket_list
            ticket_list = []
        return JsonResponse(data=data)


def booking(request):
    print('hwllo')
    if request.POST:
        print('Hello world')
        data = json.loads(request.POST.get('choosedTickets'))
        print(data)
        seance_id = request.POST.get('seance_id')
        user_id = request.POST.get('user_id')
        print(seance_id, user_id)
        for key, value in data.items():
            for row, seat in value.items():
                Ticket(row=row, seat=seat, seance_id=seance_id, user_id=user_id).save()
        return JsonResponse(data={'Success': 200})
    return render(request, '../templates/kino_app/booking.html', context=None)


def main(request):
    top_carousel = TopCarousel.objects.all()
    bottom_carousel = BottomCarousel.objects.all()
    banners_sliders = {"top_carousel": top_carousel, "bottom_carousel": bottom_carousel}
    today_date = date.today()
    seances_today = Seance.objects.filter(date=today_date)
    seances_today = seances_today.distinct("film")

    unreleased_films = Film.objects.filter(released__gt=today_date)
    data = {'seances_today': seances_today, 'unreleased_films': unreleased_films, 'banners_sliders': banners_sliders,
            "today_date": today_date.today()}
    return render(request, '../templates/kino_app/main2.html', context=data)


def cinemas(request):
    cinemas = Cinema.objects.all()
    data = {
        "cinemas": cinemas,
    }
    return render(request, '../templates/kino_app/cinemas2.html', context=data)


class Poster(ListView):
    template_name = '../templates/kino_app/poster_soon.html'
    model = Film
    context_object_name = 'films'

    def get_queryset(self):
        '''
        этот метод переопределить значение атрибута model и
        за основы выборки будут взяты данные указанные здесь
        '''
        return Film.objects.filter(released__lte=date.today())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Афиша'
        return context


class Soon(ListView):
    template_name = '../templates/kino_app/poster_soon.html'
    model = Film
    context_object_name = 'films'

    def get_queryset(self):
        return Film.objects.filter(released__gte=date.today())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Скоро'
        return context


def posterSoonAjax(request):
    if request.GET['page'] == 'poster':
        data = {
            'type': 'poster',
            'films': Film.objects.filter(released__lte=date.today())
        }
    if request.GET['page'] == 'soon':
        data = {
            'type': 'soon',
            'films': Film.objects.filter(released__gte=date.today())
        }
    return render(request, '../templates/kino_app/poster_soon_ajax.html', context=data)


def schedule(request):
    template = '../templates/kino_app/schedule2.html'
    seances = Seance.objects.all()
    if is_ajax(request):
        template = '../templates/kino_app/schedule_items.html'
        date_filter = request.GET.get('period')
        halls_filter = request.GET.getlist('halls_filter')
        films_filter = request.GET.getlist('films_filter')
        techs_filter = request.GET.getlist('techs_filter')
        if date_filter:
            if date_filter == 'tomorrow':
                seances = seances.filter(date=date.today() + timedelta(days=1))
            if date_filter == 'week':
                seances = seances.filter(date__lte=date.today() + timedelta(days=7), date__gte=date.today())
            if date_filter == 'today':
                seances = seances.filter(date=date.today())
            if date_filter == 'months':
                seances = seances.filter(date=date.today().month)

        if halls_filter:
            seances = seances.filter(hall__number__in=halls_filter)
        if films_filter:
            seances = seances.filter(film_id__in=films_filter)
        if techs_filter:
            seances = seances.filter(tech_type__name__in=techs_filter)

    result = []
    for film_seance in seances.distinct('film_id'):
        film_seances = seances.filter(film_id=film_seance.film_id)
        date_film = []

        for date_seance in film_seances.distinct('date'):
            date_seances = film_seances.filter(date=date_seance.date)
            hall_film = []

            for hall_seance in date_seances.distinct('hall'):
                hall_seances = date_seances.filter(hall=hall_seance.hall)
                tech_film = []

                for tech_seance in hall_seances.distinct('tech_type'):
                    tech_seances = hall_seances.filter(tech_type=tech_seance.tech_type)
                    tech_film.append((tech_seance.tech_type.name, tech_seances))

                hall_film.append((hall_seance.hall, tech_film))

            date_film.append((date_seance.date, hall_film))
        result.append((film_seance.film, date_film))

    film_list = []
    today_date = date.today()

    for film in Film.objects.filter(released__lt=today_date).order_by('name'):
        film_list.append(('unchecked', film))
    tech_list = []
    for tech in TechnologyType.objects.order_by('name'):
        tech_list.append(('unchecked', tech))

    hall_list = []
    for hall in Hall.objects.order_by('number'):
        hall_list.append(('unchecked', hall))

    data = {
        "result": result,
        'hall_list': hall_list,
        'film_list': film_list,
        "tech_list": tech_list,
    }
    return render(request, template, context=data)


def schedule_for_film(request):
    seances = Seance.objects.all()
    date_filter = request.GET.get('period')
    halls_filter = request.GET.getlist('halls_filter')
    films_filter = request.GET.getlist('films_filter')
    techs_filter = request.GET.getlist('techs_filter')
    if date_filter:
        if date_filter == 'tomorrow':
            seances = seances.filter(date=date.today() + timedelta(days=1))
        if date_filter == 'week':
            seances = seances.filter(date__lte=date.today() + timedelta(days=7), date__gte=date.today())
        if date_filter == 'today':
            seances = seances.filter(date=date.today())
        if date_filter == 'months':
            seances = seances.filter(date=date.today().month)

    if halls_filter:
        seances = seances.filter(hall__number__in=halls_filter)
    if films_filter:
        seances = seances.filter(film_id__in=films_filter)
    if techs_filter:
        seances = seances.filter(tech_type__name__in=techs_filter)

    result = []
    for date_seance in seances.distinct('date'):
        date_seances = seances.filter(date=date_seance.date)
        hall_film = []

        for hall_seance in date_seances.distinct('hall'):
            hall_seances = date_seances.filter(hall=hall_seance.hall)
            tech_film = []

            for tech_seance in hall_seances.distinct('tech_type'):
                tech_seances = hall_seances.filter(tech_type=tech_seance.tech_type)
                tech_film.append((tech_seance.tech_type.name, tech_seances))

            hall_film.append((hall_seance.hall, tech_film))

        result.append((date_seance.date, hall_film))

    film_list = []
    for film in Film.objects.order_by('name'):
        film_list.append(('unchecked', film))
    tech_list = []
    for tech in TechnologyType.objects.order_by('name'):
        tech_list.append(('unchecked', tech))

    hall_list = []
    for hall in Hall.objects.order_by('number'):
        hall_list.append(('unchecked', hall))

    data = {

        "result": result,
        'hall_list': hall_list,
        'film_list': film_list,
        "tech_list": tech_list,
    }
    return render(request, '../templates/kino_app/schedule_for_film.html', context=data)


def card_cinema(request, name):
    cinema = Cinema.objects.get(name=name)
    cinema_imgs = CinemaImg.objects.filter(cinema_id=cinema.id)
    halls = Hall.objects.filter(cinema_id=cinema.id)
    seances = Seance.objects.filter(date=date.today())

    data = {
        'cinema': cinema, "cinema_imgs": cinema_imgs,
        "halls": halls, "halls_num": halls.__len__(),
        'seances': seances,
    }
    return render(request, '../templates/kino_app/cinema_card2.html', context=data)


def film_card(request, name):
    seances = Seance.objects.filter(film__name=name)
    date_filter = request.GET.get('date_filter')
    halls_filter = request.GET.getlist('halls_filter')
    techs_filter = request.GET.getlist('techs_filter')
    if date_filter:
        new_date = datetime.datetime.strptime(date_filter, '%Y-%m-%d').strftime('%Y-%m-%d')
        seances = seances.filter(date=new_date)
    if halls_filter:
        seances = seances.filter(hall__number__in=halls_filter)
    if techs_filter:
        seances = seances.filter(tech_type__name__in=techs_filter)

    result = []
    for film_seance in seances.distinct('film_id'):
        film_seances = seances.filter(film_id=film_seance.film_id)
        date_film = []

        for date_seance in film_seances.distinct('date'):
            date_seances = film_seances.filter(date=date_seance.date)
            hall_film = []

            for hall_seance in date_seances.distinct('hall'):
                hall_seances = date_seances.filter(hall=hall_seance.hall)
                tech_film = []

                for tech_seance in hall_seances.distinct('tech_type'):
                    tech_seances = hall_seances.filter(tech_type=tech_seance.tech_type)
                    tech_film.append((tech_seance.tech_type.name, tech_seances))

                hall_film.append((hall_seance.hall, tech_film))

            date_film.append((date_seance.date, hall_film))
        result.append((film_seance.film, date_film))

    hall_list = Hall.objects.order_by('number')
    tech_list = TechnologyType.objects.order_by('name')

    film = Film.objects.get(name=name)
    scriptwriter = film.scriptwriters.all()
    editor = film.editors.all()
    producer = film.producers.all()
    operator = film.operators.all()
    country = film.countries.all()
    genres = film.genres.all()
    film_imgs = FilmImg.objects.filter(film=film)

    data = {
        "result": result,
        'hall_list': hall_list,
        "tech_list": tech_list,
        'film': film,
        'genres': genres,
        'scriptwriters': scriptwriter,
        'editors': editor,
        'producers': producer,
        'operators': operator,
        'film_imgs': film_imgs,
        'countries': country,
        'title': film.name,
    }
    return render(request, '../templates/kino_app/film_card2.html', context=data)


def hall(request, id):
    hall = Hall.objects.get(pk=id)
    hall_imgs = HallImg.objects.filter(hall_id=hall.id)
    seances = Seance.objects.filter(hall=hall, date=date.today())
    data = {
        'hall': hall,
        'hall_imgs': hall_imgs,
        'seances': seances
    }

    return render(request, '../templates/kino_app/hall2.html', context=data)


def bar(request):
    return render(request, '../templates/kino_app/bar.html')


def vip_hall(request):
    return render(request, '../templates/kino_app/vip_hall.html')


def kids_room(request):
    return render(request, '../templates/kino_app/kids_room.html')


def ads(request):
    return render(request, '../templates/kino_app/ads.html')


def mobile_apps(request):
    return render(request, '../templates/kino_app/mobile_apps.html')


def contacts(request):
    contact = Contact.objects.all()
    cinema = Cinema.objects.get(id=1)
    data = {
        'contacts': contact,
        'cinema': cinema,
    }
    return render(request, '../templates/kino_app/contacts2.html', context=data)


def news(request):
    news = News.objects.filter(turn_on=True).order_by('creation_date')
    paginator = Paginator(news, 2)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    data = {'news_list': page.object_list, 'page': page, }
    return render(request, '../templates/kino_app/news2.html', context=data)


def stocks(request):
    stocks = Stock.objects.filter(turn_on=True).order_by('creation_date')
    paginator = Paginator(stocks, 2)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    data = {'stocks': page.object_list, 'page': page, }
    return render(request, '../templates/kino_app/stocks2.html', context=data)


def page_stock(request):
    return render(request, '../templates/kino_app/page_stock.html')


def page_news(request):
    return render(request, '../templates/kino_app/page_news.html')


def search(request):
    film_name = request.GET['search_film']
    film = Film.objects.get(name=film_name)
    return film_card(request, film.name)


def profile(request):
    tickets = Ticket.objects.filter(user_id=request.user.id)
    data = {
        'tickets': tickets
    }
    return render(request, '../templates/kino_app/profile.html', context=data)
