# Sistema de gestión de pólizas de seguro
Mini-sistema interno para que un asesor administre clientes y las pólizas asociadas a cada uno. Hecho con Django + PostgreSQL, corriendo en Docker.

## Funcionalidades

**Clientes**
- Crear un nuevo cliente.
- Ver el listado y el detalle de cada cliente.
- Editar o dar de baja un cliente.

**Pólizas**
- Crear una nueva póliza.
- Ver el listado y el detalle de cada póliza.
- Editar o dar de baja una póliza.
- Buscar y filtrar pólizas por estado o por número/cliente.
- Renovar una póliza vigente o vencida.
- Navegar entre una póliza y la anterior o la vigente, cuando forman parte de un historial de renovaciones.

**Tipos de póliza**
- Cargar un nuevo tipo de póliza.
- Ver el listado de tipos de póliza.
- Deshabilitar un tipo de póliza. 

## Cómo levantar el proyecto
1. Clonar el repositorio.
2. Copiar el archivo de variables de entorno:
   ```bash
   cp .env.example .env
   ```
3. Levantar los contenedores:
   ```bash
   docker compose up --build
   ```
Las migraciones se aplican automáticamente al levantar el proyecto.

4. Crear un superusuario para poder loguearte:
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```
5. Entrar a http://localhost:8000/, loguearte con ese usuario, y usar la app.


## Decisiones de modelado


### Tipos de póliza
Para el tipo de póliza (auto, hogar, vida...) opté por armar un catálogo aparte, en vez de dejarlo como una simple lista de opciones fija. La razón es que considero esto más práctico ya que ese catálogo lo administra el propio usuario y puede crecer con el tiempo (aparece un nuevo tipo de póliza, se deja de ofrecer otro) sin que eso implique tocar código ni hacer un nuevo deploy.

También puse una opción que permita "dar de baja" un tipo de póliza sin romper el historial: un tipo inactivo deja de estar disponible para pólizas nuevas, pero las pólizas que ya lo usaban lo conservan sin problema.

### Estado de la póliza
A diferencia del tipo de póliza, el estado (vigente / vencida / renovada) lo modele como una simple lista de opciones fija, no como un catálogo aparte. El criterio detrás de esta diferencia: un catálogo aparte tiene sentido cuando el conjunto de valores lo administra una persona del negocio y puede crecer o cambiar, como pasa con los tipos de póliza. El estado, en cambio, es un conjunto cerrado y fijo, definido por las reglas propias del sistema (que se venza la fecha, que alguien renueve) — nadie va a "agregar un estado nuevo" desde una pantalla de administración. Entiendo que armar un catálogo aparte para esto hubiera sido más complejo, sin ser realmente útil. 

### Numeración de pólizas
El número de póliza se genera automáticamente (con un prefijo “P” y una secuencia numérica) en vez de que lo cargue el usuario a mano, para evitar duplicados y errores de tipeo.
En un principio había usado un prefijo distinto para las pólizas que salen de una renovación, y después lo cambié para que todas usen el mismo prefijo. Ya que considere que el número es solo un identificador, no tiene por qué contar la historia de la póliza. Esa historia se guarda de forma explícita en otro lugar, conectando cada póliza con la que le dio origen — de ahí salen los botones para navegar entre la póliza anterior y la vigente en el detalle de cada una.

### Bajas de clientes y pólizas
En relación a esto decidí que un cliente no se puede eliminar si tiene pólizas asociadas, porque esas pólizas quedarían huérfanas (sin cliente al que pertenecer).
Con las pólizas, al principio permitía eliminarlas directamente de la base de datos, pero terminé cambiando ese criterio: aunque no conozco en profundidad la lógica de negocio de un seguro, me imagino que por cuestiones legales o de auditoría hace falta conservar el registro de una póliza aunque ya no esté vigente. Por eso, en vez de borrarla, la baja hace un "soft delete": la póliza se oculta de los listados, pero el registro se mantiene en la base de datos.

### Renovación de pólizas
En relación a esto permite que solo las pólizas vencidas o vigentes puedan ser renovadas. Y las renovadas no tienen esa opción ya que ya fueron renovadas, y solo quedan como parte del historial. 
Por otro lado, al renovar una póliza, en vez de generar la nueva póliza automáticamente con los mismos datos, se muestra antes una vista previa donde el administrador puede revisar y modificar la prima y las fechas antes de confirmar. Esto es porque en un seguro esos datos pueden variar de una renovación a otra, y no siempre se van a mantener igual que en la póliza anterior.

### Cómo resolví lo de "vencida"
El estado se calcula cada vez que alguien abre el listado de pólizas, comparando la fecha de vencimiento contra la fecha actual solo de las pólizas vigentes; en vez de correr un proceso en segundo plano. Esto se recalcula sobre las pólizas activas, antes de aplicar los filtros de búsqueda.
Se eligió este enfoque en vez de una tarea programada por simplicidad: me pareció que esta era una buena opción para el volumen de datos de este challenge. Con más volumen de pólizas, en una segunda iteración convendría mover este cálculo a una tarea periódica en vez de calcularlo en cada visita.

### Listado sin recargar la página
El mismo listado filtrable de pólizas (por estado y por búsqueda de número/cliente) también funciona sin recargar la página. Al aplicar un filtro, se consulta un endpoint que devuelve los datos, y la tabla se actualiza en vivo con eso, sin modificar la URL. 

### Inicio de sesión
Decidí sumar un panel de inicio de sesión y protegí las rutas de la aplicación: solo se puede acceder a ellas si primero se inició sesión.

### Qué dejaría para una segunda iteración
- Subcategorías dentro de los tipos de póliza — sé que en la vida real cada tipo (auto, hogar, vida...) tiene varias opciones dentro, y no llegué a modelar ese nivel de detalle.
- Filtro/búsqueda en el listado de clientes — la consigna solo lo pide para pólizas; lo dejé sin agregar por tiempo.
- Mover el cálculo de "vencida" a una tarea programada, para no depender de que alguien visite el listado.
- Mejoraría toda la parte frontend ya que considero que la deje muy sencilla debido a que me enfoque principalmente en la funcionalidades y en tratar de aprender estas nuevas tecnologías.


