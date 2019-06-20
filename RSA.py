#!/usr/bin/env python3

"""
    RSA Key Encryption Program
    Jordan Garcia
    jjg14e
    CIS4930
"""


import math


class RSA(object):
    """ A class containing functions for an RSA encryption system """

    def __init__(self):
        print("RSA Object created!")
        self.e = 0
        self.d = 0
        self.myList = []

    def inputFunc(self):
        numMessages = int(input("Enter the number of messages: "))
        print("Enter the messages")

        for msg in range(0, numMessages):
            self.myList.append(int(input()))

    def printFunc(self, num):
        return "message is " + str(num)

    def primeGen(self, minValue):
        counter = 0

        while counter < 2:
            if self.isPrime(minValue):
                if counter == 0:
                    self.p = minValue
                elif counter == 1:
                    self.q = minValue

                counter += 1

            minValue += 1

    def keyGen(self):
        minValue = int(input("Enter a minimum value: "))
        self.primeGen(minValue)
        self.N = self.p * self.q
        print("N = ", self.N)

        self.t = self.totient(self.N)
        for num in range(2, self.t):
            if math.gcd(num, self.t) == 1:
                self.e = num
                break

        print("e = ", self.e)

        # to prevent a program crash if minValue is a very small int
        if minValue < 65:
            for num in range(2, self.t):
                if (self.e * num % self.t) == 1:
                    self.d = num
                    break
        else:
            self.d = self.myGCD(self.e, self.t)

    def encrypt(self, num):
        assert num < self.N
        return num ** self.e % self.N

    def decrypt(self, encryptedNum):
        return pow(encryptedNum, self.d, self.N)

    def messages(self):
        self.inputFunc()
        self.keyGen()

        encryptedNumbers = []
        lit = iter(self.myList)

        while True:
            try:
                encryptedNumbers.append(self.encrypt(next(lit)))
            except StopIteration:
                break

        for encryptedNum in encryptedNumbers:
            my_encrypted = self.encrypt_decorator(self.printFunc)
            print(my_encrypted(encryptedNum))

        decryptedNumbers = []
        lit = iter(encryptedNumbers)

        # for verifying decrypted messages
        while True:
            try:
                decryptedNumbers.append(self.decrypt(next(lit)))
            except StopIteration:
                break

        for num in decryptedNumbers:
            my_decrypted = self.decrypt_decorator(self.printFunc)
            print(my_decrypted(num))

    """
        Decorator functions
    """

    def encrypt_decorator(self, func):
        def func_wrapper(num):
            return "The encrypted " + func(num)
        return func_wrapper

    def decrypt_decorator(self, func):
        def func_wrapper(num):
            return "The decrypted " + func(num)
        return func_wrapper

    """
        These are functions that are not part of the requirements
        but I created to assist me with the other functions
    """

    # function to calculate totient for keyGen method
    def totient(self, value):
        return int((self.p - 1) * (self.q - 1))

    # Helper function used for extendedEuclideanAlgorithm
    def myGCD(self, e, t):
        a_values, b_values, f_values, r_values = [], [], [], []
        a, b = int(e), int(t)
        f, r = a // b, a % b

        while r != 1:
            a, b = b, r
            f, r = a // b, a % b
            a_values.append(a)
            b_values.append(b)
            f_values.append(f)
            r_values.append(r)

        return self.extendedEuclideanAlgorithm(a_values, b_values, f_values, r_values)

    def extendedEuclideanAlgorithm(self, a_values, b_values, f_values, r_values):
        a, b, c, d = 1, a_values.pop(), f_values.pop() * -1, b_values.pop()

        # popping r_value for correct comparison
        r_values.pop()
        r = r_values.pop()

        while r != self.e:
            if d == r:  # replace d
                a = a + (c * f_values.pop() * -1)
                d = a_values.pop()
            elif b == r:  # replace b
                c = c + (f_values.pop() * a * -1)
                b = a_values.pop()

            if len(r_values) == 0:
                r = self.e
            else:
                r = r_values.pop()

        return a

    def isPrime(self, value):
        if value == 0:
            return False

        if value == 1 or value == 2 or value == 3:
            return True

        if value % 2 == 0 or value % 3 == 0:
            return False

        for num in range(2, int(math.sqrt(value)) + 1):
            if value % num == 0:
                return False

        return True


if __name__ == "__main__":
    rsa = RSA()
    rsa.messages()
