import numpy as np  

# Matrice Rcon contenant un vecteur pour chaque ronde
Rcon = [[0x1, 0, 0, 0],
        [0x2, 0, 0, 0],
        [0x4, 0, 0, 0],
        [0x8, 0, 0, 0],
        [0x10, 0, 0, 0],
        [0x20, 0, 0, 0],
        [0x40, 0, 0, 0],
        [0x80, 0, 0, 0],
        [0x1b, 0, 0, 0],
        [0x36, 0, 0, 0]
]

# Matrice sbox pour les subBytes
sbox = [
        [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
        [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
        [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
        [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
        [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
        [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
        [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
        [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
        [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
        [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
        [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
        [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
        [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
        [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
        [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
        [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
]

# Matrice de Rinjdael
Rinjdael = [
    [0x02, 0x03, 0x01, 0x01],
    [0x01, 0x02, 0x03, 0x01],
    [0x01, 0x01, 0x02, 0x03],
    [0x03, 0x01, 0x01, 0x02]
]

# fonction permetant d'effectuer le subByte sur un vecteur apartir de la matrice sbox
def subBytes(state):
    l = []
    for i in range(len(state)):
        t = hex(state[i])
        if state[i] > 15:
            k = int(t[-2], 16)
        else:
            k = 0
        j = int(t[-1], 16)
        l.append(sbox[k][j])
    state = l

# Fonction permetant de faire un shiftRows sur une matrice
def ShiftRows(x):
    x[1:] = [np.append(x[i][i:], x[i][:i]) for i in range(1, 4)]
    return x

# Fonction permetant de faire un Ou exclusif binaire entre deux vecteur
def xor(array1, array2):
    r = []
    for i, el in enumerate(array1):
        r.append(array1[i] ^ array2[i])
    return r

# FOnction permetant de caluler la cleé de la ronde suivante a partir de laclé de la ronde précédente et du rang
def next_key(key, n):
    key = [[0]*4]*4
    dc = [] # Dernière colone de la matrice cle
    pc = [] # première colone de la matrice cle
    kc2 = [] # Deuxieme colone de la matrice cle
    kc3 = [] # Troisieme colone de la matrice cle
    for el in key:
        dc.append(el[-1])
        pc.append(el[0])
        kc2.append(el[1])
        kc3.append(el[2])
    #retournement de la dernière colone
    temp = dc[0]
    for i, el in enumerate(dc):
        dc[i] = dc[(i+1) % 4]
    dc[-1] = temp
    # suBbyte sur la dernière colone
    subBytes(dc)
    # On calcule les colones de la clé suivante 
    tmp = xor(dc, pc)
    c1 = xor(tmp, Rcon[n -1])
    for k, el in enumerate(c1):
        key[k][0] = el
    c2 = xor(c1, kc2)
    for k, el in enumerate(c2):
        key[k][1] = el
    c3 = xor(c2, kc3)
    for k, el in enumerate(c3):
        key[k][2] = el
    c4 = xor(c3, dc)
    for k, el in enumerate(c4):
        key[k][3] = el
    return key

# FOnction qui chiffre le message durant une ronde a partir du messge obtenue a la ronde précédente et la clé de la ronde suivante
def cipher(m, key):
    # On effectue un Subbyte sur le message
    subBytes(m[0])
    subBytes(m[1])
    subBytes(m[2])
    subBytes(m[3])
    #on effectue un shiftrows sur le message
    m = ShiftRows(m)
    
    #on multipli le message par la matrice de Rinsdael
    for k, el in enumerate(m):
        for i, e in enumerate(el):
            m[k][i] = m[k][i] * Rinjdael[k][i] 

    # for k, el in enumerate(m):
    #     for i, f in enumerate(el):
    #         m[k][i] = (m[k][i])
    
    # On effectue un xor entre le message et la clé
    r = [[0]*4]*4
    r[0] = xor(m[0], key[0])
    r[1] = xor(m[1], key[1])
    r[2] = xor(m[2], key[2])
    r[3] = xor(m[3], key[3])

    return r

def main():
    m = str(input("Entrez le message (16 caractères): "))
    key = str(input("Entrez la clé (16 caracctères): "))
    # Transformation du message et de la clé en matrice de nombre
    l = []
    for i in m:
        l.append(ord(i))
    m = [[0]*4]*4
    for k, el in enumerate(l):
        m[k % 4][abs(k - 4) % 4] = (el) 
    l = []
    for i in key:
        l.append(ord(i))
    key = [[0]*4]*4
    for k, el in enumerate(l):
        key[k % 4][abs(k - 4) % 4] = (el)
    # Premier XOR du message avec le clé
    m[0] = xor(m[0], key[0])
    m[1] = xor(m[1], key[1])
    m[2] = xor(m[2], key[2])
    m[3] = xor(m[3], key[3])
    # On effectue 10 ronde de chiffrement
    for i in range(1, 11):
        key = next_key(key, 1) # on détermine la clé de la ronde suivante a partir de celle de la ronde précédente
        m = cipher(m, key) # on chiffre le message obtenue apres la ronde précédente avec le clé de la ronde suivante
        #ainsi de suite jusqu'a la 10e ronde
    # Retransformation de la matrice de nombre obtenue en un texte affichable
    l = [0]*16
    print(m)
    for k, el in enumerate(m):
        for i, e in enumerate(el):
            l[(k % 4) + (abs(i%4) * 4)] = chr((e))
    print("".join(l))

if __name__ == "__main__":
    main()








