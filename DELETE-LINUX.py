import os
import sys
import subprocess
import shutil
import re

def print_banner():
    """Mostrar un banner ASCII bonito."""
    banner = """
  DDDD    EEEEE   L       EEEEE   TTTTT   EEEEE       L       I   N   N   U   U   X   X
  D   D   E       L       E         T     E           L       I   NN  N   U   U    X X
  D   D   EEEE    L       EEEE      T     EEEE        L       I   N N N   U   U     X
  D   D   E       L       E         T     E           L       I   N  NN   U   U    X X
  DDDD    EEEEE   LLLLL   EEEEE     T     EEEEE       LLLLL   I   N   N   UUUU   X    X  by @Isaac-maker
    """
    print(banner)

def get_linux_distro():
    try:
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if line.startswith('ID='):
                    distro_id = line.split('=')[1].strip().strip('"')
                if line.startswith('ID_LIKE='):
                    distro_like = line.split('=')[1].strip().strip('"')
                    if 'arch' in distro_like:
                        return 'arch'
                    elif distro_id in ['ubuntu', 'debian']:
                        return 'debian'
                    else:
                        print(f"Distribución {distro_id} no soportada.")
                        sys.exit(1)
    except FileNotFoundError:
        print("No se pudo determinar la distribución de Linux.")
        sys.exit(1)

def check_tool_installed(tool):
    return shutil.which(tool) is not None

def install_tool(tool, distro):
    package = 'coreutils' if tool == 'shred' else 'wipe'
    
    if distro == 'debian':
        cmd = ['sudo', 'apt', 'install', '-y', package]
    elif distro == 'arch':
        cmd = ['sudo', 'pacman', '-S', '--noconfirm', package]
    
    print(f"Instalando {package}...")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"Error al instalar {package}.")
        sys.exit(1)
    print(f"{package} instalado correctamente.")

def main():
    print_banner()  # Mostrar el banner al inicio
    
    print("Seleccione la herramienta a utilizar:")
    print("1. shred")
    print("2. wipe")
    opcion = input("Ingrese 1 o 2: ").strip()
    
    if opcion not in ['1', '2']:
        print("Opción no válida.")
        sys.exit(1)
    
    tool = 'shred' if opcion == '1' else 'wipe'
    distro = get_linux_distro()
    
    if not check_tool_installed(tool):
        install_tool(tool, distro)
    else:
        print(f"{tool} ya está instalado.")
    
    if tool == 'shred':
        while True:
            try:
                N = int(input("Iteraciones (1-64): "))
                if 1 <= N <= 64: break
                print("Número debe ser 1-64")
            except ValueError:
                print("Ingrese un número válido.")
        
        T = input("Extensiones (ej. MP4,jpg): ").strip().lower()
        extensions = [ext.strip() for ext in T.split(',') if ext.strip()]
        
        if not extensions:
            print("Debe ingresar al menos una extensión.")
            sys.exit(1)
        
        for ext in extensions:
            if not re.match(r'^[a-z0-9_]+$', ext):
                print(f"Extensión inválida: {ext}")
                sys.exit(1)
        
        patterns = ' '.join([f'*.{ext}' for ext in extensions])
        cmd = f"sudo shred -vxuz -n {N} {patterns}"
    else:
        while True:
            try:
                N = int(input("Pasadas (1-64): "))
                if 1 <= N <= 64: break
                print("Número debe ser 1-64")
            except ValueError:
                print("Ingrese un número válido.")
        
        T = input("Directorio a eliminar: ").strip()
        if not os.path.isdir(T):
            print(f"El directorio {T} no existe.")
            sys.exit(1)
        
        cmd = f"sudo wipe -p {N} -s -f -r {T}"
    
    print("\nComando a ejecutar:")
    print(cmd)
    confirm = input("¿Continuar? (s/n): ").lower()
    if confirm != 's':
        print("Operación cancelada.")
        sys.exit()
    
    print("Ejecutando...")
    result = subprocess.run(cmd, shell=True)
    print("Operación completada con éxito." if result.returncode == 0 else "Error al ejecutar")

if __name__ == "__main__":
    main()
