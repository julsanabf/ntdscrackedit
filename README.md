# NTDIS CRACKER
Herramienta para automatizar el proceso de NTLM hash cracking y despliegue de resultados
## Requisitos
Debe tener instalada la herramienta **hashcat**. Distribuciones como Kali Linux y Parrot OS ya la traen por defecto.

Link oficial de hashcat: https://hashcat.net/hashcat/
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
![image](https://github.com/user-attachments/assets/dc26ba06-4c31-4db8-b970-1ef99147df5b)
