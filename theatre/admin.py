from django.contrib import admin
from django.contrib.auth.models import User

from theatre.models import (TheatreHall,
                            Reservation,
                            Ticket,
                            Performance,
                            Play,
                            Genre,
                            Actor)

admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Play)
admin.site.register(TheatreHall)
admin.site.register(Reservation)
admin.site.register(Performance)
admin.site.register(Ticket)