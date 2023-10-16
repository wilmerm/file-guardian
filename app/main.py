import sys
from commands import (
    decrypt,
    decrypt_text,
    encrypt,
    encrypt_text,
    secure_delete,
)


# Define un diccionario de comandos y sus funciones asociadas
command_map = {
    'delete': secure_delete,
    'encrypt': encrypt,
    'decrypt': decrypt,
    'encrypt_text': encrypt_text,
    'decrypt_text': decrypt_text,
}


def show_help():
    """
    Muestra la información de uso del programa.
    """
    print('Uso: python secure_app.py [COMMAND] [OPTIONS]')
    print('Comandos disponibles:')
    for command, description in command_map.items():
        print(f'>> python secure_app.py {command} {description.__doc__.strip()}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Faltan argumentos. {sys.argv=}')
        show_help()
        exit(1)

    if sys.argv[1] in ('help', 'h'):
        print('Mostrando ayuda:')
        show_help()
        exit(0)

    command_name = sys.argv[1]
    options = sys.argv[2:]

    if command_name not in command_map:
        print(f'Comando "{command_name}" no válido.')
        show_help()
        exit(1)

    command = command_map[command_name]

    # Verifica si se proporcionan suficientes argumentos
    if len(options) < len(command.__annotations__):
        print(f'Faltan argumentos. Se requieren {len(command.__annotations__)} argumentos.')
        show_help()
        exit(1)

    # Ejecuta el comando con los argumentos proporcionados
    try:
        command(*options)
    except Exception as e:
        print(f'Error al ejecutar el comando "{command_name}": {str(e)}')


