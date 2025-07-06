from django.shortcuts import render,redirect
from django.forms import modelformset_factory
from .models import Cliente, Venta,VentaDetalle
from .forms import VentaForm, VentaDetalleForm
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout #Funciones claves
from django.contrib.auth.decorators import login_required,permission_required

def handle_undefined_url(request):
    '''
    Gestiona los urls que no estan definidos
    '''
    if not request.user.is_authenticated:
        messages.warning(request, 'Debe iniciar sesión para acceder al sistema')
        return redirect('login')
    else:
        messages.info(request, 'La página solicitada no existe. Se redirigirá al inicio')
    return redirect('home')



#Creando nuestro login de entrada
def user_login(request):
    #Si ya esta autenticado, enviarlo a home
    if request.user.is_authenticated:
        return redirect("home") # Si el usuario esta authenticado que se valla a home
    
    #Si no está autenticado pedir usuario y clave
    if request.method =="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(request, username=username , password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Error de usuario o clave")
        else:
            messages.error(request,"Ingresa los datos")
    #Si hay fallo de autenticación,permitir reintentar
    return render(request,"venta/login.html")   


#Vista principal del sistema(Creo una funcion para que me pueda mostrar el home.html que le ancle a templates y dps se ancla en la url)
@login_required
def home(request):
    #Obtener los permisos del nuevo usuario que se creo que es us_cliente
    user_permissions = {
        "can_manage_clients" : (
            request.user.is_superuser or
            request.user.groups.filter(name="grp_cliente").exists() or
            request.user.has_perm("venta.add_cliente")
        ),
        "can_manage_products" : (
            request.user.is_superuser or
            request.user.groups.filter(name="grp_producto").exists() 
            
        ),
        "can_manage_providers" : (
            request.user.is_superuser or
            request.user.groups.filter(name="grp_proveedor").exists()
        ),
        "is_admin" : request.user.is_superuser
        
    }

    context = {
        "user_permissions" : user_permissions,
        "user" : request.user
    }
    return render(request,"venta/home.html",context)

#implementacion de logout
def user_logout(request):
    logout(request)
    messages.success(request,"Sesion cerrada correctamente")
    return redirect("login")
from django.http import HttpResponseForbidden
# consulta_clientes es la vista que muestra la lista
@login_required
@permission_required("venta.view_cliente", raise_exception=True)
def consulta_clientes(request):
    #verificar los permisos
    if not(request.user.is_superuser or
           request.user.groups.filter(name = "grp_cliente").exists() or
           request.user.has_perm("venta.view_cliente")):
        return HttpResponseForbidden("No tiene permisos para ingresar aqui")


    # Se requiere obtner los datos a gestionar
    #clientes = Cliente.objects.all().order_by('ape_nom') # la data es la que se requiera 
    clientes = Cliente.objects.all().order_by('id_cliente') # la data es la que se requiera 
    # Estos datos deben estar disponibles para una plantilla (Template)
    # Se crea un diccionario llamado context (será accesible desde la plantilla)
    context = { # en el template será objetos y valores
        'clientes' : clientes,
        'titulo'   : 'Lista de Clientes',
        'mensaje'  : 'Hola'
    }
    # Se devolverá el enlace entre la plantilla y el contexto
    return render(request, 'venta\lista_clientes.html', context)

from .models import Producto

def q_producto(request):
    productos = Producto.objects.all()
    contexto = {
        'titulo': 'Lista de Productos',
        'productos': productos,
    }
    return render(request, 'venta/lista_productos.html', contexto)

from .forms import ProductoForm
# Vista para registrar un nuevo producto
def crea_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            form = ProductoForm()
            mensaje = "Producto registrado correctamente."  #Sale este mensaje cuando puso un producto
            return render(request, 'venta/crea_producto.html', {'form': form, 'titulo': 'Registrar Producto', 'mensaje': mensaje})
    else:
        form = ProductoForm()
    
    return render(request, 'venta/crea_producto.html', {'form': form, 'titulo': 'Registrar Producto'})

from django.shortcuts import render, get_object_or_404, redirect

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'venta/detalle_producto.html', {'producto': producto})

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('q_producto')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'venta/crea_producto.html', {'form': form, 'titulo': 'Editar Producto'})

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('q_producto')
    return render(request, 'venta/eliminar_producto.html', {'producto': producto})

from .forms import ClienteCreateForm, ClienteUpdateForm
from django.contrib import messages
from django.shortcuts import redirect

@login_required
@permission_required("venta.add_cliente",raise_exception=True)
def crear_cliente(request):
    #Verificar los permisos
    if not(request.user.is_superuser or
           request.user.groups.filter(name = "grp_cliente").exists() or
           request.user.has_perm("venta.add_cliente")
           ):
        return HttpResponseForbidden("No tiene permisos para crear cliente")
        
    dni_duplicado = False

    if request.method == 'POST':
        form = ClienteCreateForm(request.POST)
        if form.is_valid():
            form.save() # salvar los datos
            messages.success(request, 'Cliente registrado correctamente')
            print('Se guardó bien')
            return redirect('crear_cliente') # se redirecciona a la misma página
        else:
            if 'id_cliente' in form.errors:
                for error in form.errors['id_cliente']:
                    if str(error) == "DNI_DUPLICADO": # se recibe del raise de forms
                        dni_duplicado = True
                        # Limpiar los errores 
                        form.errors['id_cliente'].clear()
                        print('DNI Duplicado!')
                        break

    else:
        form = ClienteCreateForm() # No hace nada, devuelve la misma pantalla

    context = {
        'form':form,
        'dni_duplicado':dni_duplicado # Enviar el estado del dni duplicado
    }
    return render(request, 'venta/crear_cliente.html', context) 

@login_required
@permission_required("venta.change_cliente",raise_exception=True)
def actualizar_cliente(request):
    #Verificar los permisos del grupo
    if not(request.user.is_superuser or
           request.user.groups.filter(name = "grp_cliente").exists() or
           request.user.has_perm("venta.change_cliente")
           ):
        return HttpResponseForbidden("No tiene permisos para modificar cliente")
    cliente = None
    dni_buscado = None
    form = None

    if request.method == 'POST':
        if 'buscar' in request.POST:
            # Buscar el cliente por DNI
            dni_buscado = request.POST.get('dni_busqueda')
            if dni_buscado:
                try: # intentar considerar la busqueda del cliente
                    # Obtener un objeto del tipo cliente
                    cliente = Cliente.objects.get(id_cliente=dni_buscado)
                    # Crear un formulario con los datos del objeto cliente
                    form = ClienteUpdateForm(instance=cliente)
                    messages.success(request, f'Cliente con DNI {dni_buscado} encontrado')
                except Cliente.DoesNotExist: # execepcion de dato no existente
                    messages.error(request, 'No se encontró Cliente con ese DNI')    
            else:
                messages.error(request, 'Por favor ingrese el DNI para buscar') 
        elif 'guardar' in request.POST:
            dni_buscado = request.POST.get('dni_busqueda') or request.POST.get('id_cliente')
            if dni_buscado:
                try:
                    cliente = Cliente.objects.get(id_cliente = dni_buscado)
                    form = ClienteUpdateForm(request.POST, instance=cliente)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Cliente actualizado correctamente')
                        # formulario con datos actualizados
                        cliente.refresh_from_db()
                        # devolver al formulario
                        form = ClienteUpdateForm(instance=cliente)
                    else:
                        messages.error(request, 'Error en los datos del formulario')
                except Cliente.DoesNotExist:
                    messages.error(request, 'Cliente no encontrado')
                    

            else:
                messages.error(request, 'No se puede identificar al cliente para actaualizar')
    context = {
        'form':form,
        'dni_buscado': dni_buscado,
        'cliente_encontrado': cliente is not None,
        'cliente':cliente
    }
    return render(request,'venta/u_cliente.html', context)
                     
# Eliminar clientes
@login_required
@permission_required("venta.delete_cliente",raise_exception=True)
def borrar_cliente(request):
    #Verificar los permisos del grupo
    if not(request.user.is_superuser or
           request.user.groups.filter(name = "grp_cliente").exists() or
           request.user.has_perm("venta.delete_cliente")
           ):
        return HttpResponseForbidden("No tiene permisos para eliminar cliente")
    clientes_encontrados = []
    tipo_busqueda = 'dni'
    termino_busqueda = '' # pa dentro de las cajas
    total_registros = 0

    if request.method == 'POST':
        #
        if 'consultar' in request.POST:
            # Realizar la búsqueda
            tipo_busqueda = request.POST.get('tipo_busqueda', 'dni')
            termino_busqueda = request.POST.get('termino_busqueda','').strip()

            if termino_busqueda:
                # procesar
                if tipo_busqueda == 'dni':
                    try:
                        cliente = Cliente.objects.get(id_cliente = termino_busqueda)
                        clientes_encontrados = [cliente]
                    except Cliente.DoesNotExist:
                        messages.error(request, 'No se encontró cliente con ese DNI')    

                elif tipo_busqueda == 'nombre':
                    clientes_encontrados = Cliente.objects.filter(
                        ape_nom__icontains = termino_busqueda # obtener las coincidencias
                    ).order_by('id_cliente') # debe estar ordenado

                    if not clientes_encontrados:
                        messages.error(request, 'No se encontraron clientes con ese nombre')

                total_registros = len(clientes_encontrados)

                if total_registros > 0:
                    messages.success(request, f'Se encontraron {total_registros} registro(s)')        

            else:
                messages.error(request, 'Ingrese un término de búsqueda')    

        elif 'eliminar' in request.POST:
            # Eliminar cliente
            dni_eliminar = request.POST.get('dni_eliminar')

            if dni_eliminar:
                try:
                    # buscar al cliente a eliminar
                    cliente = Cliente.objects.get(id_cliente = dni_eliminar)
                    cliente.delete()
                    messages.success(request, f'Cliente con DNI {dni_eliminar} eliminado correctamente')

                    # Volver a hacer la búsqueda para actualizar la lista
                    tipo_busqueda = request.POST.get('tipo_busqueda_actual', 'dni')
                    termino_busqueda = request.POST.get('termino_busqueda_actual','')

                    if termino_busqueda:
                        if tipo_busqueda == 'dni':
                            # Para DNI, no mostrar nada porque ya se eliminó
                            clientes_encontrados = []
                        elif tipo_busqueda == 'nombre':
                            # En este caso hay que buscar nuevamente lo que queda
                            clientes_encontrados = Cliente.objects.filter(
                                ape_nom__icontains = termino_busqueda
                            ).order_by('id_cliente')

                        total_registros = len(clientes_encontrados)
                

                except Cliente.DoesNotExist:
                    messages.error(request, 'Cliente no encontrado')
    
    context = {
        'clientes_encontrados' : clientes_encontrados,
        'tipo_busqueda' : tipo_busqueda,
        'termino_busqueda' : termino_busqueda,
        'total_registros' : total_registros
    }

    return render(request, 'venta/borrar_cliente.html', context)



def lista_ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'venta/lista_ventas.html', {'ventas': ventas})

def crear_venta(request):
    VentaDetalleFormSet = modelformset_factory(VentaDetalle, form=VentaDetalleForm, extra=3)  # 3 productos por venta

    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        formset = VentaDetalleFormSet(request.POST, queryset=VentaDetalle.objects.none())

        if venta_form.is_valid() and formset.is_valid():
            venta = venta_form.save(commit=False)
            venta.total = 0
            venta.save()

            total = 0
            for detalle_form in formset:
                detalle = detalle_form.save(commit=False)
                detalle.cod_venta = venta
                detalle.subtotal = detalle.cantidad * detalle.precio_unitario
                detalle.save()
                total += detalle.subtotal

            venta.total = total
            venta.save()

            return redirect('lista_ventas')  # O la url que uses para listar ventas

    else:
        venta_form = VentaForm()
        formset = VentaDetalleFormSet(queryset=VentaDetalle.objects.none())

    return render(request, 'venta/crear_venta.html', {
        'venta_form': venta_form,
        'formset': formset,
    })


def editar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    VentaDetalleFormSet = modelformset_factory(VentaDetalle, form=VentaDetalleForm, extra=0, can_delete=True)

    if request.method == 'POST':
        venta_form = VentaForm(request.POST, instance=venta)
        formset = VentaDetalleFormSet(request.POST, queryset=VentaDetalle.objects.filter(cod_venta=venta))

        if venta_form.is_valid() and formset.is_valid():
            venta = venta_form.save(commit=False)
            total = 0

            detalles = formset.save(commit=False)

            # Guardar los detalles y calcular total
            for detalle in detalles:
                detalle.cod_venta = venta
                detalle.subtotal = detalle.cantidad * detalle.precio_unitario
                detalle.save()
                total += detalle.subtotal
            
            # Eliminar detalles marcados para borrar
            for detalle_borrar in formset.deleted_objects:
                detalle_borrar.delete()

            venta.total = total
            venta.save()

            return redirect('lista_ventas')

    else:
        venta_form = VentaForm(instance=venta)
        formset = VentaDetalleFormSet(queryset=VentaDetalle.objects.filter(cod_venta=venta))

    return render(request, 'venta/editar_venta.html', {
        'venta_form': venta_form,
        'formset': formset,
        'venta': venta,
    })

def eliminar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        return redirect('lista_ventas')

    return render(request, 'venta/eliminar_venta.html', {'venta': venta})





