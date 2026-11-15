---
title: "SPA_Samsung Drive Manager FAQ Ver 2.5.pdf"
source_file: "硬盘驱动文件\Samsung Drive Manager Manuals\Spanish\SPA_Samsung Drive Manager FAQ Ver 2.5.pdf"
type: 全量文档抽取
ext: ".pdf"
size_mb: "0.074"
modified: "2012-06-27"
is_backup: "否"
char_count: 11877
---

# 原文抽取：SPA_Samsung Drive Manager FAQ Ver 2.5.pdf

> 来源路径：`硬盘驱动文件\Samsung Drive Manager Manuals\Spanish\SPA_Samsung Drive Manager FAQ Ver 2.5.pdf` ｜ 类型：.pdf ｜ 大小：0.074MB ｜ 修改：2012-06-27 ｜ 备份：否

```text
Samsung Drive Manager Preguntas frecuentes

Instalación
P.: Mi disco duro externo Samsung está conectado, pero no sucede nada.
R.: Compruebe la conexión del cable USB. Si el disco duro externo Samsung está conectado correctamente, el LED estará iluminado.
R. Si el disco duro emite un sonido de tic tac, significa que el suministro eléctrico es insuficiente. Si puerto USB actual no reconoce el disco duro, pruebe a conectarlo a otro puerto USB.
P. No puedo instalar Samsung Drive Manager.
R.: Revise los requisitos mínimos del sistema para usar un disco duro externo Samsung. Consulte las especificaciones del sistema en el capítulo 1 del manual de usuario para obtener más información.
P. La ventana "Control de cuentas de usuario" aparece una y otra vez cuando ejecuto Samsung Drive Manager en Windows Vista. ¿ Có mo puedo hacer que deje de aparecer la ventana "Control de cuentas de usuario"?
R. Para poder usar Samsung Drive Manager para acceder directa o indirectamente a un disco duro externo es necesario elevar privilegios. El uso de Samsung Drive Manager queda restringido si no se autoriza el acceso del tipo "Control de cuentas de usuario". Para hacer que deje de aparecer la ventana "Control de cuentas de usuario",

seleccione Cuentas de usuario en el Panel de control y desactive el control de cuentas de usuario.

Samsung AutoBackup
P.: ¿ De qué debería hacer copias de seguridad?
R. En general, se deben hacer copias de seguridad de los archivos de datos generados al utilizarse otro software. No se recomienda realizar copias de seguridad de los archivos de programa, ya que, si hubiera problemas con el equipo, los programas tendrán que volver a instalarse. Se recomienda hacer copias de seguridad de archivos de datos que se puedan restaurar posteriormente.
P. ¿ Con qué frecuencia debo hacer copias de seguridad de los datos?
R. Si no realiza copias de seguridad con frecuencia, se recomienda que haga copias de seguridad de los archivos importantes, los datos personales como por ejemplo imágenes y archivos que no se puedan volver a crear o que sean difíciles de crear.
P. A pesar de que algunos archivos incluían cambios, la copia de seguridad en tiempo real no los ha incluido.
R. Samsung AutoBackup no puede hacer una copia de seguridad en tiempo real de un archivo que cambie si éste no se ha configurado como origen de copia de seguridad. Asegúrese de que los tipos de archivo de los que quiera hacer copias de seguridad en tiempo real se hayan definido a tal efecto.

R. Otra causa puede ser que se haya incluido una carpeta o un archivo del SO en un origen de copia de seguridad. Samsung AutoBackup no puede hacer copias de seguridad de este tipo de archivos, ya que los estará utilizando el sistema. Asegúrese de que las carpetas y los archivos del sistema SO no se hayan incluido como origen de copia de seguridad.
P. Utilizo Samsung AutoBackup en Windows Vista o en Windows 7, pero no puedo ver los datos de los cuales se ha hecho copia de seguridad ni los registros de las copias de seguridad.
R. Este problema lo causa la función Control de cuentas de usuario que se introdujo con la versión Windows Vista.
Un HDD con formato NTFS en Windows XP no tiene otorgado el derecho
(Usuarios autenticados) cuando se ha aplicado el formato en Windows Vista o en Windows 7. Si se conecta un HDD sin este derecho a Windows Vista o a Windows 7 y se utiliza, los datos de copia de seguridad no se actualizan correctamente.
※ FAT32 no se ve afectado por este problema.
P. Tengo suficiente espacio disponible en mi disco duro externo Samsung, pero no puedo hacer copias de seguridad de archivos de más de 2 GB o 4 GB.

R. El tamaño de archivo máximo del que se puede hacer una copia de seguridad depende del sistema de archivos del disco duro externo Samsung.

Tabla 1: sistema de archivos

Tipo de sistema de archivos

Tamañ o máximo de archivo de copia de
seguridad

FAT

2 GB

FAT32

4 GB

NTFS

16 TB

R. Para hacer una copia de seguridad de un archivo de más de 2 GB, el sistema de archivos debe cambiarse a FAT32 o a NTFS. Para hacer una copia de seguridad de un archivo de más de 4 GB, el sistema de archivos debe cambiarse a NTFS.
NOTA: SI SE CAMBIA EL SISTEMA DE ARCHIVOS, TODOS LOS DATOS ALMACENADOS EN SU DISCO DURO
EXTERNO SAMSUNG SE ELIMINARÁ N. HAGA UNA COPIA DE SEGURIDAD DE TODOS LOS DATOS IMPORTANTES EN OTRO DISCO DURO ANTES DE CAMBIAR EL SISTEMA DE
ARCHIVOS.

P. He formateado el equipo y he vuelto a instalar Windows. ¿ Cómo puedo restaurar mis datos de copia de seguridad en otro dispositivo?

R. Instale Samsung Drive Manager y ejecute Samsung AutoBackup. A continuación, seleccione los datos que quiera restaurar en la lista de trabajos. Los datos de copia de seguridad se pueden usar así (consulte el capítulo 2 del manual del usuario para obtener más información).
P. Tras producirse un fallo en el proceso de copia de seguridad, comprobé el registro de copia de seguridad y vi que se habían producido varios fallos.
R. No es posible acceder a los archivos del SO para hacer copias de seguridad. No es posible crear copias de seguridad de los archivos del SO. Este problema se produce a menudo cuando se define una carpeta de Windows o una carpeta de "Archivos de programa" como origen de copia de seguridad. Para evitar que esto suceda, no defina una carpeta raíz entera como origen de copia de seguridad. Defina sólo carpetas de usuario como orígenes de copia de seguridad.
R. Otra manera de evitar esta situación es excluir el archivo fallido como origen de copia de seguridad y volver a realizar la operación de copia de seguridad.
P.: He formateado mi disco duro externo Samsung y su software Samsung se ha eliminado.
R. El software Samsung que acompaña al disco duro externo Samsung se puede descargar desde el sitio web de asistencia técnica al cliente de Samsung. (http://www.samsung.com/sec)

P. He realizado una copia de seguridad de un programa que se instaló cuando yo instalé un producto. Tuve un problema con el producto, así que eliminé el programa y restauré el archivo de copia de seguridad, pero no puedo ejecutar el producto. ¿ He hecho algo mal durante el proceso de copia de seguridad y restauración?
R. Todos los programas de software requieren un entorno concreto para poder ejecutarse. Cuando se instala un programa en un equipo, también se instala un entorno junto con los archivos de programa y, cuando se ejecuta el programa, se prueba el entorno instalado. Puesto que Samsung AutoBackup no hace una copia de seguridad de este entorno, el programa no se puede ejecutar, incluso a pesar de que se haya hecho una copia de seguridad de él y se haya restaurado.
P.: Cuando se está ejecutando Samsung AutoBackup no puedo retirar mi disco duro externo Samsung mediante la función "Quitar hardware de forma segura".
R. El disco duro externo Samsung no se puede quitar de forma segura cuando se está utilizando. Pruebe de nuevo después de cerrar Samsung AutoBackup.
P.: La transferencia de archivos tarda demasiado.
R. Si su equipo no admite USB 2.0 o 3.0, o bien si el disco duro externo Samsung está conectado a un puerto distinto al puerto USB 2.0 o 3.0, la velocidad de transferencia de

archivos se verá mermada. Conecte su disco duro externo Samsung a un puerto que admita USB 2.0 o superior.
P. No puedo copiar archivos en mi equipo Macintosh.
R. La compatibilidad de los sistemas de archivos puede ser un problema. Si el formato aplicado al disco duro externo Samsung es NTFS, los datos almacenados sólo se podrán leer en un sistema Macintosh.
P.: Cuando compruebo mis archivos de copia de seguridad en mi dispositivo de copia de seguridad, aparece un mensaje que me indica que el archivo no tiene el formato adecuado y que los archivos no se pueden leer.
R. Si se ha seleccionado Copia seg. cifrada en las opciones de copia de seguridad, los archivos se cifrarán antes de realizar la copia de seguridad. Cuando se abre un archivo cifrado, se produce un error o aparece un mensaje que indica que el archivo no tiene el formato adecuado. Antes de poder abrirse, deberá restaurarse el archivo cifrado.
P. He realizado una copia de seguridad con la opción "Cifrar" activada, pero sólo se han cifrado los archivos seleccionados.
R. Sólo se cifran, y se crea copia de seguridad de ellos, los archivos cuya copia de seguridad se ha realizado después de activar Cifrar. Los archivos cuya copia de seguridad se ha creado antes de activar Cifrar no se cifran. Esto significa

que puede haber al mismo tiempo en el mismo dispositivo de copia de seguridad tanto archivos cifrados como no cifrados.
P.: ¿ Puedo conectar un disco duro externo Samsung que contenga datos de copia de seguridad de otro equipo y restaurar los datos de copia de seguridad? Si es así, ¿ cómo?
R. Para restaurar y usar datos cuya copia de seguridad se ha realizado desde otro equipo, conecte su disco duro externo Samsung al equipo e instale Samsung Drive Manager. A continuación, ejecute Samsung Auto Backup y seleccione el archivo de copia de seguridad que quiera restaurar.
P.: ¿ Cómo puedo comprobar los resultados de las operaciones de copia de seguridad, restauración o eliminación?
R. Después de finalizar la operación de copia de seguridad, restauración o eliminación, podrá ver el resultado en "Registro", en el menú de trabajos en la pantalla de Samsung AutoBackup.

Samsung SecretZone
P.: ¿ Có mo puedo proteger mi unidad segura de otros usuarios?
R.: Seleccione la imagen que quiera proteger en Samsung SecretZone y luego elija "Desconectar". Los demás usuarios no podrán ver la unidad segura hasta que el administrador seleccione "Conectar".
P.: ¿ Có mo puedo utilizar mi unidad segura otra vez después de volver a instalar el SO?
R.: Para volver a utilizar su unidad segura después de instalar el SO, vuelva a instalar Samsung Drive Manager, conecte el disco duro externo Samsung, seleccione la unidad segura que quiera usar en Samsung SecretZone y haga clic en "Conectar".
P.: ¿ Cuál es el tamañ o máximo de la unidad segura?
R.: El tamaño de una unidad segura puede ser tan grande como el espacio libre disponible en el disco duro externo Samsung.

P.: ¿ Qué debo hacer si olvido la contraseñ a?
R.: Samsung SecretZone es un programa de seguridad y la unidad segura no se puede utilizar si no se proporciona la contraseña correcta. Asegúrese de que la contraseña que defina para la unidad segura sea una que pueda recordar fácilmente.
P.: Cuando se está ejecutando Samsung SecretZone no puedo retirar mi disco duro externo Samsung mediante la funció n "Quitar hardware de forma segura".
R.: Desconecte todas las unidades seguras que se estén ejecutando, cierre Samsung SecretZone y, a continuación, retire de forma segura el disco duro externo Samsung.

P.: Tras activar "Conexió n automática" en mi unidad segura, ésta no se conecta.
R.: Dependiendo de las especificaciones de su PC, es posible que se tarde un rato en conectar el disco duro externo Samsung. Espere un momento hasta que se establezca la conexión.
P.: Aparece un mensaje de error cuando desconecto la unidad segura.
R.: Si la unidad segura se desconecta inmediatamente después de copiar o guardar un archivo grande o varios archivos, es posible que se produzca un error. Si así sucede, pruebe de nuevo transcurridos 30 segundos o un minuto.

Samsung Secure Manager
P.: ¿ Puedo desbloquear el disco duro externo Samsung sin instalar Samsung Drive Manager?
R.: Conecte el disco duro externo Samsung, ejecute Secure Unlocker_win.exe dentro de la unidad de CD que se ve en "Mi PC" y, a continuación, introduzca su contraseña para desbloquear el disco.
A. Secure Unlock_mac.app es la versión de este ejecutable para Macintosh.
P.: ¿ Para qué sirve la función Restablecer valores de fábrica?
R.: La función Restablecer valores de fábrica borra todos los datos guardados en el disco duro externo y restaura la configuración de seguridad predeterminada.
```
