\"""Componentes reutilizables para la interfaz gráfica.

Este módulo contiene componentes de UI reutilizables para mantener
la consistencia visual en toda la aplicación.
"""
import customtkinter as ctk
from tkinter import filedialog
import os

class AppTitle(ctk.CTkLabel):
    """Componente de título de aplicación reutilizable."""
    
    def __init__(self, parent, text, **kwargs):
        """Inicializar componente de título.
        
        Args:
            parent: Widget padre
            text: Texto del título
            **kwargs: Argumentos adicionales para CTkLabel
        """
        font = kwargs.pop('font', ctk.CTkFont(size=20, weight="bold"))
        super().__init__(parent, text=text, font=font, **kwargs)

class AppFooter(ctk.CTkFrame):
    """Componente de pie de página reutilizable."""
    
    def __init__(self, parent, **kwargs):
        """Inicializar componente de pie de página.
        
        Args:
            parent: Widget padre
            **kwargs: Argumentos adicionales para CTkFrame
        """
        fg_color = kwargs.pop('fg_color', "transparent")
        super().__init__(parent, fg_color=fg_color, **kwargs)
        
        # First line: Developer and year
        self.credits_line1 = ctk.CTkLabel(
            self,
            text="Desarrollado por: Luis Fernando Moreno Montoya | 2024",
            font=ctk.CTkFont(size=13),
            text_color="#CCCCCC"
        )
        self.credits_line1.pack(pady=(10, 3))
        
        # Second line: Special message (split for heart color)
        self.message_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.message_frame.pack(pady=(3, 10))

        # First part of message
        self.part1 = ctk.CTkLabel(
            self.message_frame,
            text="Hecho con ",
            font=ctk.CTkFont(size=13),
            text_color="#CCCCCC"
        )
        self.part1.pack(side="left")

        # Red heart
        self.heart = ctk.CTkLabel(
            self.message_frame,
            text="♥",
            font=ctk.CTkFont(size=13),
            text_color="#FF0000"
        )
        self.heart.pack(side="left")

        # Last part of message
        self.part2 = ctk.CTkLabel(
            self.message_frame,
            text=" para PromiTierra",
            font=ctk.CTkFont(size=13),
            text_color="#CCCCCC"
        )
        self.part2.pack(side="left")

class ProgressBarComponent(ctk.CTkFrame):
    """Componente de barra de progreso reutilizable."""
    
    def __init__(self, parent, **kwargs):
        """Inicializar componente de barra de progreso.
        
        Args:
            parent: Widget padre
            **kwargs: Argumentos adicionales para CTkFrame
        """
        super().__init__(parent, **kwargs)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        self.progress_bar.set(0)
        
        # Progress label
        self.progress_label = ctk.CTkLabel(self, text="0%")
        self.progress_label.pack(pady=5)
        
    def update_progress(self, value, text=None):
        """Actualizar valor de la barra de progreso.
        
        Args:
            value: Valor de progreso (0-1)
            text: Texto opcional para mostrar (si es None, muestra porcentaje)
        """
        self.progress_bar.set(value)
        
        if text is None:
            # Convertir a porcentaje
            percentage = int(value * 100)
            self.progress_label.configure(text=f"{percentage}%")
        else:
            self.progress_label.configure(text=text)

class FileSelector(ctk.CTkFrame):
    """Componente de selección de archivos reutilizable."""
    
    def __init__(self, parent, button_text="Seleccionar Archivo", 
                 file_types=None, select_folder=False, command=None, **kwargs):
        """Inicializar componente de selección de archivos.
        
        Args:
            parent: Widget padre
            button_text: Texto del botón
            file_types: Tipos de archivo permitidos
            select_folder: Si es True, selecciona carpetas en lugar de archivos
            command: Función a ejecutar cuando se selecciona un archivo
            **kwargs: Argumentos adicionales para CTkFrame
        """
        super().__init__(parent, **kwargs)
        
        self.file_types = file_types
        self.select_folder = select_folder
        self.selected_path = None
        self.callback = command
        
        # Button
        icon = "📁 " if select_folder else "📄 "
        self.select_button = ctk.CTkButton(
            self,
            text=f"{icon}{button_text}",
            command=self._select_path
        )
        self.select_button.pack(pady=10)
        
    def _select_path(self):
        """Abrir diálogo de selección de archivo o carpeta."""
        if self.select_folder:
            path = filedialog.askdirectory()
        else:
            path = filedialog.askopenfilename(filetypes=self.file_types)
            
        if path:
            self.selected_path = path
            if self.callback:
                self.callback(path)
                
    def get_selected_path(self):
        """Obtener ruta seleccionada.
        
        Returns:
            str: Ruta seleccionada o None si no hay selección
        """
        return self.selected_path