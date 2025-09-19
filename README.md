# Gestión de Créditos - Delta Data Consulting

Sistema web para el **registro y gestión de créditos bancarios**, desarrollado como parte de un examen práctico.  
Incluye un backend en **Flask** y un frontend responsivo con **Bootstrap** y **Chart.js** para la visualización de métricas.

---

## Descripción

La aplicación permite **registrar, editar, eliminar y visualizar** créditos bancarios en una interfaz sencilla e intuitiva.  
El dashboard incluye **gráficas interactivas** y **tarjetas métricas** que se actualizan en tiempo real con cada operación.

---

## Características

- **CRUD completo** de créditos (crear, listar, actualizar y eliminar)  
- **Dashboard con métricas dinámicas**: monto total, número de clientes y total de créditos  
- **3 visualizaciones interactivas** con Chart.js:
  1. Evolución mensual de créditos   
  2. Distribución de créditos por cliente   
  3. Distribución por rangos de monto   
- **Interfaz responsiva** con diseño moderno usando Bootstrap 5  
- **Validaciones y modales** para confirmación de acciones  
- **Actualización automática** de la tabla y gráficas tras cada operación CRUD  

---

## Tecnologías Utilizadas

- **Backend:** Python 3 + Flask + Flask-SQLAlchemy + Flask-CORS  
- **Base de Datos:** SQLite  
- **Frontend:** HTML5, CSS3, JavaScript (ES6)  
- **UI Framework:** Bootstrap 5  
- **Gráficas:** Chart.js  
- **Fuentes:** Google Fonts (Poppins, Montserrat)  

---

## Estructura del Proyecto

```bash
proyecto/
├── app.py              # Aplicación principal Flask
├── routes.py           # Endpoints y lógica de API
├── models.py           # Definición del modelo Credito
├── extensions.py       # Configuración de extensiones (SQLAlchemy)
├── database.db         # Base de datos SQLite
├── requirements.txt    # Dependencias del proyecto
├── templates/
│   └── index.html      # Interfaz principal
├── static/
│   ├── script.js       # Lógica de frontend
│   └── style.css       # Estilos personalizados
└── README.md           # Documentación
```

## Base de Datos

La base de datos SQLite contiene una sola tabla `creditos` con la siguiente estructura:

| Campo              | Tipo     | Descripción                        |
|--------------------|----------|------------------------------------|
| id                 | INTEGER  | Clave primaria autoincremental     |
| cliente            | TEXT     | Nombre del cliente                 |
| monto              | REAL     | Monto del crédito                  |
| tasa_interes       | REAL     | Tasa de interés anual              |
| plazo              | INTEGER  | Plazo en meses                     |
| fecha_otorgamiento | TEXT     | Fecha en formato `YYYY-MM-DD`      |

---

## 🔗 Endpoints de la API

| Método | Endpoint                | Descripción                        |
|--------|-------------------------|------------------------------------|
| GET    | `/creditos`             | Listar todos los créditos          |
| POST   | `/creditos`             | Crear un nuevo crédito             |
| PUT    | `/creditos/<id>`        | Actualizar crédito existente       |
| DELETE | `/creditos/<id>`        | Eliminar crédito                   |
| GET    | `/creditos/por_cliente` | Créditos agrupados por cliente     |
| GET    | `/creditos/por_rangos`  | Créditos distribuidos por rangos   |
| GET    | `/creditos/total`       | Total del monto de créditos        |

---

## Funcionalidades

### Registro de Créditos
- Formulario validado con campos obligatorios.  
- Confirmación en modal tras un registro exitoso.  

### Gestión de Créditos
- Tabla dinámica con todos los registros.  
- Edición mediante modal.  
- Eliminación con confirmación.  
- Cambios reflejados en tiempo real.  

### Dashboard y Métricas
- **Monto total otorgado**.  
- **Clientes únicos registrados**.  
- **Total de créditos creados**.  
- **Promedio de crédito por cliente**.  

### Visualizaciones
1. **Gráfica de línea** → Evolución mensual de créditos.  
2. **Gráfica circular** → Distribución por cliente.  
3. **Gráfica de dona** → Créditos agrupados por rangos.  

---

## Diseño

- **Diseño responsivo** para escritorio y móvil.  
- **Colores corporativos**: azul marino y rojo.  
- **Tipografías modernas**: *Poppins* y *Montserrat*.  
- **Hover effects** en botones para mejor UX.  
- **Tarjetas métricas** destacadas sobre las gráficas.  

---

## Instalación y Uso
Prerrequisitos:
- **Python 3.7 o superior**
- **pip (gestor de paquetes de Python)**

```bash
# Clonar repositorio
git clone https://github.com/andres-pg9/Registro-Creditos.git
cd Registro-Creditos

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Activar entorno virtual (macOS/Linux)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Congelar dependencias (guardar librerías instaladas)
pip freeze > requirements.txt

# Ejecutar servidor Flask
python app.py
```

