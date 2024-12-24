"""
Progress dialog module for showing conversion progress.
"""
import tkinter as tk
import customtkinter as ctk

class ProgressDialog(ctk.CTkToplevel):
    """Dialog showing conversion progress."""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self._setup_window()
        self._create_widgets()
        
    def _setup_window(self):
        """Configure dialog window properties."""
        self.title("Progreso")
        self.geometry("300x150")
        self.resizable(False, False)
        
        # Center on parent
        self.transient(self.master)
        self.grab_set()
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
    def _create_widgets(self):
        """Create and configure dialog widgets."""
        # Progress label
        self.progress_label = ctk.CTkLabel(
            self,
            text="Procesando archivos..."
        )
        self.progress_label.grid(row=0, column=0, padx=10, pady=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.progress_bar.set(0)
        
        # Cancel button
        self.cancel_btn = ctk.CTkButton(
            self,
            text="Cancelar",
            command=self.master.pdf_converter.cancel_conversion
        )
        self.cancel_btn.grid(row=2, column=0, padx=10, pady=10)
        
    def update_progress(self, current: int, total: int):
        """Update progress bar and label."""
        progress = current / total if total > 0 else 0
        self.progress_bar.set(progress)
        self.progress_label.configure(
            text=f"Procesando archivo {current} de {total}..."
        )
        self.update()
        
    def show(self):
        """Show dialog and center on parent."""
        self.deiconify()
        self.focus_set()
        
        # Center on parent
        x = self.master.winfo_x() + (self.master.winfo_width() - self.winfo_width()) // 2
        y = self.master.winfo_y() + (self.master.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
        
    def hide(self):
        """Hide dialog."""
        self.withdraw()
