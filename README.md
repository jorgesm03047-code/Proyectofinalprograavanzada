# proyectofinal
T-Bank

Banco de Tiempo Comunitario

La plataforma que convierte tu tiempo en la moneda más valiosa de tu comunidad.


¿Qué es T-Bank?

T-Bank es un sistema de gestión comunitaria donde las personas intercambian servicios usando horas como moneda (sin dinero de por medio).

¿Sabes cocinar? ¿Dar clases? ¿Reparar cosas? Todo eso tiene valor. Ayudas a alguien durante 2 horas → ganas 2 horas. Usas esas horas para recibir ayuda de otro vecino.

Nadie pierde. Todos ganan. La comunidad crece.


¿Para quién es?

Colonias y barrios - Fortalecen lazos entre vecinos y reducen gastos cotidianos.
Adultos mayores - Acceden a ayuda con trámites, tecnología o compras sin pagar.
Estudiantes - Ofrecen sus conocimientos y reciben servicios que necesitan.
Personas con oficios - Monetizan sus habilidades sin necesidad de dinero en efectivo.
Organizaciones comunitarias - Gestionan redes de voluntariado de forma ordenada y transparente.
Municipios y gobiernos locales - Implementan programas de economía solidaria con trazabilidad total.


¿Cómo funciona?

Te registras con tu nombre y colonia — en menos de un minuto ya eres parte de la red.

Publicas lo que sabes hacer — clases, cocina, plomería, cuidados, transporte, tecnología y más.

Exploras el catálogo de servicios que tu comunidad ofrece y solicitas lo que necesitas.

Confirman el intercambio — ambas partes validan que el servicio se realizó.

Las horas se acreditan automáticamente a tu saldo. Úsalas cuando quieras.

Valoras la experiencia — construyendo una red de confianza entre vecinos.


¿Qué puedes ofrecer o solicitar?

Educación — clases, tutorías, idiomas, apoyo escolar

Hogar — plomería, electricidad, limpieza, jardinería

Salud y cuidados — cuidado de adultos mayores, primeros auxilios

Tecnología — soporte técnico, redes sociales, computación básica

Cocina — recetas, talleres, preparación de alimentos

Transporte — traslados, mandados, acompañamiento


¿Te interesa implementarlo en tu comunidad?

Este sistema está diseñado para ser adoptado por colonias, asociaciones vecinales, municipios, OSC y cualquier organización que quiera fortalecer los lazos de su comunidad a través del intercambio solidario.

“Conectando personas. Fortaleciendo comunidades.”


Estructura del Código

El sistema está estructurado bajo principios de orientación a objetos y modularidad en Python, dividiendo las responsabilidades en distintas carpetas para facilitar su mantenimiento y escalabilidad.

Punto de Entrada

main.py
Es el archivo principal que inicializa la aplicación con CustomTkinter. Carga la base de datos local y gestiona el flujo de navegación entre la pantalla de autenticación y los respectivos paneles de control.

Requerimientos

requirements.txt
Define las dependencias necesarias de terceros para que la interfaz gráfica, gráficas estadísticas y recursos de iconos funcionen correctamente.

Modelo de Negocio (clases)

usuario.py
Define la clase base para cualquier tipo de usuario en el sistema con sus datos generales.

consumidor.py
Clase que hereda de Usuario. Contiene la lógica del usuario común, permitiendo solicitar e iniciar intercambios, confirmar servicios y valorar.

administrador.py
Clase que hereda de Usuario. Implementa los privilegios del administrador como suspender o activar cuentas y procesar aclaraciones.

servicio.py
Modela las ofertas de servicio creadas por la comunidad, conteniendo título, descripción y costo en horas.

intercambio.py
Modela el contrato de un intercambio específico y gestiona la progresión de sus estados.

transaccion.py
Lleva el control de la transferencia de horas entre el emisor y el receptor.

Interfaz de Usuario (pantallas)

login.py
Maneja las interfaces para iniciar sesión y el formulario de registro de nuevos usuarios.

panel_usuario.py
Pantalla principal para el rol de consumidor. Permite ver el saldo, explorar el catálogo de servicios locales, gestionar intercambios y responder notificaciones.

panel_admin.py
Pantalla de administración. Proporciona estadísticas generales, listado interactivo para gestionar estados de cuentas y el buzón de disputas.

dialogs.py
Contiene cuadros de diálogo interactivos para publicar servicios, transferir horas de forma manual, ingresar retroalimentaciones y reportar incidentes.

Base de Datos (database)

basededatos.py
Gestiona la persistencia de datos localmente. Se encarga de leer, escribir y actualizar los archivos planos CSV de forma dinámica sin necesidad de servidores externos.

Almacenamiento de Datos (data)

En este directorio se encuentran los archivos CSV que simulan las tablas de la base de datos:
usuarios.csv - Listado de cuentas y credenciales.
servicios.csv - Base de servicios ofrecidos.
intercambios.csv - Solicitudes de intercambio y su estado.
transacciones.csv - Historial de transferencias de horas de tiempo.
notificaciones.csv - Mensajes y alertas del sistema para cada usuario.
valoraciones.csv - Reseñas y puntajes otorgados al finalizar intercambios.
aclaraciones.csv - Casos de mediación reportados a los administradores.

Estilos y Recursos (assets)

styles.py
Configuración de la paleta de colores y tipografía de la interfaz.

icons.py
Controlador para importar y redimensionar los iconos requeridos en los paneles.


Cuentas de Prueba

Para realizar pruebas completas y verificar el comportamiento del sistema desde diferentes roles, puede iniciar sesión con las siguientes credenciales:

Rol Administrador

Permite visualizar disputas abiertas, ver estadísticas generales y suspender o reactivar cuentas de usuarios.
Correo electrónico: admin@timebank.com
Contraseña: admin123

Rol Consumidor (Usuarios de prueba)

Permite publicar servicios, explorar la red, solicitar intercambios y transferir saldo en horas.

Usuario Juan
Correo electrónico: juan@email.com
Contraseña: 1234

Usuario María
Correo electrónico: maria@email.com
Contraseña: 1234

Usuario Carlos
Correo electrónico: carlos@email.com
Contraseña: 1234

Usuario Lalo
Correo electrónico: lalo@gmail.com
Contraseña: 1234


Instrucciones de Instalación y Ejecución

Asegúrese de contar con Python 3.8 o superior instalado en su computadora.

Instalar dependencias obligatorias
Abra una ventana de comandos en la carpeta raíz del proyecto y ejecute:
pip install -r requirements.txt

Lanzar el programa
Una vez configuradas las dependencias, inicie la aplicación ejecutando:
python main.py


Desarrollado en Puebla, México — 2026.