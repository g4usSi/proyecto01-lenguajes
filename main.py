import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
import itertools

class TruthTableGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Tablas de Verdad")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        self.history_stack = []
        
        # Variables
        self.expression = tk.StringVar()
        self.expression.trace('w', self.on_expression_change)
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
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
        
        # Frame contenedor horizontal para variables y operadores
        h_frame = ttk.Frame(main_frame)
        h_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        h_frame.columnconfigure(0, weight=1)
        h_frame.columnconfigure(1, weight=1)

        # Frame para botones de variables
        var_frame = ttk.LabelFrame(h_frame, text="Variables Proposicionales", padding="10")
        var_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # Botones de variables (p, q, r, s, t, u, v, w, x, y)
        variables = ['p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y']
        for i, var in enumerate(variables):
            btn = ttk.Button(var_frame, text=var, width=4,
                           command=lambda v=var: self.add_to_expression(v))
            btn.grid(row=i//5, column=i%5, padx=2, pady=2)
        
        # Frame para operadores lógicos
        op_frame = ttk.LabelFrame(h_frame, text="Operadores Lógicos", padding="10")
        op_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Definir operadores con sus símbolos y descripciones
        operators = [
            ('∧', 'AND'),
            ('∨', 'OR'), 
            ('¬', 'NOT'),
            ('→', 'Condicional'),
            ('↔', 'Bicondicional'),
            ('(', 'Paréntesis izq.'),
            (')', 'Paréntesis der.')
        ]

        for i, (symbol, desc) in enumerate(operators):
            btn = ttk.Button(
                op_frame,
                text=f"{symbol} {desc}",   
                width=14,
                command=lambda s=symbol: self.add_to_expression(s)
            )
            btn.grid(row=i//4, column=i%4, padx=5, pady=5, sticky='ew')

        
        # Frame para la expresión
        expr_frame = ttk.LabelFrame(main_frame, text="Expresión Lógica", padding="10")
        expr_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        expr_frame.columnconfigure(0, weight=1)
        
        # Entry para mostrar la expresión actual
        self.expression_entry = ttk.Entry(
            expr_frame,
            textvariable=self.expression,
            font=self.expression_font,
            state='readonly',
            justify='center'
        )
        self.expression_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Botón de control de expresión
        ttk.Button(expr_frame, 
                   text="Limpiar", 
                  command=self.clear_expression).grid(row=0, column=1, padx=10)
        
        ttk.Button(expr_frame, 
            text="Deshacer", 
            command=self.undo_expression).grid(row=0, column=2, padx=5)
        
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
        
        # Frame para mostrar la tabla usando Treeview
        table_frame = ttk.LabelFrame(main_frame, text="Tabla de Verdad", padding="10")
        table_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        # Frame para contener el Treeview y scrollbars
        tree_container = ttk.Frame(table_frame)
        tree_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_container.columnconfigure(0, weight=1)
        tree_container.rowconfigure(0, weight=1)
        
        # Crear Treeview para la tabla
        self.tree = ttk.Treeview(tree_container, show='headings')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid del Treeview y scrollbars
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
    def add_to_expression(self, symbol):
        current = self.expression.get()
        new_expression = current + symbol
        self.expression.set(new_expression)
        
    def clear_expression(self):
        self.expression.set("")
        # También limpiar la tabla si existe
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Limpiar las columnas del treeview
        self.tree['columns'] = ()
        print("Expresión limpiada")  # Para debug

    def undo_expression(self):
        if len(self.history_stack) > 1:
            self.history_stack.pop()  
            last_expr = self.history_stack[-1]
            self.expression.set(last_expr)
        elif self.history_stack:
            self.expression.set("")  
            self.history_stack.clear()
            
            
    def on_expression_change(self, *args):
        expr = self.expression.get()

        if not self.history_stack or self.history_stack[-1] != expr:
            self.history_stack.append(expr)

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
        
        try:
            from tree import ExpressionTree
            tree = ExpressionTree(expr)
            tree.build_tree()
            
            detected_vars = sorted(variables)
            tree_vars = sorted(tree.variables)
            
            if detected_vars != tree_vars:
                messagebox.showwarning("Advertencia", 
                    f"Variables detectadas: {detected_vars}\n"
                    f"Variables en árbol: {tree_vars}")
            
            var_list = sorted(tree.variables)
            combinations = list(itertools.product([False, True], repeat=len(var_list)))
            
            # Limpiar tabla anterior
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Configurar columnas
            columns = var_list + ['Resultado']
            self.tree['columns'] = columns
            
            # Configurar encabezados
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=80, anchor='center')
            
            # Generar filas de la tabla
            for i, combination in enumerate(combinations):
                # Crear diccionario de variables para esta combinación
                var_dict = dict(zip(var_list, combination))
                
                # Evaluar la expresión
                result = tree.evaluate(var_dict)
                
                # Convertir valores booleanos a V/F para mostrar
                row_values = []
                for var in var_list:
                    row_values.append('V' if var_dict[var] else 'F')
                row_values.append('V' if result else 'F')
                
                # Insertar fila en el Treeview
                self.tree.insert('', 'end', values=row_values)
            
            # Actualizar el frame de información
            info_text = f"Variables: {', '.join(var_list)}\n"
            info_text += f"Filas generadas: {len(combinations)}\n"
            info_text += f"Expresión evaluada: {tree.inorder_expression()}"
            
        except Exception as e:
            messagebox.showerror("Error", 
                f"Error al generar la tabla de verdad:\n\n{str(e)}\n\n"
                f"Verifique que la expresión esté bien formada.\n"
                f"Ejemplo valido: [ p ∧ q ∨ ¬r ]" )
            print(f"Error detallado: {e}")  # Para debug

def main():
    root = tk.Tk()
    app = TruthTableGUI(root)
    root.mainloop()





main()