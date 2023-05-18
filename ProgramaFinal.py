import tkinter as tk            #para tener un objeto de tkinter
from tkinter import *           #para usar todas las funciones que están en tkinter
from tkinter import messagebox  #para el mensaje de error
from tkinter import filedialog  #para el dialogo de archivos cuando cargemos una imagen 
import sqlite3                  #para usar bases de datos
import io                       #para entradas y salidas
from PIL import Image, ImageTk  #para reconstruir los binarios a imágenes
from tkinter import ttk         #para vista de los elementos en filas y columnas

def conectar_db():              #creamos la base de datos con las columnas y los tipos de campos
    db = sqlite3.connect("Almacen.db")
    datos = db.cursor()
    db.execute("""
                CREATE TABLE IF NOT EXISTS Medicamentos(
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Nombre VARCHAR, Descripcion VARCHAR,
                    Precio INTEGER, Imagen BLOB)
    """)
    db.commit()
    db.close()

def buscarImagen():                             #diálogo para buscar en los archivos de la computadora
    global getImagen
    getImagen = filedialog.askopenfilenames(initialdir = "/", title="Selecciona la imagen", filetypes=(("All files","*.*"),("png","*.png"),("jpg","*.jpg")))

def imagenABinario(filename):                   #convierte a binario la imagen
    with open(filename, 'rb') as file:
        imagen = file.read()
    return imagen

def get_medicamentos():                         #obtiene todo de la tabla medicamentos
    conexion = sqlite3.connect("Almacen.db")    
    cursor = conexion.cursor()
    registros_raw = cursor.execute("SELECT Id, Nombre, Descripcion, Precio FROM Medicamentos")
    registros_fetch = registros_raw.fetchall()
    global registros
    registros = registros_fetch
    cursor.close()

#función nueva-------
def buscarEnfermedad(sintoma): #busqueda de medicamento por imagenes utilizando LIKE 
    conexion = sqlite3.connect("Almacen.db")    
    cursor = conexion.cursor()
    registros_raw = cursor.execute("SELECT Id, Nombre, Descripcion, Precio FROM Medicamentos WHERE Descripcion LIKE '%" + sintoma + "%'")
    registros_fetch = registros_raw.fetchall()
    cursor.close()
    print(sintoma)
    actualiza_listado_sintomas(registros_fetch)
    

def actualiza_listado():                        #actualiza los registros cada vez que se añada uno nuevo
    registros_lb.delete(0, tk.END)
    get_medicamentos()
    for registro in registros:
        registros_lb.insert(tk.END, registro)
        
#función nueva------
def actualiza_listado_sintomas(registroList):
    registros_lb.delete(0, tk.END)
    for registro in registroList:
        registros_lb.insert(tk.END, registro)

def guardar_medicamento():                      #inserta los datos del formulario
    conexion = sqlite3.connect("Almacen.db")
    datos= conexion.cursor()
    if nombre.get() == "" or descripcion.get() == "" or precio.get() == "" :
        messagebox.showerror("Incompleto", "LLene todos los campos por favor")
        return
    print(nombre.get())
    print(descripcion.get())
    int_precio = int(precio.get())
    print(int_precio)

    for Imagen in getImagen:
        insertImg = imagenABinario(Imagen)
        datos.execute("INSERT INTO Medicamentos (Nombre, Descripcion, Precio, Imagen) VALUES (?,?,?,:Imagen)",
                   (nombre.get(), descripcion.get(), int_precio, insertImg))

    conexion.commit()
    conexion.close()
    ventana_nuevo.destroy()
    actualiza_listado()

def nuevo_medicamento():                                                #nueva ventana para insertar medicamentos
    ventana_nuevo_medicamento = tk.Toplevel(ventana)                    #jerarquía de la ventana
    ventana_nuevo_medicamento.title("Agregar medicamento")              #nombre de la ventana
    ventana_nuevo_medicamento.configure(bg="#FFF", pady=50, padx=50)    #color de fondo de la ventana nueva y proporciones
    ventana_nuevo_medicamento.grab_set()

    ancho_ventana = 500                                         #tamaño de la ventana
    alto_ventana = 300
    x_ventana=ventana.winfo_screenwidth()//2 - ancho_ventana // 2
    y_ventana=ventana.winfo_screenheight()//2 - alto_ventana // 2
    posicion=str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
    ventana_nuevo_medicamento.geometry(posicion)
    ventana_nuevo_medicamento.resizable(0,0)

    #campo nombre
    nombre_label = tk.Label(ventana_nuevo_medicamento, text="Nombre:")
    nombre_label.grid(row=0, column=0, padx=(10, 0))
    nombre_label.configure(bg="#FFF")

    nombre_entry = tk.Entry(ventana_nuevo_medicamento, justify=tk.CENTER)
    nombre_entry.grid(row=0, column=1, padx=(0, 10), pady=(10, 0))

    #campo descripción
    descripcion_label = tk.Label(ventana_nuevo_medicamento, text="Descripción:")
    descripcion_label.grid(row=1, column=0, padx=(10,0))
    descripcion_label.configure(bg="#FFF")

    descripcion_entry = tk.Entry(ventana_nuevo_medicamento, justify=tk.CENTER)
    descripcion_entry.grid(row=1, column=1, padx=(0, 10), pady=(10, 0))

    #campo precio
    precio_label = tk.Label(ventana_nuevo_medicamento, text="Precio:")
    precio_label.grid(row=2, column=0, padx=(10,0))
    precio_label.configure(bg="#FFF")

    precio_entry = tk.Entry(ventana_nuevo_medicamento, justify=tk.CENTER)
    precio_entry.grid(row=2, column=1, padx=(0, 10), pady=(10, 0))

    #campo imagen
    imagen_entry = tk.Button(ventana_nuevo_medicamento, text="Buscar imagen", command=buscarImagen)
    imagen_entry.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

    global nombre                                           #declaración de variables globales
    nombre = nombre_entry
    nombre.configure(width="50")
    global descripcion
    descripcion = descripcion_entry
    descripcion.configure(width="50")
    global precio
    precio = precio_entry
    precio.configure(width="50")
    global imagen
    imagen = imagen_entry
    imagen.configure(width="50")
    global ventana_nuevo
    ventana_nuevo = ventana_nuevo_medicamento

    #button para enviar datos
    submit_button1 = tk.Button(ventana_nuevo_medicamento, command=guardar_medicamento, text="Añadir", bg="#002D4F", fg="#fff", width="30")
    submit_button1.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

def verImagenes(imgID):                                              #nueva ventana para ver imagenes
    ventana_nueva_imagenes = tk.Toplevel(ventana)                    #jerarquía de la ventana
    ventana_nueva_imagenes.title("Ver imágenes")                     #nombre de la ventana
    ventana_nueva_imagenes.configure(bg="#FFF", padx=30, pady=30)    #color de fondo de la ventana nueva y proporciones
    ventana_nueva_imagenes.grab_set()

    ancho_ventana = 300                                         #tamaño de la ventana
    alto_ventana = 360
    x_ventana=ventana.winfo_screenwidth()//2 - ancho_ventana // 2
    y_ventana=ventana.winfo_screenheight()//2 - alto_ventana // 2
    posicion=str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
    ventana_nueva_imagenes.geometry(posicion)
    ventana_nueva_imagenes.resizable(0,0)

    global ventana_nueva
    ventana_nueva = ventana_nueva_imagenes

    conexion = sqlite3.connect("Almacen.db")        #consulta
    puntero = conexion.cursor()
    sql = "SELECT Imagen FROM Medicamentos WHERE Id=?"
    puntero.execute(sql,(imgID,))
    row = puntero.fetchone()
    puntero.close()
    conexion.close()

    if row is not None:     #comprobar que haya una imagen
        elemento = row[0]
        binary = Image.open(io.BytesIO(elemento))
        img = ImageTk.PhotoImage(binary)
        mostrar = tk.Label(ventana_nueva_imagenes, image=img, pady=0, padx=0)
        mostrar.configure(width=250, height=330, bg="#FFF")
    else:
        mostrar = tk.Label(ventana_nueva_imagenes, text="Imagen no disponible")
        mostrar.configure(bg="#FFF", fg="#000")

    mostrar.grid(row=0, column=0)   #posición de la imagen
    ventana.mainloop()              #ejecutar

#función modificada-----------
def verLista():                                             #mostrammos lo que hay en la bd cuando se escoge la opción correspondiente del menú
    #parte busqueda
    mensaje2 = tk.Label(ventana, text="Ingresa los sintomas")         #mensaje para el usuario
    mensaje2.pack(pady=5)

    recibir_sintomas = Entry(ventana, justify=tk.CENTER, width=30)                                      #recibimos el ID
    recibir_sintomas.pack(pady=0, padx=10)

    buscarSintoma = tk.Button(ventana, command=lambda: buscarEnfermedad(buscarSintomaTxt.get()), text="Buscar", bg="#002D4F", fg="#fff", width="10") #
    buscarSintoma.pack(pady=10, padx=3)

    refercarRegistros = tk.Button(ventana, command=lambda: actualiza_listado(), text="refrescar", bg="#002D4F", fg="#fff", width="10") #
    refercarRegistros.pack(pady=10, padx=3)

    #tabla de registros
    registros_lb.configure(justify=tk.CENTER, bg="#FFF", fg="#000", font="Arial 11", width=80)
    registros_lb.pack()

    mensaje = tk.Label(ventana, text="Ingresa el ID de la imagen que quieras ver")         #mensaje para el usuario
    mensaje.pack(pady=10)

    recibir_ID = Entry(ventana, justify=tk.CENTER)                                      #recibimos el ID
    recibir_ID.pack(pady=0, padx=10)

    valor=recibir_ID.get()  #recibir el valor del entry

    enviarID = tk.Button(ventana, command=lambda: verImagenes(recibir.get()), text="Aceptar", bg="#002D4F", fg="#fff", width="30") #enviamos el ID
    enviarID.pack(pady=10)
    
    global recibir
    recibir = recibir_ID
    global buscarSintomaTxt
    buscarSintomaTxt = recibir_sintomas
    

############################################################# MAIN ######################################################################
#main modificado-------
conectar_db()                                               #se hace la conexión
get_medicamentos()                                          #se hace select a la base de datos
ventana = tk.Tk()                                           #se crea una instancia de tkinter
ancho_ventana = 700                                         #tamaño de la ventana
alto_ventana =  600
x_ventana=ventana.winfo_screenwidth()//2 - ancho_ventana // 2
y_ventana=ventana.winfo_screenheight()//2 - alto_ventana // 2
posicion=str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
ventana.geometry(posicion)
ventana.resizable(0,0)
ventana.title("Examen 2")                                                                #nombre de la ventana
ventana.configure(bg="#F0F0F0")                                                          #color de fondo de la venta

#menú.
barra_menu = tk.Menu()                                      #se llama a la clase clase Menu
menu = tk.Menu(barra_menu, tearoff=False)                   #se crea un menú

#opciones del menú
barra_menu.add_cascade(menu=menu, label="Opciones")                                      #nombre del menú
menu.add_command(label="Agregar medicamento", command=nuevo_medicamento)                 #opción 1 del menú
menu.add_command(label="Consultar lista de medicamentos", command=verLista)              #opción 2 del menú
ventana.config(menu=barra_menu) #se añade el menú a la ventana

registros_lb = tk.Listbox(ventana)
for registro in registros:
    registros_lb.insert(tk.END, registro)

mensaje = tk.Label(ventana, text="¡Bienvenido!, pulsa en opciones para usar el programa" )       #texto de bienvenida
mensaje.pack(pady=20)                                                                            #altura del texto en la ventana
mensaje.configure(font=('Arial 14'))                                                             #fuente y tamaño del texto
ventana.mainloop()                                                                               #loop para ejecutar el programa
