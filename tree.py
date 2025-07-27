class Node:
    def __init__(self,value):
        self.value= value
        self.left:Node|None=None
        self.right:Node|None=None
        
class ExpressionTree:
    def __init__(self, expression:str):
        self.root=None
        self.expression = expression
        self.variables= set()
    

    def __parentesis_balance(self,expression:str=None)->bool:
        if expression is None:
            expression= self.expression
        balance=0
        for char in expression:
            if char == '(':
                balance +=1
            elif char == ')':
                balance-=1
                if balance < 0:
                    return False
        return balance ==0
    
    def __operator_priority(self, operator:str)->int:
        if operator in ['↔']:
            return 1
        elif operator in ['→']:
            return 2
        elif operator in ['∨']:
            return 3
        elif operator in ['∧']:
            return 4
        elif operator in ['¬']:
            return 5
        return 0
    
    def evaluate(self,variables:dict)->bool:
        if variables is None:
            variables={}
        missing_vars= self.variables-set(variables.keys())
        if missing_vars:
            raise ValueError(f"Faltan variables ")
        return self.__evaluate_node(self.root, variables)
    
    def __evaluate_node(self, node:Node|None,variables:dict)->bool:
        if node is None:
            return False
        if node.value in variables:
            return variables[node.value]
        
        # Si es un operador
        
        left_value= self.__evaluate_node(node.left,variables)
        right_value=self.__evaluate_node(node.right, variables)

        if node.value =='¬':
            return not left_value if node.left else not right_value  
        elif node.value =='∧':
            return left_value and right_value
        elif node.value =='∨':
            return left_value or right_value
        elif node.value=='→':
            return not left_value or right_value
        elif node.value == '↔':
            return left_value == right_value

    def build_tree(self):
        if not self.__parentesis_balance():
            raise ValueError("Expresión no balanceada")
        self.root = self.__build_tree(self.expression.replace(" ", ""))
    
    def __build_tree(self, expression:str)->Node|None:
         # Eliminar paréntesis exteriores redundantes
        while (len(expression) > 0 and
               expression[0] == '(' and
               expression[-1] == ')' and
               self.__parentesis_balance(expression[1:-1])):
            expression=expression[1:-1]
            
        if not expression:
            return None
        # buscamos el de menor prioridad que este fuera de los parentesis 
        min_priority=float('inf') #inicializa con el valor mas alto y luego el minimo se asigna durante el reccorrido 
        index=-1
        level=0
        for i, char in enumerate(expression):
            if char =='(':
                 level +=1
            elif char == ')':
                 level -=1
            elif level == 0 and char in ['↔', '→', '∨', '∧', '¬']:
                priority=self.__operator_priority(char)
                if priority<= min_priority:
                   min_priority=priority
                   index=i
        if index==-1:
            if len(expression)==1 and expression.isalpha(): # and expression.isalpha()
                self.variables.add(expression)
                return Node(expression)
            else:
                raise ValueError("expresion no valida")
        
        op = expression[index]
        # Operador unario ¬
        if op=='¬':
             right=self.__build_tree(expression[index+1:])
             node=Node(op)
             node.right=right
             return node
        else:
            left = self.__build_tree(expression[:index])
            right = self.__build_tree(expression[index+1:])
            node=Node(op)
            node.left=left
            node.right=right
            return node
        
    def inorder_expression(self, node: Node = None) -> str:
        if node is None:
            node = self.root
        if node is None:
            return ""
        if node.left is None and node.right is None:
            return str(node.value)
        if node.value == '¬':
            return f"{node.value}{self.inorder_expression(node.right)}"
        return f"({self.inorder_expression(node.left)}{node.value}{self.inorder_expression(node.right)})"

   

    
    
def Main():
    et = ExpressionTree("(p∧q)→(r∨¬s)")
    et.build_tree()
    print("Expresión en orden:", et.inorder_expression())
    resultado = et.evaluate({'p': True, 'q': False, 'r': True, 's': True})
    print("Resultado:", resultado)
    


if __name__ == "__main__":
    Main()


        