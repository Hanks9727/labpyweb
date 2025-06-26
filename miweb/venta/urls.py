from django.urls import path
from . import views

urlpatterns = [
    path('q_producto/', views.q_producto, name='q_producto'),
    path('crea_producto/', views.crea_producto, name='crea_producto'),
    path('detalle_producto/<int:pk>/', views.detalle_producto, name='detalle_producto'),
    path('editar_producto/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    
    path('venta/q_cliente',views.consulta_clientes,name='lista_clientes'),
    path('venta/c_cliente',views.crear_cliente,name='crear_cliente'),
    path('venta/u_cliente',views.actualizar_cliente,name='actualizar_cliente'),
    path('venta/d_cliente',views.borrar_cliente,name='borrar_cliente'),
]