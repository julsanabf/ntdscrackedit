# NTDSCrackeDIT
Herramienta para automatizar el proceso de NTLM hash cracking y despliegue de sus resultados.
## Requisitos
- Debe tener instaladas las herramientas **hashcat** y **python3**. Distribuciones como Kali Linux y Parrot OS ya las traen por defecto.
    - Link de descarga de hashcat: https://hashcat.net/hashcat/
    - Link de descarga de python3: https://www.python.org/downloads/
- Debe tener a mano un archivo de hashes con el siguiente formato:
```
<usuario>:<RID>:<LM hash>:<NT hash>:::
```
**Donde:**
- **Usuario:** nombre de usuario de Active Directory
- **RID:** Relative Identifier, un identificador único para cada usuario dentro de un dominio.
- **LM hash**: hash de LAN Manager (LM). Aunque obsoleto y menos seguro, todavía puede estar presente en algunos sistemas.
- **NT hash**: hash NT, que es más seguro que el hash LM y se utiliza comúnmente para la autenticación en sistemas Windows.

### Ejemplo de archivos de hashes
![image](https://github.com/user-attachments/assets/f8562174-cb7e-4e4d-a2c1-47d26014411c)

## Instalación
```
git clone https://github.com/julsanabf/ntdis-cracker
cd ntdis-cracker
chmod +x ntdis-cracker.py
```
## Ejecución
### Menú de ayuda
```
ntdis-cracker.py [-h] -i INPUTFILE [-w WORDLIST] [-o OUTPUTFILE]
options:
  -h, --help            Muestra el menú de ayuda
  -i INPUTFILE, --inputfile    Define la ruta del archivo que contiene los hashes NTLM extraídos de NTDIS.DIT
                        Ejemplo: -i /path/to/hashesfile.txt
  -w WORDLIST, --wordlist    Define la ruta del diccionario de contraseñas a utilizar para crackear los hashes
                        Ejemplo: -w /path/to/wordlist.txt. Por defecto se utiliza /usr/share/wordlists/rockyou.txt
  -o OUTPUTFILE, --outputfile OUTPUTFILE    Define la ruta del archivo donde se guardarán los resultados (Lista de hashes crackeados y sus respectivos usernames)
                        Ejemplo: -o /path/to/results.txt. Por defecto se utiliza results.txt
```
### Screenshot
![image](https://github.com/user-attachments/assets/86e3975f-0b2d-4af2-836e-85101a747a5a)
