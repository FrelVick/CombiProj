# -*- coding: utf-8 -*
import Rules as R
import Tree
import math

"""
GRAMMAIRES
"""

# Arbres binaires
treeGram = {
    "Tree" : R.UnionRule("Node", "Leaf"),
    "Node" : R.ProductRule("Tree", "Tree",
                           lambda (l) : Tree.Node(l)),
    "Leaf" : R.SingletonRule(Tree.Leaf)
}

# Mots de Fibonacci
fiboGram = { 
    "Fib"   : R.UnionRule("Vide", "Cas1"),
    "Cas1"  : R.UnionRule("CasAu", "Cas2"),
    "Cas2"  : R.UnionRule("AtomB", "CasBAu"),
    "Vide"  : R.EpsilonRule(""),
    "CasAu" : R.ProductRule("AtomA", "Fib", "".join),
    "AtomA" : R.SingletonRule("A"),
    "AtomB" : R.SingletonRule("B"),
    "CasBAu": R.ProductRule("AtomB", "CasAu", "".join)
}

# Mots sur l'alphabet AB
ABGram = {
    "AB" : R.UnionRule("Vide", "CasAB"),
    "AtomA" : R.SingletonRule("A"),
    "AtomB" : R.SingletonRule("B"),
    "CasAB" : R.UnionRule("CasAu", "CasBu"),
    "Vide" : R.EpsilonRule(""),
    "CasAu" : R.ProductRule("AtomA", "AB", "".join),
    "CasBu" : R.ProductRule("AtomB", "AB", "".join)
}

#  Mots de Dyck
DyckGram = {
    "Dyck" : R.UnionRule("Vide", "Casuu"),
    "Casuu" : R.ProductRule("Dyck", "Cas(u", "".join),
    "Vide" : R.EpsilonRule(""),
    "AtomLPAR" : R.SingletonRule("("),
    "AtomRPAR" : R.SingletonRule(")"),
    "Cas(u" : R.ProductRule("AtomLPAR", "Casu)", "".join),
    "Casu)" : R.ProductRule("Dyck", "AtomRPAR", "".join)
}

# Mots qui n'ont pas deux lettres consécutives égales
TwoGram = {
    "Two" : R.UnionRule("CasAu", "CasBAu"),
    "Vide" : R.EpsilonRule(""),
    "AtomA" : R.SingletonRule("A"),
    "AtomB" : R.SingletonRule("B"),
    "CasAu" : R.UnionRule ("Vide", "CasABu"),
    "CasABu": R.ProductRule("AtomA", "CasBu", "".join),
    "CasBu" : R.UnionRule ("CasBAu", "Vide"),
    "CasBAu" : R.ProductRule("AtomB", "CasAu", "".join),
}

# Mots qui n'ont pas trois lettres consécutives égales
ThreeGram = {
    "Three" : R.UnionRule("Vide", "S"),
    "Vide" : R.EpsilonRule(""),
    "AtomA" : R.SingletonRule("A"),
    "AtomB" : R.SingletonRule("B"),
    "AA"   : R.ProductRule("AtomA", "AtomA", "".join),
    "BB"   : R.ProductRule("AtomB", "AtomB", "".join),
    "S"    : R.UnionRule ("U", "T"),
    "U"    : R.UnionRule("AtomA", "U1"),
    "U1"   : R.UnionRule("AA", "U2"),
    "U2"   : R.UnionRule("AT", "AAT"),
    "AT"   : R.ProductRule("AtomA", "T", "".join),
    "AAT"  : R.ProductRule("AtomA", "AT", "".join),
    "T"    : R.UnionRule("AtomB", "T1"),
    "T1"   : R.UnionRule("BB", "T2"),
    "T2"   : R.UnionRule("BU", "BBU"),
    "BU"   : R.ProductRule("AtomB", "U", "".join),
    "BBU"  : R.ProductRule("AtomB", "BU", "".join),
}

# Palindromes sur l'alphabet A, B
ABPalindrome = {
    "Pal" : R.UnionRule("Vide", "S"),
    "Vide" : R.EpsilonRule(""),
    "AtomA" : R.SingletonRule("A"),
    "AtomB" : R.SingletonRule("B"),

    "S"    : R.UnionRule ("AtomA", "S1"),
    "S1"   : R.UnionRule("AtomB", "S2"),
    "S2"   : R.UnionRule("ASA", "BSB"),

    "ASA"   : R.ProductRule("AtomA", "ASA1", "".join),
    "ASA1"  : R.ProductRule("Pal", "AtomA", "".join),
 
    "BSB"   : R.ProductRule("AtomB", "BSB1", "".join),
    "BSB1"  : R.ProductRule("Pal", "AtomB", "".join),
 
}

# Palindromes sur l'alphabet A, B, C
ABCPalindrome = {
    "Pal" : R.UnionRule("Vide", "S"),
    "Vide" : R.EpsilonRule(""),
    "AtomA" : R.SingletonRule("A"),
    "AtomB" : R.SingletonRule("B"),
    "AtomC" : R.SingletonRule("C"),

    "S"    : R.UnionRule ("AtomA", "S1"),
    "S1"   : R.UnionRule("AtomB", "S2"),
    "S2"   : R.UnionRule("AtomC", "S3"),
    "S3"   : R.UnionRule("ASA", "S4"),
    "S4"   : R.UnionRule("BSB", "CSC"),

    "ASA"   : R.ProductRule("AtomA", "ASA1", "".join),
    "ASA1"  : R.ProductRule("Pal", "AtomA", "".join),
 
    "BSB"   : R.ProductRule("AtomB", "BSB1", "".join),
    "BSB1"  : R.ProductRule("Pal", "AtomB", "".join),

    "CSC"   : R.ProductRule("AtomC", "CSC1", "".join),
    "CSC1"  : R.ProductRule("Pal", "AtomC", "".join),
}

"""
Incorrect : génère plusieurs fois les memes mot
EvenGram = {
    "S" : R.UnionRule("Vide", "S1"),
    "Vide" : R.EpsilonRule(""),
    "AtomA" : R.SingletonRule("A"),
    "AtomB" : R.SingletonRule("B"),

    "S1"   : R.UnionRule("aA", "bB"),
  
    "aA"  : R.ProductRule("AtomA", "A", "".join),
    "A"   : R.UnionRule("aAA", "bS"),
    "aAA" : R.ProductRule("AtomA", "AA", "".join),
    "AA"  : R.ProductRule("A", "A", "".join),
    "bS"  : R.ProductRule("AtomB", "S", "".join),
    
    "bB"  : R.ProductRule("AtomB", "B", "".join),
    "B"   : R.UnionRule("bBB", "aS"),
    "bBB" : R.ProductRule("AtomB", "BB", "".join),
    "BB"  : R.ProductRule("B", "B", "".join),
    "aS"  : R.ProductRule("AtomA", "S", "".join)
 
}
"""


"""
FONCTIONS CARDINALITE (pour les tests) 
"""

def fibo_count(n, d = {}):
    if (n < 0):
        raise ValueError("Negative number")
    elif (n <= 1):
        return n
    else:
        if not n - 1 in d:
            d[n - 1] = fibo_count(n - 1, d)
        if not n - 2 in d:
            d[n - 2] = fibo_count(n - 2, d) 
        return d[n - 1] + d[n - 2]

def catalan (n):
    if n < 0:
        raise ValueError ("Catalan sequence not defined for n < 0")
    num = 1 
    den = 1
    if n < 2:
        return 1
    for i in range (2, n+1):
        num *= (i + n) 
        den *=  i
    return num/den

def dyck_count (n):
    if n % 2 == 0:
        return catalan (n/2)
    else:
        return 0

def tree_count (n):
    if n == 0:
        return 0
    else:
        f = math.factorial(n-1)
        return math.factorial(2*(n-1))/(f*f*n)

def palindrome_count (base, n):
    if n == 0:
        return 1
    elif n <= 2:
        return base 
    else:
        return base ** ((n+1)/2)

def three_count (n):
    if n == 0:
        return 1
    if n == 1:
        return 2
    if n == 2:
        return 4
    if n == 3:
        return 6
    return three_count(n-1) + three_count(n-2)

def two_count (n):
    if n == 0:
        return 1
    return 2

grammars = {

    "treeGram"  : [treeGram, "Tree", tree_count],
    "fiboGram"  : [fiboGram, "Fib", lambda(n) : fibo_count(n+2)],
    "TwoGram"   : [TwoGram, "Two", two_count],
    "ThreeGram" : [ThreeGram, "Three", three_count ],
    "ABGram"    : [ABGram, "AB", lambda (n) : 2**n],
    "DyckGram"  : [DyckGram, "Dyck", dyck_count],
    "ABPalindrome" : [ABPalindrome, "Pal", lambda(x) : palindrome_count(2, x) ],
    "ABCPalindrome": [ABCPalindrome, "Pal", lambda(x) : palindrome_count(3, x)],

}

def get_rule_init (g, name):
    return g[name][0][g[name][1]]
