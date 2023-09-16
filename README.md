# ReportSAE Data Scraper - UF17

## Descripción

Este script de Python automatiza la tarea de descargar varios informes del sistema ReportSAE. Está diseñado específicamente para la UF17 y utiliza la biblioteca Selenium para interactuar con la interfaz web del sistema.

## Dependencias

- Selenium
- Pandas
- Datetime

## Funcionamiento General

1. **Inicialización**: Importa todas las bibliotecas necesarias y define las variables iniciales como las credenciales de inicio de sesión y las fechas a iterar.
2. **Preparación de Fechas**: Crea un DataFrame con las fechas que aún no se han descargado.
3. **Automatización del Navegador**: Utiliza Selenium para automatizar un navegador web y realizar las acciones necesarias para descargar los informes.
4. **Descarga de Informes**: Descarga varios informes como 'Viajes Desglosados', 'Acciones de Regulación', 'Actividad de Bus', entre otros, para las fechas especificadas.
5. **Almacenamiento de Datos**: Mueve los archivos descargados a las ubicaciones de almacenamiento especificadas y los renombra de acuerdo con un patrón determinado.

## Uso

1. Asegúrese de tener todas las bibliotecas necesarias instaladas.
2. Actualice las variables como las credenciales de inicio de sesión y la ruta del almacenamiento, si es necesario.
3. Ejecute el script.

## Autores

- Javier Tellez

## Fecha

- 21 de marzo de 2023


