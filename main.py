import mysql.connector # Conector de base de datos
from faker import Faker # Paquete que permite generar datos
import random # Vamos a utilizar el generador de numeros aleatorios
from dotenv import load_dotenv # Vamos a llamar a dotenv para leer el archivo .env
import os # Para poder leer los directorios de ejecución del script

# Cargar variables de entorno
load_dotenv()

# Conexion a base de datos mysql

mydb = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

cursor = mydb.cursor()

# Crear tabla agentes
# Si existe, continua.
cursor.execute('''
               CREATE TABLE IF NOT EXISTS agentes(
                   documento VARCHAR(10) PRIMARY KEY,
                   apellido_nombre VARCHAR(255),
                   sexo VARCHAR(20),
                   email VARCHAR(255),
                   ocupacion VARCHAR(255)
               )
               ''')

# Inicializar Faker en español
fake = Faker('es_ES')

# Variable acumuladora de documentos
# Aquí insertaremos todos los documentos generados.
documentos_insertados = set()

# Insertar 1 millón de registros
for i in range(1000000):
    while True:
        documento = str(random.randint(15000000,99999999))
        if documento not in documentos_insertados:
            documentos_insertados.add(documento)
            break
        
    sexo = fake.random_element(elements=('Masculino','Femenino'))
    apellido_nombre = fake.name()
    email = fake.email()
    ocupacion = fake.job()
    
    cursor.execute('''
                   INSERT INTO agentes (documento, apellido_nombre, sexo, email, ocupacion)
                   VALUES (%s, %s, %s, %s, %s)
                   ''', (documento, apellido_nombre, sexo, email, ocupacion))
    # Al pasarle a print el parámetro f, le estamos dando un formato, para acceder a la variable utilizamos {} llaves
    print(f"Documento: {documento} - Sexo: {sexo} - Apellido Nombre: {apellido_nombre} - Email: {email} - Ocupacion: {ocupacion}")
# Guardar los cambios en la base de datos y cerramos la conexion

mydb.commit()
mydb.close()

print("Base de datos creada y llenada con 1 millon de registros aleatorios")