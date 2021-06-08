from sqlalchemy import create_engine, update
import pandas as pd
import os

UPLOAD_FOLDER = os.path.abspath('./project/data/')
FILE_XLS = os.path.abspath('./project/data/catalog_data.xls')
ALLOWED_EXTENSIONS = set(['xls', 'xlsx', 'png', 'jpg'])
SHEET = ['Importadora Usy', 'Marca ', 'Dijonas']


engine = create_engine('sqlite:///project/data/products.db', echo=False)


def allowed_file(filename):
    '''verificacion de archivos permitidos'''
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def file_management(f, filename):
    ''' renombrar archivo xls, spaces ' ' to '_' '''
    data_folder = os.listdir(UPLOAD_FOLDER)
    if 'catalog_data.xls' in data_folder:
        #replace file
        os.remove(UPLOAD_FOLDER + '\\catalog_data.xls')
        f.save(os.path.join(UPLOAD_FOLDER, filename))
        print('file.xls SOBRESCRITO')
    else:
        f.save(os.path.join(UPLOAD_FOLDER, filename))
        print('file.xls  CREADO    ')
    rename_file = os.path.abspath('./project/data/catalog_data.xls')
    os.rename(os.path.abspath('./project/data/'+filename.replace(' ', '_')), rename_file)

def img_management(f, filename):
    print(f)
    print(filename)
    pass

def import_data():
    '''sistema de importacion de datos, convierte .xls en dataframe y lo vacia en DB'''
    for n in SHEET:
        datos = pd.read_excel(FILE_XLS, sheet_name=n)
        #creacion data frame
        df = pd.DataFrame(data=datos)

        #remplazar casillas vacias NULL con 0
        df = df.drop([0,1,2,3], axis=0)
        df = df.fillna(0)

        #df = df.assign(Categoria = '') asignar nueva columna categ
        if 0 == SHEET.index(n):
            df.rename(columns={'LISTA DE PRECIOS USY':'id', 'Unnamed: 1':'Disponibilidad', 
            'Unnamed: 2':'Transito', 'Unnamed: 3': 'Precio', 'Unnamed: 4':'Descuento', 
            'Unnamed: 5':'Precio_oferta', 'Unnamed: 6':'Descripcion', 'Unnamed: 7':'UM'}, inplace=True)
            df.to_sql('hoja1', con=engine, if_exists='replace', index=False)
        if 1 == SHEET.index(n):
            df.rename(columns={'LISTA DE PRECIOS MARCAS':'id', 'Unnamed: 1':'REF', 
            'Unnamed: 2':'Transito', 'Unnamed: 3':'Disponibilidad','Unnamed: 4':'Precio', 
            'Unnamed: 5':'Descuento', 'Unnamed: 6':'Precio_oferta', 'Unnamed: 7':'Descripcion', 
            'Unnamed: 8':'UM'}, inplace=True)
            df.to_sql('hoja2', con=engine, if_exists='replace', index=False)
        if 2 == SHEET.index(n):
            df.rename(columns={'LISTA DE PRECIOS  DIJONAS':'id', 'Unnamed: 1':'REF',
            'Unnamed: 2':'Disponibilidad', 'Unnamed: 3':'Transito', 'Unnamed: 4':'Precio', 
            'Unnamed: 5':'Descripcion', 'Unnamed: 6':'UM'}, inplace=True)
            df.to_sql('hoja3', con=engine, if_exists='replace', index=False)

    #hoja1 = engine.execute('SELECT * FROM hoja1 WHERE Disponibilidad > 0 OR Disponibilidad IS NULL').fetchall()
    return 


def render_file_pdf():

    return