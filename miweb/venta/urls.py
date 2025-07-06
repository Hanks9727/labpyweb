from django.urls import path, re_path
from . import views

urlpatterns = [
    path('q_producto/', views.q_producto, name='q_producto'),
    path('crea_producto/', views.crea_producto, name='crea_producto'),
    path('detalle_producto/<int:pk>/', views.detalle_producto, name='detalle_producto'),
    path('editar_producto/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),

    #(del login)
    path("",views.user_login,name = "login"),
    path("home/",views.home,name = "home"), 
    path("logout/",views.user_logout,name = "logout"),

    #path("",views.home,name= "home"), #pagina principal anclando 
    path('venta/q_cliente',views.consulta_clientes,name='lista_clientes'),
    path('venta/c_cliente',views.crear_cliente,name='crear_cliente'),
    path('venta/u_cliente',views.actualizar_cliente,name='actualizar_cliente'),
    path('venta/d_cliente',views.borrar_cliente,name='borrar_cliente'),
        
   
    # VENTAS
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('ventas/crear/', views.crear_venta, name='crear_venta'),
    path('ventas/editar/<int:pk>/', views.editar_venta, name='editar_venta'),
    path('ventas/eliminar/<int:pk>/', views.eliminar_venta, name='eliminar_venta'),




    # Poner al final de la lista  
    re_path(r'^.*/$', views.handle_undefined_url, name = 'catch_all'),
]