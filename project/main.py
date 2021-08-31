from flask import Blueprint 
from flask import render_template
from flask import request 
"""
from flask import send_file
from flask import make_response 
from flask import redirect 
from flask import url_for 
from flask import session
from flask_login import login_required, current_user
"""
from flask import flash
from .files import file_management, allowed_file, import_data, img_management
from werkzeug.utils import secure_filename
from .models import get_data
from datetime import datetime
import cv2


main = Blueprint('main', __name__)


#______________________________________ panel de administracion de datos_______________________________________________-
@main.route('/', methods=['GET', 'POST'])
def dashboard():
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

    return  render_template('dashboard.html')


#______________________________________ vista creacion catalogo_______________________________________________-
@main.route('/catalogo', methods=['GET', 'POST'], defaults={"page": 1})
@main.route('/catalogo/<int:page>', methods=['GET', 'POST'])
def catalogo(page):
    productos, categories, description = get_data(page)
    
    ordered_products= []
    not_img_products= []
    temp_list = []
    arr_index = 0
    run  = True
    while(run):
        temp_list = []
        count = 0
        while(count < 9.0 and run):
            if (arr_index < len(productos)):
                size = ""
                try:
                    #tratamos de encontrar la imagen dentro de la carpeta del catalogo
                    img = cv2.imread(f'./project/static/images/catalogo/{productos[arr_index].id}.png')
                    height, width, channels = img.shape
                    #print (f'h:{height} w:{width} c:{channels}  #########################  IMAGEN EXISTE')
                    size = size_images(height, width)
                    productos[arr_index].Descripcion = productos[arr_index].Descripcion + ";" + size
                    # establecer que antes de guardar el producto en la lista temporal este no valga mas que 9
                    if ((size == "high" or size == "wide") and (count + 2 <= 9)):
                        count = count + 2
                        temp_list.append(productos[arr_index])
                    if ((size == "big") and (count + 4 <= 9)):
                        count = count + 4
                        temp_list.append(productos[arr_index])
                    if ((size == "normal")and (count + 1 <= 9)):
                        count = count + 1
                        temp_list.append(productos[arr_index])
                except:
                    #not_img_products.append(productos[arr_index])
                    #temp_list.append(not_img_products)
                    not_img_products.append(productos[arr_index])
                arr_index = arr_index + 1   
            else:
                run = False
        ordered_products.append(temp_list)
    arr_index = 0
    for i in range(len(not_img_products)):
        """
        organizacion de productos sin imagenes
        """
        temp_list = []
        for n in range(21):
            if (arr_index < len(not_img_products)):
                not_img_products[arr_index].Descripcion = not_img_products[arr_index].Descripcion + ";not_img" 
                temp_list.append(not_img_products[arr_index])
                arr_index = arr_index + 1
            else:
                break
        else:
            ordered_products.append(temp_list)
            continue
        break  

    time = datetime.now()
    edition = "CATALOGO " + " 0" + str(page)
    return render_template('catalogue.html', catalogo = ordered_products, time = time, edition = edition, description = description, categories = categories )


def size_images(h, w):
    if (h >= 280 and w <= 320):
        size = "high"
    elif (h <= 200 and w >= 350):
        size = "wide"
    elif (h > 500 and w > 500):
        size = "big"
    else:
        size= "normal"
    return  size





""""""
