import random
import os
#==========ERROR AND MESSAGES============
hit_any_key = "[!] Press any key to continue..."
wrong_keysize_input = "[-] Wrong keysize input!"
wrong_message_input = "[-] Wrong message input!"
#==========MENU LABEL==============
menuLabel = """
******************************************** RSA ********************************************
- Use key length greater than 32!
- Small values can lead to incorrect encryption and decryption!
*********************************************************************************************
"""

def rabinMiller(n, d):
    a = random.randint(2, (n - 2) - 2)
    x = pow(a, int(d), n) # a^d%n
    if x == 1 or x == n - 1:
        return True

    # square x
    while d != n - 1:
        x = pow(x, 2, n)
        d *= 2

        if x == 1:
            return False
        elif x == n - 1:
            return True
    
    # is not prime
    return False

def isPrime(n):
    """
        return True if n prime
        fall back to rabinMiller if uncertain
    """

    # 0 и 1 - не простые
    if n < 2:
        return False

    # список маленьких простых для экономии времени
    lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

    # если число в списке
    if n in lowPrimes:
        return True

    # если простые числа делятся на n
    for prime in lowPrimes:
        if n % prime == 0:
            return False
    
    # найти такое с, чтобы c * 2 ^ r = n - 1
    c = n - 1 # c even bc n not divisible by 2
    while c % 2 == 0:
        c /= 2 # make c odd

    # prove not prime 128 times
    for i in range(128):
        if not rabinMiller(n, c):
            return False

    return True


def genLargprime(keysize):
    # Генерируем большие случайные простые числа
    while True:
        randnum = random.randrange(2**(keysize - 1), 2**keysize - 1)
        if (isPrime(randnum)):
            return randnum

def isCoPrime(p, q):
    # Возращает Тру, если они взаимопростые
    return gcd(p, q) == 1

def gcd(a, b):
    #Используем алгоритм Евклида для нахождения НОД
    while b:
        a, b = b, a % b
    return a

def egcd(a, b):
    s = 0; old_s = 1
    t = 1; old_t = 0
    r = b; old_r = a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    #Врзращаем НОД, х и у
    return old_r, old_s, old_t

def modinv(a, b):
    gcd, x, y = egcd(a, b)

    if x < 0:
        x += b

    return x

def genKeyPairs(keysize=1024):
    e = d = n = 0

    #Генерируем два простых больших числа
    p = genLargprime(keysize)
    q = genLargprime(keysize)
    
    print(f"p: {p}")
    print(f"q: {q}")

    n = p * q # RSA Modulus
    funcElr = (p - 1) * (q - 1) # totient

    # choose e
    # e is coprime with phiN & 1 < e <= funcElr
    while True:
        e = random.randrange(2**(keysize - 1), 2**keysize - 1)
        if (isCoPrime(e, funcElr)):
            break

    # ищем d (закрытый ключ)
    # d( e * d (mod phiN) = 1 )
    d = modinv(e, funcElr)

    return e, d, n

def encrypt(e, n, msg):
    ciphertext = ""

    for c in msg:
        m = ord(c)
        ciphertext += str(pow(m, e, n)) + " "

    return ciphertext

def decrypt(d, n, ciphertext):
    msg = ""

    parts = ciphertext.split()
    for part in parts:
        if part:
            c = int(part)
            msg += chr(pow(c, d, n))

    return msg

def main():
    print(menuLabel)
    try:
        keysize = int(input("[!] Input keysize [5;54] >> "))
        if keysize < 5 or keysize > 54:
            raise Exception(wrong_keysize_input)
    except:
        print(wrong_keysize_input)
        input(hit_any_key)
        os.system('cls')
        main()
    print(f"----------- KEYS OPTIONS -----------\n")
    e, d, n = genKeyPairs(keysize)
    print(f"n: {n}\n")
    print(f"------------ KEYS PAIRS ------------\nOpen Key: (e:{e}, n:{n})\nPrivat Key: (d:{d}, n:{n})\n")

    try:
        msg = input("[!] Input message >> ")
        if len(msg) == 0:
            raise Exception(wrong_message_input)
    except:
        print(wrong_message_input)
        input(hit_any_key)
        os.system('cls')
        main()
    enc = encrypt(e, n, msg)
    dec = decrypt(d, n, enc)
    
    print(f"-------- ENCRYPTED MESSAGE --------\n{enc}\n")
    print(f"-------- DECRYPTED MESSAGE --------\n{dec}\n")
    print("*********************************************************************************************")
    input(hit_any_key)

main()
