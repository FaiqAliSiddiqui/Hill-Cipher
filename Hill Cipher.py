# -*- coding: utf-8 -*-
"""
Created on Mon May 27 12:20:16 2024

@author: Dell
"""
import math
import numpy as np
import sympy 

def modInverse(a, n):
    a = a % n
    for x in range(1, n):
        if (a * x) % n == 1:
            return x
    return 1

def KeyMatrix_inv(key, n):
    Matrix = []
    for i in range(n):
        temp = []
        for j in range(n):
            temp.append(ord(key[i*n + j]) - 97)
        Matrix.append(temp)

    Matrix = np.array(Matrix)
    det = int(np.round(np.linalg.det(Matrix)))  # Calculate the determinant and round it to the nearest integer
    if det == 0:
        print("Invalid Key!")
        exit(None)

    det_inv = modInverse(det, 26)
    if det_inv == 1:
        print("Invalid Key! No modular inverse found.")
        exit(None)

    adjugate = np.array(sympy.Matrix(Matrix).adjugate())  # Compute the adjugate matrix using sympy
    inv_matrix = (det_inv * adjugate) % 26  # Calculate the inverse matrix modulo 26

    for i in range(n):
        for j in range(n):
            Matrix[i][j] = inv_matrix[i, j]
    return Matrix

def KeyMatrix(key, n):
    Matrix = []
    for i in range(n):
        temp = []
        for j in range(n):
            temp.append(ord(key[i*n + j]) - 97)
        Matrix.append(temp)

    Matrix = np.array(Matrix)
    if np.linalg.det(Matrix) == 0:
        print("Invalid Key!")
        exit(None)

    return Matrix

def Multiply(x, y):
    y = np.array([[ord(char) - 97] for char in y])
    result = np.dot(x, y)
    return result

def Hill_encrypt(plain, key_matrix, n):
    cipher = ""
    for i in range(0, len(plain), n):
        temp = Multiply(key_matrix, plain[i:i+n])
        for x in range(n):
            cipher += chr(temp[x][0] % 26 + 97)
    return cipher

def Hill_decrypt(cipher, inv_key_matrix, n):
    plain = ""
    for i in range(0, len(cipher), n):
        temp = Multiply(inv_key_matrix, cipher[i:i+n])
        for x in range(n):
            plain += chr(temp[x][0] % 26 + 97)
    return plain

if __name__ == "__main__":
    mode = input("Choose mode (encrypt/decrypt): ").lower()

    if mode == "encrypt":
        key = ''.join(input("Key: ").lower().split())
        plain = ''.join(input("PlainText: ").lower().split())

        n = int(math.sqrt(len(key)))
        if n != math.sqrt(len(key)) or n == 0:
            print("Invalid Key!")
            exit(None)
        n = math.floor(n)

        if len(plain) % n != 0:
            for i in range(n - len(plain) % n):
                plain += 'x'

        key_matrix = KeyMatrix(key, n)
        cipher_text = Hill_encrypt(plain, key_matrix, n)
        print("CipherText: ", cipher_text)

    elif mode == "decrypt":
        key = ''.join(input("Key: ").lower().split())
        cipher = ''.join(input("CipherText: ").lower().split())

        n = int(math.sqrt(len(key)))
        if n != math.sqrt(len(key)) or n == 0:
            print("Invalid Key!")
            exit(None)
        n = math.floor(n)

        inv_key_matrix = KeyMatrix_inv(key, n)
        plain_text = Hill_decrypt(cipher, inv_key_matrix, n)
        print("PlainText: ", plain_text)

    else:
        print("Invalid mode selected!")

# Example Input/Output
# Key: cddg
# PlainText: attack
# CipherText:  fkmfiolz

# Usage:
# Choose mode (encrypt/decrypt): encrypt
# Key: cddg
# PlainText: attack
# CipherText: fkmfiolz

# Choose mode (encrypt/decrypt): decrypt
# Key: cddg
# CipherText: fkmfiolz
# PlainText: attackx


        
    