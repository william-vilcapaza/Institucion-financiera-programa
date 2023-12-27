import numpy as np 
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

class Cliente:
    def _init_(self, tipo, tiempo_atencion):
        self.tipo = tipo
        self.tiempo_atencion = tiempo_atencion

def simular_atencion(n_ventanillas, n_clientes, listbox_llegada, listboxes_atendidos):
    tipos_clientes = ["Tarjeta", "Cuenta común", "VIP Persona", "Común Persona",
                      "VIP Jurídica", "Sin tarjeta", "Preferencial", "Mayores de 60", "Con deficiencia", "Necesidades especiales"]

    ventanillas_disponibles = list(range(1, n_ventanillas + 1))

    tiempo_simulacion = 480  # Tiempo en minutos de simulación (8 horas de trabajo)

    clientes = []

    for _ in range(n_clientes):
        tipo_cliente = random.choice(tipos_clientes)
        tiempo_atencion = np.random.uniform(2, 15)  # Tiempo de atención aleatorio entre 2 y 15 minutos
        clientes.append(Cliente(tipo_cliente, tiempo_atencion))

    tiempo_actual = 0
    clientes_en_espera = []

    while tiempo_actual < tiempo_simulacion:
        # Verificar si llega un nuevo cliente
        if random.random() < 0.2:  # Probabilidad de llegada de un nuevo cliente
            nuevo_cliente = random.choice(clientes)
            mensaje = f"Llega un nuevo cliente {nuevo_cliente.tipo}"
            listbox_llegada.insert(tk.END, mensaje)

            # Asignar una ventanilla disponible al cliente
            ventanilla_asignada = None
            for i, disponible in enumerate(ventanillas_disponibles):
                if disponible:
                    ventanilla_asignada = disponible 
                    ventanillas_disponibles[i] = 0
                    break

            if ventanilla_asignada is not None and ventanilla_asignada != 0:
                ventanillas_disponibles[ventanilla_asignada - 1] = ventanilla_asignada
                mensaje = f"Cliente {nuevo_cliente.tipo} atendido en ventanilla {ventanilla_asignada}"
                for listbox_atendidos in listboxes_atendidos:
                    listbox_atendidos.insert(tk.END, mensaje)
            else:
                mensaje = "No hay ventanillas disponibles. Cliente en espera."
                listbox_llegada.insert(tk.END, mensaje)
                clientes_en_espera.append(nuevo_cliente)

        tiempo_actual += 1
        
    

    mensaje = "Simulación finalizada\nClientes en espera:"
    listbox_llegada.insert(tk.END, mensaje)
    for cliente in clientes_en_espera:
        mensaje = f"Cliente {cliente.tipo} - Tiempo de atención: {cliente.tiempo_atencion:.2f} minutos"
        listbox_llegada.insert(tk.END, mensaje)


 
# Función para iniciar la simulación desde la interfaz
# Función para iniciar la simulación desde la interfaz
def iniciar_simulacion():
    num_ventanillas = int(ventanillas_entry.get())
    num_clientes = int(clientes_entry.get())
    
    # Crear un frame para los resultados de llegada
    frame_llegada = ttk.Frame(root, borderwidth=2, relief="solid")  # Añadir borde y resaltado
    frame_llegada.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
    
    # Crear un Label para el título de la llegada
    label_llegada = ttk.Label(frame_llegada, text="Clientes que llegan:")
    label_llegada.pack()

    # Crear un Listbox para mostrar los clientes que llegan
    listbox_llegada = tk.Listbox(frame_llegada)
    listbox_llegada.pack(expand=True, fill="both")
    root.columnconfigure(0, weight=1)

    # Crear frames para los resultados de atendidos
    frames_atendidos = []
    listboxes_atendidos = []

    for i in range(num_ventanillas):
        frame_atendidos = ttk.Frame(root, borderwidth=2, relief="solid")  # Añadir borde y resaltado
        frame_atendidos.grid(row=3, column=i+1, padx=10, pady=5, sticky="nsew")
    
        # Crear un Label para el título de atendidos
        label_atendidos = ttk.Label(frame_atendidos, text=f"Clientes atendidos en ventanilla {i+1}:")
        label_atendidos.pack()

        # Crear un Listbox para mostrar los clientes atendidos
        listbox_atendidos = tk.Listbox(frame_atendidos)
        listbox_atendidos.pack(expand=True, fill="both")

        frames_atendidos.append(frame_atendidos)
        listboxes_atendidos.append(listbox_atendidos)
        root.columnconfigure(i+1, weight=1)

    simular_atencion(num_ventanillas, num_clientes, listbox_llegada, listboxes_atendidos)


# Crear la interfaz gráfica principal
root = tk.Tk()
root.title("Simulación de Atención al Cliente")


# Crear widgets en la interfaz principal
ventanillas_label = ttk.Label(root, text="Número de ventanillas:")
ventanillas_entry = ttk.Entry(root)

clientes_label = ttk.Label(root, text="Número de clientes:")
clientes_entry = ttk.Entry(root)

iniciar_button = ttk.Button(root, text="Iniciar Simulación", command=iniciar_simulacion)

# Posicionar widgets en la interfaz principal
ventanillas_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
ventanillas_entry.grid(row=0, column=1, padx=10, pady=5)

clientes_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
clientes_entry.grid(row=1, column=1, padx=10, pady=5)

iniciar_button.grid(row=2, column=0, columnspan=2, pady=10)

# Iniciar el bucle principal de la interfaz
root.mainloop()