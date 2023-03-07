import fileinput
import re

#El texto es HEX?
def EncontrarHexa(texto):
    existe = 0
    patron = r'\b[0-9A-F]+\b'
    existe = re.findall(patron, texto)
    return len(existe) > 0


def KSA(key):
    key_length = len(key) #asegurar que la long es la misma
    S = list(range(256)) #tamaño maximo
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i] 
    return S

#Cambios
def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1)% 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K

#RC4
def RC4(key):
    key = [ord(c) for c in key]
    S = KSA(key)

    return PRGA(S)

#Obtener el texto
lines = []
for line in fileinput.input():
    lines.append(line)
#decir que es que
key = lines[0].strip()
textoclaro = lines[1].strip()


keystream = RC4(key)
#convierte en bytes la cadena
plaintext = [ord(c) for c in textoclaro] 
ciphertext = []
for p,k in zip(plaintext, keystream): 
    #agrega un nuevo elemento que se le haya hecho xor
    ciphertext.append(p ^ k) 

#con format(c, '02X') se toma el número ascii del for que recorre ciphertext y lo transforma a hexadecimal en formato tradicional
# con join() podemos unir toda la cadena de caracteres 
ciphertext = ''.join([format(c, '02X') for c in ciphertext])
print(ciphertext)

