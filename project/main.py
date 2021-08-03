from flask import Blueprint 
from flask import render_template
from flask import request 
from flask import send_file
from flask import make_response 
from flask import redirect 
from flask import url_for 
from flask import session
from flask import flash
from flask_login import login_required, current_user
from .files import file_management, allowed_file, import_data, img_management
from werkzeug.utils import secure_filename
from .models import  all_paginated, get_productos_usy, get_productos_marca, get_productos_dijonas,  Productos_usy, Productos_marca, Productos_dijonas
from datetime import datetime
#import pdfkit

import os 
import numpy as np
import cv2


main = Blueprint('main', __name__)

# _______________________________ vistas de catalogo por seccion _________________________________________--
@main.route('/catalogo-suministro-roleo-1')
def catalogue_one():
    productos = get_productos_usy()
    time = datetime.now()
    return render_template('catalogue_one.html', productos = productos, time = time)


@main.route('/catalogo-suministro-roleo-2')
def catalogue_two():
    productos = get_productos_marca()
    time = datetime.now()
    return render_template('catalogue_two.html', productos = productos, time = time)


@main.route('/catalogo-suministro-roleo-3')
def catalogue_three():
    productos = get_productos_dijonas()
    time = datetime.now()
    return render_template('catalogue_three.html', productos = productos, time = time)



@main.route('/catalogo')
def catalogo():
    productos = get_productos_marca()

    ordered_products= []
    temp_list = []
    arr_index = 0
    run  = True
    while(run):
        temp_list = []
        count = 0
        while(count < 9 and run):
            if (arr_index < len(productos)):
                size = ""
                try:
                    #tratamos de encontrar la imagen dentro de la carpeta del catalogo
                    img = cv2.imread(f'./project/static/images/catalogo/{productos[arr_index].id}.png')
                    height, width, channels = img.shape
                    print (f'h:{height} w:{width} c:{channels}  #########################  IMAGEN EXISTE')
                    size = size_images(height, width)
                    temp_list.append(productos[arr_index])
                    productos[arr_index].Descripcion = productos[arr_index].Descripcion + ";" + size
                    
                    if (size == "high" or size == "wide"):
                        count = count + 2
                    if (size == "big"):
                        count = count + 4
                    if (size == "normal"):
                        count = count + 1
                except:
                    temp_list.append(productos[arr_index])
                    productos[arr_index].Descripcion = productos[arr_index].Descripcion + ";"+"not image"
                    count = count + 1
                
                arr_index = arr_index + 1
                
            else:
                run = False
        ordered_products.append(temp_list)
    print(ordered_products[1][1].Descripcion)
    return render_template('base_catalog.html', catalogo = ordered_products)


def size_images(h, w):
    if (h >= 300 and w <= 200):
        size = "high"
    elif (h <= 200 and w >= 300):
        size = "wide"
    elif (h >= 400 and w >= 400):
        size = "big"
    else:
        size= "normal"
    return  size


#______________________________________ panel de administracion de datos_______________________________________________-
@main.route('/', methods=['GET', 'POST'], defaults={"page": 1, "page_m": 1})
@main.route('/<int:page>/<int:page_m>', methods=['GET', 'POST'])
def dashboard(page, page_m):

    #Recive archivo excel
    if request.form.get('btn') == 'Subir Archivo':
        if request.method == 'POST':
            f = request.files['upfile']
            if f.filename == '' or 'upfile' not in request.files:
                flash('No se ha selecionado ningun archivo.info') 
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                file_management(f, filename) 
                try:
                    import_data()
                    flash('Base de datos actualizada.success') 
                except ValueError:
                    flash('Ocurrio un error al intentar actualizar los productos.warning') 

 
    #Recive imagen png
    if request.form.get('btn') == 'Subir Imagen':
        if request.method == 'POST':
            f = request.files['upimage']
            if f.filename == ''  or 'upimage' not in request.files:
                flash('No se ha selecionado ninguna imagen.info') 
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                img_management(f, filename) 
                flash('Imagen subida exitosamente.success') 


    page = page
    
    page_m = page_m
    pages = 10


    productos_usys = all_paginated(page, pages)
    productos_marcas = Productos_marca.query.paginate(page=page, per_page=pages, error_out=True)
    productos_dijona = Productos_dijonas.query.paginate(page=page_m, per_page=pages, error_out=True)

    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        productos_usys = Productos_usy.query.filter(Productos_usy.id.contains(search.upper())).paginate(per_page=pages, error_out=True)
        return render_template('dashboard.html',  productos_usy_table = productos_usys, productos_marcas_table = productos_marcas, productos_dijona_table = productos_dijona ,tag = tag)

    if request.method == 'POST' and 'tag_m' in request.form:
        tag_m = request.form["tag_m"]
        search = "%{}%".format(tag_m)
        productos_marcas = Productos_marca.query.filter(Productos_marca.id.contains(search.upper())).paginate(per_page=pages, error_out=True)
        return render_template('dashboard.html',  productos_usy_table = productos_usys, productos_marcas_table = productos_marcas, productos_dijona_table = productos_dijona ,tag_m = tag_m)

    if request.method == 'POST' and 'tag_d' in request.form:
        tag_d = request.form["tag_d"]
        search = "%{}%".format(tag_d)
        productos_dijona = Productos_dijonas.query.filter(Productos_dijonas.id.contains(search.upper())).paginate(per_page=pages, error_out=True)
        return render_template('dashboard.html',  productos_usy_table = productos_usys, productos_marcas_table = productos_marcas, productos_dijona_table = productos_dijona ,tag_d = tag_d)




    return  render_template('dashboard.html',  productos_usy_table = productos_usys, productos_marcas_table = productos_marcas, productos_dijona_table = productos_dijona)


