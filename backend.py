# backend.py - VERSIÓN COMPLETA CON RELACIONES BIYECTIVAS
import json
import os
from datetime import datetime

class GestorDatos:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.archivos = {
            'recursos': os.path.join(self.base_dir, "recursos.json"),
            'personal': os.path.join(self.base_dir, "personal.json"),
            'escenas': os.path.join(self.base_dir, "escenas.json"),
            'config': os.path.join(self.base_dir, "configuracion.json"),
            'producciones': os.path.join(self.base_dir, "producciones.json")
        }
        
        print(f"📁 Directorio de trabajo: {self.base_dir}")
        
        self.cargar_configuracion()
        self.cargar_datos()

    def cargar_configuracion(self):
        if os.path.exists(self.archivos['config']):
            with open(self.archivos['config'], 'r', encoding='utf-8') as f:
                self.configuracion = json.load(f)
        else:
            self.configuracion = {
                "auto_save": True,
                "auto_save_interval": 300,
                "last_backup": None,
                "theme": "light",
                "language": "en"
            }
            self.guardar_configuracion()

    def cargar_datos(self):
        self.datos = {}
        
        # Cargar recursos
        if os.path.exists(self.archivos['recursos']):
            with open(self.archivos['recursos'], 'r', encoding='utf-8') as f:
                self.datos['recursos'] = json.load(f)
        else:
            self.datos['recursos'] = {
                "camara": 6,
                "equipo implementador de vestimenta": 2,
                "silla del director": 2,
                "claqueta": 2,
                "altavoces": 3,
                "luces": 4,
                "autos": 2,
                "armas blancas falsas": 2,
                "equipo de proteccion": 3,
                "equipo de pirotecnia": 2,
                "microfono": 6
            }
            self.guardar_recursos()
        
        # Cargar personal
        if os.path.exists(self.archivos['personal']):
            with open(self.archivos['personal'], 'r', encoding='utf-8') as f:
                self.datos['personal'] = json.load(f)
        else:
            self.datos['personal'] = {
                "actor_principal_1": 1,
                "actor_principal_2": 1,
                "secundarios": 4,
                "doblaje": 1,
                "de riesgo": 2,
                "director_de_escena": 1,
                "vicedirector de escenas": 1,
                "personal de inicio de escenas": 2,
                "profesional de camaras": 4,
                "sujetador de claqueta": 2,
                "profesional de edicion": 1,
                "profesional de iluminacion": 2,
                "profesional en conduccion": 2,
                "profesional maquillista": 2,
                "profesional de sonido": 2
            }
            self.guardar_personal()
        
        # Cargar escenas
        if os.path.exists(self.archivos['escenas']):
            with open(self.archivos['escenas'], 'r', encoding='utf-8') as f:
                escenas_data = json.load(f)
                if isinstance(escenas_data, dict):
                    self.datos['escenas'] = list(escenas_data.keys())
                else:
                    self.datos['escenas'] = escenas_data
        else:
            self.datos['escenas'] = [
                "sala de maquillaje",
                "escenas_de_principales",
                "escenas de riesgo",
                "escenas_ secundarias",
                "camerino",
                "camerino de actores principales",
                "salon de edicion"
            ]
            self.guardar_escenas()
        
        # Cargar producciones
        if os.path.exists(self.archivos['producciones']):
            with open(self.archivos['producciones'], 'r', encoding='utf-8') as f:
                self.datos['producciones'] = json.load(f)
        else:
            self.datos['producciones'] = {}
            self.guardar_producciones()
        
        return self.datos

    # ========== MÉTODOS PARA OBTENER DATOS ==========
    def obtener_recursos(self):
        return self.datos['recursos']
    
    def obtener_personal(self):
        return self.datos['personal']
    
    def obtener_escenas(self):
        return self.datos['escenas']
    
    def obtener_configuracion(self):
        return self.configuracion
    
    def obtener_producciones(self):
        return self.datos['producciones']
    
    # ========== MÉTODOS PARA AGREGAR ==========
    def agregar_recurso(self, nombre, cantidad):
        if nombre in self.datos['recursos']:
            self.datos['recursos'][nombre] += cantidad
        else:
            self.datos['recursos'][nombre] = cantidad
        self.guardar_recursos()
        return True

    def agregar_personal(self, puesto, cantidad):
        if puesto in self.datos['personal']:
            self.datos['personal'][puesto] += cantidad
        else:
            self.datos['personal'][puesto] = cantidad
        self.guardar_personal()
        return True

    def agregar_escena(self, descripcion):
        if descripcion not in self.datos['escenas']:
            self.datos['escenas'].append(descripcion)
            self.guardar_escenas()
            return True
        return False

    def agregar_produccion(self, fecha, produccion_data):
        if self.existe_produccion_en_fecha(fecha):
            return None
        
        if fecha not in self.datos['producciones']:
            self.datos['producciones'][fecha] = []
        
        produccion_id = f"prod_{len(self.datos['producciones'][fecha]) + 1:03d}"
        produccion_data['id'] = produccion_id
        produccion_data['fecha'] = fecha
        produccion_data['estado'] = 'programada'
        
        # Descontar recursos
        recursos_utilizados = produccion_data.get('recursos_utilizados', {})
        for recurso, cantidad in recursos_utilizados.items():
            if recurso in self.datos['recursos']:
                self.datos['recursos'][recurso] -= cantidad
                if self.datos['recursos'][recurso] < 0:
                    self.datos['recursos'][recurso] = 0
        
        # Descontar personal
        personal_asignado = produccion_data.get('personal_asignado', {})
        for puesto, cantidad in personal_asignado.items():
            if puesto in self.datos['personal']:
                self.datos['personal'][puesto] -= cantidad
                if self.datos['personal'][puesto] < 0:
                    self.datos['personal'][puesto] = 0
        
        self.datos['producciones'][fecha].append(produccion_data)
        
        self.guardar_recursos()
        self.guardar_personal()
        self.guardar_producciones()
        
        return produccion_id
    
    # ========== MÉTODOS PARA ELIMINAR ==========
    def eliminar_recurso(self, nombre):
        if nombre in self.datos['recursos']:
            del self.datos['recursos'][nombre]
            self.guardar_recursos()
            return True
        return False

    def eliminar_personal(self, puesto):
        if puesto in self.datos['personal']:
            del self.datos['personal'][puesto]
            self.guardar_personal()
            return True
        return False

    def eliminar_escena(self, indice):
        if 0 <= indice < len(self.datos['escenas']):
            escena = self.datos['escenas'][indice]
            del self.datos['escenas'][indice]
            self.guardar_escenas()
            return True
        return False

    def eliminar_produccion(self, fecha, produccion_id):
        if fecha in self.datos['producciones']:
            for i, prod in enumerate(self.datos['producciones'][fecha]):
                if prod.get('id') == produccion_id:
                    # Restaurar recursos
                    for recurso, cantidad in prod.get('recursos_utilizados', {}).items():
                        if recurso in self.datos['recursos']:
                            self.datos['recursos'][recurso] += cantidad
                    
                    # Restaurar personal
                    for puesto, cantidad in prod.get('personal_asignado', {}).items():
                        if puesto in self.datos['personal']:
                            self.datos['personal'][puesto] += cantidad
                    
                    del self.datos['producciones'][fecha][i]
                    
                    if not self.datos['producciones'][fecha]:
                        del self.datos['producciones'][fecha]
                    
                    self.guardar_recursos()
                    self.guardar_personal()
                    self.guardar_producciones()
                    
                    return True
        return False
    
    # ========== MÉTODOS PARA ACTUALIZAR ==========
    def actualizar_recurso(self, nombre, nueva_cantidad):
        if nombre in self.datos['recursos']:
            self.datos['recursos'][nombre] = nueva_cantidad
            self.guardar_recursos()
            return True
        return False

    def actualizar_produccion(self, fecha, produccion_id, nuevos_datos):
        if fecha in self.datos['producciones']:
            for i, prod in enumerate(self.datos['producciones'][fecha]):
                if prod.get('id') == produccion_id:
                    self.datos['producciones'][fecha][i].update(nuevos_datos)
                    self.guardar_producciones()
                    return True
        return False

    # ========== MÉTODOS PARA OBTENER ESPECÍFICOS ==========
    def obtener_producciones_por_fecha(self, fecha):
        return self.datos['producciones'].get(fecha, [])

    def obtener_producciones_por_mes(self, año, mes):
        producciones_mes = {}
        for fecha, prods in self.datos['producciones'].items():
            try:
                fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
                if fecha_obj.year == año and fecha_obj.month == mes:
                    producciones_mes[fecha] = prods
            except:
                continue
        return producciones_mes
    
    def existe_produccion_en_fecha(self, fecha):
        producciones = self.datos['producciones'].get(fecha, [])
        return len(producciones) > 0

    def obtener_produccion_existente_en_fecha(self, fecha):
        producciones = self.datos['producciones'].get(fecha, [])
        if producciones:
            return producciones[0]
        return None

    # ========== MÉTODOS PARA GUARDAR ==========
    def guardar_recursos(self):
        try:
            with open(self.archivos['recursos'], 'w', encoding='utf-8') as f:
                json.dump(self.datos['recursos'], f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving resources: {e}")
            return False

    def guardar_personal(self):
        try:
            with open(self.archivos['personal'], 'w', encoding='utf-8') as f:
                json.dump(self.datos['personal'], f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving staff: {e}")
            return False

    def guardar_escenas(self):
        try:
            with open(self.archivos['escenas'], 'w', encoding='utf-8') as f:
                json.dump(self.datos['escenas'], f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving scenes: {e}")
            return False

    def guardar_producciones(self):
        try:
            with open(self.archivos['producciones'], 'w', encoding='utf-8') as f:
                json.dump(self.datos['producciones'], f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving productions: {e}")
            return False

    def guardar_configuracion(self):
        try:
            with open(self.archivos['config'], 'w', encoding='utf-8') as f:
                json.dump(self.configuracion, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving configuration: {e}")
            return False

    def guardar_todo(self):
        success = True
        success = self.guardar_recursos() and success
        success = self.guardar_personal() and success
        success = self.guardar_escenas() and success
        success = self.guardar_producciones() and success
        success = self.guardar_configuracion() and success
        
        if success:
            self.configuracion['last_backup'] = datetime.now().isoformat()
            self.guardar_configuracion()
            print("✅ Todos los datos guardados exitosamente")
        
        return success


class LogicaNegocio:
    def __init__(self, gestor_datos):
        self.gestor = gestor_datos
        
        # PRECIOS
        self.precios_recursos = {
            "camara": 5000,
            "equipo implementador de vestimenta": 1500,
            "silla del director": 300,
            "claqueta": 200,
            "altavoces": 800,
            "luces": 1200,
            "autos": 20000,
            "armas blancas falsas": 500,
            "equipo de proteccion": 1000,
            "equipo de pirotecnia": 2500,
            "microfono": 300
        }
        
        self.salarios_personal = {
            "actor_principal_1": 10000,
            "actor_principal_2": 9000,
            "secundarios": 3000,
            "doblaje": 4000,
            "de riesgo": 6000,
            "director_de_escena": 12000,
            "vicedirector de escenas": 8000,
            "personal de inicio de escenas": 2500,
            "profesional de camaras": 5000,
            "sujetador de claqueta": 2000,
            "profesional de edicion": 4500,
            "profesional de iluminacion": 4000,
            "profesional en conduccion": 3500,
            "profesional maquillista": 3000,
            "profesional de sonido": 4000
        }
        
        # ========== RELACIONES BIYECTIVAS RECURSO ↔ PERSONAL ==========
        
        # 1. RELACIÓN 1:1 EXCLUSIVA (misma cantidad)
        self.relacion_biyectiva = {
            "claqueta": "sujetador de claqueta",
            "luces": "profesional de iluminacion",
            "camara": "profesional de camaras",
            "equipo implementador de vestimenta": "profesional maquillista",
            "autos": "profesional en conduccion",
            "equipo de proteccion": "de riesgo",
            "altavoces": "profesional de sonido"
        }
        
        # Relación inversa para fácil acceso
        self.relacion_biyectiva_inversa = {v: k for k, v in self.relacion_biyectiva.items()}
        
        # 2. RELACIÓN ESPECIAL: silla del director (solo UN director)
        self.silla_director = "silla del director"
        self.directores = ["director_de_escena", "vicedirector de escenas"]
        
        # 3. RELACIÓN ESPECIAL: micrófono (compartido)
        self.requieren_microfono = [
            "actor_principal_1", "actor_principal_2", "secundarios", "doblaje", "profesional de sonido"
        ]
        
        # 4. RELACIÓN: profesional de sonido puede usar altavoces O microfono
        self.sonido_alternativas = ["altavoces", "microfono"]
        
        # ========== DEPENDENCIAS DE ESCENAS ==========
        
        self.personal_prohibido_por_escena = {
            "escenas de riesgo": ["actor_principal_1", "actor_principal_2"],
            "camerino de actores principales": [
                "director_de_escena", "vicedirector de escenas", 
                "profesional de camaras", "profesional de iluminacion", 
                "sujetador de claqueta", "personal de inicio de escenas", 
                "de riesgo", "secundarios", "doblaje", "profesional de sonido", 
                "profesional maquillista"
            ]
        }
        
        self.recursos_prohibidos_por_escena = {
            "escenas_de_principales": ["equipo de pirotecnia", "armas blancas falsas"]
        }
        
        self.personal_obligatorio_por_escena = {
            "sala de maquillaje": ["profesional maquillista"],
            "escenas_de_principales": [
                "personal de inicio de escenas", "profesional de iluminacion",
                "profesional de camaras", "sujetador de claqueta", "profesional de sonido"
            ],
            "escenas de riesgo": [
                "personal de inicio de escenas", "profesional de iluminacion",
                "profesional de camaras", "sujetador de claqueta", "profesional de sonido"
            ],
            "escenas_ secundarias": [
                "personal de inicio de escenas", "profesional de iluminacion",
                "profesional de camaras", "sujetador de claqueta", "profesional de sonido"
            ],
            "salon de edicion": ["profesional de edicion", "doblaje"]
        }
        
        self.recursos_obligatorios_por_escena = {
            "escenas_de_principales": ["camara", "luces", "claqueta", "altavoces"],
            "escenas de riesgo": ["equipo de proteccion"],
            "escenas_ secundarias": ["camara", "luces", "claqueta", "altavoces"],
            "salon de edicion": ["microfono", "camara"]
        }
        
        self.actores_obligatorios_por_escena = {
            "escenas_de_principales": ["actor_principal_1", "actor_principal_2"],
            "camerino de actores principales": ["actor_principal_1", "actor_principal_2"]
        }
        
        self.escenas_con_director_obligatorio = [
            "escenas_de_principales", "escenas de riesgo", "escenas_ secundarias"
        ]
    
    # ========== MÉTODOS DE VALIDACIÓN ==========
    
    def validar_relaciones_biyectivas(self, recursos, personal):
        errores = []
        
        for recurso, personal_asociado in self.relacion_biyectiva.items():
            cantidad_recurso = recursos.get(recurso, 0)
            cantidad_personal = personal.get(personal_asociado, 0)
            
            if cantidad_recurso > 0 and cantidad_personal == 0:
                errores.append(f"❌ Recurso '{recurso}' requiere personal '{personal_asociado}'")
            elif cantidad_recurso == 0 and cantidad_personal > 0:
                errores.append(f"❌ Personal '{personal_asociado}' requiere recurso '{recurso}'")
            elif cantidad_recurso > 0 and cantidad_personal > 0 and cantidad_recurso != cantidad_personal:
                errores.append(f"❌ Cantidades desiguales: '{recurso}'={cantidad_recurso}, '{personal_asociado}'={cantidad_personal}")
        
        cantidad_silla = recursos.get("silla del director", 0)
        cantidad_director = personal.get("director_de_escena", 0)
        cantidad_vicedirector = personal.get("vicedirector de escenas", 0)
        total_directores = cantidad_director + cantidad_vicedirector
        
        if cantidad_silla > 0 and total_directores == 0:
            errores.append("❌ Recurso 'silla del director' requiere un director")
        elif cantidad_silla == 0 and total_directores > 0:
            errores.append("❌ Director(es) requieren 'silla del director'")
        elif cantidad_silla > 0 and total_directores > 0 and cantidad_silla != total_directores:
            errores.append(f"❌ Sillas ({cantidad_silla}) no coinciden con directores ({total_directores})")
        
        if cantidad_director > 0 and cantidad_vicedirector > 0:
            if cantidad_silla < cantidad_director + cantidad_vicedirector:
                errores.append("❌ No pueden estar ambos directores a la vez con una sola silla")
        
        total_personas_con_microfono = 0
        for persona in self.requieren_microfono:
            total_personas_con_microfono += personal.get(persona, 0)
        
        cantidad_microfonos = recursos.get("microfono", 0)
        
        if total_personas_con_microfono > 0 and cantidad_microfonos == 0:
            errores.append(f"❌ {total_personas_con_microfono} persona(s) requieren micrófono(s)")
        elif total_personas_con_microfono > cantidad_microfonos:
            errores.append(f"❌ Insuficientes micrófonos: {total_personas_con_microfono} necesitan, solo {cantidad_microfonos}")
        
        cantidad_sonidista = personal.get("profesional de sonido", 0)
        if cantidad_sonidista > 0:
            tiene_altavoces = recursos.get("altavoces", 0) > 0
            tiene_microfono = recursos.get("microfono", 0) > 0
            if not tiene_altavoces and not tiene_microfono:
                errores.append("❌ 'profesional de sonido' requiere altavoces o micrófono")
        
        return errores
    
    def validar_produccion(self, escena, recursos_seleccionados, personal_seleccionado):
        errores = []
        estados = {
            'recursos': {},
            'personal': {},
            'directores_valido': True
        }
        
        if escena not in self.gestor.obtener_escenas():
            errores.append(f"La escena '{escena}' no existe en el catálogo")
            return False, errores, estados
        
        errores.extend(self.validar_relaciones_biyectivas(recursos_seleccionados, personal_seleccionado))
        
        if escena in self.recursos_obligatorios_por_escena:
            for recurso_obligatorio in self.recursos_obligatorios_por_escena[escena]:
                if recursos_seleccionados.get(recurso_obligatorio, 0) <= 0:
                    errores.append(f"Recurso obligatorio faltante: {recurso_obligatorio}")
                    estados['recursos'][recurso_obligatorio] = 'obligatorio_falta'
                else:
                    estados['recursos'][recurso_obligatorio] = 'obligatorio_cumplido'
        
        if escena in self.personal_obligatorio_por_escena:
            for personal_obligatorio in self.personal_obligatorio_por_escena[escena]:
                if personal_seleccionado.get(personal_obligatorio, 0) <= 0:
                    errores.append(f"Personal obligatorio faltante: {personal_obligatorio}")
                    estados['personal'][personal_obligatorio] = 'obligatorio_falta'
                else:
                    estados['personal'][personal_obligatorio] = 'obligatorio_cumplido'
        
        if escena in self.actores_obligatorios_por_escena:
            actores_opciones = self.actores_obligatorios_por_escena[escena]
            tiene_actor = False
            for actor in actores_opciones:
                if personal_seleccionado.get(actor, 0) > 0:
                    tiene_actor = True
                    estados['personal'][actor] = 'obligatorio_cumplido'
                else:
                    estados['personal'][actor] = 'obligatorio_falta'
            if not tiene_actor:
                errores.append(f"Se requiere al menos uno de estos actores: {', '.join(actores_opciones)}")
        
        if escena in self.escenas_con_director_obligatorio:
            tiene_director = False
            for director in self.directores:
                if personal_seleccionado.get(director, 0) > 0:
                    tiene_director = True
                    estados['personal'][director] = 'obligatorio_cumplido'
                else:
                    estados['personal'][director] = 'obligatorio_falta'
            if not tiene_director:
                errores.append("Se requiere al menos un director")
        
        if escena in self.recursos_prohibidos_por_escena:
            for recurso_prohibido in self.recursos_prohibidos_por_escena[escena]:
                if recursos_seleccionados.get(recurso_prohibido, 0) > 0:
                    errores.append(f"Recurso prohibido: {recurso_prohibido}")
                    estados['recursos'][recurso_prohibido] = 'prohibido'
        
        if escena in self.personal_prohibido_por_escena:
            for personal_prohibido in self.personal_prohibido_por_escena[escena]:
                if personal_seleccionado.get(personal_prohibido, 0) > 0:
                    errores.append(f"Personal prohibido: {personal_prohibido}")
                    estados['personal'][personal_prohibido] = 'prohibido'
        
        if escena in self.escenas_con_director_obligatorio:
            if personal_seleccionado.get("personal de inicio de escenas", 0) <= 0:
                errores.append("'personal de inicio de escenas' es obligatorio")
                estados['personal']["personal de inicio de escenas"] = 'obligatorio_falta'
            else:
                estados['personal']["personal de inicio de escenas"] = 'obligatorio_cumplido'
        
        for recurso in recursos_seleccionados:
            if recurso not in estados['recursos']:
                estados['recursos'][recurso] = 'opcional'
        
        for persona in personal_seleccionado:
            if persona not in estados['personal']:
                estados['personal'][persona] = 'opcional'
        
        return len(errores) == 0, errores, estados
    
    def verificar_conflictos_recursos(self, fecha, recursos_necesarios, personal_necesario=None):
        conflictos = []
        recursos_totales = self.gestor.obtener_recursos()
        for recurso, cantidad in recursos_necesarios.items():
            disponible = recursos_totales.get(recurso, 0)
            if disponible < cantidad:
                conflictos.append(f"'{recurso}': {disponible} disp, {cantidad} needed")
        
        if personal_necesario:
            personal_total = self.gestor.obtener_personal()
            for puesto, cantidad in personal_necesario.items():
                disponible = personal_total.get(puesto, 0)
                if disponible < cantidad:
                    conflictos.append(f"'{puesto}': {disponible} disp, {cantidad} needed")
        return conflictos
    
    def calcular_costo_produccion(self, produccion_data):
        costo = 0
        if 'recursos_utilizados' in produccion_data:
            for r, c in produccion_data['recursos_utilizados'].items():
                costo += self.precios_recursos.get(r, 100) * c
        if 'personal_asignado' in produccion_data:
            for p, c in produccion_data['personal_asignado'].items():
                salario = self.salarios_personal.get(p, 3000)
                dias = produccion_data.get('duracion_horas', 8) / 8
                costo += c * (salario / 20) * dias
        return round(costo, 2)
    
    def obtener_estadisticas_produccion(self, año=None, mes=None):
        if año and mes:
            producciones = self.gestor.obtener_producciones_por_mes(año, mes)
        else:
            producciones = self.gestor.obtener_producciones()
        
        total = comp = prog = costo = 0
        for fecha, prods in producciones.items():
            total += len(prods)
            for p in prods:
                if p.get('estado') == 'completada':
                    comp += 1
                elif p.get('estado') == 'programada':
                    prog += 1
                costo += self.calcular_costo_produccion(p)
        
        return {
            "total_producciones": total,
            "completadas": comp,
            "programadas": prog,
            "costo_total": round(costo, 2),
            "costo_promedio": round(costo / max(total, 1), 2)
        }
    
    def obtener_estadisticas(self):
        r = self.gestor.obtener_recursos()
        p = self.gestor.obtener_personal()
        e = self.gestor.obtener_escenas()
        return {
            "total_recursos": sum(r.values()),
            "total_personal": sum(p.values()),
            "total_escenas": len(e),
            "tipos_recursos": len(r),
            "tipos_personal": len(p),
            "costo_evento_promedio": 0
        }
    
    def producir_escena(self, tipo_escena):
        return f"Escena '{tipo_escena}' producida (simulación)"