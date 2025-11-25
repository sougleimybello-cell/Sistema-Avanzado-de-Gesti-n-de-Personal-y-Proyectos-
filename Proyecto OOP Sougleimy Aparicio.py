import abc 
from typing import List

_Unico_ID: int = 1

class Empleado(abc.ABC):
    
    def __init__(self, nombre: str, salario_base: float):
        global _Unico_ID
        self.__nombre: str = nombre
        self.__id_empleado: int = _Unico_ID
        _Unico_ID = _Unico_ID + 1
        self.__salario_base: float = salario_base
        self._proyectos_asignados: List['Proyecto'] = [] 

    def nombre(self) -> str:
        return self.__nombre
    def id_empleado(self) -> int:
        return self.__id_empleado
    def salario_base(self) -> float:
        return self.__salario_base
    def get_num_proyectos(self) -> int:
        return len(self._proyectos_asignados)

    @abc.abstractmethod
    def calcular_salario(self) -> float:
        pass

    def mostrar_informacion(self) -> None:
        salario: float = self.calcular_salario()
        print("--- Empleado: " + self.nombre() + " (ID: " + str(self.id_empleado()) + ") ---")
        print("Salario Calculado: $" + "{:,.2f}".format(salario))
        print("Proyectos Asignados: " + str(self.get_num_proyectos()))

    def asignar_proyecto(self, proyecto: 'Proyecto') -> None:
        pass


class Proyecto:

    def __init__(self, nombre: str, presupuesto: float):
        self.nombre: str = nombre
        self.presupuesto: float = presupuesto
        self.empleados: List[Empleado] = []

    def agregar_empleado(self, empleado: Empleado) -> None:
        limite_proyectos: int = 0
        tipo_empleado: str = type(empleado).__name__
        
        if tipo_empleado == 'Desarrollador':
            limite_proyectos = 3
        elif tipo_empleado == 'Diseñador':
            limite_proyectos = 2
        elif tipo_empleado == 'Gerente':
            print("--- Error de Asignacion: " + empleado.nombre() + " (Gerente) no puede ser asignado a un proyecto como miembro. Solo como responsable.")
            return
        else:
            limite_proyectos = 3
            
        if empleado.get_num_proyectos() >= limite_proyectos:
            print("--- Error de Limite: " + empleado.nombre() + " (ID: " + str(empleado.id_empleado()) + ") ya esta en su limite de " + str(limite_proyectos) + " proyectos activos.")
            return

        if empleado in self.empleados:
            print("--- Error de Duplicado: " + empleado.nombre() + " ya esta asignado al proyecto '" + self.nombre + "'.")
            return

        self.empleados.append(empleado)
        empleado._proyectos_asignados.append(self)
        print("  " + empleado.nombre() + " ha sido asignado al proyecto '" + self.nombre + "'.")

    def costo_total(self) -> float:
        total: float = 0.0
        for e in self.empleados:
            total = total + e.calcular_salario()
        return total

    def viabilidad(self) -> bool:
        costo: float = self.costo_total()
        viable: bool = costo <= self.presupuesto * 0.7
        print("--- Viabilidad de Proyecto '" + self.nombre + "' ---")
        print("Presupuesto: $" + "{:,.2f}".format(self.presupuesto) + " | Costo Estimado: $" + "{:,.2f}".format(costo) + " | Limite (70%): $" + "{:,.2f}".format(self.presupuesto * 0.7))
        print("Viable: " + str(viable))
        return viable


class Desarrollador(Empleado):
    def __init__(self, nombre: str, salario_base: float, lenguajes: List[str], nivel: str):
        super().__init__(nombre, salario_base)
        self.lenguajes: List[str] = lenguajes 
        self.nivel: str = nivel 
        
    def calcular_salario(self) -> float:
        bono: float = 0.0
        if self.nivel == "Junior":
            bono = 200.0
        elif self.nivel == "SemiSenior":
            bono = 500.0
        elif self.nivel == "Senior":
            bono = 1000.0
        return self.salario_base() + bono
    
    def mostrar_informacion(self) -> None:
        super().mostrar_informacion()
        print("  Nivel: " + self.nivel + ", Lenguajes: " + ", ".join(self.lenguajes))


class Diseñador(Empleado):
    def __init__(self, nombre: str, salario_base: float, herramientas: List[str], especialidad: str):
        super().__init__(nombre, salario_base)
        self.herramientas: List[str] = herramientas 
        self.especialidad: str = especialidad 

    def calcular_salario(self) -> float:
        bono: float = 0.0
        usa_figma: bool = False
        if "Figma" in self.herramientas:
            usa_figma = True
            
        usa_photoshop_illustrator: bool = False
        for h in ["Photoshop", "Illustrator"]:
            if h in self.herramientas:
                usa_photoshop_illustrator = True
                break
                
        usa_tres_o_mas: bool = len(self.herramientas) >= 3

        if usa_figma:
            bono = bono + 300.0
        
        if not usa_figma and usa_photoshop_illustrator:
            bono = bono + 200.0
            
        if usa_tres_o_mas:
            bono = bono + 400.0

        return self.salario_base() + bono

    def mostrar_informacion(self) -> None:
        super().mostrar_informacion()
        print("  Especialidad: " + self.especialidad + ", Herramientas: " + ", ".join(self.herramientas))


class Gerente(Empleado):
    def __init__(self, nombre: str, salario_base: float, departamento: str):
        super().__init__(nombre, salario_base)
        self.departamento: str = departamento 
        self.equipo: List[Empleado] = [] 

    def agregar_al_equipo(self, empleado: Empleado) -> None:
        if not isinstance(empleado, (Desarrollador, Diseñador)):
            print("--- Error: El Gerente solo puede agregar Desarrolladores o Diseñadores. No se agrego a " + empleado.nombre())
            return
        self.equipo.append(empleado)
        print("  " + empleado.nombre() + " ha sido agregado al equipo del Gerente " + self.nombre())

    def calcular_salario(self) -> float:
        total_salarios_equipo: float = 0.0
        for e in self.equipo:
            total_salarios_equipo = total_salarios_equipo + e.calcular_salario()
            
        bono_equipo: float = total_salarios_equipo * 0.15
        return self.salario_base() + bono_equipo

    def mostrar_informacion(self) -> None:
        super().mostrar_informacion()
        print("  Departamento: " + self.departamento + ", Empleados a cargo: " + str(len(self.equipo)))
        print("  Bono por Equipo: $" + "{:,.2f}".format(self.calcular_salario() - self.salario_base()))


def procesar_empleados(lista_empleados: List[Empleado], titulo: str) -> None:
    print("")
    print("  " + titulo)
    for empleado in lista_empleados:
        empleado.mostrar_informacion()
    print("="*50)
    print("")

print("")
print("           SISTEMA AVANZADO DE GESTIÓN DE PERSONAL Y PROYECTOS")
print("")

dev_senior: Desarrollador = Desarrollador("Andres Senior", 4000.0, ["Python", "JS", "SQL"], "Senior")
dev_junior: Desarrollador = Desarrollador("Diego Junior", 2500.0, ["Java", "C#"], "Junior")
designer: Diseñador = Diseñador("Alucard Designer", 3000.0, ["Figma", "Photoshop", "Illustrator"], "UI")

manager: Gerente = Gerente("Diana Gerente", 5000.0, "Desarrollo de Producto")
manager.agregar_al_equipo(dev_senior)
manager.agregar_al_equipo(dev_junior)
manager.agregar_al_equipo(designer)

lista_todos_empleados: List[Empleado] = [manager, dev_senior, dev_junior, designer]

proyecto_a: Proyecto = Proyecto("Alfa", 50000.0)
proyecto_b: Proyecto = Proyecto("Omega", 20000.0)

procesar_empleados(lista_todos_empleados, "ESTADO INICIAL DE EMPLEADOS (0 PROYECTOS)")

print("--- ASIGNACIÓN DE PROYECTOS ---")

proyecto_a.agregar_empleado(dev_senior)
proyecto_a.agregar_empleado(dev_junior)
proyecto_a.agregar_empleado(designer)

proyecto_b.agregar_empleado(dev_senior)
proyecto_b.agregar_empleado(dev_junior)

proyecto_a.agregar_empleado(manager) 

procesar_empleados(lista_todos_empleados, "ESTADO FINAL DE EMPLEADOS (PROYECTOS ASIGNADOS)")


print("--- PRUEBA DE LÍMITES DE PROYECTOS ---")

dev_senior_p3: Proyecto = Proyecto("Proyecto 3", 10000.0)
dev_senior_p4: Proyecto = Proyecto("Proyecto 4", 10000.0) 

dev_senior_p3.agregar_empleado(dev_senior)

dev_senior_p4.agregar_empleado(dev_senior) 

print("")
print("--- ANÁLISIS DE VIABILIDAD ---")
proyecto_a.viabilidad()
proyecto_b.viabilidad()