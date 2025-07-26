import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import font as tkFont

class TruthTableGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Tablas de Verdad")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.expression = tk.StringVar()
        self.expression.trace('w', self.on_expression_change)
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        """Configurar estilos personalizados"""
        self.title_font = tkFont.Font(family="Arial", size=14, weight="bold")
        self.button_font = tkFont.Font(family="Arial", size=12)
        self.expression_font = tkFont.Font(family="Courier", size=12)
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid del root
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Generador de Tablas de Verdad", 
                               font=self.title_font)
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame para botones de variables
        var_frame = ttk.LabelFrame(main_frame, text="Variables Proposicionales", padding="10")
        var_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Botones de variables (p, q, r, s, t, u, v, w, x, y)
        variables = ['p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y']
        for i, var in enumerate(variables):
            btn = ttk.Button(var_frame, text=var, width=4,
                           command=lambda v=var: self.add_to_expression(v))
            btn.grid(row=i//5, column=i%5, padx=2, pady=2)
        
        # Frame para operadores lógicos
        op_frame = ttk.LabelFrame(main_frame, text="Operadores Lógicos", padding="10")
        op_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Definir operadores con sus símbolos y descripciones
        operators = [
            ('∧', 'AND'),
            ('∨', 'OR'), 
            ('¬', 'NOT'),
            ('→', 'Implicación'),
            ('↔', 'Bicondicional'),
            ('(', 'Parentesis izq.'),
            (')', 'Parentesis der.')
        ]
        
        for i, (symbol, desc) in enumerate(operators):
            btn = ttk.Button(op_frame, text=f"{symbol}\n{desc}", width=12,
                           command=lambda s=symbol: self.add_to_expression(s))
            btn.grid(row=i//4, column=i%4, padx=5, pady=5)
        
        # Frame para la expresión
        expr_frame = ttk.LabelFrame(main_frame, text="Expresión Lógica", padding="10")
        expr_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        expr_frame.columnconfigure(0, weight=1)
        
        # Entry para mostrar la expresión actual
        self.expression_entry = ttk.Entry(expr_frame, textvariable=self.expression, 
                                        font=self.expression_font, state='readonly')
        self.expression_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Botones de control de expresión
        control_frame = ttk.Frame(expr_frame)
        control_frame.grid(row=0, column=1)
        
        ttk.Button(control_frame, text="Limpiar", 
                  command=self.clear_expression).grid(row=0, column=0, padx=2)
        ttk.Button(control_frame, text="Deshacer", 
                  command=self.undo_last).grid(row=0, column=1, padx=2)
        
        # Entry manual para escribir expresion
        manual_frame = ttk.Frame(expr_frame)
        manual_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        manual_frame.columnconfigure(0, weight=1)
        
        # Frame para información de la expresión
        info_frame = ttk.LabelFrame(main_frame, text="Información", padding="10")
        info_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.info_label = ttk.Label(info_frame, text="Variables detectadas: Ninguna\nFilas en tabla: 0")
        self.info_label.grid(row=0, column=0, sticky=tk.W)
        
        # Botón para generar tabla
        generate_frame = ttk.Frame(main_frame)
        generate_frame.grid(row=5, column=0, columnspan=3, pady=(0, 10))
        
        self.generate_btn = ttk.Button(generate_frame, text="Generar Tabla de Verdad", 
                                     command=self.generate_truth_table,
                                     style='Accent.TButton')
        self.generate_btn.pack()
        
        # Frame para mostrar la tabla (placeholder por ahora)
        table_frame = ttk.LabelFrame(main_frame, text="Tabla de Verdad", padding="10")
        table_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        # ScrolledText para mostrar la tabla
        self.table_display = scrolledtext.ScrolledText(table_frame, height=15, width=80,
                                                      font=("Courier", 10), state='disabled')
        self.table_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Variables para historial
        self.expression_history = []
        
    def add_to_expression(self, symbol):
        current = self.expression.get()
        new_expression = current + symbol
        self.expression_history.append(current)
        self.expression.set(new_expression)
        
    def clear_expression(self):
        self.expression_history.append(self.expression.get())
        self.expression.set("")
        
    def undo_last(self):
        if self.expression_history:
            last_expression = self.expression_history.pop()
            self.expression.set(last_expression)
            
    def load_manual_expression(self, event=None):
        manual_text = self.manual_entry.get().strip()
        if manual_text:
            self.expression_history.append(self.expression.get())
            self.expression.set(manual_text)
            self.manual_entry.delete(0, tk.END)
            
    def on_expression_change(self, *args):
        expr = self.expression.get()
        variables = self.detect_variables(expr)
        num_vars = len(variables)
        num_rows = 2 ** num_vars if num_vars > 0 else 0
        
        var_text = ", ".join(sorted(variables)) if variables else "Ninguna"
        info_text = f"Variables detectadas: {var_text}\nFilas en tabla: {num_rows}"
        self.info_label.config(text=info_text)
        
        # Habilitar/deshabilitar botón de generar
        self.generate_btn.config(state='normal' if variables and num_vars <= 10 else 'disabled')
        
    def detect_variables(self, expression):
        variables = set()
        valid_vars = set('pqrstuvwxy')
        
        for char in expression:
            if char in valid_vars:
                variables.add(char)
                
        return variables
        
    def generate_truth_table(self):
        expr = self.expression.get().strip()
        if not expr:
            messagebox.showwarning("Advertencia", "Por favor ingrese una expresión lógica.")
            return
            
        variables = self.detect_variables(expr)
        if not variables:
            messagebox.showwarning("Advertencia", "No se detectaron variables en la expresión.")
            return
            
        if len(variables) > 10:
            messagebox.showerror("Error", "Máximo 10 variables permitidas.")
            return
            
        # Placeholder para la tabla
        self.table_display.config(state='normal')
        self.table_display.delete(1.0, tk.END)
        
        table_text = f"Expresión: {expr}\n"
        table_text += f"Variables: {', '.join(sorted(variables))}\n"
        table_text += "=" * 50 + "\n"
        table_text += "TABLA DE VERDAD (Funcionalidad pendiente)\n"
        table_text += "=" * 50 + "\n\n"
        table_text += "Aquí se mostrará la tabla de verdad generada\n"
        table_text += "una vez que implementes el árbol de expresiones\n"
        table_text += "y la lógica de evaluación."
        
        self.table_display.insert(1.0, table_text)
        self.table_display.config(state='disabled')
        
        messagebox.showinfo("Información", 
                          f"Tabla generada para la expresión: {expr}\n"
                          f"Variables: {', '.join(sorted(variables))}\n"
                          f"Combinaciones: {2**len(variables)}")

def main():
    root = tk.Tk()
    app = TruthTableGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()