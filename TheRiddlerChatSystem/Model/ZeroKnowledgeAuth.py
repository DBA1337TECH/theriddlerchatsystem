"""
DBA 1337_TECH, AUSTIN TEXAS © July 2021
Proof of Concept code, No liabilities or warranties expressed or implied.
"""

'''
 ____________ _________________  ___________           .__
/_   \_____  \\_____  \______  \ \__    ___/___   ____ |  |__
 |   | _(__  <  _(__  <   /    /   |    |_/ __ \_/ ___\|  |  \
 |   |/       \/       \ /    /    |    |\  ___/\  \___|   Y  \
 |___/______  /______  //____/     |____| \___  >\___  >___|  /
            \/       \/                       \/     \/     \/
ZeroKnowlegeAuth is a class that gives a True or False
whether a password is true or not, given the username.
Therefore verifies that the Sha256(creds) is indeed contains
the password, and the correct password.  Without storing any
hashes in plain text and definitely without storing the hash of the password.
only a token Alpha.
'''
import os
import sys

sys.path.insert(0, '../Controllers')
sys.path.insert(1, '../Model')
sys.path.insert(2, '../Views')

import CryptoTools
import secrets
import json
# import FileInterface

import Crypto.Util.number
# import numba
# import numpy as np
import struct

sys.path.insert(0, '../Controllers')
sys.path.insert(1, '../Model')
sys.path.insert(2, '../Views')
import Constants

gknot = 3


class FileInterface:
    def __init__(self, filename: str = None):
        self.filename = filename

    def ReadFile(self):
        if self.filename:
            self.fd = open(self.filename, 'rb')
            result = self.fd.read()
            return result

    def CloseFile(self):
        if self.fd:
            self.fd.close()


class ZeroKnowledgeAuthClient():
    p = 4074071952668972172536891376818756322102936787331872501272280898708762599526673412366794779

    def __init__(self, username, x, randomToken):
        G = "4074071952668972172536891376818756322102936787331872501272280898708762599526673412366794779"
        self.gknot = 3
        self.crypt = CryptoTools.CryptoTools()
        self.x = x  # sha256(pwd)
        self.Y = modexp(gknot, int.from_bytes(self.x, byteorder='little'), self.p)
        self.r = int(secrets.choice(G))
        self.T1 = modexp(gknot, self.r, self.p)
        self.a = randomToken
        self.c = self.CalculateC()
        self.zx = self.r - (self.c * (int.from_bytes(self.x, 'little')))
        print("CLIENT")
        print('Y:' + str(self.Y))
        print('Z:' + str(self.zx))
        print('C:' + str(self.c))
        print('a:' + str(self.a))
        print("T1")
        print(self.T1)

    def init(self):
        # TODO:
        return

    def CalculateC(self):
        # TODO:
        self.c = int.from_bytes(self.crypt.Sha256(str(self.Y).encode() + str(self.T1).encode() + str(self.a).encode()),
                                byteorder='little')
        return self.c

    def SendZeroKnowledgeAuth(self):
        # TODO: send self.c, self.zx
        return

    def IsItAuthenticated(self, Data):
        # TODO:
        return


class ZeroKnowledgeAuthServer():
    p = 4074071952668972172536891376818756322102936787331872501272280898708762599526673412366794779

    # Clients sends username and (c,z)
    # the server calculates T=Y^c g^z and verifies that c = H(Y,T',a)
    def __init__(self):
        self.crypt = CryptoTools.CryptoTools()
        self.session = self.GenerateSession()
        self.gknot = 3

    def registration(self, username, Y):
        # get json dictionary called users
        try:
            usersFile = FileInterface(os.getcwd() + Constants.USERS_FILE)
        except OSError as error:
            print(str(usersFile))
            if 'No such file or directory' in usersFile:
                # create the first user and the infrastructure on the server
                usersFile = open(Constants.USERS_FILE, 'w+')
                usersFile.close()
        try:
            usersFile = FileInterface(Constants.USERS_FILE)
        except OSError as error:
            if 'No such file or directory' in str(error):
                print("SOMETHING MESSED UP AND NO USER FILES, ERROR")
                return
        try:
            jsonUsers = usersFile.ReadFile()
            print("USERS" + str(jsonUsers))
            if 'No such file or directory' in str(jsonUsers):
                # create the first user and the infrastructure on the server
                print('ABOUT TO WRITE TO a FILE \n\n\n')
                usersFile = open(Constants.USERS_FILE, 'w+')
                usersFile.close()
        except OSError as err:
            print('[ZeroKnowledgeServer] ERROR' + str(err))
        usersFile = FileInterface(Constants.USERS_FILE)
        jsonUsers = usersFile.ReadFile()
        if username == None or username == '':
            print('FAILING> USER CANNOT BE NONE OR NULL')
            return False
        if username in jsonUsers:
            print('FAILING> USER ALREADY EXISTS')
            return False
        if not (username in jsonUsers):
            if (jsonUsers != ''):
                jsonimage = json.loads(jsonUsers)
                # 1)store Y
            else:
                jsonimage = {}
            jsonimage[username] = Y
            usersFile.CloseFile()
            fd = FileInterface(Constants.USERS_FILE)
            fd.WriteFile(json.JSONEncoder(ensure_ascii=False).encode(jsonimage))

        # 2)Create folder and allocate storage for Y
        # 3)return back successful or not
        return True

    def GenerateSession(self):
        self.session = secrets.randbelow(self.p)
        return self.session

    def SendSession(self):
        if self.session == 0 or self.session == None:
            return False
        else:
            return self.session

    def Authenticate(self, username, c, z):
        self.a = self.session
        self.c = c
        self.z = z
        self.u = username
        self.Y = self.LookupPublicKey(self.u)
        t1 = natural_modexp((natural_modexp(self.Y, self.c, self.p) * natural_modexp(gknot, self.z, self.p)), 1, self.p)
        digest = int.from_bytes(self.crypt.Sha256(str(self.Y).encode() + str(t1).encode() + str(self.a).encode()),
                                byteorder='little')
        print("SERVER:")
        print('Y:' + str(self.Y))
        print('Z:' + str(self.z))
        print('C:' + str(self.c))
        print('a:' + str(self.a))
        print("T1")
        print(t1)

        if c == digest:
            return True
        else:
            print(c)
            print('digest: ' + str(digest))
            return False

    def LookupPublicKey(self, u):
        # TODO:Implement this
        usersFile = FileInterface(os.getcwd().replace('Views', 'Model') + Constants.USERS_FILE)
        jsonUsers = usersFile.ReadFile()
        jsonimage = json.loads(jsonUsers)
        Y = jsonimage[u]
        del jsonUsers
        del jsonimage
        usersFile.CloseFile()
        return Y


def modexp(x, y, n):
    result = 1
    while y != 0:
        if (y & 1) != 0:
            result = (result * x) % n
        y >>= 1
        x = (x * x) % n
    return result


def modexpRecursive(x, y, n):
    if y == 0:
        result = 1;
        return;
    z = modexp(x, y >> 2, n)

    if y % 2 == 0:
        result = (z * z) % n
        return
    else:
        result = (x * z * z) % n
        return


def powCustom(x, y):
    result = 1
    while y != 0:
        if (y & 1) != 0:
            result *= x
        y >>= 1
        x *= x
    return result


"""Modular exponentiation
Provides a pure python implementation of modular exponentiation
modexp(b, e, m) computes b^e mod m using python's pow(b, e, m)
by range reducing b, e and m to natural numbers
For negative exponents, modexp uses the identity b^-e == (b^-1)^e mod m
The multiplicative inverse b^-1 mod m is computed using the Extended GCD
modexp always returns natural numbers. negative numbers are converted
to the additive inverses of their magnitudes using the identity -a mod m = m-a mod m
"""


def natural_mod(a, m):
    "mod returning natural number"

    assert isinstance(a, int) and isinstance(m, int)

    invert = False

    if m < 0:
        invert = True
        m = -m

    am = a % m
    if am < 0:
        am += m

    assert am >= 0 and m >= 0

    if invert:
        assert am <= m
        am = m - am

    return am


def congruent(a, b, m):
    "test for a = b mod m"

    return natural_mod(a, m) == natural_mod(b, m)


def natural_multiplicative_inverse(b, m):
    "modular multiplicative inverse returning natural number"

    assert isinstance(b, int) and isinstance(m, int)

    egcd = ExtendedGCD(b, m)
    mi = egcd.multiplicative_inverse
    mi_m = natural_mod(mi, m)

    return mi_m


def natural_additive_inverse(a, m):
    "modular additive inverse returning natural number"

    assert isinstance(a, int) and isinstance(m, int)

    ai = natural_mod(-a, m)

    return ai


def natural_pow(b, e, m, sign):
    "modular power for natural numbers returning natural number"

    assert isinstance(b, int) and isinstance(e, int)
    assert isinstance(m, int)
    assert sign == 1 or sign == -1
    assert b >= 0 and e >= 0 and m >= 0

    np = natural_mod(sign * pow(b, e, m), m)
    return np


def natural_modexp(b, e, m):
    "modular exponentiation returning natural number"

    assert isinstance(b, int) and isinstance(e, int) and isinstance(m, int)

    sign = 1

    if m < 0:
        sign = -sign
        m = -m

    if b < 0:
        b = natural_mod(b, m)

    if e < 0:
        e = - e
        b = natural_multiplicative_inverse(b, m)

    return natural_pow(b, e, m, sign)


def computed_method(f):
    def wrapped(self):
        self.compute()
        return f(self)

    return wrapped


class ExtendedGCD():
    def __init__(self, a, b):
        assert isinstance(a, int) and isinstance(b, int)
        self._a = a
        self._b = b
        self.computed = False

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    @property
    @computed_method
    def bézout(self):
        return self._bézout

    @property
    @computed_method
    def gcd(self):
        return self._gcd

    @property
    @computed_method
    def quotient(self):
        return self._quotient

    @property
    def multiplicative_inverse(self):
        if self.gcd != 1:
            raise ValueError('gcd({}, {}) != 1, no multiplicative inverse exists'.format(self.a, self.b))
        return self.bézout[0]

    def compute(self):
        if not self.computed:
            r, prev_r = self.b, self.a
            s, prev_s = 0, 1
            t, prev_t = 1, 0

            while r != 0:
                q = prev_r // r
                prev_r, r = r, prev_r - q * r
                prev_s, s = s, prev_s - q * s
                prev_t, t = t, prev_t - q * t

            self._bézout = prev_s, prev_t
            self._gcd = prev_r
            self._quotient = s, t

            self.computed = True


# class CommitmentScheme(object):
#     def __init__(self, oneWayPermutation, hardcorePredicate, securityParameter):
#         '''
#             oneWayPermutation: int -> int
#             hardcorePredicate: int -> {0, 1}
#         '''
#         self.oneWayPermutation = oneWayPermutation
#         self.hardcorePredicate = hardcorePredicate
#         self.securityParameter = securityParameter
#
#         # a random string of length `self.securityParameter` used only once per commitment
#         self.secret = self.generateSecret()
#
#     def generateSecret(self):
#         raise NotImplemented
#
#     def commit(self, x):
#         raise NotImplemented
#
#     def reveal(self):
#         return self.secret
#
# def goodPrime(p):
#     return p % 4 == 3 and probablyPrime(p, accuracy=100)
#
# def findGoodPrime(numBits=512):
#     candidate = 1
#
#     while not goodPrime(candidate):
#         candidate = random.getrandbits(numBits)
#
#     return candidate
#
# def makeModulus(numBits=512):
#     return findGoodPrime(numBits) * findGoodPrime(numBits)
#
# def blum_blum_shub(modulusLength=512):
#     modulus = makeModulus(numBits=modulusLength)
#
#     def f(inputInt):
#         return pow(inputInt, 2, modulus)
#
#     return f
#
# def parity(n):
#     return sum(int(x) for x in bin(n)[2:]) % 2
#
# class BBSBitCommitmentScheme(CommitmentScheme):
#     def generateSecret(self):
#         # the secret is a random quadratic residue
#         self.secret = self.oneWayPermutation(random.getrandbits(self.securityParameter))
#         return self.secret
#
#     def commit(self, bit):
#         unguessableBit = self.hardcorePredicate(self.secret)
#         return (
#             self.oneWayPermutation(self.secret),
#             unguessableBit ^ bit,  # python xor
#         )
#
# class BBSBitCommitmentVerifier(object):
#     def __init__(self, oneWayPermutation, hardcorePredicate):
#         self.oneWayPermutation = oneWayPermutation
#         self.hardcorePredicate = hardcorePredicate
#
#     def verify(self, securityString, claimedCommitment):
#         trueBit = self.decode(securityString, claimedCommitment)
#         unguessableBit = self.hardcorePredicate(securityString)  # wasteful, whatever
#         return claimedCommitment == (
#             self.oneWayPermutation(securityString),
#             unguessableBit ^ trueBit,  # python xor
#         )
#
#     def decode(self, securityString, claimedCommitment):
#         unguessableBit = self.hardcorePredicate(securityString)
#         return claimedCommitment[1] ^ unguessableBit
#
#
# class Verifier(object):
#     def __init__(self, graph, oneWayPermutation, hardcorePredicate):
#         self.graph = [tuple(sorted(e)) for e in graph]
#         self.oneWayPermutation = oneWayPermutation
#         self.hardcorePredicate = hardcorePredicate
#         self.committedColoring = None
#         self.verifier = commitment.BBSIntCommitmentVerifier(2, oneWayPermutation, hardcorePredicate)
#
#     def chooseEdge(self, committedColoring):
#         self.committedColoring = committedColoring
#         self.chosenEdge = random.choice(self.graph)
#         return self.chosenEdge
#
#     def accepts(self, revealed):
#         revealedColors = []
#
#         for (w, bitSecrets) in zip(self.chosenEdge, revealed):
#             trueColor = self.verifier.decode(bitSecrets, self.committedColoring[w])
#             revealedColors.append(trueColor)
#             if not self.verifier.verify(bitSecrets, self.committedColoring[w]):
#                 return False
#
#         return revealedColors[0] != revealedColors[1]
#
# class BBSIntCommitmentScheme(CommitmentScheme):
#     def __init__(self, numBits, oneWayPermutation, hardcorePredicate, securityParameter=512):
#         '''
#             A commitment scheme for integers of a prespecified length `numBits`. Applies the
#             Blum-Blum-Shub bit commitment scheme to each bit independently.
#         '''
#         self.schemes = [BBSBitCommitmentScheme(oneWayPermutation, hardcorePredicate, securityParameter)
#                         for _ in range(numBits)]
#         super().__init__(oneWayPermutation, hardcorePredicate, securityParameter)
#
#     def generateSecret(self):
#         self.secret = [x.secret for x in self.schemes]
#         return self.secret
#
#     def commit(self, integer):
#         # first pad bits to desired length
#         integer = bin(integer)[2:].zfill(len(self.schemes))
#         bits = [int(bit) for bit in integer]
#         return [scheme.commit(bit) for scheme, bit in zip(self.schemes, bits)]
#
# class BBSIntCommitmentVerifier(object):
#     def __init__(self, numBits, oneWayPermutation, hardcorePredicate):
#         self.verifiers = [BBSBitCommitmentVerifier(oneWayPermutation, hardcorePredicate)
#                           for _ in range(numBits)]
#
#     def decodeBits(self, secrets, bitCommitments):
#         return [v.decode(secret, commitment) for (v, secret, commitment) in
#                 zip(self.verifiers, secrets, bitCommitments)]
#
#     def verify(self, secrets, bitCommitments):
#         return all(
#             bitVerifier.verify(secret, commitment)
#             for (bitVerifier, secret, commitment) in
#             zip(self.verifiers, secrets, bitCommitments)
#         )
#
#     def decode(self, secrets, bitCommitments):
#         decodedBits = self.decodeBits(secrets, bitCommitments)
#         return int(''.join(str(bit) for bit in decodedBits))
#
# class Prover(object):
#     def __init__(self, graph, coloring, oneWayPermutation=ONE_WAY_PERMUTATION, hardcorePredicate=HARDCORE_PREDICATE):
#         self.graph = [tuple(sorted(e)) for e in graph]
#         self.coloring = coloring
#         self.vertices = list(range(1, numVertices(graph) + 1))
#         self.oneWayPermutation = oneWayPermutation
#         self.hardcorePredicate = hardcorePredicate
#         self.vertexToScheme = None
#
#     def commitToColoring(self):
#         self.vertexToScheme = {
#             v: commitment.BBSIntCommitmentScheme(
#                 2, self.oneWayPermutation, self.hardcorePredicate
#             ) for v in self.vertices
#         }
#
#         permutation = randomPermutation(3)
#         permutedColoring = {
#             v: permutation[self.coloring[v]] for v in self.vertices
#         }
#
#         return {v: s.commit(permutedColoring[v])
#                 for (v, s) in self.vertexToScheme.items()}
#
#     def revealColors(self, u, v):
#         u, v = min(u, v), max(u, v)
#         if not (u, v) in self.graph:
#             raise Exception('Must query an edge!')
#
#         return (
#             self.vertexToScheme[u].reveal(),
#             self.vertexToScheme[v].reveal(),
#         )
#
#
# class Verifier(object):
#     def __init__(self, graph, oneWayPermutation, hardcorePredicate):
#         self.graph = [tuple(sorted(e)) for e in graph]
#         self.oneWayPermutation = oneWayPermutation
#         self.hardcorePredicate = hardcorePredicate
#         self.committedColoring = None
#         self.verifier = commitment.BBSIntCommitmentVerifier(2, oneWayPermutation, hardcorePredicate)
#
#     def chooseEdge(self, committedColoring):
#         self.committedColoring = committedColoring
#         self.chosenEdge = random.choice(self.graph)
#         return self.chosenEdge
#
#     def accepts(self, revealed):
#         revealedColors = []
#
#         for (w, bitSecrets) in zip(self.chosenEdge, revealed):
#             trueColor = self.verifier.decode(bitSecrets, self.committedColoring[w])
#             revealedColors.append(trueColor)
#             if not self.verifier.verify(bitSecrets, self.committedColoring[w]):
#                 return False
#
#         return revealedColors[0] != revealedColors[1]
#
#
# def runProtocol(G, coloring, securityParameter=512):
#     oneWayPermutation = blum_blum_shub.blum_blum_shub(securityParameter)
#     hardcorePredicate = blum_blum_shub.parity
#
#     prover = Prover(G, coloring, oneWayPermutation, hardcorePredicate)
#     verifier = Verifier(G, oneWayPermutation, hardcorePredicate)
#
#     committedColoring = prover.commitToColoring()
#     chosenEdge = verifier.chooseEdge(committedColoring)
#
#     revealed = prover.revealColors(*chosenEdge)
#     revealedColors = (
#         verifier.verifier.decode(revealed[0], committedColoring[chosenEdge[0]]),
#         verifier.verifier.decode(revealed[1], committedColoring[chosenEdge[1]]),
#     )
#     isValid = verifier.accepts(revealed)
#
#     print("{} != {} and commitment is valid? {}".format(
#         revealedColors[0], revealedColors[1], isValid
#     ))
#
#     return isValid


if __name__ == "__main__":
    logo = ''' \t\t____________ _________________  ___________           .__
/_   \_____  \\_____  \______  \ \__    ___/___   ____ |  |__
 |   | _(__  <  _(__  <   /    /   |    |_/ __ \_/ ___\|  |  \\
 |   |/       \/       \ /    /    |    |\  ___/\  \___|   Y  \\
 |___/______  /______  //____/     |____| \___  >\___  >___|  /
            \/       \/                       \/     \/     \/ '''
    print(logo)
    print("\n\n")
    print("Beginning Registration")
    import Crypto.Util.number

    gknot = 3

    p = 4074071952668972172536891376818756322102936787331872501272280898708762599526673412366794779

    print(pow(gknot, 256))

    server = ZeroKnowledgeAuthServer()
    crypt = CryptoTools.CryptoTools()
    username = 'cheaner'
    x = crypt.Sha256(str('thisIsNotThePasswordYouAreLookingFor').encode())
    Y = modexp(gknot, int.from_bytes(x, byteorder='little'), p)
    server.registration(username, Y)
    a = server.SendSession()
    print('a: ' + str(a))
    client = ZeroKnowledgeAuthClient('cheaner', crypt.Sha256(str('thisIsNotThePasswordYouAreLookingFor').encode()), a)
    didweAuth = server.Authenticate(username, client.c, client.zx)
    print("Did we Authenticate: " + str(didweAuth))

    # import blum_blum_shub
    # securityParameter = 10
    # oneWayPerm = blum_blum_shub.blum_blum_shub(securityParameter)
    # hardcorePred = blum_blum_shub.parity
    #
    # print('Int commitment')
    # scheme = BBSIntCommitmentScheme(10, oneWayPerm, hardcorePred)
    # verifier = BBSIntCommitmentVerifier(10, oneWayPerm, hardcorePred)
    # choices = list(range(1024))
    # for _ in range(10):
    #     theInt = random.choice(choices)
    #     commitments = scheme.commit(theInt)
    #     secrets = scheme.reveal()
    #     trueInt = verifier.decode(secrets, commitments)
    #     valid = verifier.verify(secrets, commitments)
    #
    #     print('{} == {}? {}; {} {}'.format(theInt, trueInt, valid, secrets, commitments))
