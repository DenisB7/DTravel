from data import title, departures


def site_header(request):
    site_headers = {
        'title': title,
        'departure': departures,
    }

    return site_headers
