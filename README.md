Proyecto: Sistema de Gestión de Inventario "Garza Gaming"

Alumno: Abraham Garza

Materia: Diseño y Arquitectura de Software

Fecha: Abril 2026 
¿Qué problema resuelve mi aplicación?

Mi aplicación ayuda a una tienda de videojuegos a llevar el control de su stock de consolas de manera eficiente. Registra las entradas de inventario y, de forma automática, genera un log de auditoría en segundo plano para asegurar que cada movimiento quede guardado por seguridad sin que el vendedor tenga que esperar a que el proceso termine.
¿Cuál era el problema del monolito?

Cuando probé el monolito original con Apache Benchmark, me di cuenta de que el sistema era muy lento porque intentaba hacer todo al mismo tiempo. Si yo configuraba un retraso para simular el guardado de un log pesado, la terminal me mostraba que las peticiones se quedaban "en cola" y el tiempo de respuesta era eterno. Básicamente, un solo usuario pesado podía dejar a toda la tienda sin poder usar el sistema.
¿Qué responsabilidad tiene cada microservicio?

    Servicio A: Es el recepcionista del sistema; recibe los datos de la consola desde el formulario, los guarda en la tabla productos y le avisa al segundo servicio que debe auditar el movimiento.

    Servicio B: Es el especialista en seguridad; recibe el aviso de A, espera el tiempo necesario para procesar el log y finalmente guarda el resultado en la tabla auditoria_stock.

¿Cómo se comunican los servicios?

Utilicé la librería requests para que el Servicio A hiciera una llamada HTTP tipo POST hacia el Servicio B. Lo interesante aquí es que no usé una dirección IP, sino el nombre http://servicio_b:5001. Esto funciona porque Docker actúa como un directorio telefónico interno que traduce ese nombre a la dirección correcta dentro de su red privada.
Tablas en la base de datos
Tabla	Servicio dueño	Qué guarda
productos	Servicio A	

Nombre de la consola y la cantidad registrada
auditoria_stock	Servicio B	

El mensaje de confirmación del log de seguridad
¿Qué pasa si el Servicio B se cae?

Durante mi prueba de resiliencia, apagué el contenedor del Servicio B y volví a usar el formulario. Lo que observé es que el Servicio A no falló; simplemente me mostró un mensaje diciendo que el servicio de auditoría estaba en mantenimiento. Esto es genial porque el inventario se siguió guardando en la base de datos y la tienda pudo seguir operando aunque una parte del sistema estuviera caída.
