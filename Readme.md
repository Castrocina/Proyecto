# Estructura

El codigo donde se trabajo el modelo inicial, sin refactorizar se encuentra en el archivo llamado cirrhosis.ipynb ubicado en la carpeta de notebooks.
Una vez refactorizado se debe crear el notebook refactorizado con otro nombre en la carpeta de notebooks y las classes en scripts de python y el codigo main se debe de guardar en la carpeta refactoring.
En la carpeta de data se van a guardar todos los archivos de datos, para poder llevar el control de sus versiones.
En la carpeta de models se van a guardar todos los modelos, para poder llevar el control de sus versiones
Se agrego la carpeta remote_storage, que contiene todos los archivos de dvc en su format de almacenamiento, para que puedan jalar los archivos sin ningun problema.

# Instrucciones de uso

El jupyter notebook se puede ejecutar de principio a fin una vez que se hayan instalado todas las librerias con el comando pip install -r requirments.txt.
para jalar los archivos de dvc simplemente hay que ejecutar el comando dv pull, eso deberia generar todos los archivos en local sin ningun problema dentro de la carpeta models y data.
Cuando se agregue un nuevo archivo de datos o se modifique uno existente hay que ejecutar el comando dvc ,/ add data y posteriormente el comando dvc push.
Cuando se agregue un nuevo archivo de modelo o se modifique uno existente hay que ejecutar el comando dvc ,/ add models y posteriormente el comando dvc push.
Para bajar todos los archivos de dvc hay que ejcutar el comando dvc pull (Avisarme si no funciona)

