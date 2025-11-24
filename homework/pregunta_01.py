# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""
import zipfile
import os
import pandas as pd

def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


    """
    # Definir la ubicación del archivo comprimido
    archivo_zip = "files/input.zip"
    # Especificar el directorio donde se extraerán los contenidos
    directorio_destino = "input"

    # Comprobar si el archivo ZIP existe
    if not os.path.exists(archivo_zip):
        print(f"No se encuentra el archivo {archivo_zip}.")
        return

    # Extraer el contenido del archivo ZIP
    with zipfile.ZipFile(archivo_zip, 'r') as archivo_comprimido:
        archivo_comprimido.extractall(directorio_destino)


# Ejecutar la función para descomprimir el archivo
pregunta_01()

# Crear la carpeta de salida si no existe
directorio_salida = os.path.join('files', 'output')
if not os.path.exists(directorio_salida):
    os.makedirs(directorio_salida)

# Inicializar listas para almacenar frases y sentimientos de los datasets
frases_prueba = []
etiquetas_prueba = []
frases_entrenamiento = []
etiquetas_entrenamiento = []

# Definir las rutas base para las carpetas de 'test' y 'train'
directorio_prueba = os.path.join('input', 'input', 'test')
directorio_entrenamiento = os.path.join('input', 'input', 'train')

# Especificar los subdirectorios que contienen las frases etiquetadas
directorios_sentimiento = ['positive', 'negative', 'neutral']

# Procesar los archivos dentro de las carpetas de 'test'
for sentimiento in directorios_sentimiento:
    ruta_sentimiento = os.path.join(directorio_prueba, sentimiento)
    
    if not os.path.exists(ruta_sentimiento):
        print(f"El directorio {ruta_sentimiento} no se encuentra.")
        continue

    # Leer cada archivo de texto y añadir su contenido a las listas correspondientes
    for archivo in os.listdir(ruta_sentimiento):
        ruta_archivo = os.path.join(ruta_sentimiento, archivo)
        
        if os.path.isfile(ruta_archivo):
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo_txt:
                frase = archivo_txt.read().strip()
                
            frases_prueba.append(frase)
            etiquetas_prueba.append(sentimiento)

# Procesar los archivos dentro de las carpetas de 'train'
for sentimiento in directorios_sentimiento:
    ruta_sentimiento = os.path.join(directorio_entrenamiento, sentimiento)
    
    if not os.path.exists(ruta_sentimiento):
        print(f"El directorio {ruta_sentimiento} no se encuentra.")
        continue

    # Leer cada archivo de texto y agregar su contenido a las listas
    for archivo in os.listdir(ruta_sentimiento):
        ruta_archivo = os.path.join(ruta_sentimiento, archivo)
        
        if os.path.isfile(ruta_archivo):
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo_txt:
                frase = archivo_txt.read().strip()
                
            frases_entrenamiento.append(frase)
            etiquetas_entrenamiento.append(sentimiento)

# Crear DataFrames con las frases y etiquetas para 'test' y 'train'
data_prueba = pd.DataFrame({'phrase': frases_prueba, 'target': etiquetas_prueba})
data_entrenamiento = pd.DataFrame({'phrase': frases_entrenamiento, 'target': etiquetas_entrenamiento})

# Aleatorizar los datos
data_prueba = data_prueba.sample(frac=1, random_state=42).reset_index(drop=True)
data_entrenamiento = data_entrenamiento.sample(frac=1, random_state=42).reset_index(drop=True)

# Guardar los DataFrames como archivos CSV en el directorio de salida
data_prueba.to_csv(os.path.join(directorio_salida, "test_dataset.csv"), index=False)
data_entrenamiento.to_csv(os.path.join(directorio_salida, "train_dataset.csv"), index=False)

print("Los archivos 'train_dataset.csv' y 'test_dataset.csv' se han generado correctamente en la carpeta 'files/output'.")