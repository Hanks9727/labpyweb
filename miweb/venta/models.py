from django.db import models

# Definir la entidad(el nombre de la tabla y sus atributos(con tipos y validaciones))
#Cliente
#   id_cliente,texto numérico de 8 caracteres,clave principal
#    ape_nom,texto,max 80 caracteres


class Cliente(models.Model):
    #Creación de los atributos de Cliente
    id_cliente = models.CharField(primary_key=True,max_length=80,error_messages='El texto debe tener max 8 digitos')
    ape_nom=models.CharField(max_length=80)
    fec_reg=models.DateField() #solo es fecha
    fec_sis=models.DateTimeField(auto_now=True) # fecha y hora actual

    def __str__(self):
        return f"Nombres : {self.ape_nom},DNI : {self.id_cliente}"


class Producto(models.Model):
    id_Producto = models.AutoField(primary_key=True)  # entero autocorrelativo, clave primaria
    nom_prod = models.CharField(max_length=50)       # texto hasta 50 caracteres
    des_prod = models.TextField(max_length=500)      # texto multilinea, hasta 500 caracteres
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # número real con 2 decimales
    stock = models.PositiveIntegerField()             # entero >= 0
    activo = models.BooleanField(default=True)        # valor lógico, True por defecto
    fec_vencim = models.DateField()                    # fecha (AAAA-MM-DD)
    fec_reg = models.DateTimeField(auto_now_add=True) # fecha y hora al guardar (timestamp)

    def __str__(self):
         return f"{self.nom_prod} - s/.{self.precio} (stock: {self.stock})"
    
class Venta(models.Model):
    cod_venta = models.AutoField(primary_key=True)  # Autocorrelativo
    cod_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fec_venta = models.DateField(auto_now_add=True)  # opcional, para registrar la fecha de venta

    def __str__(self):
        return f"Venta #{self.cod_venta} - Cliente: {self.cod_cliente.ape_nom} - Total: s/.{self.total}"

class VentaDetalle(models.Model):
    cod_venta_detalle = models.AutoField(primary_key=True)
    cod_venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    cod_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.cod_producto.nom_prod} en venta {self.cod_venta.cod_venta}"


    
    


