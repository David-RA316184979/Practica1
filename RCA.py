import fileinput
import re

#Funcion para determinar si el texto claro tiene un hexadecimal
def EncontrarHexa(texto):
    existe = 0
    patron = r'\b[0-9A-F]+\b'
    existe = re.findall(patron, texto)
    return len(existe) > 0

def KSA(key):
    key_length = len(key) 
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i] 
    return S

def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1)% 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K

def RC4(key):
    key = [ord(c) for c in key]
    S = KSA(key)

    return PRGA(S)

#Para obtener el input de la llave y el texto claro
lines = []
for line in fileinput.input():
    lines.append(line)

key = lines[0].strip()
textoclaro = lines[1].strip()

keystream = RC4(key)
#convierte en bytes la cadena
plaintext = [ord(c) for c in textoclaro] 
ciphertext = []
#zip es una función que itera al mismo tiempo en dos colecciones
for p,k in zip(plaintext, keystream): 
    #agrega un nuevo elemento que se le haya hecho xor
    ciphertext.append(p ^ k) 

#con format(c, '02X') se toma el número ascii del for que recorre ciphertext y lo transforma a hexadecimal en formato tradicional
# con join() podemos unir toda la cadena de caracteres 
ciphertext = ''.join([format(c, '02X') for c in ciphertext])
print(ciphertext) 