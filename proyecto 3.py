from abc import ABC, abstractmethod # para imponer reglas en tus clases

# Variable global para generar IDs únicos automáticamente
identificador_unico = 1

# 1. Clase base abstracta Empleado
class Empleado(ABC):
    """Clase base abstracta para todos los empleados de la empresa."""
    
    def __init__(self, nombre_completo: str, salario_base_mensual: float):
        global identificador_unico
        # Atributos privados (Encapsulamiento)
        self.__nombre_completo = nombre_completo
        self.__identificador_empleado = identificador_unico
        self.__salario_base_mensual = salario_base_mensual
        self.__proyectos_activos = [] # Lista de objetos Proyecto
        identificador_unico += 1

    def obtener_nombre(self):
        return self.__nombre_completo

    def obtener_id_empleado(self):
        return self.__identificador_empleado

    def obtener_salario_base(self):
        return self.__salario_base_mensual

    def obtener_proyectos_activos(self):
        return self.__proyectos_activos

    nombre = property(obtener_nombre)
    id_empleado = property(obtener_id_empleado)
    salario_base = property(obtener_salario_base)
    proyectos_activos = property(obtener_proyectos_activos)


    # DEBE ser implementado por las subclases (sin @abstractmethod)
    def calcular_salario(self) -> float:
        """Calcula el salario total, implementado de forma polimórfica."""
        if type(self) is Empleado:
            print("⚠️ Error: calcular_salario debe ser implementado en la subclase.")
            return 0.0
        pass
    
    # Método para definir el límite de proyectos por rol
    def _limite_proyectos(self):
        """Límite por defecto según el requisito general."""
        return 3

    def mostrar_informacion(self):
        """Muestra la información básica del empleado y su salario calculado."""
        salario_final = self.calcular_salario()
        print("   > Nombre: " + self.__nombre_completo)
        print("   > ID: " + str(self.__identificador_empleado))
        # SIN .format()
        print("   > Salario Base: $" + str(round(self.__salario_base_mensual, 2)))
        print("   > Salario Calculado: $" + str(round(salario_final, 2)))

    def asignar_proyecto(self, proyecto):
        """Agrega el empleado a un proyecto, verificando el límite y restricciones."""
        limite = self._limite_proyectos()
        
        # Restricción para Gerente
        if isinstance(self, Gerente):
            print("Error: El Gerente " + self.nombre + " no puede ser asignado a un proyecto como miembro.")
            return False

        # Restricción por límite
        if len(self.__proyectos_activos) >= limite:
            print("Error: " + self.nombre + " ya está en su límite de " + str(limite) + " proyectos activos.")
            return False
        
        # Asignación
        if proyecto not in self.__proyectos_activos:
            self.__proyectos_activos = self.__proyectos_activos + [proyecto]
            return True
        return False

# ----------------------------------------------------
# 2. Clases concretas derivadas
# ----------------------------------------------------

class Desarrollador(Empleado):
    """Representa a un empleado desarrollador."""
    
    def __init__(self, nombre_completo: str, salario_base_mensual: float, lenguajes_programacion: list, nivel_seniority: str):
        super().__init__(nombre_completo, salario_base_mensual)
        self.lenguajes_programacion = lenguajes_programacion
        # Lógica manual para simular .capitalize()
        self.nivel_seniority = nivel_seniority[0].upper() + nivel_seniority[1:].lower() if nivel_seniority else ""
        
    def _limite_proyectos(self):
        return 3 # Límite específico de Desarrollador

    def calcular_salario(self) -> float:
        """Salario + bono por nivel."""
        bonos = {"Junior": 200.0, "Semisenior": 500.0, "Senior": 1000.0}
        bono = bonos.get(self.nivel_seniority, 0.0)
        return self.salario_base + bono

    def mostrar_informacion(self):
        super().mostrar_informacion()
        print("   > Rol: Desarrollador (" + self.nivel_seniority + ")")
        print("   > Lenguajes:", end=" ")
        lenguajes_str = ""
        contador = 0
        for lenguaje in self.lenguajes_programacion:
            lenguajes_str = lenguajes_str + lenguaje
            contador += 1
            if contador < len(self.lenguajes_programacion):
                lenguajes_str = lenguajes_str + ", "
        print(lenguajes_str)


class Diseñador(Empleado):
    """Representa a un empleado diseñador."""
    
    def __init__(self, nombre_completo: str, salario_base_mensual: float, herramientas_diseño: list, especialidad_diseño: str):
        super().__init__(nombre_completo, salario_base_mensual)
        # Normaliza las herramientas: reemplazo de .capitalize() por lógica manual
        herramientas_normalizadas = []
        for h in herramientas_diseño:
            if len(h) > 0:
                herramientas_normalizadas = herramientas_normalizadas + [h[0].upper() + h[1:].lower()]
        self.herramientas_diseño = herramientas_normalizadas
        self.especialidad_diseño = especialidad_diseño
        
    def _limite_proyectos(self):
        return 2 # Límite específico de Diseñador

    def calcular_salario(self) -> float:
        """Salario + bono por herramientas (lógica compleja)."""
        salario_base = self.salario_base
        bono_total = 0.0
        
        tiene_figma = "Figma" in self.herramientas_diseño
        numero_herramientas = len(self.herramientas_diseño)
        
        # 1. Bono por Figma
        if tiene_figma:
            bono_total = bono_total + 300.0
        
        # 2. Bono por solo Photoshop o Illustrator (excluyente si tiene Figma o >2 herramientas)
        usa_solo_ph_il = (numero_herramientas in [1, 2] and 
                          not tiene_figma and 
                          all(h in ["Photoshop", "Illustrator"] for h in self.herramientas_diseño))
        if usa_solo_ph_il:
              bono_total = bono_total + 200.0
              
        # 3. Bono por al menos tres herramientas (aditivo)
        if numero_herramientas >= 3:
            bono_total = bono_total + 400.0

        return salario_base + bono_total

    def mostrar_informacion(self):
        super().mostrar_informacion()
        print("   > Rol: siseñador (" + self.especialidad_diseño + ")")
        print("   > Herramientas:", end=" ")
        herramientas_str = ""
        contador = 0
        for herramienta in self.herramientas_diseño:
            herramientas_str = herramientas_str + herramienta
            contador += 1
            if contador < len(self.herramientas_diseño):
                herramientas_str = herramientas_str + ", "
        print(herramientas_str)


class Gerente(Empleado):
    """Representa a un empleado gerente."""
    
    def __init__(self, nombre_completo: str, salario_base_mensual: float, nombre_departamento: str):
        super().__init__(nombre_completo, salario_base_mensual)
        self.nombre_departamento = nombre_departamento
        self.equipo_a_cargo = [] # Lista de empleados a cargo (Composición)

    def _limite_proyectos(self):
        return 0 # No puede ser miembro de un proyecto

    def calcular_salario(self) -> float:
        """Salario + 15% del total de salarios de su equipo directo."""
        total_salarios_equipo = sum(emp.calcular_salario() for emp in self.equipo_a_cargo)
        bono = total_salarios_equipo * 0.15
        return self.salario_base + bono

    def agregar_al_equipo(self, empleado):
        """Solo acepta Desarrollador o Diseñador."""
        if not isinstance(empleado, (Desarrollador, Diseñador)):
            print("⚠️ Error: Solo se pueden agregar Desarrolladores o Diseñadores al equipo del Gerente.")
            return
        
        if empleado not in self.equipo_a_cargo:
            self.equipo_a_cargo = self.equipo_a_cargo + [empleado]
        else:
            print("⚠️ Advertencia: " + empleado.nombre + " ya está en el equipo de " + self.nombre + ".")

    def mostrar_informacion(self):
        super().mostrar_informacion()
        print("   > Rol: Gerente (" + self.nombre_departamento + ")")
        nombres_equipo = [emp.nombre for emp in self.equipo_a_cargo]
        print("   > Equipo a cargo (" + str(len(nombres_equipo)) + " miembros):", end=" ")
        equipo_str = ""
        contador = 0
        for nombre in nombres_equipo:
            equipo_str = equipo_str + nombre
            contador += 1
            if contador < len(nombres_equipo):
                equipo_str = equipo_str + ", "
        if not nombres_equipo:
            equipo_str = "N/A"
        print(equipo_str)

# ----------------------------------------------------
# 3. Clase Proyecto (Composición)
# ----------------------------------------------------

class Proyecto:
    """Representa un proyecto de la empresa."""
    
    def __init__(self, nombre_proyecto: str, presupuesto_asignado: float):
        self.nombre_proyecto = nombre_proyecto
        self.presupuesto_asignado = presupuesto_asignado
        self.lista_empleados = [] # Lista de objetos Empleado

    def obtener_nombre(self):
        return self.nombre_proyecto
    
    def obtener_presupuesto(self):
        return self.presupuesto_asignado

    nombre = property(obtener_nombre)
    presupuesto = property(obtener_presupuesto)

    def agregar_empleado(self, empleado: Empleado):
        """Asigna un empleado al proyecto, verificando límites y duplicados."""
        
        if empleado in self.lista_empleados:
            print("Error: El empleado " + empleado.nombre + " ya está asignado al proyecto " + self.nombre_proyecto + ".")
            return

        try:
            if empleado.asignar_proyecto(self):
                self.lista_empleados = self.lista_empleados + [empleado]
                print(empleado.nombre + " agregado al proyecto " + self.nombre_proyecto + ".")
        except ValueError as e:
            print(e)
            return

    def costo_total(self) -> float:
        """Devuelve la suma de los salarios mensuales de los empleados asignados."""
        # Polimorfismo: llama a calcular_salario() de cada empleado
        return sum(emp.calcular_salario() for emp in self.lista_empleados)

    def viabilidad(self) -> bool:
        """Retorna True si costo_total() <= presupuesto * 0.7."""
        costo = self.costo_total()
        limite_costo = self.presupuesto_asignado * 0.7
        es_viable = costo <= limite_costo
        
        print("") 
        print("--- Viabilidad del Proyecto '" + self.nombre_proyecto + "' ---")
        print("   > Presupuesto Total: $" + str(round(self.presupuesto_asignado, 2)))
        print("   > Límite de Costo (70%): $" + str(round(limite_costo, 2)))
        print("   > Costo Total Mensual: $" + str(round(costo, 2)))
        print("   > Viable: " + ('Sí' if es_viable else 'No'))
        
        return es_viable

# ----------------------------------------------------
# 4. Función de procesamiento y Utilidades Interactivas
# ----------------------------------------------------

def _obtener_float_input(prompt):
    """Función auxiliar para asegurar que el input sea un número positivo."""
    while True:
        try:
            valor = float(input(prompt))
            if valor <= 0:
                print(" Entrada inválida. Por favor, ingrese un número positivo.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número positivo.")

def _obtener_lista_input(prompt):
    """Función auxiliar para obtener una lista separada por comas."""
    data_str = input(prompt)
    lista_resultado = []
    elementos = data_str.split(',')
    for elemento in elementos:
        if len(elemento) > 0:
            lista_resultado = lista_resultado + [elemento] 
    return lista_resultado

def crear_empleado_interactivo(rol: str):
    """Solicita datos al usuario para crear un empleado."""
    print("")
    print("--- Creación de " + rol + " ---")
    nombre_completo = input("Nombre del " + rol + ": ")
    salario_base_mensual = _obtener_float_input("Salario Base de " + nombre_completo + " (ej. 3500.00): $")
            
    if rol == "Desarrollador":
        lenguajes_programacion = _obtener_lista_input("Lenguajes (separados por coma, ej: Python,Java): ")
        while True:
            nivel_seniority_input = input("Nivel (Junior/SemiSenior/Senior): ")
            nivel_seniority = nivel_seniority_input[0].upper() + nivel_seniority_input[1:].lower() if nivel_seniority_input else ""
            if nivel_seniority in ["Junior", "Semisenior", "Senior"]:
                return Desarrollador(nombre_completo, salario_base_mensual, lenguajes_programacion, nivel_seniority_input)
            print("Nivel inválido. Intente de nuevo.")
        
    elif rol == "Diseñador":
        herramientas_diseño = _obtener_lista_input("Herramientas (separadas por coma, ej: Figma,Photoshop): ")
        especialidad_diseño = input("Especialidad (UI/UX/Gráfico): ")
        return Diseñador(nombre_completo, salario_base_mensual, herramientas_diseño, especialidad_diseño)
        
    elif rol == "Gerente":
        nombre_departamento = input("Departamento: ")
        return Gerente(nombre_completo, salario_base_mensual, nombre_departamento)
        
    return None

def crear_proyecto_interactivo():
    """Solicita datos al usuario para crear un proyecto."""
    nombre_proyecto = input("Nombre del Proyecto: ")
    presupuesto_asignado = _obtener_float_input("Presupuesto del proyecto '" + nombre_proyecto + "' (ej. 20000.00): $")
    return Proyecto(nombre_proyecto, presupuesto_asignado)

def procesar_empleados(lista_empleados: list[Empleado]):
    """Muestra la información detallada de los empleados y sus proyectos."""
    print("")
    print("PROCESAMIENTO DE INFORMACIÓN DE EMPLEADOS")
    
    for emp in lista_empleados:
        print("") 
        print("--- Información de " + emp.nombre + " ---")
        emp.mostrar_informacion()
        proyectos_asignados = emp.proyectos_activos
        numero_proyectos = len(proyectos_asignados)
        nombres_proyectos = [p.nombre for p in proyectos_asignados]

        print("   > Proyectos Asignados (" + str(numero_proyectos) + "):", end=" ")
        proyectos_str = ""
        contador = 0
        for nombre in nombres_proyectos:
            proyectos_str = proyectos_str + nombre
            contador += 1
            if contador < len(nombres_proyectos):
                proyectos_str = proyectos_str + ", "
        if not nombres_proyectos:
            proyectos_str = "Ninguno"
        print(proyectos_str)


# ----------------------------------------------------
# 5. Programa principal (Lógica de Prueba Interactivo)
# ----------------------------------------------------

def main_interactivo():
    """Ejecuta la prueba del sistema solicitando datos al usuario."""
    
    lista_empleados = []
    lista_proyectos = []
    
    print("") 
    print("SISTEMA AVANZADO DE GESTIÓN (MODO INTERACTIVO)")
    print("") 

    ## PASO 1: Creación de 1 Gerente, 2 Desarrolladores y 1 Diseñador
    
    print("--- 1. Creación de Gerente y Equipo (3 miembros) ---")
    
    # 1. Gerente
    gerente1 = crear_empleado_interactivo("Gerente")
    lista_empleados = lista_empleados + [gerente1]
    
    # 2. Desarrolladores
    print("")
    print("----------" + " Creando el Equipo Directo para " + gerente1.nombre + " " + "----------")
    desarrollador1 = crear_empleado_interactivo("Desarrollador")
    lista_empleados = lista_empleados + [desarrollador1]
    gerente1.agregar_al_equipo(desarrollador1)
    
    desarrollador2 = crear_empleado_interactivo("Desarrollador")
    lista_empleados = lista_empleados + [desarrollador2]
    gerente1.agregar_al_equipo(desarrollador2)

    # 3. Diseñador
    disenador1 = crear_empleado_interactivo("Diseñador")
    lista_empleados = lista_empleados + [disenador1]
    gerente1.agregar_al_equipo(disenador1)
    
    ## PASO 2: Creación de Proyectos
    print("") 
    print("="*30)
    print("--- 2. Creación de Proyectos (2 Requeridos + 1 Extra) ---")
    proyecto_alpha = crear_proyecto_interactivo()
    lista_proyectos = lista_proyectos + [proyecto_alpha]
    proyecto_beta = crear_proyecto_interactivo()
    lista_proyectos = lista_proyectos + [proyecto_beta]
    
    # Proyecto extra para forzar el límite (cuarto proyecto)
    print("") 
    print("Creando Proyecto Extra (para prueba de límite de Desarrollador):")
    proyecto_extra = crear_proyecto_interactivo()
    lista_proyectos = lista_proyectos + [proyecto_extra]
    
    ## PASO 3: Asignación de Empleados
    print("") 
    print("="*30)
    print("--- 3. Asignación de Empleados a Proyectos ---")
    
    # Desarrollador 1 (Límite 3)
    print("") 
    print("Asignando a " + desarrollador1.nombre + " (máx 3):")
    proyecto_alpha.agregar_empleado(desarrollador1) # 1/3
    proyecto_beta.agregar_empleado(desarrollador1)  # 2/3
    proyecto_extra.agregar_empleado(desarrollador1) # 3/3
    
    # Desarrollador 2 (Límite 3)
    print("") 
    print("Asignando a " + desarrollador2.nombre + " (máx 3):")
    proyecto_alpha.agregar_empleado(desarrollador2) # 1/3
    proyecto_beta.agregar_empleado(desarrollador2)  # 2/3
    
    # Diseñador 1 (Límite 2)
    print("") 
    print("Asignando a " + disenador1.nombre + " (máx 2):")
    proyecto_alpha.agregar_empleado(disenador1)      # 1/2
    proyecto_beta.agregar_empleado(disenador1)       # 2/2
    
    ## PASO 4: Pruebas de Fallo y Captura de Error
    print("") 
    print("="*30)
    print("--- 4. Pruebas de Límite y Restricciones (Captura de Error) ---")

    # Intento 1: Asignar el 4to proyecto al Desarrollador 1 (DEBE FALLAR)
    print("") 
    print("Intentando asignar un 4to proyecto a " + desarrollador1.nombre + ":")
    proyecto_extra_fallo = Proyecto("PROYECTO 4 FALLIDO", 1000.0) 
    proyecto_extra_fallo.agregar_empleado(desarrollador1) 
    
    # Intento 2: Asignar el 3er proyecto al Diseñador 1 (DEBE FALLAR)
    print("") 
    print("Intentando asignar un 3er proyecto a " + disenador1.nombre + ":")
    proyecto_extra_fallo.agregar_empleado(disenador1) 
    
    # Intento 3: Asignar al Gerente como miembro (DEBE FALLAR)
    print("") 
    print("Intentando asignar al Gerente " + gerente1.nombre + " como miembro de proyecto:")
    proyecto_alpha.agregar_empleado(gerente1) 

    ## PASO 5: Procesamiento de Resultados Finales
    
    # Muestra información de todos los empleados
    procesar_empleados(lista_empleados)
    
    # Muestra la viabilidad de cada proyecto
    print("") 
    print("="*30)
    print("--- 5. Viabilidad de Proyectos Definidos ---")
    proyecto_alpha.viabilidad()
    proyecto_beta.viabilidad()
    proyecto_extra.viabilidad()


if __name__ == "__main__":
    main_interactivo()
