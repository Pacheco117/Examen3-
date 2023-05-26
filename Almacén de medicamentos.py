import tkinter as tk            #para tener un objeto de tkinter
from tkinter import *           #para usar todas las funciones que están en tkinter
from tkinter import messagebox  #para el mensaje de error
from tkinter import filedialog  #para el dialogo de archivos cuando cargemos una imagen 
import sqlite3                  #para usar bases de datos
import io                       #para entradas y salidas
from PIL import Image, ImageTk  #para reconstruir los binarios a imágenes
import re                       #para expresiones regulares                   

def conectarDB():   #CONEXIÓN     
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

class agregarMedicamentos(tk.Frame):    #CLASE PARA AGREGAR MEDICAMENTOS
    def getMedicamentos(self):                        
        conexion = sqlite3.connect("Almacen.db")    
        cursor = conexion.cursor()
        registros_raw = cursor.execute("SELECT Id, Nombre, Descripcion, Precio FROM Medicamentos")
        registros_fetch = registros_raw.fetchall()
        global registros
        registros = registros_fetch
        cursor.close()
    
    def buscarImagen(self):                         
        global getImagen
        getImagen = filedialog.askopenfilenames(initialdir = "/", title="Selecciona la imagen", filetypes=(("All files","*.*"),("png","*.png"),("jpg","*.jpg")))

    def imagenABinario(self, filename):                   
        with open(filename, 'rb') as file:
            imagen = file.read()
        return imagen

    def actualizarListado(self):           
        registros_lb.delete(0, tk.END)
        self.getMedicamentos()
        for registro in registros:
            registros_lb.insert(tk.END, registro)

    def insertMedicamento(self):             
        conexion = sqlite3.connect("Almacen.db")
        datos = conexion.cursor()
        if nombre.get() == "" or descripcion.get() == "" or precio.get() == "" :
            messagebox.showerror("Incompleto", "LLene todos los campos por favor")
            return
        print(nombre.get())
        print(descripcion.get())
        int_precio = int(precio.get())
        print(int_precio)
        for Imagen in getImagen:
            insertImg = self.imagenABinario(Imagen)
            datos.execute("INSERT INTO Medicamentos (Nombre, Descripcion, Precio, Imagen) VALUES (?,?,?,:Imagen)",
                       (nombre.get(), descripcion.get(), int_precio, insertImg))
        conexion.commit()
        conexion.close()
        ventana_nuevo.destroy()
        self.actualizarListado()

    def nuevoMedicamento(self):                                              
        ventana_nuevo_medicamento = tk.Toplevel(ventanaPrincipal)                    
        ventana_nuevo_medicamento.title("Agregar medicamento")              
        ventana_nuevo_medicamento.configure(bg="#FFF", pady=50, padx=50)    
        ventana_nuevo_medicamento.grab_set()

        ancho_ventana = 500                                         
        alto_ventana = 300
        x_ventana=ventana_nuevo_medicamento.winfo_screenwidth()//2 - ancho_ventana // 2
        y_ventana=ventana_nuevo_medicamento.winfo_screenheight()//2 - alto_ventana // 2
        posicion=str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        ventana_nuevo_medicamento.geometry(posicion)
        ventana_nuevo_medicamento.resizable(0,0)

        nombre_label = tk.Label(ventana_nuevo_medicamento, text="Nombre:")
        nombre_label.grid(row=0, column=0, padx=(10, 0))
        nombre_label.configure(bg="#FFF")

        nombre_entry = tk.Entry(ventana_nuevo_medicamento, justify=tk.CENTER)
        nombre_entry.grid(row=0, column=1, padx=(0, 10), pady=(10, 0))

        descripcion_label = tk.Label(ventana_nuevo_medicamento, text="Descripción:")
        descripcion_label.grid(row=1, column=0, padx=(10,0))
        descripcion_label.configure(bg="#FFF")

        descripcion_entry = tk.Entry(ventana_nuevo_medicamento, justify=tk.CENTER)
        descripcion_entry.grid(row=1, column=1, padx=(0, 10), pady=(10, 0))

        precio_label = tk.Label(ventana_nuevo_medicamento, text="Precio:")
        precio_label.grid(row=2, column=0, padx=(10,0))
        precio_label.configure(bg="#FFF")

        precio_entry = tk.Entry(ventana_nuevo_medicamento, justify=tk.CENTER)
        precio_entry.grid(row=2, column=1, padx=(0, 10), pady=(10, 0))

        imagen_entry = tk.Button(ventana_nuevo_medicamento, text="Buscar imagen", command=self.buscarImagen)
        imagen_entry.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

        global nombre                                          
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

        submit_button1 = tk.Button(ventana_nuevo_medicamento, command=self.insertMedicamento, text="Añadir", bg="#002D4F", fg="#fff", width="30")
        submit_button1.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

class consultarMedicamentos(tk.Frame):  #CLASE PARA VER MEDICAMENTOS
    def getMedicamentos(self):                        
        conexion = sqlite3.connect("Almacen.db")    
        cursor = conexion.cursor()
        registros_raw = cursor.execute("SELECT Id, Nombre, Descripcion, Precio FROM Medicamentos")
        registros_fetch = registros_raw.fetchall()
        global registros
        registros = registros_fetch
        cursor.close()
    
    def actualizarListado(self):           
        registros_lb.delete(0, tk.END)
        self.getMedicamentos()
        for registro in registros:
            registros_lb.insert(tk.END, registro)

    def actualiza_listado_sintomas(self, registroList):   
        registros_lb.delete(0, tk.END)
        for registro in registroList:
            registros_lb.insert(tk.END, registro)

    def buscarEnfermedad(self, sintoma):  
        conexion = sqlite3.connect("Almacen.db")    
        cursor = conexion.cursor()
        registros_raw = cursor.execute("SELECT Id, Nombre, Descripcion, Precio FROM Medicamentos WHERE Descripcion LIKE '%" + sintoma + "%'")
        registros_fetch = registros_raw.fetchall()
        cursor.close()
        self.actualiza_listado_sintomas(registros_fetch)
    
    def verLista(self):                 
        mensaje1 = tk.Label(ventanaPrincipal, text="Ingresa los sintomas")        
        mensaje1.pack(pady=5)

        recibir_sintomas = Entry(ventanaPrincipal, justify=tk.CENTER, width=30)                  
        recibir_sintomas.pack(pady=0, padx=10)

        buscarSintoma = tk.Button(ventanaPrincipal, command=lambda: self.buscarEnfermedad(buscarSintomaTxt.get()), text="Filtrar", bg="#002D4F", fg="#FFF", width="10") 
        buscarSintoma.pack(pady=10, padx=3)

        refrescarRegistros = tk.Button(ventanaPrincipal, command=self.actualizarListado, text="Ver todo", bg="#002D4F", fg="#FFF", width="10") 
        refrescarRegistros.pack(pady=10, padx=3)

        registros_lb.configure(justify=tk.CENTER, bg="#FFF", fg="#000", font="Arial 12", width="80")
        registros_lb.pack()

        mensaje2 = tk.Label(ventanaPrincipal, text="Ingresa el ID del medicamento que quieras ver")        
        mensaje2.pack(pady=10)

        recibir_ID = Entry(ventanaPrincipal, justify=tk.CENTER)                                      
        recibir_ID.pack(pady=0, padx=10)

        valor=recibir_ID.get() 

        enviarID = tk.Button(ventanaPrincipal, command=lambda: self.verImagenes(recibir.get()), text="Aceptar", bg="#002D4F", fg="#FFF", width="30") 
        enviarID.pack(pady=10)
            
        global recibir
        recibir = recibir_ID
        global buscarSintomaTxt
        buscarSintomaTxt = recibir_sintomas

    def verImagenes(self, imgID):                                             
        ventana_nueva_imagenes = tk.Toplevel(ventanaPrincipal)                    
        ventana_nueva_imagenes.title("Ver medicamentos")                    
        ventana_nueva_imagenes.configure(bg="#FFF", padx=30, pady=30)
        ventana_nueva_imagenes.grab_set()

        ancho_ventana=300                 
        alto_ventana=500
        x_ventana=ventana_nueva_imagenes.winfo_screenwidth()//2 - ancho_ventana // 2
        y_ventana=ventana_nueva_imagenes.winfo_screenheight()//2 - alto_ventana // 2
        posicion=str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        ventana_nueva_imagenes.geometry(posicion)
        ventana_nueva_imagenes.resizable(0,0)

        global ventana_nueva
        ventana_nueva = ventana_nueva_imagenes

        conexion=sqlite3.connect("Almacen.db")    
        puntero=conexion.cursor()
        consulta1="SELECT Nombre FROM Medicamentos WHERE Id=?"
        puntero.execute(consulta1,(imgID,))
        nombre=puntero.fetchone()
        consulta2="SELECT Descripcion FROM Medicamentos WHERE Id=?"
        puntero.execute(consulta2,(imgID,))
        descripcion=puntero.fetchone()
        consulta3="SELECT Precio FROM Medicamentos WHERE Id=?"
        puntero.execute(consulta3,(imgID,))
        precio=puntero.fetchone()
        consulta4="SELECT Imagen FROM Medicamentos WHERE Id=?"
        puntero.execute(consulta4,(imgID,))
        imagen=puntero.fetchone()
        puntero.close()
        conexion.close()

        tup1=nombre    
        valor1=''.join(tup1)
        nombre_re=re.sub(r"[^a-zA-Z0-9 ]", "", valor1)

        nombreMedicamento_label=tk.Label(ventana_nueva_imagenes, text=nombre_re) 
        nombreMedicamento_label.config(font='Arial 12', fg="#000", bg="#FFF")
        nombreMedicamento_label.pack(pady=10)

        tup2=descripcion 
        valor2=''.join(tup2)
        descripcion_re=re.sub(r"[^a-zA-Z0-9 ]", "ñ", valor2)

        descripcionMedicamento_label=tk.Label(ventana_nueva_imagenes, text=descripcion_re) 
        descripcionMedicamento_label.config(font='Arial 12', fg="#000", bg="#FFF")
        descripcionMedicamento_label.pack(pady=10)

        precioMedicamento_label=tk.Label(ventana_nueva_imagenes, text=precio) 
        precioMedicamento_label.config(font='Arial 12', fg="#000", bg="#FFF")
        precioMedicamento_label.pack(pady=10)

        if imagen is not None:    
            elemento=imagen[0]
            binario=Image.open(io.BytesIO(elemento))
            img=ImageTk.PhotoImage(binario)
            mostrar=tk.Label(ventana_nueva_imagenes, image=img, pady=0, padx=0)
            mostrar.configure(width=220, height=300, bg="#FFFFFF")
            mostrar.place(x=10, y=150)
        else:
            mostrar = tk.Label(ventana_nueva_imagenes, text="Imagen no disponible")
            mostrar.configure(bg="#FFF", fg="#000")

        ventana_nueva_imagenes.mainloop()             

class aplicacion(tk.Frame): #PROGRAMA PRINCIPAL
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

########## MAIN ##########

ventanaPrincipal = tk.Tk()
ventanaPrincipal.title("Almacén de medicamentos")
ventanaPrincipal.configure(bg="#F0F0F0") 
ancho_ventana = 700                                       
alto_ventana = 500
x_ventana = ventanaPrincipal.winfo_screenwidth()//2 - ancho_ventana // 2
y_ventana = ventanaPrincipal.winfo_screenheight()//2 - alto_ventana // 2
posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
ventanaPrincipal.geometry(posicion)
ventanaPrincipal.resizable(0,0)

conectarDB()
agregar = agregarMedicamentos()
consultar = consultarMedicamentos()
consultar.getMedicamentos()

barra_menu = tk.Menu()                                      
menu = tk.Menu(barra_menu, tearoff=False)                

barra_menu.add_cascade(menu=menu, label="Opciones")                                     
menu.add_command(label="Agregar medicamento", command=agregar.nuevoMedicamento)            
menu.add_command(label="Consultar lista de medicamentos", command=consultar.verLista)             
ventanaPrincipal.config(menu=barra_menu) 

registros_lb = tk.Listbox(ventanaPrincipal)
for registro in registros:
    registros_lb.insert(tk.END, registro)

mensaje = tk.Label(ventanaPrincipal, text="¡Bienvenido!, pulsa en opciones para usar el programa", font='Arial 14')      
mensaje.pack(pady=10)                                                                                                                                    

app = aplicacion(master=ventanaPrincipal)
app.mainloop()
