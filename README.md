Proyecto: Sistema de Gestión de Inventario 

Alumno: Abraham Garza

Materia: Diseño y Arquitectura de Software

Fecha: Abril 2026
¿Qué problema resuelve mi aplicación?

Queria hacer una aplicacion sencilla para un inventario de videojuegos y consolas, se puede registrar los datos principales y como uso un mismo cuadro de texto de entrada se puede usar para mas que consolas y juegos, asi como coleccionables u otro tipo de objetos que se puedan vender en ese tipo de tiendas. Se supone que automatiza un proceso de auditoria para llegar un historial de los movimientos sin interrumpir el agregado a la base de datos, por eso los microservicios.
¿Cuál era el problema del monolito?

Esto mas que nada para evitar que procesos se vean afectados por otros procesos, como lo es el caso de agregar inventario al stock y procesar datos enviandolos a la base de datos, si la aplicacion es un monolito toda la aplicacion se puede bloquear por un solo proceso que no este funcionando bien, puede funcionar para proyectos pequeños pero cuando se trabaja a grande escala es mejor migrar a microservicios.

¿Qué responsabilidad tiene cada microservicio?
El servicio a solo recibe los datos del formulario de la pagina principal y los registra en la tabla de productos, el servicio b recibe la notificacion del servicio a y genera un log para despues guardarlo de manera permanente en la tabla auditoria_stock

¿Cómo se comunican los servicios?

Por medio de una peticion POST. En el codigo solo se uso el nombre del servicio "servicio_b:5001". Esto por el DNS interno de DOcker donde reconoce los nombres de los contenedores de la misma red y los conecta automaticamente.

Tablas en la base de datos
Tabla	Servicio dueño	Qué guarda
productos	Servicio A	Nombre de la consola y el stock inicial.
auditoria_stock	Servicio B	El historial de registros y confirmaciones de seguridad.

¿Qué pasa si el Servicio B se cae?

En la prueba cuando se apago el servicio B, la aplicacion no se detiene al ser basada en microservicios, el servicio a al detectar la ausencia del b, muestra en pantalla que esta en "mantenimiento" pero guardandolo temporalmente hasta que vuelva a tener conexion. Asi si una parte falla el sistema principal puede seguir encendido.

Cómo levantar el proyecto

# 1. Clonar el repositorio
git clone https://github.com/Yugidar/abraham-garza-microservicios.git

# 2. Entrar a la carpeta
cd abraham-garza-microservicios/microservicios

# 3. Configurar las variables de entorno en docker-compose.yml
# (cambiar DB_HOST con el endpoint de RDS, DB_USER, DB_PASSWORD, DB_NAME)

# 4. Levantar
docker-compose up --build -d

# 5. Abrir en el navegador
http://184.73.30.154:5000

Reflexión Final

Lo mas dificil fue asegurarse de que todo funcionara bien, primero la pagina no estaba abriendo pero era por que no estaba configurada la regla de entrada del puerto 500 dentro de los grupos de seguridad, luego era detectar por que el servidor no dejaba conectarse internamente y era por que en el codigo habian ciertas partes del codigo que estaban extras, luego era ver por que aveces el docker-compose no construia la imagen y era por que la version indicada no era la correcta entonces tenia que eliminar la version indicada, o que estaba usando el nombre incorrecto de la base de datos y por eso no se conectaba a ella, tal cual no hubo algo en especifico que se me hiciera mas dificl, simplemente fue el proceso de hacer troubleshooting junto a la IA para ver que estaba mal y como se podia arreglar.
Entendi que la migracion a microservicios puede ser dificl y tediosa y mas teniendo en cuenta que en una situacion real se pueden esta manejando con cientos de miles de datos, en mi caso fue solo un base de datos con dos tablas, y con un monolito con solo dos procesos, pero en un  entorno real donde los servicios dentro del monolito pueden llegar a los cientos de de miles de datos y los procesos dentro del monolito pueden ser arriba de 50 la migracion si podria ser mas batallosa y puedo entender por que quiza algunas personas mejor opten por quedarse con esta estructura.
En una situacion real usaria monolitos realmente para cualquier cosa, aun si estas construyendo un proyecto realtivamente pequeño creo que vale la pena hacer el esfuerzo de implementar microservicios desde un principio para hacer el flujo de trabajo mas facil y evitar que si quieres escalar el proyecto en un futuro no tengas que estar batallando con la migracion, pero si se busca un caso mas especifico creo que el mejor de los casos seria un banco donde la confidencialidad es sumamente importate, con eso te aseguras de que los microservicios puedan llevar a cabo cualquier tipo de operacion que requiera maxima seguridad.

Checklist de Autoevaluación

MONOLITO

    [x] El código del monolito original está en la carpeta /monolito

    [x] El Dockerfile del monolito existe y es funcional

    [x] Hay captura del docker build sin errores

    [x] Hay captura del docker run con el contenedor corriendo

    [x] Hay captura de Apache Benchmark mostrando saturación

README

    [x] Explica el dominio de la aplicación

    [x] Explica el problema del monolito con sus propias palabras

    [x] Define la responsabilidad de cada servicio en una oración

    [x] Explica la comunicación entre servicios

    [x] Incluye los comandos para levantar el proyecto

    [x] Incluye la reflexión final
