# -*- coding: utf-8 -*
import Rules as R
import Tree
import math


# Fonctions utilisées pour permettre l'ajout de rank :
# elles permettent de différencier quel règle est à l'origine d'un mot (dans le cas Union)
# ou de récupérer le couple (a, b) créé par une règle product

def string_empty (s):
    return s==""

def first_char(s):
    return s[0]

def sep_first(s):
    return (s[0], s[1:])

def sep_last(s):
    return (s[:len(s)-1], s[len(s)-1])

def sep_dyck (s):
    i_lpar = 0
    count = 0
    for i in range(len(s)):
        if s[i] == "(" and count == 0:
            i_lpar = i
            count += 1
        elif s[i] == "(":
            count += 1
        else:
            count -= 1
    return (s[:i_lpar], s[i_lpar:])


"""
GRAMMAIRES
"""

''' ARBRES BINAIRES '''

treeGram = {
    "Tree" : R.UnionRule("Node", "Leaf", lambda t: not (t.is_leaf())),
    "Node" : R.ProductRule("Tree", "Tree",
                           lambda a : Tree.Node(a[0], a[1]), lambda t : (t.left(), t.right())),
    "Leaf" : R.SingletonRule(Tree.Leaf)
}


''' MOTS DE FIBONNACI '''

fiboGram = { 
    "Fib"   : R.UnionRule("Vide", "Cas1", string_empty),
    "Cas1"  : R.UnionRule("CasAu", "Cas2", lambda s : s[0] == "A"),
    "Cas2"  : R.UnionRule("AtomB", "CasBAu", lambda s : s == "B"),
    "Vide"  : R.EpsilonRule(""),
    "CasAu" : R.ProductRule("AtomA", "Fib", "".join, sep_first), 
    "AtomA" : R.SingletonRule("A"),
    "AtomB" : R.SingletonRule("B"),
    "CasBAu": R.ProductRule("AtomB", "CasAu", "".join, sep_first)
}

''' MOTS SUR L'ALPHABET A, B '''

ABGram = {
    "AB" : R.UnionRule("Vide", "CasAB", string_empty),
    "AtomA" : R.SingletonRule("A"),
    "AtomB" : R.SingletonRule("B"),
    "CasAB" : R.UnionRule("CasAu", "CasBu", lambda s :  s[0] == 'A'),
    "Vide" : R.EpsilonRule(""),
    "CasAu" : R.ProductRule("AtomA", "AB", "".join, sep_first),
    "CasBu" : R.ProductRule("AtomB", "AB", "".join, sep_first)
}
            
''' MOTS DE DYCK '''

DyckGram = {
    "Dyck" : R.UnionRule("Vide", "Casuu", string_empty),
    "Casuu" : R.ProductRule("Dyck", "Cas(u", "".join, sep_dyck),
    "Vide" : R.EpsilonRule(""),
    "AtomLPAR" : R.SingletonRule("("),
    "AtomRPAR" : R.SingletonRule(")"),
    "Cas(u" : R.ProductRule("AtomLPAR", "Casu)", "".join, sep_first),
    "Casu)" : R.ProductRule("Dyck", "AtomRPAR", "".join, sep_last)
}


''' MOTS QUI N'ONT PAS DEUX LETTRES CONSECUTIVES EGALES '''

TwoGram = {
    "Two" : R.UnionRule ("CasAu", "CasBAu", lambda s: s=='' or s[0] == 'A'),
    "Vide" : R.EpsilonRule(""),
    "AtomA" : R.SingletonRule("A"),
    "AtomB" : R.SingletonRule("B"),
    "CasAu" : R.UnionRule ("Vide", "CasABu", string_empty),
    "CasABu": R.ProductRule("AtomA", "CasBu", "".join, sep_first),
    "CasBu" : R.UnionRule ("CasBAu", "Vide", lambda s : not string_empty(s)),
    "CasBAu" : R.ProductRule("AtomB", "CasAu", "".join, sep_first),
}

''' MOTS QUI N'ONT PAS TROIS LETTRES CONSECUTIVES EGALES '''

ThreeGram = {
    "Three" : R.UnionRule("Vide", "S", string_empty),
    "Vide" : R.EpsilonRule(""),
    "AtomA" : R.SingletonRule("A"),
    "AtomB" : R.SingletonRule("B"),
    "AA"   : R.ProductRule("AtomA", "AtomA", "".join, sep_first),
    "BB"   : R.ProductRule("AtomB", "AtomB", "".join, sep_first),
    "S"    : R.UnionRule ("U", "T", lambda s : s[0] == 'A'),
    "U"    : R.UnionRule("AtomA", "U1", lambda s : s=='A'),
    "U1"   : R.UnionRule("AA", "U2", lambda s : s =="AA"),
    "U2"   : R.UnionRule("AT", "AAT", lambda s : s[0] == "A" and s[1] == "B"),
    "AT"   : R.ProductRule("AtomA", "T", "".join, sep_first),
    "AAT"  : R.ProductRule("AtomA", "AT", "".join, sep_first),
    "T"    : R.UnionRule("AtomB", "T1", lambda s : s == "B"),
    "T1"   : R.UnionRule("BB", "T2", lambda s : s == "BB"),
    "T2"   : R.UnionRule("BU", "BBU", lambda s : s[0] == "B" and s[1] == "A"),
    "BU"   : R.ProductRule("AtomB", "U", "".join, sep_first),
    "BBU"  : R.ProductRule("AtomB", "BU", "".join, sep_first),
}

''' PALINDROMES SUR L'ALPHABET A, B '''

ABPalindrome = {
    "Pal" : R.UnionRule("Vide", "S", string_empty),
    "Vide" : R.EpsilonRule(""),
    "AtomA" : R.SingletonRule("A"),
    "AtomB" : R.SingletonRule("B"),

    "S"    : R.UnionRule ("AtomA", "S1", lambda s : s == "A"),
    "S1"   : R.UnionRule("AtomB", "S2", lambda s : s == "B"),
    "S2"   : R.UnionRule("ASA", "BSB", lambda s : s[0] == "A"),

    "ASA"   : R.ProductRule("AtomA", "ASA1", "".join, sep_first),
    "ASA1"  : R.ProductRule("Pal", "AtomA", "".join, sep_last),
 
    "BSB"   : R.ProductRule("AtomB", "BSB1", "".join, sep_first),
    "BSB1"  : R.ProductRule("Pal", "AtomB", "".join, sep_last),
 
}

''' PALINDROMES SUR L'ALPHABET A, B, C '''

ABCPalindrome = {
    "Pal" : R.UnionRule("Vide", "S", string_empty),
    "Vide" : R.EpsilonRule(""),
    "AtomA" : R.SingletonRule("A"),
    "AtomB" : R.SingletonRule("B"),
    "AtomC" : R.SingletonRule("C"),

    "S"    : R.UnionRule ("AtomA", "S1", lambda s : s == "A"),
    "S1"   : R.UnionRule("AtomB", "S2", lambda s : s == "B"),
    "S2"   : R.UnionRule("AtomC", "S3", lambda s : s == "C"),
    "S3"   : R.UnionRule("ASA", "S4", lambda s: s[0] == "A"),
    "S4"   : R.UnionRule("BSB", "CSC", lambda s : s[0] == "B"),

    "ASA"   : R.ProductRule("AtomA", "ASA1", "".join, sep_first),
    "ASA1"  : R.ProductRule("Pal", "AtomA", "".join, sep_last),
 
    "BSB"   : R.ProductRule("AtomB", "BSB1", "".join, sep_first),
    "BSB1"  : R.ProductRule("Pal", "AtomB", "".join, sep_last),

    "CSC"   : R.ProductRule("AtomC", "CSC1", "".join, sep_first),
    "CSC1"  : R.ProductRule("Pal", "AtomC", "".join, sep_last),
}

''' MOTS QUI ONT LE MEME NOMBRE DE A QUE DE B '''

EqualGram = {
    "Vide" : R.EpsilonRule(""),
    "A"    : R.SingletonRule("A"),
    "B"    : R.SingletonRule("B"),
    "S"    : R.UnionRule("Vide", "S1", string_empty),
    "S1"   : R.UnionRule("aTbS", "bUaS", lambda s : s[0] == "A"),
    
    "T"    : R.UnionRule("Vide", "aTbT", string_empty),
    "U"    : R.UnionRule("Vide", "bUaU", string_empty),

    "aTbS" : R.ProductRule("A", "TbS", "".join, sep_first),
    "TbS"  : R.ProductRule("T", "bS", "".join),
    "bS"   : R.ProductRule("B", "S", "".join, sep_first),

    "bUaS" : R.ProductRule("B", "UaS", "".join, sep_first),
    "UaS"  : R.ProductRule("U", "aS", "".join),
    "aS"   : R.ProductRule("A", "S", "".join, sep_first),

    "aTbT" : R.ProductRule("A", "TbT", "".join, sep_first),
    "TbT"  : R.ProductRule("T", "bT", "".join),
    "bT"   : R.ProductRule("B", "T", "".join, sep_first),

    "bUaU" : R.ProductRule("B", "UaU", "".join, sep_first),
    "UaU"  : R.ProductRule("U", "aU", "".join),
    "aU"   : R.ProductRule("A", "U", "".join, sep_first),

}


"""
FONCTIONS CARDINALITE (pour les tests) 
"""


def fibo_count(n, d = {}):
    ''' Pour la grammaire des mots de Fibonacci ''' 
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
    return num//den

def dyck_count (n):
    ''' Pour la grammaire des mots de Dyck '''
    if n % 2 == 0:
        return catalan (n//2)
    else:
        return 0

def tree_count (n):
    ''' Pour la grammaire des arbres '''
    if n == 0:
        return 0
    else:
        f = math.factorial(n-1)
        return math.factorial(2*(n-1))//(f*f*n)

def palindrome_count (base, n):
    ''' Pour les grammaires des palindromes '''
    if n == 0:
        return 1
    elif n <= 2:
        return base 
    else:
        return base ** ((n+1)//2)

def three_count (n):
    ''' Pour la grammaires des mots n'ayant pas trois lettres consécutives égales '''
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
    ''' Pour la grammaire des mots n'ayant pas deux lettres consécutives égales '''
    if n == 0:
        return 1
    return 2

def central_binomial(n):
    num = math.factorial(n)
    return math.factorial(2*n) // (num * num)

def equal_count (n):
    if n % 2 == 1:
        return 0
    return central_binomial(n//2)

grammars = {

    "treeGram"     : [treeGram, "Tree", tree_count],
    "fiboGram"     : [fiboGram, "Fib", lambda n : fibo_count(n+2)],
    "TwoGram"      : [TwoGram, "Two", two_count],
    "ThreeGram"    : [ThreeGram, "Three", three_count ],
    "ABGram"       : [ABGram, "AB", lambda n: 2**n],
    "DyckGram"     : [DyckGram, "Dyck", dyck_count],
    "ABPalindrome" : [ABPalindrome, "Pal", lambda x : palindrome_count(2, x) ],
    "ABCPalindrome": [ABCPalindrome, "Pal", lambda x : palindrome_count(3, x)],
    "EqualGram"    : [EqualGram, "S", equal_count ]
 
}


def get_rule_init (g, name):
    ''' Retourne la règle initiale de la grammaire '''
    return g[name][0][g[name][1]]

def print_grammar(g):
    ''' Affiche la grammaire '''
    for rule in g:
        print(rule+" : "+str(g[rule]))
