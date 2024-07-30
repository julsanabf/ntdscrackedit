#!/usr/bin/python3
import argparse
import subprocess

def setColors():
    # Definir colores para texto a desplegar en consola
    global RED
    global BLUE
    global GREEN
    global YELLOW
    global PURPLE
    global CYAN
    global END
    RED = "\33[91m"
    BLUE = "\33[94m"
    GREEN = "\033[32m"
    YELLOW = "\033[93m"
    PURPLE = '\033[0;35m' 
    CYAN = "\033[36m"
    END = "\033[0m"

def showBanner():
    print(f"""
{YELLOW}
 __    _  _______  ______   ___   _______    _______  ______    _______  _______  ___   _  _______  ______   
|  |  | ||       ||      | |   | |       |  |       ||    _ |  |   _   ||       ||   | | ||       ||    _ |  
|   |_| ||_     _||  _    ||   | |  _____|  |       ||   | ||  |  |_|  ||       ||   |_| ||    ___||   | ||  
|       |  |   |  | | |   ||   | | |_____   |       ||   |_||_ |       ||       ||      _||   |___ |   |_||_ 
|  _    |  |   |  | |_|   ||   | |_____  |  |      _||    __  ||       ||      _||     |_ |    ___||    __  |
| | |   |  |   |  |       ||   |  _____| |  |     |_ |   |  | ||   _   ||     |_ |    _  ||   |___ |   |  | |
|_|  |__|  |___|  |______| |___| |_______|  |_______||___|  |_||__| |__||_______||___| |_||_______||___|  |_|

Herramienta para automatizar el proceso de NTLM hash cracking a partir de hashes obtenidos de un archivo NTDIS.DIT

+---------------------------------------------+
|       Autor: Julio Sanabria Figueredo       |
|                Versión 1.0                  |
|        https://github.com/julsanabf         |
+---------------------------------------------+

""")

def crackHashes(hashfilepath, wordlistpath):
    # Preparar archivo temphashes.txt para ser utilizado por hashcat
    hashfile = open(hashfilepath)
    
    temphashesfile = open('/tmp/temphashes.txt','w')
    crackedhashesfile = open('/tmp/crackedhashes.txt','w')
    hashesformatted = {}
    crackedhashesformatted = {}
    
    for line in hashfile:
        hashesformatted.update({line.split(':')[0]: line.split(':')[3].strip()})
        temphashesfile.write(f"{line.split(':')[3]}\n")
    
    temphashesfile.close()
    
    # Crack hashes
    print(f"{CYAN}[*] Cracking hashes")
    cmdcrack = ['hashcat', '-m', '1000', '/tmp/temphashes.txt', wordlistpath]
    try:
        subprocess.run(cmdcrack, capture_output=True, text=True)
    except Exception as e:
        print(f"{RED}Error al realizar cracking de hashes: {e}")

    # Obtener hashes crackeados con --show
    print(f"{CYAN}[*] Procesando resultados")
    cmdshow = ['hashcat', '-m', '1000', '/tmp/temphashes.txt', wordlistpath, '--show']
    try:
        result = subprocess.run(cmdshow, capture_output=True, text=True)
        line = result.stdout
        crackedhashestemp = line.split('\n')
        crackedhashestemp.pop()
        crackedhashesfile.write(result.stdout)
        
        for item in crackedhashestemp:
            crackedhashesformatted.update({item.split(':')[0]: item.split(':')[1]})    
    except Exception as e:
        print(f"{RED}Error al mostrar resultado de hashes crackeados: {e}")
    
    # Invocar método de procesamiento de datos para generar resultados
    if hashesformatted and crackedhashesformatted:
        print(f"{CYAN}[*] Desplegando resultados: (usuario:contraseña)\n")
        return procesarResultados(hashesformatted, crackedhashesformatted)
    print(f"{YELLOW}No se pudo obtener hashes crackeados")
    return {}

def procesarResultados(hashesformatted, crackedhashesformatted):
    resultados = {}
    
    # Mapear hashes crackeados con los usuarios correspondientes
    for k_cracked_hashes in crackedhashesformatted.keys():
    	for v_hashes_formatted in hashesformatted.values():
    	    if k_cracked_hashes == v_hashes_formatted:
    	        users = getKey(v_hashes_formatted,hashesformatted)
    	        for user in users:
    	            resultados.update({user: crackedhashesformatted[k_cracked_hashes]})
    return resultados

# Generar archivo de resultados y desplegarlos en pantalla
def guardarResultados(resultados, resultsfilepath):
    resultsfile = open(resultsfilepath, 'w')
    resultsfile.close()
    resultsfile = open(resultsfilepath, 'a')
    resultsfile.write("#####Generado por NTDIS CRACKER#####\n\n")
    for credential in resultados:
        usuario = credential
        password = resultados[credential]
        print(f"{GREEN}{usuario}:{password}")
        resultsfile.write(f"{usuario}:{password}\n")
    print(f"\n{END}Los resultados también se han guardado en el archivo {resultsfilepath}")
# Método para buscar un key en un diccionario de datos a partir de un value especificado 
def getKey(val, mydict):
    mylist = []
    for key, value in mydict.items():
        if val == value:
            mylist.append(key)
    return mylist

# Borrado de archivos temporales temphashes.txt y crackedhashes.txt
def clearFiles():
    cmdcleartemphashes = ['rm', '-rf', '/tmp/temphashes.txt']
    cmdclearcrackedhashes = ['rm', '-rf', '/tmp/crackedhashes.txt']
    try:
        subprocess.run(cmdcleartemphashes, capture_output=True, text=True)
        subprocess.run(cmdclearcrackedhashes, capture_output=True, text=True)
    except Exception as e:
        print(f"{RED}Error al borrar archivos temporales: {e}")


def main():
    # Crear parser de argumentos
    parser = argparse.ArgumentParser(description='NTDIS CRACKER: Herramienta para automatizar el proceso de NTLM hash cracking a partir de hashes obtenidos de un archivo NTDIS.DIT')

    # Declarar argumentos
    parser.add_argument('-i','--inputfile', type=str, required=True, help='Ejemplo: -i /path/to/hashesfile.txt')
    parser.add_argument('-w','--wordlist', type=str, default='/usr/share/wordlists/rockyou.txt', help='Ejemplo: -w /path/to/wordlist.txt. Default: /usr/share/wordlists/rockyou.txt')
    parser.add_argument('-o','--outputfile', type=str, default='results.txt', help='Ejemplo: -o /path/to/results.txt. Default: results.txt')

    # Parsear argumentos
    args = parser.parse_args()

    hashfilepath = args.inputfile
    wordlistpath = args.wordlist
    outputfilepath = args.outputfile
    
    # Ejecutar métodos principales del script: definición de colores, mostrar banner de bienvenida, procesar y guardar resultados, borrar archivos temporales.
    setColors()
    showBanner()
    guardarResultados(crackHashes(hashfilepath,wordlistpath), outputfilepath)
    clearFiles()


if __name__ == "__main__":
    main()
