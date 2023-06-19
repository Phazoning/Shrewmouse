# Proyecto Alonso Morenas Díaz - Propuesta

## Introducción 

> Como parte del currículum de CFGS se pide que los alumnos cursen una serie de prácticas en empresas (Formación en Centros de Trabajo) amén de la realización de un proyecto personal donde se muestren los contenidos aprendidos en el curso

> Es por esto que se redacta el siguiente documento, para poder realizar una propuesta de proyecto personal, indicando las tecnologías empleadas, el esquema de la aplicación y cómo se va a proceder a su desarrollo

## Vocabulario

### Desarrollo

- Etiqueta: forma de envolver un valor para su uso en algún lenguaje, siguiendo la sintaxis <aaa bbb>ccc</aaa> donde aaa es la etiqueta, bbb sus propiedades y ccc el valor de ésta
- Lenguaje de etiquetas/marcas: lenguaje de definición de elementos que usa etiquetas para ésto
- Lenguaje de programación: conjunto de instrucciones en texto plano que permiten realizar tareas en un ordenador
- \* de alto nivel: lenguaje de programación cuyas instrucciones y algoritmos son similares a la sintaxis humana
- \* orientado a objetos: lenguaje de programación que permite la construcción de objetos
- \* interpretado: lenguaje de programación cuya sintaxis es hecha efectiva en tiempo real a través de un programa llamado de forma general intérprete
- \* debilmente tipado: lenguaje de programación donde las variables no reciben un tipo fijo
- \* asíncrono: lenguaje de programación donde sus instrucciones se mantienen en un mismo hilo del procesador
- \* síncrono; lenguaje de programación donde sus instrucciones van siendo delegadas a los diferentes hilos que tenga disponibles el procesador
- Objeto: máximo nivel de abstracción en un lenguaje de programación orientado a objetos, consistente en definir en conjunto atributos y procedimientos
- Clase: prototipo de objeto que permite instanciarlo al indicar el valor de sus atributos
- C: lenguaje de programación de medio nivel. Muy rápido y ligero
- Python: lenguaje interpretado de alto nivel orientado a objetos debilmente tipado de sintaxis sencilla. Administrado por la Python Software Foundation.
- dict: clase de Python que define un mapeo clave-valor
- Javascript: lenguaje interpretado de alto nivel orientado a objetos debilmente tipado con una definición de objetos flexible
- json (Javascript): acrónimo de JavaScript Object Notation, fragmentos de texto plano que contienen mapeos clave-valor. Llamados así porque siguen el patrón de objetos de Javascript
- XML: abreviatura de eXtensible Markup Language, lenguaje de etiquetas usado para almacenar datos
- csv: formato de archivo consistente en cadenas de valores separados por un símbolo (habitualmente "," o ";") que suele constrar de una primera línea indicando el nombre de las columnas
- CPython: intérprete de Python que delega la interpretación de ciertas partes del código en el lenguaje de programación C
- Entorno virtual: un entorno virtual (venv) es una instancia del intérprete de Python creada con objeto de usar un intérprete que contenga solo los módulos necesarios-Precisa de ser activado para ser usado
- PyPI: repositorio de módulos de Python que se pueden instalar usando PiP
- PiP: herramienta de Python que permite instalar, actualizar y eliminar paquetes de Python de la instalación activada. También permite reflejar los requisitos de un módulo mediante el comando "freeze"
- pprint (módulo de Python): que permite imprimir por pantalla datos de ciertos tipos de forma legible
- json (módulo de Python): módulo  que permite operar entre archivos con formato json y diccionarios
- etree (módulo de python): módulo destinado al manejo de xml de forma simple
- request (módulo de Python): módulo  dedicado a la comunicación servidor-cliente mediante requests HTTPS
- pickle (módulo de Python): módulo que permite convertir objetos en array de bits para su almacenamiento
- rabbit MQ: sistema de procesamiento de requests en masa mediante el uso de colas
- Cola (rabbitMQ): pila de mensajes recibida que se va procesando mediante el sistema FIFO
- Pipeline: proceso el cual está destinado a poderse enlazar siempre con otro en sucesión


### Bases de datos

- Base de datos: sistema de almacenamiento de datos de forma abstracta
- \* no relacional: base de datos que no establece vínculos entre tablas permitiendo así la libre existencia de datos
- \* documental: base de datos no relacional cuya base para almacenar datos es el documento
- \* local: base de datos cuya existencia no lleva aparejada por defecto el estar incluida en un servidor si no que se almacena en el ordenador del administrador de ésta 
- MongoDB: base de datos documental basada en javascript
- Tabla: sección de la base de datos donde se define un tipo de dato concreto que almacenar, la cual posee una serie de columnas que indican las características de cada registro
- Documento: mapeo explícito clave-valor para un registro
- Aggregate: operación procedural mediante el uso de pipelines que permite ejecutar procedimientos complejos sobre una tabla
- Group: pipeline que permite realizar operaciones sobre una tabla centrando los resultados sobre un valor
- Project: pipeline que permite manipular los datos a mostrar de una tabla y la forma en que éstos se muestran

### Sistemas y redes

- HTTP: protocolo de comunicación entre ordenadores usando la red
- venv: abreviatura de "virtual environment", en español entorno virtual, es decir, un intérprete separado de un lenguaje determinado existente solo en el ámbito (servidor, computadora, ...) que lo contiene
- API: acrónimo de Aplication Programming Interface, programa que se crea para que sirva de puente entre dos aplicaciones
- *\ REST: API cuyas request son en formato json
- *\ SOAP: API cuyas request son en formato xml
- Request: parámetros que se le proporcionan a una API para que ésta realice su trabajo
- *\ HTTP: request que usa el protocolo HTTP para transferir un objeto a una API con los parámetros de una operación, se compone de tres partes (línea, cabeza y cuerpo) y dos métodos (GET y POST)
- línea (Request HTTP): parte que lleva los datos de a dónde se dirige la request, el método y el protocolo HTTP a usar
- cabeza (Request HTTP): parte que engloba los metadatos de la request, como el dominio del servidor (Host)
- cuerpo (Request HTTP): parte de tamaño libre donde se almacenan los parámetros que usará la API en sí
- GET (Request HTTP): método usado para obtener datos de la API y que lleva una request de respuesta al servidor que la realiza
- POST (Request HTTP): método usado para proporcionar datos a la API

## Planteamiento del proyecto

> El proyecto se separa en dos partes, la base de datos a usar y la API que permitirá que ésta pueda ser usada por cualquier plataforma autorizada

### Tecnologías

> Se usarán las siguientes tecnologías para desarrollar el proyecto:
> 1. Base de datos:
>   * Python (3.6+)
>   * json
>   * pickle
>   * pprint
> 2. API:
>   * request

### La base de datos

#### Introducción

> Se busca crear una base de datos local documental. Para ello es recomendable usar un lenguaje de programación que sea débilmente tipado para que los documentos no tengan que depender de definiciones de tipos
> Asimismo, las que existen del mismo tipo o parecidos son basadas en javascript (por ejemplo, MongoDB), nos basaremos en otros lenguajes para hacer que nuestra base de datos sea un producto único en el mercado
> Por esto se elige Python, por ser otro lenguaje débilmente tipado con capacidades similares y que es a día de hoy uno de los lenguajes más usados
> Como Python es, por ser interpretado, un lenguaje lento, se realizarán las menos operaciones posibles almacenando datos voluminosos en memoria, por lo que cosas como acceder a las colecciones se hará mediante un json donde se indiquen los datos de la base de datos

#### Planteamiento

> La idea final es que nuestra base de datos tenga una sintaxis similar a esta

```python
db.coleccion.operacion(parametros)
```

> Donde:
> - db -> Instancia del objeto que nos apunta a una base de datos y sus parámetros (colecciones, accesos, ...)
> - coleccion -> Instancia del objeto que nos apunta a una colección extraída de "db"
> - operacion -> Método de "coleccion" que nos permite ejecutar una operación sobre la colección y sus datos
> - parametros -> Diccionario con los parámetros del método "operacion", los cuales pueden variar entre métodos

> También, por características del lenguaje, será posible encadenar operaciones

```python
db.coleccion.operacion1(parametros1).operacion2(parametros2)
```

> Esto nos permite ejecutar sobre la colección la operación 1 y después la operación 2. No obstante, para ejecutar según que operaciones de forma procedural no es posible realizar esto, por lo que se implementará un método con este fin

#### Clases

> En nuestra base de datos intervendrán cuatro clases básicas
> 1. BaseFile -> accede a un fichero con los datos
>   * Métodos
>     * get_collection: devuelve un objeto Collection que contiene una colección con un nombre determinado 
>     * create_collection: crea un archivo json con los datos necesarios para la existencia de una colección con un nombre determinado y altera el documento original para añadir ésta colección a las relacionadas a la base de datos
>     * delete_collection: elimina el archivo json de una colección con un nombre determinado y elimina la referencia a ésta en el json de la base de datos
>   * Parámetros
>     * file: el archivo json con los datos de la base de datos
>     * collections: diccionario con las colecciones, que sigue la estructura {nombre:ruta_al_archivo}
>
> Profundizando en el archivo de la base de datos, tendrá esta estructura
```js
{
    "name": "nombre_base_de_datos", //Nombre de la base de datos
    "collections": { //Colecciones asociadas a la base de datos, se convierte en Basefile.collections
        "coleccion1":"ruta/a/coleccion/1",
        "coleccion2":"ruta/a/coleccion/2",
        ...
    }
}
```

> 2. Collection
>    * Métodos:
>      * find: método para encontrar todos los registros cuyos campos cumplan unos requisitos. Los parámetros son de la forma `{"parametro1":"valor1","parametro2":"valor2"}`
>      * insert: método para insertar un nuevo registro en la colección con requisito de que sea coherente con el parámetro Collection.prototype
>      * delete: método que busca una serie de registros determinados (similar a Collection.find) y los elimina de la colección
>      * modify: método que busca una serie de registros determinados (similar a Collection.find) y les modifica sus valores de acuerdo a un segundo conjunto de pares clave-valor si éste es coherente con Collection.prototype
>      * aggregate: llama a un Aggregator para ejecutar una serie de operaciones procedurales proporcionadas como parámetros sobre la colección
>      * fetch_data: método que nos va a permitir obtener los datos de una operación Collection.find o Collection.aggregate para, mostrarlos por pantalla, mostrarlos por pantalla de forma visual u obtenerlos en un archivo, en cualquiera de los formatos csv o json
>    * Atributos:
>      * __col: los datos resultantes de una operación Collection.find o Collection.aggregate, no accesible al usuario para aumentar la seguridad de la base de datos