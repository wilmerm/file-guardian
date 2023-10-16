import os
import hashlib
import base64
from cryptography.fernet import Fernet, InvalidToken


def secure_delete(path: str, auto=False,  verbose=True):
    """
    Elimina de forma segura los archivos y directorios en la ruta especificada.

    Parámetros:
        * `path` (str): La ruta al archivo o directorio que se desea eliminar.
            - Si la ruta es un directorio, se eliminará cada archivo y subdirectorio.
            - Si la ruta es un archivo, se sobrescribirá su contenido y se borrará.
        * `auto` (bool, Default False): Si es True, no se solicitará confirmación al usuario.
        * `verbose` (bool, Default True): Añade la opción 'v' al comando shred.

    Nota: Esta función utiliza el comando 'shred' y debe ejecutarse con permisos
    de administrador (sudo) para garantizar una eliminación segura.
    """
    if os.path.isdir(path):
        listdir = os.listdir(path)

        if not auto:
            prompt = f'¿Seguro desea eliminar permanentemente todos los archivos del directorio "{path}"? N/y: '
            if not confirm(prompt):
                return

        for filename in listdir:
            _path = os.path.join(path, filename)
            secure_delete(_path, auto=True, verbose=verbose)

    elif os.path.isfile(path) or os.path.islink(path):
        if not auto:
            prompt = f'¿Seguro desea eliminar permanentemente el archivo "{path}"? N/y: '
            if not confirm(prompt):
                return

        shred_options = 'fuvxz'

        if not verbose:
            shred_options = shred_options.replace('v', '')

        os.system(f'sudo shred -{shred_options} "{path}"')

    else:
        raise ValueError(f'"{path}" no es un archivo o directorio válido.')


def encrypt(path: str, key: str, delete=True):
    """
    Cifra archivos en una ruta dada utilizando una clave proporcionada.

    Parámetros:
        * `path` (str): La ruta al archivo o directorio que se desea cifrar.
        * `key` (str): La clave que se utilizará para cifrar los archivos.
        * `delete` (bool): Si es True, también eliminará el archivo original.

    1. La función recorre la ruta especificada y cifra los archivos encontrados.
    Si la ruta es un directorio, cifrará todos los archivos y subdirectorios
    de forma recursiva.

    2. Los archivos cifrados se guardarán con la extensión '.encrypted'.

    3. La clave debe ser una cadena (str) válida.

    Ejemplo de Uso:
    ```py
    key = 'clave_secreta'
    ruta = '/ruta/al/archivo_o_directorio'
    encrypt(ruta, key)
    ```
    """
    if os.path.isdir(path):
        for filename in os.listdir(path):
            _path = os.path.join(path, filename)
            encrypt(_path, key, delete)
    elif os.path.isfile(path) or os.path.islink(path):
        print(f'Cifrando "{path}"...')
        with open(path, 'rb') as file:
            text = file.read()
            encrypted_text = encrypt_text(text, key)
            with open(path + '.encrypted', 'wb') as encrypted_file:
                encrypted_file.write(encrypted_text)
        # Se procede a eliminar el archivo original (si aplica)
        if delete:
            print(f'Eliminando "{path}"...')
            secure_delete(path, auto=True, verbose=False)
    else:
        raise ValueError(f'"{path}" no es un archivo o directorio válido.')


def decrypt(path: str, key: str, delete=True):
    """
    Descifra archivos cifrados en una ruta dada utilizando una clave proporcionada.

    Parámetros:
        * `path` (str): La ruta al archivo o directorio que se desea descifrar.
        * `key` (str): La clave que se utilizará para descifrar los archivos.
        * `delete` (bool): Si es True, también eliminará el archivo cifrado.

    La función recorre la ruta especificada y descifra los archivos cifrados que
    encuentre. Si la ruta es un directorio, descifrará todos los archivos y
    subdirectorios de forma recursiva.

    Ejemplo de Uso:
    ```py
    key = 'clave_secreta'
    ruta = '/ruta/al/archivo_o_directorio'
    decrypt(ruta, key)
    ```
    """
    if os.path.isdir(path):
        for filename in os.listdir(path):
            _path = os.path.join(path, filename)
            decrypt(_path, key)
    elif os.path.isfile(path) or os.path.islink(path):
        print(f'Descifrando "{path}"...')
        with open(path, 'rb') as encrypted_file:
            encrypted_text = encrypted_file.read()
            text = decrypt_text(encrypted_text, key)
            with open(path.replace('.encrypted', '', 1), 'wb') as file:
                file.write(text)
        # Se procede a eliminar el archivo cifrado (si aplica)
        if delete:
            print(f'Eliminando "{path}"...')
            secure_delete(path, auto=True, verbose=False)
    else:
        raise ValueError(f'"{path}" is not valid file or directory.')


def encrypt_text(text: str | bytes, key: str):
    """
    Cifrar un texto o bytes utilizando una clave proporcionada.

    Parámetros:
        * `text` (str | bytes): El texto o bytes que se desea cifrar.
        * `key` (str): La clave que se utilizará para cifrar el texto.

    Retorna:
        bytes: El texto cifrado en forma de bytes.

    La función utiliza la biblioteca Fernet para cifrar el texto.

    Ejemplo de Uso:
    ```py
    key = 'clave_secreta'
    texto = 'Este es un mensaje confidencial.'
    texto_cifrado = encrypt_text(texto, key)
    print(texto_cifrado)
    ```
    """
    bkey = get_fernet_key(key)
    fernet = Fernet(bkey)
    bytes_text = text if isinstance(text, bytes) else text.encode()
    encrypted_text = fernet.encrypt(bytes_text)
    return encrypted_text


def decrypt_text(encrypted_text: str, key: str):
    """
    Descifrar un texto cifrado utilizando la clave proporcionada.

    Parámetros:
        * `encrypted_text` (str): El texto cifrado que se desea descifrar.
        * `key` (str): La clave que se utilizará para descifrar el texto.

    Retorna:
        str: El texto descifrado.

    La función utiliza la biblioteca Fernet para descifrar el texto.
    La clave debe ser la misma que se utilizó para cifrar el texto, de lo
    contrario, se generará una excepción ValueError.

    Ejemplo de Uso:
    ```py
    key = 'clave_secreta'
    texto_cifrado = '...'
    texto_descifrado = decrypt_text(texto_cifrado, key)
    print(texto_descifrado)
    ```
    """
    bkey = get_fernet_key(key)
    fernet = Fernet(bkey)

    try:
        text = fernet.decrypt(encrypted_text)
    except InvalidToken as e:
        raise ValueError('Clave incorrecta.')
    return text


def get_fernet_key(key: str):
    """
    Genera una clave Fernet a partir de una clave proporcionada.

    Esta función toma una clave como entrada y genera una clave Fernet
    utilizando el algoritmo MD5. La clave Fernet es necesaria para cifrar y
    descifrar texto de forma segura.
    """
    passcode = key.encode()
    assert isinstance(passcode, bytes)
    hlib = hashlib.md5()
    hlib.update(passcode)
    return base64.urlsafe_b64encode(hlib.hexdigest().encode())


def confirm(prompt: str):
    confirm = input(prompt)
    if confirm.lower() in ('y', 'yes'):
        return True
    return False
