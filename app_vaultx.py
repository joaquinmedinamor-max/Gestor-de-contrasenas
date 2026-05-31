import customtkinter as ctk
import tkinter.messagebox as messagebox
import motor_db

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VaultPasswordApp(ctk.CTk):
    def __init__(self):
        #Configuracion de fondo y tamaño de la ventana
        super().__init__(fg_color="#1E1E1E")
        self.title("VaultPassword")
        self.geometry("550x700")
        self.resizable(False, False)
        
        self.id_en_edicion = None

        #Títulos
        self.lbl_titulo = ctk.CTkLabel(self, text="VaultPassword 🔒", font=("Roboto", 32, "bold"), text_color="#ffffff")
        self.lbl_titulo.pack(pady=(35, 5))
        
        self.lbl_sub = ctk.CTkLabel(self, text="Gestor de credenciales local", text_color="#cbd5e1", font=("Arial", 14))
        self.lbl_sub.pack(pady=(0, 25))

        # RECTÁNGULO 1: FORMULARIO
        self.frame_form = ctk.CTkFrame(self, corner_radius=12, fg_color="#0f172a", border_width=1, border_color="#1e293b")
        self.frame_form.pack(pady=10, padx=35, fill="x")

        # Cajas de texto con un azul ligeramente más claro para resaltar
        self.entry_sitio = ctk.CTkEntry(self.frame_form, placeholder_text="Sitio Web (ej. linkedin.com)", width=320, height=35, fg_color="#1e293b", border_width=1, border_color="#334155")
        self.entry_sitio.pack(pady=(25, 10))

        self.entry_usuario = ctk.CTkEntry(self.frame_form, placeholder_text="Usuario o Correo", width=320, height=35, fg_color="#1e293b", border_width=1, border_color="#334155")
        self.entry_usuario.pack(pady=10)

        self.entry_password = ctk.CTkEntry(self.frame_form, placeholder_text="Contraseña", show="*", width=320, height=35, fg_color="#1e293b", border_width=1, border_color="#334155")
        self.entry_password.pack(pady=10)

        self.btn_guardar = ctk.CTkButton(self.frame_form, text="Guardar Credencial", command=self.procesar_datos, height=38, corner_radius=8)
        self.btn_guardar.pack(pady=(15, 10))

        self.lbl_mensaje = ctk.CTkLabel(self.frame_form, text="", font=("Arial", 12, "bold"))
        self.lbl_mensaje.pack(pady=(0, 15))

        # Botón Intermedio 
        self.btn_mostrar = ctk.CTkButton(self, text="Actualizar Base", command=self.mostrar_datos, fg_color="#0d9488", hover_color="#0f766e", corner_radius=8)
        self.btn_mostrar.pack(pady=10)

        # RECTÁNGULO 2: BÓVEDA (Color Azul Marino) 
        self.frame_resultados = ctk.CTkScrollableFrame(self, corner_radius=12, fg_color="#0f172a", border_width=1, border_color="#1e293b")
        self.frame_resultados.pack(pady=(0, 25), padx=35, fill="both", expand=True)
        
        self.mostrar_datos()

    #Lógica Unificada 
    def procesar_datos(self):
        sitio = self.entry_sitio.get()
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()

        if sitio and usuario and password:
            if self.id_en_edicion is None:
                exito, msj = motor_db.guardar_credencial(sitio, usuario, password)
                texto_exito = "¡Guardado de forma segura!"
            else:
                exito, msj = motor_db.actualizar_credencial(self.id_en_edicion, sitio, usuario, password)
                texto_exito = "¡Actualizado de forma segura!"

            if exito:
                self.lbl_mensaje.configure(text=texto_exito, text_color="#34d399")
                self.limpiar_formulario()
                self.mostrar_datos()
            else:
                self.lbl_mensaje.configure(text="Error en la operación", text_color="#f87171")
        else:
            self.lbl_mensaje.configure(text="Por favor llena todos los campos", text_color="#fbbf24")

    def limpiar_formulario(self):
        self.entry_sitio.delete(0, 'end')
        self.entry_usuario.delete(0, 'end')
        self.entry_password.delete(0, 'end')
        self.id_en_edicion = None
        self.btn_guardar.configure(text="Guardar Credencial", fg_color=["#3B8ED0", "#1F6AA5"]) 

    def preparar_edicion(self, id_registro, sitio, usuario, password):
        self.limpiar_formulario()
        self.id_en_edicion = id_registro
        
        self.entry_sitio.insert(0, sitio)
        self.entry_usuario.insert(0, usuario)
        self.entry_password.insert(0, password)
        
        self.btn_guardar.configure(text="Actualizar Credencial", fg_color="#d97706", hover_color="#b45309")
        self.lbl_mensaje.configure(text="Modificando registro...", text_color="#fbbf24")

    def mostrar_datos(self):
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()

        exito, datos = motor_db.obtener_credenciales()
        
        if exito:
            for dato in datos:
                
                tarjeta = ctk.CTkFrame(self.frame_resultados, corner_radius=8, fg_color="#1E1E1E", border_width=1, border_color="#334155")
                tarjeta.pack(fill="x", pady=5, padx=5)

                btn_eliminar = ctk.CTkButton(tarjeta, text="🗑️", width=40, fg_color="#ef4444", hover_color="#dc2626",
                                             command=lambda i=dato['id']: self.eliminar_registro(i))
                btn_eliminar.pack(side="right", padx=(5, 15), pady=10)
                
                btn_editar = ctk.CTkButton(tarjeta, text="✏️", width=40, fg_color="#f59e0b", hover_color="#d97706",
                                           command=lambda i=dato['id'], s=dato['sitio_web'], u=dato['usuario'], p=dato['password']: self.preparar_edicion(i, s, u, p))
                btn_editar.pack(side="right", padx=(5, 5), pady=10)

                btn_copiar = ctk.CTkButton(tarjeta, text="Copiar", width=80, fg_color="#4f46e5", hover_color="#4338ca",
                                           command=lambda p=dato['password']: self.copiar_clave(p))
                btn_copiar.pack(side="right", padx=(5, 5), pady=10)

                texto = f"🌐 {dato['sitio_web']}  |  👤 {dato['usuario']}  |  🔑 ******"
                lbl = ctk.CTkLabel(tarjeta, text=texto, font=("Consolas", 12), text_color="#f8fafc", anchor="w")
                lbl.pack(side="left", fill="x", expand=True, padx=15, pady=10)

    def copiar_clave(self, password):
        self.clipboard_clear()
        self.clipboard_append(password)
        self.lbl_mensaje.configure(text="¡Contraseña copiada al portapapeles!", text_color="#34d399")

    def eliminar_registro(self, id_registro):
        respuesta = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar esta credencial?\n\nEsta acción no se puede deshacer.")
        if respuesta:
            exito, msj = motor_db.eliminar_credencial(id_registro)
            if exito:
                self.lbl_mensaje.configure(text="Credencial eliminada", text_color="#ef4444")
                self.mostrar_datos()
                self.limpiar_formulario() 
            else:
                self.lbl_mensaje.configure(text="Error al eliminar", text_color="#f87171")

if __name__ == "__main__":
    motor_db.inicializar_base_datos()
    app = VaultPasswordApp()
    app.mainloop()