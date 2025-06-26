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
