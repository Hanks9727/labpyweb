from django.contrib import admin

# Register your models here.
from .models import Cliente  # : importas desde models.py de la misma app
admin.site.register(Cliente) # : Registrandome en el mismo admin del servidor de django

from .models import Producto
admin.site.register(Producto)
