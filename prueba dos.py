# 1. CLASE BASE (Empleado)
class Empleado:
    _id_counter: int = 1

    def __init__(self, nombre: str, salario_base: float):
        self.nombre: str = nombre
        self.id_empleado: int = Empleado._id_counter
        self.salario_base: float = salario_base
        self._proyectos_asignados: list = [] 
        self._limite_proyectos: int = 0
        Empleado._id_counter += 1

    def calcular_salario(self) -> float:
        return self.salario_base

    def mostrar_informacion(self) -> None:
        salario_final: float = self.calcular_salario()
        tipo: str = self.__class__.__name__
        
        print("[" + str(tipo) + "] " + str(self.nombre) +
              " | Proyectos: " + str(len(self._proyectos_asignados)) + 
              " | Salario Total: $" + str(salario_final))

    def asignar_proyecto(self, proyecto: 'Proyecto') -> bool:
        if len(self._proyectos_asignados) >= self._limite_proyectos:
            print("Error: Límite de proyectos (" + str(self._limite_proyectos) + ") alcanzado para " + self.nombre)
            return False
        
        if proyecto in self._proyectos_asignados:
            print("Error: " + self.nombre + " ya está en ese proyecto.")
            return False
        
        self._proyectos_asignados = self._proyectos_asignados + [proyecto]
        return True 


# 2. CLASES ESPECÍFICAS (Roles)
class Desarrollador(Empleado):
    def __init__(self, nombre: str, salario_base: float, nivel: str):
        super().__init__(nombre, salario_base)
        self.nivel: str = nivel
        self._limite_proyectos: int = 3
        self.bono_dev: float = 0.0

    def calcular_salario(self) -> float:
        if self.nivel == "Senior": self.bono_dev = 1000.0
        elif self.nivel == "SemiSenior": self.bono_dev = 500.0
        return self.salario_base + self.bono_dev

class Diseñador(Empleado):
    def __init__(self, nombre: str, salario_base: float, herramientas: list[str]):
        super().__init__(nombre, salario_base)
        self.herramientas: list[str] = herramientas
        self._limite_proyectos: int = 2

    def calcular_salario(self) -> float:
        bono: float = 0.0
        if "Figma" in self.herramientas: bono += 300.0
        return self.salario_base + bono

class Gerente(Empleado):
    def __init__(self, nombre: str, salario_base: float, departamento: str):
        super().__init__(nombre, salario_base)
        self.departamento: str = departamento
        self.equipo: list[Empleado] = []
        self._limite_proyectos: int = 0

    def agregar_al_equipo(self, empleado: Empleado) -> None:
        if isinstance(empleado, (Desarrollador, Diseñador)):
            self.equipo = self.equipo + [empleado]

    # El método ahora imprime el error y usa return
    def asignar_proyecto(self, proyecto: 'Proyecto') -> bool:
        print("Error: El Gerente solo supervisa y no puede ser miembro de un proyecto.")
        return False # Fallo en la asignación


# 3. CLASE PROYECTO
class Proyecto:
    def __init__(self, nombre: str, presupuesto: float):
        self.nombre: str = nombre
        self.presupuesto: float = float(presupuesto)
        self.empleados: list[Empleado] = []

    def agregar_empleado(self, empleado: Empleado) -> None:
        if empleado.asignar_proyecto(self):
            self.empleados = self.empleados + [empleado]
            print(str(empleado.nombre) + " agregado a " + str(self.nombre))

    def viabilidad(self) -> str:
        costo: float = 0.0
        for e in self.empleados:
            costo += e.calcular_salario()
            
        limite: float = self.presupuesto * 0.7
        
        print("   -> Costo: $" + str(costo) + " / Maximo: $" + str(limite))
        
        if costo <= limite:
            return "VIABLE"
        else:
            return "NO VIABLE"

## 4. PRUEBA DEL SISTEMA (EJECUCION FINAL)
def probar_sistema():
    print("\n=== 1. CREANDO EQUIPO ===")
    
    jefe: Gerente = Gerente("Diego Castillo", 3000.0, "IT")
    dev1: Desarrollador = Desarrollador("Ana Desarrolador", 2500.0, "Senior")
    dev2: Desarrollador = Desarrollador("Beto sarrolador", 1500.0, "Junior")
    dis1: Diseñador = Diseñador("Dina Diseñador", 2000.0, ["Figma", "PS"])

    jefe.agregar_al_equipo(dev1)
    jefe.agregar_al_equipo(dev2)
    jefe.agregar_al_equipo(dis1)
    
    print("--- Calculando salario del jefe (y su equipo)... ---")
    jefe.mostrar_informacion()


    print("\n=== 2. CREANDO 2 PROYECTOS CON PRESUPUESTO ===")
    p_grande: Proyecto = Proyecto("Proyecto Grande", 20000.0)
    p_chico: Proyecto = Proyecto("Proyecto Chico", 3000.0)


    print("\n=== 3. ASIGNANDO EMPLEADOS Y VIABILIDAD ===")
    p_grande.agregar_empleado(dev1)
    p_grande.agregar_empleado(dis1)
    print("Estado Grande: " + p_grande.viabilidad())

    p_chico.agregar_empleado(dev2) 
    p_chico.agregar_empleado(dev1) 
    print("Estado Chico: " + p_chico.viabilidad())


    print("\n=== 4. PROVOCANDO ERROR (4to PROYECTO) ===")
    p_relleno: Proyecto = Proyecto("Proyecto Relleno", 5000.0)
    p_relleno.agregar_empleado(dev1) 

    print("--- Intentando asignar el cuarto proyecto (Debe fallar) ---")
    p_error: Proyecto = Proyecto("Proyecto Imposible", 1000.0)
    p_error.agregar_empleado(dev1)

if __name__ == "__main__":
    probar_sistema()