# Definizioni di eccezioni specifiche

class EmptyStackException(Exception):
    pass

class VariableNotFoundException(Exception):
    """Eccezione sollevata quando una variabile non è trovata."""
    pass

class IndexOutOfBoundsException(Exception):
    """Eccezione sollevata quando un indice è fuori dai limiti dell'array."""
    pass

class InvalidVariableError(Exception):
    """Eccezione sollevata per variabili non valide."""
    pass

class Stack:

    def __init__(self):
        self.data = []

    def push(self, x):
        self.data.append(x)

    def pop(self):
        if self.data == []:
            raise EmptyStackException
        res = self.data[-1]
        self.data = self.data[0:-1]
        return res

    def __str__(self):
        return " ".join([str(s) for s in self.data])


class Expression:

    def __init__(self):
        raise NotImplementedError()


#La funzione from_program (Metodo di Classe) divide il testo in righe e token, 
#crea le espressioni appropriate e le impila su uno stack 
#per costruire un albero di espressioni, inoltre controlla che alla fine lo stack sia di dimensione 1.
#Prende in input:-   text   (stringa): il programma da analizzare.
#                - dispatch (dizionario): associa i token ai loro corrispondenti oggetti Expression.
#Restituisce un oggetto Expression che rappresenta il programma.
    
    @classmethod
    def from_program(cls, text, dispatch):
        stack = Stack()
        for riga in text.split('\n'):
            for token in riga.split(): # x alloc -> token = "x", token = "alloc"
                if token.isdigit():
                    stack.push(Constant(int(token)))
                elif token in dispatch: # dispatch[token] = Alloc
                    arity = dispatch[token].arity # -> Alloc.arity -> 1
                    if arity == 0:
                        args = []
                    else:
                        args = [stack.pop() for _ in range(arity)] # args = [Variabile("x")]
                    stack.push(dispatch[token](args)) # -> stack = [Alloc([Variabile("x")])]
                else:
                    stack.push(Variable(token)) # stack = [Variabile("x")]
        if len(stack.data) != 1:
            for elm in stack.data:
                print(elm)
            raise ValueError("Invalid expression")
        return stack.pop()

    def evaluate(self, env):
        raise NotImplementedError()


class MissingVariableException(Exception):
    pass


"--------------------------------------------------------------------------------------------"
#Ciascuna di queste classi rappresenta un tipo specifico di espressione.

class Variable(Expression):


    def __init__(self, name):
        self.name = name

    def evaluate(self, env):
        if self.name in env:
            return env[self.name]
            
        else:
            raise VariableNotFoundException(f"Variabile '{self.name}' non trovata")

    def __str__(self):
        return self.name



#class Alloc(Expression):
# Alloca una variabile con valore iniziale 0.
#    Input: args : un argomento (1 elemento).
#    Output: Valore 0 dopo l'allocazione.
    
class Alloc(Expression):
    arity = 1
    def __init__(self, args):
        self.var_name = args[0]

    def evaluate(self, env):
        if not isinstance(self.var_name, Variable) :
            raise InvalidVariableError(Exception)
        {Variable("x").name: 0}
        {"x": 0}
        env[self.var_name.name] = 0
        return 0

x = Alloc([Variable("x")])
x = Expression.from_program("x alloc", d)

x.evaluate({})


#class Valloc(Expression):
# Alloca un array con dimensione data da un'espressione.
#    Input: args : una tupla di argomenti (2 elementi: nome variabile, posizione dell'array che voglio definire).
#    Output: Valore 0 dopo l'allocazione.
class Valloc(Expression):
    arity = 2
    def __init__(self, args):
        self.size_expr = args[1]
        self.var_name = args[0]

    def evaluate(self, env):
        if not isinstance(self.var_name, Variable) :
            raise InvalidVariableError(Exception)
        size = self.size_expr.evaluate(env)
        lista = []
        for i in range(size):
            lista.append(0)
        env[self.var_name.name] = lista
        return 0
    
#class Setq(Expression):
# Assegna un valore ad una variabile esistente.
#   Input : Tupla di argomenti (2 elementi: nome variabile, il valore che si assegna alla variabile).
#   Output: Il valore assegnato.
class Setq(Expression):
    arity = 2
    def __init__(self,args):
        self.var_name = args[0]
        self.value_expr = args[1]

    def evaluate(self, env):
        if not isinstance(self.var_name, Variable) :
            raise InvalidVariableError(Exception)
        value = self.value_expr.evaluate(env)
        if self.var_name.name not in env:
            raise ValueError(f"La variabile non è presente nell'enviroment ({self.var_name.name})")
        if  isinstance(env[self.var_name.name], list):
            raise ValueError(f"Impossibile usare setq su un array ({self.var_name.name})")
        env[self.var_name.name] = value
        return value

#class Setv(Expression):
# Assegna un valore ad un elemento di un array.
#   Input : tupla di argomenti (3 elementi: nome variabile, dispatch ,espressione per il valore)
#   Output: Il valore assegnato.
class Setv(Expression):
    arity = 3
    def __init__(self, args):
        self.var_name = args[0]
        self.index_expr = args[1]
        self.value_expr = args[2]

    def evaluate(self, env):
        if not isinstance(self.var_name, Variable) :
            raise InvalidVariableError(Exception)
        index = self.index_expr.evaluate(env)
        value = self.value_expr.evaluate(env)
        if self.var_name.name not in env or not isinstance(env[self.var_name.name],list):
            raise VariableNotFoundException(f"Variabile non trovata o non è un array: {self.var_name}")
        if index < 0 or index >= len(env[self.var_name.name]):
            raise IndexOutOfBoundsException(f"Indice {index} fuori dai limiti per l'array {self.var_name}")
        env[self.var_name.name][index] = value
        return value

class Constant(Expression):

    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        return self.value

    def __str__(self):
        return str(self.value)


class Prog2(Expression):
    arity = 2
    def __init__(self, args):
        self.expr1 = args[0]
        self.expr2 = args[1]

    def evaluate(self, env):
        self.expr1.evaluate(env)
        return self.expr2.evaluate(env)

    def __str__(self):
        return f"(prog2 {self.expr1} {self.expr2})"

class Prog3(Expression):
    arity = 3
    def __init__(self, args):
        self.expr1 = args[0]
        self.expr2 = args[1]
        self.expr3 = args[2]

    def evaluate(self, env):
        self.expr1.evaluate(env)
        self.expr2.evaluate(env)
        return self.expr3.evaluate(env)

    def __str__(self):
        return f"(prog3 {self.expr1} {self.expr2} {self.expr3})"

class Prog4(Expression):
    arity = 4
    def __init__(self, args):
        self.expr1 = args[0]
        self.expr2 = args[1]
        self.expr3 = args[2]
        self.expr4 = args[3]

    def evaluate(self, env):
        self.expr1.evaluate(env)
        self.expr2.evaluate(env)
        self.expr3.evaluate(env)
        return self.expr4.evaluate(env)

    def __str__(self):
        return f"(prog4 {self.expr1} {self.expr2} {self.expr3} {self.expr4})"

class Operation(Expression):

    def __init__(self, args):
        self.args = args

    def evaluate(self, env):
        raise NotImplementedError()

    def op(self, *args):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

#class If(Expression):
# Esegue una espressione se una condizione è vera, altrimenti un'altra.
#   Input: tupla di argomenti(3 elementi: condizione, espressione se vera, espressione se falsa)
#   Output: Il risultato dell'espressione valutata.
    
class If(Expression):

    arity = 3

    def __init__(self, args):
        print(args[1])
        self.condition = args[0]
        self.if_yes = args[1]
        self.if_no = args[2]

    def evaluate(self, env):
        if self.condition.evaluate(env):
            return self.if_yes.evaluate(env)
        else:
            return self.if_no.evaluate(env)

    def __str__(self):
        return f"(if {self.condition} {self.if_yes} {self.if_no})"


#class While(Expression):
#Esegue ripetutamente un'espressione finché una condizione rimane vera.
#   Input: tupla di argomenti (2 elementi: condizione, espressione da ripetere).
#   Output: Valore 0 dopo l'esecuzione del ciclo.

class While(Expression):

    arity = 2

    def __init__(self, args):
        self.condition = args[0]
        self.expr = args[1]

    def evaluate(self, env):
        while self.condition.evaluate(env):
            self.expr.evaluate(env)
        return 0

    def __str__(self):
        return f"(while {self.condition} {self.expr})"


#class For(Expression):
# Esegue un'espressione per un intervallo specificato di valori.
#   Input: tupla di argomenti(4 elementi: nome variabile, inizio dell'espressione, fine dell'espressione, l'espressione da eseguire)
#   Output: Valore 0 dopo l'esecuzione del ciclo.

class For(Expression):
    
    arity = 4

    def __init__(self, args):
        self.var_name = args[0]
        self.start_expr = args[1]
        self.end_expr = args[2]
        self.body_expr = args[3]

    def evaluate(self, env):
        start = self.start_expr.evaluate(env)
        end = self.end_expr.evaluate(env)
        for i in range(start, end):
            env[self.var_name.name] = i
            self.body_expr.evaluate(env)
        return 0

    def __str__(self):
        return f"(for {self.start_expr} to {self.end_expr} {self.body_expr})"


class DefSub(Expression):

    arity = 2
    def __init__(self, args):
        self.var_name = args[0]
        self.expr = args[1]

    def evaluate(self, env):
        if not isinstance(self.var_name, Variable) :
            raise InvalidVariableError(Exception)
        # Associa l'espressione alla variabile senza valutarla
        env[self.var_name.name] = self.expr
        return 0

    def __str__(self):
        return f"(defsub {self.var_name} {self.expr})"

class Call(Expression):
    arity = 1
    def __init__(self, args):
        self.var_name = args[0]

    def evaluate(self, env):
        if not isinstance(self.var_name, Variable) :
            raise InvalidVariableError(Exception)
        if self.var_name.name in env:
            return env[self.var_name.name].evaluate(env)
        else:
            raise ValueError(f"Subroutine non trovata: {self.var_name}")

    def __str__(self):
        return f"(call {self.var_name})"

class Print(Expression):
    arity = 1
    def __init__(self, expr):
        self.expr = expr[0]

    def evaluate(self, env):
        result = self.expr.evaluate(env)
        print(result)
        return result

    def __str__(self):
        return f"(print {self.expr})"

class Nop(Expression):
    arity = 0
    def __init__(self, expr):
        pass
    def evaluate(self, env):
        return 0

    def __str__(self):
        return "(nop)"


"--------------------------------------------------------------------------------------------"




class BinaryOp(Operation):
    

 
    arity = 2  # Arity per operazioni binarie

    def op(self, x, y):
        raise NotImplementedError("Deve essere implementato nelle sottoclassi")

    def evaluate(self, env):
        # Implementazione specifica nella sottoclasse
        return self.op(self.args[0].evaluate(env), self.args[1].evaluate(env))

    def __str__(self):
        # Implementazione specifica nella sottoclasse
        raise NotImplementedError()



class UnaryOp(Operation):

    arity = 1  # Arity per operazioni unarie

    def op(self, x):
        raise NotImplementedError("Deve essere implementato nelle sottoclassi")

    def evaluate(self, env):
        # Implementazione specifica nella sottoclasse
         return self.op(self.args[0].evaluate(env))

    def __str__(self):
        # Implementazione specifica nella sottoclasse
        raise NotImplementedError()





"--------------------------------------------------------------------------------------------"



class Addition(BinaryOp):
    
    def op(self, x, y):
        return x + y

    def __str__(self):
        return f"(+ {self.args[0]} {self.args[1]})"




class Subtraction(BinaryOp):

    def op(self, x, y):
        return x - y
    
    def __str__(self):
        return f"(- {self.args[0]} {self.args[1]})"


class Division(BinaryOp):

    def op(self, x, y):
        return x / y

    def __str__(self):
        return f"(/ {self.args[0]} {self.args[1]})"


class Multiplication(BinaryOp):

    def op(self, x, y):
        return x * y

    def __str__(self):
        return f"(* {self.args[0]} {self.args[1]})"



class Power(BinaryOp):


    def op(self, x, y):
        return x ** y


    def __str__(self):
        return f"(** {self.args[0]}  {self.args[1]})"

class Modulus(BinaryOp):

    def op(self, x, y):
        return x % y

    
    def __str__(self):
        return f"(% {self.args[0]} {self.args[1]})"


class GreaterThan(BinaryOp):

    def op(self, x, y):
        return x > y

    def __str__(self):
        return f"(> {self.args[0]} {self.args[1]})"

class GreaterEqual(BinaryOp):

    def op(self, x, y):
        return x >= y


    def __str__(self):
        return f"(>= {self.args[0]} {self.args[1]})"

class Equal(BinaryOp):

    def op(self, x, y):
        return x == y

    def __str__(self):
        return f"(= {self.args[0]} {self.args[1]})"

class NotEqual(BinaryOp):

    def op(self, x, y):
        return x != y

    def __str__(self):
        return f"(!= {self.args[0]} {self.args[1]})"

class LessThan(BinaryOp):

    def op(self, x, y):
        return x < y

    def __str__(self):
        return f"(< {self.args[0]} {self.args[1]})"

class LessEqual(BinaryOp):

    def op(self, x, y):
        return x <= y

    def __str__(self):
        return f"(<= {self.args[0]} {self.args[1]})"


"--------------------------------------------------------------------------------------------"




class Reciprocal(UnaryOp):

    def op(self, x):
        return 1/x

    def __str__(self):
        return f"(1/ {self.args[0]})"



class AbsoluteValue(UnaryOp):

    def op(self, x):
        return abs(x)

    def __str__(self):
        return f"(abs{self.args[0]})"




"--------------------------------------------------------------------------------------------"


d = {"+": Addition, "*": Multiplication, "**": Power, "-": Subtraction,
     "/": Division, "%": Modulus, "1/": Reciprocal, "abs": AbsoluteValue,">": GreaterThan,
    ">=": GreaterEqual,"=": Equal,"!=": NotEqual,"<": LessThan,"<=": LessEqual,
    "alloc": Alloc,"valloc": Valloc,"setq": Setq,"setv": Setv,"prog2": Prog2,
    "prog3": Prog3,"prog4": Prog4, "if": If,"while": While,"for": For,"defsub": DefSub,
    "call": Call, "print": Print,"nop": Nop}

example = "v print i j * 1 i - 10 * 1 j - + v setv 11 1 j for 11 1 i for 100 v valloc prog3"

"x 1 + x setq x 10 > while x alloc prog2"
"v print i i * i v setv prog2 10 0 i for 10 v valloc prog2"
"x print f call x alloc x 4 + x setq f defsub prog4"
"nop i print i x % 0 = if 1000 2 i for 783 x setq x alloc prog3"
"nop x print prime if nop 0 0 != prime setq i x % 0 = if 1 x - 2 i for 0 0 = prime setq prime alloc prog4 100 2 x for"

"v print i j * 1 i - 10 * 1 j - + v setv 11 1 j for 11 1 i for 100 v valloc prog3"
"x print 1 3 x * + x setq 2 x / x setq 2 x % 0 = if prog2 1 x != while 50 x setq x alloc prog3"
e = Expression.from_program(example, d)
print(e)
res = e.evaluate({})

ciao = "x 1 +"
e = Expression.from_program(ciao)
ciao.evaluate({"x": 190})