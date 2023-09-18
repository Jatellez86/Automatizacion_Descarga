# Importa las bibliotecas necesarias para la automatización del navegador con Selenium
# **********************************************************************************************
#  @Nombre: Boot descarga datos ReportSae
#  @Autor: Javier Tellez
#  @Fecha: 20230321
#  @Cambios:
#  @Ayudas:
# **********************************************************************************************
#----------------------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time 
import os
import shutil
from datetime import date
from datetime import datetime, timedelta
import pandas as pd   


# Definicion de variables ---------------------------------------------------------------------
driver = False
session_id = False
loginState = False
user = 'user_prueba'
password = 'pwd_prueba'

# Fechas a recorrer----------------------------------------------------------------------------

# Crear un objeto datetime para el primer día del año 2023 o cualquier otro
fecha = datetime(2023, 1, 1)

# Crear una lista para almacenar los días del año
dias_del_anio = []

# Obtener la fecha de ayer
ayer = datetime.now() - timedelta(days=1)

# Bucle para iterar a través de elementos o datos
# Iterar sobre los días restantes del año o rango de fechas hasta ayer
while fecha <= ayer:
    dias_del_anio.append(fecha.strftime("%d/%m/%Y"))
    fecha += timedelta(days=1)

# Crea o manipula DataFrames para almacenar y procesar datos
date_calendar = pd.DataFrame({'date': dias_del_anio})
date_calendar["date"] = pd.to_datetime(date_calendar["date"], format='%d/%m/%Y')

# lista de fechas en el directorio ------------------------------------------------------------

ruta = 'G:\\Unidades compartidas\\GM_OP_ANALISIS_DE_DATOS\\03 viajes_desglosados'

# Bucle para iterar a través de elementos o datos
archivos = [archivo for archivo in os.listdir(ruta) if 'viajes_desglosado_UF17.csv' in archivo]  # Obtener la lista de archivos en la ruta especificada

filenames = []
dates = []

# Bucle para iterar a través de elementos o datos
# Recorrer la lista de archivos y extraer la fecha y el nombre del archivo
for archivo in archivos:
    fecha = archivo[:8]  # Los primeros 8 caracteres del nombre del archivo corresponden a la fecha
    filenames.append(archivo)
    dates.append(pd.to_datetime(fecha, format='%Y%m%d').strftime('%d/%m/%Y'))  # Convertir la fecha al formato deseado

# Crea o manipula DataFrames para almacenar y procesar datos
# Crear el DataFrame con la información obtenida
df_alejandria_uf06 = pd.DataFrame({'date': dates, 'filename': filenames})
df_alejandria_uf06["date"] = pd.to_datetime(df_alejandria_uf06["date"], format='%d/%m/%Y')

# Crea o manipula DataFrames para almacenar y procesar datos
# Hacer la unión de los dos DataFrames por la columna "date"
directory_ready_uf06 = pd.merge(date_calendar, df_alejandria_uf06, on='date', how='left')

# Filtrar las fechas que están en date_calendar
df_filtrado_uf06 = directory_ready_uf06[directory_ready_uf06['filename'].isna()]
df_filtrado_uf06['date'] = pd.to_datetime(df_filtrado_uf06['date']).dt.strftime('%d/%m/%Y')

# Bucle para iterar a través de elementos o datos

for i in df_filtrado_uf06['date']:
    print(i)

# Configura el controlador del navegador para automatizar la interacción con la página web
#driver = webdriver.Chrome(executable_path=r"chromedriver.exe")
chromedriver = 'chromedriver.exe'

# Configura el controlador del navegador para automatizar la interacción con la página web
# Características en el Web Driver ------------------------------------------------------------
session_id = False
loginState = False
driver = False
options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# Functions -----------------------------------------------------------------------------------
def openBrowser():
    global session_id
    global loginState
    global driver    
    try:
        if session_id == False:        
            driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)
            driver.implicitly_wait(40)  # seconds
            driver.maximize_window()
            session_id = driver.session_id
        return True
    except Exception as e: 
        print(str(e))
        return False

# Logic --------------------------------------------------------------------------------
openBrowser()



# Introduce una demora para esperar que los elementos de la página se carguen
# pagina principal de reportsae
driver.get('http://10.50.128.91/ReportSAE/Account/Login.aspx?ReturnUrl=%2fReportSAE%2fDefault.aspx')
time.sleep(1)
# enviar llaves de usuario y contraseña

# Busca elementos en la página web utilizando sus atributos
driver.find_element('id','MainContent_LoginUser_UserName').send_keys(user)
time.sleep(1)
driver.find_element('id','MainContent_LoginUser_Password').send_keys(password)
time.sleep(1)
driver.find_element('id','MainContent_LoginUser_LoginButton').click()
time.sleep(1)

# Bucle para iterar a través de elementos o datos
for i in df_filtrado_uf06['date']:

    # Define la ruta del directorio donde se encuentran los archivos
    directorio = "C:\\Users\\javier.tellez\\Downloads"

    # Obtiene una lista con todos los archivos del directorio
    archivos = os.listdir(directorio)

# Bucle para iterar a través de elementos o datos
    # Recorre la lista de archivos y elimina cada uno de ellos
    for archivo in archivos:
        ruta_archivo = os.path.join(directorio, archivo)
        os.remove(ruta_archivo)

# Busca elementos en la página web utilizando sus atributos
    # descarga viaje desglosado
    driver.get("http://10.50.128.91/ReportSAE/Informes/InformeEstadisticas.aspx?informe=32")
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbSistema_Input').clear()
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbSistema_Input').send_keys('ZONAL')
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbSistema_Input').send_keys(Keys.ENTER)
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_dateInicio_dateInput').clear()
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_dateInicio_dateInput').send_keys(i)
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_dateFin_dateInput').clear()
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_dateFin_dateInput').send_keys(i)
    time.sleep(4)
    driver.find_element('xpath', '//*[@id="ctl00_MainContent_cmbLinea"]/div/div').click()
    time.sleep(3)
    driver.find_element('xpath', '//*[@id="ctl00_MainContent_cmbLinea"]/div/div/label/input').click()
    time.sleep(2)
    driver.find_element('xpath', '//*[@id="ctl00_MainContent_CheckTabla"]/span[1]').click()
    time.sleep(3)
    driver.find_element('id', 'ctl00_MainContent_btnver_input').click()
    time.sleep(2)
    driver.get("http://10.50.128.91/ReportSAE/Informes/VisorInformes.aspx")
    time.sleep(25)
    driver.execute_script("$find('ReportViewer1').exportReport('CSV');")
    time.sleep(2)
    driver.get("http://10.50.128.91/ReportSAE/Default.aspx")
    time.sleep(2)
    print("ok viaje desglosado")

# Busca elementos en la página web utilizando sus atributos
    # descarga acciones de regulacion
    driver.get("http://10.50.128.91/ReportSAE/Informes/InformeEstadisticas.aspx?informe=101")
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbSistema_Input').clear()
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbSistema_Input').send_keys('ZONAL')
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbSistema_Input').send_keys(Keys.ENTER)
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_dateFecha_dateInput').clear()
    time.sleep(8)
    driver.find_element('id','ctl00_MainContent_dateFecha_dateInput').send_keys(i)
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbInformes_Input').clear()
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbInformes_Input').send_keys('Tabla Acciones')
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbInformes_Input').send_keys(Keys.ENTER)
    time.sleep(2)
    driver.find_element('id', 'ctl00_MainContent_btnver_input').click()
    time.sleep(2)
    driver.get("http://10.50.128.91/ReportSAE/Informes/VisorInformes.aspx")
    time.sleep(20)
    driver.execute_script("$find('ReportViewer1').exportReport('CSV');")
    time.sleep(10)
    driver.get("http://10.50.128.91/ReportSAE/Default.aspx")
    time.sleep(1)
    print("ok acciones")

# Busca elementos en la página web utilizando sus atributos
    # descarga actividad de bus
    driver.get("http://10.50.128.91/ReportSAE/Informes/InformeEstadisticas.aspx?informe=42")
    time.sleep(4)
    driver.find_element('id','ctl00_MainContent_cmbSistema_Input').clear()
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbSistema_Input').send_keys('ZONAL')
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbSistema_Input').send_keys(Keys.ENTER)
    time.sleep(4)
    driver.find_element('id','ctl00_MainContent_dateFecha_dateInput').clear()
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_dateFecha_dateInput').send_keys(i)
    time.sleep(2)
    print("Elemento dia ok")
    clicks = driver.find_elements(By.XPATH, "//input[@class= 'rlbCheckAllItemsCheckBox']")
    for click in clicks:
        click = click.click()
    time.sleep(2)
    print("Doble check ok")
    driver.find_element('id','ctl00_MainContent_CheckTabla').click()
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_btnver_input').click()
    time.sleep(2)
    print("Boton carga visor ok")
    driver.get("http://10.50.128.91/ReportSAE/Informes/VisorInformes.aspx")
    time.sleep(40)
    print("Visor de Informes ok")
    driver.execute_script("$find('ReportViewer1').exportReport('CSV');")
    time.sleep(55)
    print("Descarga ok")
    driver.get("http://10.50.128.91/ReportSAE/Default.aspx")
    time.sleep(1)
    print("ok actividad de bus")

# Busca elementos en la página web utilizando sus atributos
    # descarga desvios
    driver.get("http://10.50.128.91/ReportSAE/Informes/InformeEstadisticas.aspx?informe=101")
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbSistema_Input').clear()
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbSistema_Input').send_keys('ZONAL')
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbSistema_Input').send_keys(Keys.ENTER)
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_dateFecha_dateInput').clear()
    time.sleep(8)
    driver.find_element('id','ctl00_MainContent_dateFecha_dateInput').send_keys(i)
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbInformes_Input').clear()
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbInformes_Input').send_keys('Tabla DesviosViaje')
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbInformes_Input').send_keys(Keys.ENTER)
    time.sleep(2)
    driver.find_element('id', 'ctl00_MainContent_btnver_input').click()
    time.sleep(2)
    driver.get("http://10.50.128.91/ReportSAE/Informes/VisorInformes.aspx")
    time.sleep(20)
    driver.execute_script("$find('ReportViewer1').exportReport('CSV');")
    time.sleep(10)
    driver.get("http://10.50.128.91/ReportSAE/Default.aspx")
    time.sleep(1)
    print("ok acciones")

# Introduce una demora para esperar que los elementos de la página se carguen
    time.sleep(3)
    driver.get("http://10.50.128.91/ReportSAE/Default.aspx")
    time.sleep(2)

# Busca elementos en la página web utilizando sus atributos
    # descarga iph
    driver.get("http://10.50.128.91/ReportSAE/Informes/InformeBase.aspx?informe=110")
    time.sleep(2)
    print('iph general')
    driver.find_element('id','ctl00_MainContent_cmbSistema_Input').clear()
    time.sleep(2)
    print('limpia zonal')
    driver.find_element('id','ctl00_MainContent_cmbSistema_Input').send_keys('ZONAL')
    time.sleep(2)
    print('ingresa zonal')
    driver.find_element('id','ctl00_MainContent_cmbSistema_Input').send_keys(Keys.ENTER)
    time.sleep(2)
    print('enter zonal')
    driver.find_element('xpath', '//*[@id="ctl00_MainContent_CheckFecha"]/span[1]').click()
    time.sleep(2)
    print('ok check')
    driver.find_element('xpath','//*[@id="ctl00_MainContent_ctl00_MainContent_dateFechaCheckPanel"]').click()
    time.sleep(2)
    print('ok contenedor')
    driver.find_element('id','ctl00_MainContent_dateFechaCheck_dateInput').send_keys(i)
    time.sleep(2)
    print('ok ingreso fechas')
    driver.find_element('xpath', '//*[@id="ctl00_MainContent_cmbJornada2"]/div').click()
    time.sleep(2)
    driver.find_element('xpath', '//*[@id="ctl00_MainContent_cmbJornada2"]/div/div/label/input').click()
    time.sleep(2)
    print('ok segun check')
    driver.find_element('id', 'ctl00_MainContent_btnver_input').click()
    time.sleep(2)
    print('ok ver informe')
    driver.get("http://10.50.128.91/ReportSAE/Informes/VisorInformes.aspx")
    time.sleep(25)
    driver.execute_script("$find('ReportViewer1').exportReport('CSV');")
    time.sleep(2)
    driver.get("http://10.50.128.91/ReportSAE/Default.aspx")
    time.sleep(1)
    print("ok iph")

# Busca elementos en la página web utilizando sus atributos

    # Matriz distancias
    driver.get('http://10.50.128.91/ReportSAE/Default.aspx')
    time.sleep(2)
    driver.get('http://10.50.128.91/ReportSAE/Informes/InformeEstadisticas.aspx?informe=108')
    time.sleep(2)
    driver.find_element('id', 'ctl00_MainContent_cmbSistema_Input').clear()
    time.sleep(2)
    driver.find_element('id', 'ctl00_MainContent_cmbSistema_Input').send_keys('ZONAL')
    time.sleep(2)
    driver.find_element('id', 'ctl00_MainContent_cmbSistema_Input').send_keys(Keys.ENTER)
    time.sleep(2)
    driver.find_element('id', 'ctl00_MainContent_dateFecha_dateInput').clear()
    time.sleep(2)
    driver.find_element('id', 'ctl00_MainContent_dateFecha_dateInput').send_keys(i)
    time.sleep(2)
    driver.find_element('xpath', '//*[@id="ctl00_MainContent_cmbLinea"]/div/div/label/input').click()
    time.sleep(2)
    driver.find_element('xpath', '//*[@id="ctl00_MainContent_cmbTipoServicio"]/div/div/label/input').click()
    time.sleep(2)
    driver.find_element('id', 'ctl00_MainContent_btnver_input').click()
    time.sleep(2)
    driver.get("http://10.50.128.91/ReportSAE/Informes/VisorInformes.aspx")
    time.sleep(15)
    driver.execute_script("$find('ReportViewer1').exportReport('CSV');")
    time.sleep(2)

    print("ok matriz")

    # descarga viajes stat

# Busca elementos en la página web utilizando sus atributos
    driver.get("http://10.50.128.91/ReportSAE/Informes/InformeEstadisticas.aspx?informe=101")
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbSistema_Input').clear()
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbSistema_Input').send_keys('ZONAL')
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbSistema_Input').send_keys(Keys.ENTER)
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_dateFecha_dateInput').clear()
    time.sleep(8)
    driver.find_element('id','ctl00_MainContent_dateFecha_dateInput').send_keys(i)
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbInformes_Input').clear()
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbInformes_Input').send_keys('Tabla IntervalosViajeStat')
    time.sleep(2)
    driver.find_element('id','ctl00_MainContent_cmbInformes_Input').send_keys(Keys.ENTER)
    time.sleep(2)
    driver.find_element('id', 'ctl00_MainContent_btnver_input').click()
    time.sleep(2)
    driver.get("http://10.50.128.91/ReportSAE/Informes/VisorInformes.aspx")
    time.sleep(20)
    driver.execute_script("$find('ReportViewer1').exportReport('CSV');")
    time.sleep(10)
    driver.get("http://10.50.128.91/ReportSAE/Default.aspx")
    time.sleep(1)
    print("ok viajes stat")





    fecha = datetime.strptime(i, "%d/%m/%Y")
    dia_ajus = fecha.strftime("%Y%m%d")

    files_to_copy = [
            {
                'download_path': 'C:\\Users\\javier.tellez\\Downloads\\Informe Viajes Desglosado.csv',
                'local_folder': 'G:\\Unidades compartidas\\GM_OP_ANALISIS_DE_DATOS\\03 viajes_desglosados',
                'prefix': dia_ajus,
                'suffix': '_viajes_desglosado_UF17.csv'
            },
            {
                'download_path': 'C:\\Users\\javier.tellez\\Downloads\\Tabla_Acciones.csv',
                'local_folder': 'G:\\Unidades compartidas\\GM_OP_ANALISIS_DE_DATOS\\05 acciones_regulacion',
                'prefix': dia_ajus,
                'suffix': '_acciones_regulacion_UF17.csv'
            },
            {
                'download_path': 'C:\\Users\\javier.tellez\\Downloads\\Informe_Diario_ActividadBus.csv',
                'local_folder': 'G:\\Unidades compartidas\\GM_OP_ANALISIS_DE_DATOS\\04 actividad_bus',
                'prefix': dia_ajus,
                'suffix': '_actividad_bus_UF17.csv'
            },
            {
                'download_path': 'C:\\Users\\javier.tellez\\Downloads\\Tabla_DesviosViaje.csv',
                'local_folder': 'G:\\Unidades compartidas\\GM_OP_ANALISIS_DE_DATOS\\07 desvios',
                'prefix': dia_ajus,
                'suffix': '_desvios_UF17.csv'
            },
            {
                'download_path': 'C:\\Users\\javier.tellez\\Downloads\\InformePlanificacionHorario.csv',
                'local_folder': 'G:\\Unidades compartidas\\GM_OP_ANALISIS_DE_DATOS\\08 iph',
                'prefix': dia_ajus,
                'suffix': '_iph_UF17.csv'
            },
            {
                'download_path': 'C:\\Users\\javier.tellez\\Downloads\\Informe Matriz de Distancias.csv',
                'local_folder': 'G:\\Unidades compartidas\\GM_OP_ANALISIS_DE_DATOS\\28 matriz_distancia',
                'prefix': dia_ajus,
                'suffix': '_matriz_distancia_UF17.csv'
            },
            {
                'download_path': 'C:\\Users\\javier.tellez\\Downloads\\Tabla_IntervalosViajeStat.csv',
                'local_folder': 'G:\\Unidades compartidas\\GM_OP_ANALISIS_DE_DATOS\\26 viajes_intervalo_stat',
                'prefix': dia_ajus,
                'suffix': '_stat_UF17.csv'
            }]

# Introduce una demora para esperar que los elementos de la página se carguen
    time.sleep(5)
        
    # ciclo para copiar los archivos en un nuevo directorio
    for file in files_to_copy:
        download_path = file['download_path']
        local_folder = file['local_folder']
        prefix = file['prefix']
        suffix = file['suffix']
        filename = prefix + suffix
        new_file_path = os.path.join(local_folder, filename)
        
        os.makedirs(local_folder, exist_ok=True)
        shutil.copy(download_path, new_file_path)
        os.remove(download_path)

driver.close()

print("proceso finalizado")
