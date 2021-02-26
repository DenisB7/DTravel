from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.views import View
from random import sample

from data import description, subtitle, departures, tours


class MainView(View):

    def get(self, request):
        tours_pictures = []
        tours_list = []
        for tour_id, tour_info in tours.items():
            tour_info_copy = tour_info.copy()
            tour_info_copy['stars'] = int(tour_info_copy['stars']) * '★'
            del tour_info_copy['departure']
            tours_list.append({tour_id: tour_info_copy})
            tours_pictures.append(tour_info_copy['picture'])
        tours_random = sample(tours_list, 6)
        tours_random_dicts = {}
        for tour in tours_random:
            tours_random_dicts.update(tour)
        tours_picture_random = sample(tours_pictures, 1)
        tours_info = {
            'subtitle': subtitle,
            'description': description,
            'tours_random_dicts': tours_random_dicts,
            'tours_picture_random': tours_picture_random[0],
        }
        return render(request, 'main.html', context=tours_info)


class DepartureView(View):

    def get(self, request, departure):
        tours_dict = {}
        prices = []
        nights = []
        departure_city = set()
        for tour_id, tour_info in tours.items():
            tour_info_copy = tour_info.copy()
            if departure == tour_info_copy['departure']:
                tour_info_copy['stars'] = int(tour_info_copy['stars']) * '★'
                tours_dict.update({tour_id: tour_info_copy})
                prices.append(tour_info_copy['price'])
                nights.append(tour_info_copy['nights'])
                departure_city.add(departures[departure])
        tours_num = len(tours_dict)
        tours_min_price = min(prices)
        tours_max_price = max(prices)
        tours_min_nights = min(nights)
        tours_max_nights = max(nights)
        departure_info = {
            'tours_dict': tours_dict,
            'departure_city': departure_city.pop(),
            'tours_num': tours_num,
            'tours_min_price': tours_min_price,
            'tours_max_price': tours_max_price,
            'tours_min_nights': tours_min_nights,
            'tours_max_nights': tours_max_nights,
        }
        return render(request, 'departure.html', context=departure_info)


class TourView(View):

    def get(self, request, tour_id):
        tour = tours.get(tour_id).copy()
        del tour['departure'], tour['date']
        tour['stars'] = int(tour['stars']) * '★'
        tour_departure = {
            'tour': tour,
        }
        return render(request, 'tour.html', context=tour_departure)


def custom_handler404(request, exception):
    return HttpResponseNotFound('404 ошибка - ошибка на стороне '
                                'сервера (страница не найдена)')


def custom_handler500(request):
    return HttpResponseServerError('внутренняя ошибка сервера')
