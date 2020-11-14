from django.contrib import admin
from .models import needforvideo
from .models import feedback
from .models import product
from .models import kolvo
from .models import Type

#admin.site.register(needforvideo)
admin.site.register(feedback)
admin.site.register(product)
admin.site.register(Type)
admin.site.register(kolvo)