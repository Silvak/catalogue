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
from .models import  all_paginated, get_productos_usy, get_productos_marca, get_productos_dijonas
from datetime import datetime
#import pdfkit


main = Blueprint('main', __name__)

#landing page
@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


#______________________________________ catalogo de busqueda online ___________________________________
@main.route('/catalogo')
def online_catalog():
    productos = all_paginated()
    return  render_template('catalog.html', productos = productos)


#_____________________________________ links buttons de descarga pdf _________________________________
@main.route('/descarga', methods=['GET', 'POST'])
def download():

    return render_template('download_link.html')


#generar descargas automaticas de archivos pdf subidos
@main.route('/descarga/catalogo',  methods=['GET', 'POST'])
def download_file():
    #paht_catalog =  './data/pdf/catalogo_roleo_1.pdf' 
    return '_' #send_file(paht_catalog, as_attachment=True)


'''
#generacion catalogo individual - vistas individuales de descarga catalogo
@main.route('/descarga-catalogo-electricos')
def download_one():
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe") 
    productos = get_productos()
    time = datetime.now()
    rendered =  render_template('download.html', productos = productos, time = time)
    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response
'''

# _______________________________ vistas de catalogo por seccion _________________________________________--
@main.route('/catalogo-suministro-roleo-1', methods=['GET', 'POST'])
def catalogue_one():
    productos = get_productos_usy()
    time = datetime.now()
    return render_template('download.html', productos = productos, time = time)


@main.route('/catalogo-suministro-roleo-2', methods=['GET', 'POST'])
def catalogue_two():
    productos = get_productos_marca()
    time = datetime.now()
    return render_template('download.html', productos = productos, time = time)


@main.route('/catalogo-suministro-roleo-3', methods=['GET', 'POST'])
def catalogue_three():
    productos = get_productos_dijonas()
    time = datetime.now()
    return render_template('download_dijonas.html', productos = productos, time = time)



#______________________________________ panel de administracion de datos_______________________________________________-
@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    #Recive archivo excel
    if request.form.get('btn') == 'Actualizar DB':
        if request.method == 'POST':
            f = request.files['upfile']
            if f.filename == '' or 'upfile' not in request.files:
                flash('No se ha selecionado ningun archivo.info') 
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                file_management(f, filename) 
                flash('Actualizacion exitosa.success') 
                #import_data()

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


    return  render_template('dashboard.html', username=current_user.username)




