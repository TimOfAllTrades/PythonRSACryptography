import random


# Euler's GCD theorem, used to determine if numbers are coprime
def Eulers_GCD(a, b):
    r = a % b
    q = a//b
    while r != 0:
        a = b
        b = r
        q = a//b
        r = a - b*q
    return b

# The Miller Rabin tests if the input number n is prime.


def miller_rabin(n, k):

    # The optimal number of rounds for this test is 40
    # See http://stackoverflow.com/questions/6325576/how-many-iterations-of-rabin-miller-should-i-use-for-cryptographic-safe-primes
    # for justification

    if n == 2 or n == 3:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# This function calculates the private key using the two p and q prime numbers and one more prime number n as the exponent


def Get_Private_Key(p, q, n):
    totient = (p-1)*(q-1)
    for i in range(0, n):
        if ((i * totient)+1) % n == 0:
            print("Found private key ")
            print("on iteration ", i)
            return ((i * totient)+1)//n


# This is the modulo exponent solver function
def ModuloExponent(base, exponent, modulus):
    if modulus == 1:
        return 0
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent //= 2
        base = (base*base) % modulus
    return result


# Introduction

# RSA cryptography is a method to perform asymmetric cryptography.
# In asymmetric cryptography, a public key and a private key are created and only the public key is broadcasted to the public.
# Data encrypted by the private key can only be decrypted by the public key.
# Data encrypted by the public key can only be decrypted by the private key.
# The former is an example of digital signing, while the latter is used for securing internet traffic.

# First is to get two prime numbers. Use Miller Rabin test to determine if number is prime
#p = 12985409850392870357275039480392840985634587665498794651321321654879876546132132165498798798654615631565165487974654646511332165498797979877987465465132132165465469879798464625132465498798794641475258963699911654687654321265464988317
#q = 5498794651319918949878484451952926263636291919484879465498798498498498798357539867294569875293849284565423459384675892449384414541645657466658465847968574978989457568446657434276546133454663545457982753987598741987439128749823754362545643546646546476654765645856546675496456946046940605439218237648657546657465466454698569287987198723981739187192872346542365456435245645346655611

p = 6007
q = 11035
print("\n\nRSA cryptography tutorial:")
print("This python script will show you a step by step process on how RSA cryptography works")
print("First a prime number p is needed.  Enter in a random integer and the next prime number will be automatically found")

p = int(input())
print("Testing if ", p, " is a prime number.  If not, the next prime will be found")
while miller_rabin(p, 40) == False:
    p += 1
print("Using ", p, " as the first prime.")


print("\n\nNext a prime number q is needed.  Just like before, enter in a random integer and the next prime number will be automatically found")

q = int(input())
print("Now testing if ", q, " is prime.  If not, the next prime will be found")
while miller_rabin(q, 40) == False:
    q += 1
print("Using ", q, " as the second prime.\n\n")


modulus = p*q
print("The modulus ", p, " * ", q, "is ", modulus)
print("And the totient (p-1)(q-1) ", p-1, " * ", q-1, "is ", (p-1)*(q-1))

print("\n\nFinally, we need a prime integer n that is coprime with the Totient, (usually 65537 works)")
n = int(input())

while miller_rabin(n, 40) == False or Eulers_GCD((p-1)*(q-1), n) != 1:
    n += 1

print("Using n with a value of ", n)
print("\n\nTo obtain the private key, we need to solve an equation so that: ")
print("(Private Key) * (n) mod(totient) = 1")
print("To solve this, we will iterate over all values of i so that")
print("Private Key = (i * (", (p-1)*(q-1), " + 1)) /", n, " results in an integer")
input("Press Enter to continue...")


pkey = Get_Private_Key(p, q, n)
print("The private key is ", pkey)

print("\n\nNow we will attempt to encrypt a number.  This is done by taking the number to the",
      n, "th power modulo", modulus)
ptext = int(input())

ctext = ModuloExponent(ptext, pkey, modulus)
print("The encrypted number (ciphertext) is: ", ctext)
input("Press Enter to continue...")

print("\n\nTo decrypt the ciphertext, we need to find the remainder of the cipher text to the private key's power divided by the modulus")
print("or", ctext, "to the", pkey, "power modulo", modulus)
input("Press Enter to continue...")
print("The decrypted number (plaintext) is:",
      ModuloExponent(ctext, n, modulus))
print("From here you can we have encrypted a number with n and the modulus which is the public key, then we decrypted it with the private key")
