from flask_login import UserMixin
from . import db
import pandas as pd
from werkzeug.security import  check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    def __init__(self, id, username, email, password):
        self.id = id 
        self.username = username
        self.email = email
        self.password = password
 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(400))


class Productos_usy(db.Model):
    __tablename__= 'hoja1'
    def __init__(self, id, Disponibilidad, Transito, Precio, Descuento, Precio_oferta, Descripcion, um):
      self.id = id
      self.Disponibilidad = Disponibilidad
      self.Transito = Transito
      self.Precio =  Precio
      self.Descuento = Descuento 
      self.Precio_oferta = Precio_oferta
      self.Descripcion = Descripcion
      self.UM = um

    id = db.Column(db.String, primary_key=True)
    Disponibilidad = db.Column(db.Integer)
    Transito = db.Column(db.String(300))
    Precio = db.Column(db.Float)
    Descuento = db.Column(db.Float)
    Precio_oferta = db.Column(db.String(300))
    Descripcion = db.Column(db.String(300))
    UM = db.Column(db.String(10))



class Productos_marca(db.Model):
    __tablename__= 'hoja2'
    def __init__(self, id, ref , Transito, Disponibilidad, Precio, Descuento, Precio_oferta, Descripcion, um):
      self.id = id
      self.ref = ref
      self.Disponibilidad = Disponibilidad
      self.Transito = Transito
      self.Precio =  Precio
      self.Descuento = Descuento 
      self.Precio_oferta = Precio_oferta
      self.Descripcion = Descripcion
      self.UM = um

    id = db.Column(db.String, primary_key=True)
    REF = db.Column(db.String(100), unique=True)
    Transito = db.Column(db.String(300))
    Disponibilidad = db.Column(db.Integer)
    Precio = db.Column(db.Float)
    Descuento = db.Column(db.Float)
    Precio_oferta = db.Column(db.String(300))
    Descripcion = db.Column(db.String(300))
    UM = db.Column(db.String(10))



class Productos_dijonas(db.Model):
    __tablename__= 'hoja3'
    def __init__(self, id, ref, Disponibilidad, Transito, Precio, Descuento, Descripcion, um):
      self.id = id
      self.ref = ref
      self.Disponibilidad = Disponibilidad
      self.Transito = Transito
      self.Precio =  Precio
      self.Descuento = Descuento 
      self.Descripcion = Descripcion
      self.UM = um
      self.Descuento = Descuento 

    id = db.Column(db.String, primary_key=True)
    REF = db.Column(db.String(100), unique=True)
    Disponibilidad = db.Column(db.Integer)
    Transito = db.Column(db.String(300))
    Precio = db.Column(db.Float)
    Descripcion = db.Column(db.String(300))
    UM = db.Column(db.String(10))
    Descuento = db.Column(db.Float)




#_____________________________________DATA_______________________________________
ITEMS_USY = [
            'accesorio', 'Jabonera', 'Perchero', 'toallero' , 'papel', 'regadera' , 'ducha', 'fregadero', 'griferia', 'lavamanos', 'rejilla cuadrada', 'rejilla rectangular', 'calentador'
            'canilla', 'desague para', 'herraje para', 'flotante', 'colector', 'conexión para manguera', 'manguera', 'conector', 'unión', 'check', 'valvula' , 'compacta', 'compuerta', 'vastago', 'manilla metálica', 'manilla plástic', 'extension', 'agua', 'sifon', 'tubo flexible', 
            'Bomba', 'tanque', 'hidrocompacto', 'gato', 'taladro', 'tronzadora', 'sierra',
            'toma', 'enchufe', 'interruptor' , 'timbre' , 'breakers', 'cable', 'receptáculo', 'receptaculo', 'socate',
            'bombillo', 'oval', 'lámpara', 'lampara', 'luminaria', 'fotocélula', 'lente', 'reflector', 'LED', 'tirrap'
            'cepillo', 'espatula', 'cinta', 'teipe', 'tirro', 'cuchara', 'cizalla', 'deztupidor', 'amolar', 'pistola', 'plato', 'probador', 'tijera', 'tenaza', 
            'cerradura', 'cerrojo', ' '
            ]

ITEMS_MARCA = [
            ' 3M', ' Black & Decker',  ' Dewalt',  ' EarthBulb', ' Eaton', ' EZ WELD', ' Flexon', ' Lenox', ' Pedrollo', ' Stanley', ' Valley', ' Wisdom', ' Sunico',
            ' West Chester', ' Torin Jack', ' Tramontina', ' Victor', 'West Arco', ' AW hogar', ' Korclass', ' Kdp', ' '   
            ]

ITEMS_DIJONAS = ['fregadero', 'lavamanos', 'sanitario', 'herraje', 'tapa',  'batea', 'porcelanato', 'mueble', ' ']


def get_data(sheet):
    order_items = []

    if (sheet == 1):
        items = ITEMS_USY
        for item in items:
            data = Productos_usy.query.filter(Productos_usy.Descripcion.contains(item) & (Productos_usy.Disponibilidad != '0' or Productos_usy.Disponibilidad != None)).all()
            order_items.extend(data)
        description = "Baños - Plomeria - Herramientas - Maquinaria - Electricidad - Iluminación - Cerraduras"
    elif (sheet == 2):
        items = ITEMS_MARCA
        for item in items:
            data = Productos_marca.query.filter(Productos_marca.Descripcion.contains(item) & (Productos_marca.Disponibilidad != '0' or Productos_marca.Disponibilidad != None)).all()
            order_items.extend(data)
        description = "Herramientas - Electricidad"
    else:
        items = ITEMS_DIJONAS
        for item in items:
            data = Productos_dijonas.query.filter(Productos_dijonas.Descripcion.contains(item) & (Productos_dijonas.Disponibilidad != '0' or Productos_dijonas.Disponibilidad != None)).all()
            order_items.extend(data)
        description = "Baños - Muebles"
    return pd.unique(order_items), items, description