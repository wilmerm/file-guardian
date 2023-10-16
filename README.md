# Aplicación de Cifrado y Eliminación Segura

Esta aplicación de Python te permite cifrar archivos y directorios de forma segura utilizando la biblioteca Fernet y eliminarlos permanentemente con el comando 'shred'. Es útil para proteger datos confidenciales y garantizar que no puedan ser recuperados.

## Características Principales

- **Cifrado Seguro:** Utiliza la biblioteca Fernet para cifrar archivos y directorios con una clave proporcionada.

- **Eliminación Segura:** Elimina permanentemente archivos y directorios con el comando 'shred', garantizando la eliminación segura de datos.

- **Recursividad:** La aplicación puede cifrar y eliminar archivos en directorios de forma recursiva.

- **Opciones de Confirmación:** Puedes configurar la aplicación para requerir confirmación del usuario antes de cifrar o eliminar archivos.

## Requisitos

- Python 3.x
- Bibliotecas: cryptography, hashlib

## Uso

### Uso de main.py y guardian.sh

El archivo `main.py` es el punto de entrada para ejecutar la aplicación. Puedes utilizarlo para ejecutar los comandos de cifrado, descifrado y eliminación segura desde la línea de comandos. Además, hay un script bash llamado `guardian.sh`, que simplifica la ejecución de comandos en la aplicación. Puedes usar `guardian.sh` para ejecutar comandos fácilmente.

Para ejecutar un comando con guardian.sh, utiliza el siguiente formato:

```sh
./guardian.sh [COMMAND] [OPTION1] [OPTION2]
```

Por ejemplo, para cifrar un archivo:

```sh
./guardian.sh encrypt /ruta/al/archivo clave_secreta
```


### Cifrado de Archivos y Directorios

Puedes cifrar archivos y directorios utilizando el comando `encrypt`. La función recorre la ruta especificada y cifra los archivos encontrados. Si la ruta es un directorio, cifrará todos los archivos y subdirectorios de forma recursiva.

Ejemplo:

```py
key = 'clave_secreta'
ruta = '/ruta/al/archivo_o_directorio'
encrypt(ruta, key)
```

### Descifrado de Archivos y Directorios

Para descifrar archivos cifrados, utiliza la función `decrypt`. Al igual que con el cifrado, esta función puede recorrer directorios de forma recursiva.

Ejemplo:

```py
key = 'clave_secreta'
ruta = '/ruta/al/archivo_o_directorio'
decrypt(ruta, key)
```

### Eliminación Segura

La eliminación segura de archivos y directorios se realiza con la función `secure_delete`. Esta función utiliza el comando 'shred' y debe ejecutarse con permisos de administrador (sudo) para garantizar una eliminación segura. Puedes configurar si se requiere confirmación del usuario antes de la eliminación.

Ejemplo:

```py
ruta = '/ruta/al/archivo_o_directorio'
secure_delete(ruta)
```

### Cifrado y Descifrado de Texto

También puedes cifrar y descifrar texto utilizando las funciones `encrypt_text` y `decrypt_text`. Estas funciones son útiles para proteger mensajes y datos confidenciales.

Ejemplo:

```py
key = 'clave_secreta'
texto = 'Este es un mensaje confidencial.'
texto_cifrado = encrypt_text(texto, key)
```

## Configuración

Asegúrate de instalar las bibliotecas requeridas. Puedes hacerlo con el siguiente comando:

```sh
pip install -r requirements.txt
```

Asegúrate de que tienes permisos de administrador (sudo) para utilizar la eliminación segura.

## Contribuciones

Si deseas contribuir a esta aplicación o informar sobre problemas, no dudes en abrir un problema o enviar una solicitud de extracción en el repositorio de GitHub.

## Licencia

Esta aplicación se distribuye bajo la Licencia MIT.



