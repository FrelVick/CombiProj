# -*- coding: utf-8 -*
import CRules as CR
import Tree
import math

"""
GRAMMAIRES
"""
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

''' ARBRES BINAIRES '''

treeGram = {
    "Tree" : CR.Union(CR.Prod(CR.NonTerm("Tree"), CR.NonTerm("Tree"),
                              lambda l : Tree.Node(l),lambda t : (t.left(), t.right())),
                      CR.Singleton(Tree.Leaf), lambda t: not (t.is_leaf()))
}

''' MOTS DE FIBONNACI '''

fiboGram = {
    "Fib" : CR.Union(CR.Epsilon(""), CR.NonTerm("Cas1"), string_empty),
    "Cas1" : CR.Union(CR.NonTerm("CasAu"), CR.NonTerm("Cas2"), lambda s : s[0] == "A"),
    "Cas2"  : CR.Union(CR.Singleton("B"), CR.Prod(CR.Singleton("B"), CR.NonTerm("CasAu"), "".join, sep_first), lambda s : s == "B"),
    "CasAu" : CR.Prod(CR.Singleton("A"), CR.NonTerm("Fib"), "".join, sep_first)
}

''' MOTS SUR L'ALPHABET A, B '''

ABGram = {
    "AB" : CR.Union(CR.Epsilon(""), CR.NonTerm("CasAB"), string_empty),
    "CasAB" : CR.Union(CR.NonTerm ("CasAu"), CR.NonTerm("CasBu"), lambda s :  s[0] == 'A'),
    "CasAu" : CR.Prod(CR.Singleton("A"), CR.NonTerm("AB"), "".join, sep_first),
    "CasBu" : CR.Prod(CR.Singleton("B"), CR.NonTerm("AB"), "".join, sep_first)
}

''' MOTS DE DYCK '''

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
            

DyckGram = {
    "Dyck" : CR.Union(CR.Epsilon(""), CR.NonTerm("Casuu"), string_empty),
    "Casuu" : CR.Prod(CR.NonTerm("Dyck"), CR.NonTerm("Cas(u"), "".join, sep_dyck),
    "Cas(u" : CR.Prod(CR.Singleton("("), CR.NonTerm("Casu)"), "".join, sep_first),
    "Casu)" : CR.Prod(CR.NonTerm("Dyck"), CR.Singleton(")"), "".join, sep_last)
}

''' MOTS QUI N'ONT PAS DEUX LETTRES CONSECUTIVES EGALES '''

TwoGram = {
    "Two" : CR.Union(CR.NonTerm("CasAu"), CR.NonTerm("CasBAu"), lambda s: s[0] == 'A'),
    "CasAu" : CR.Union (CR.Epsilon(""), CR.NonTerm("CasABu"), string_empty),
    "CasABu": CR.Prod(CR.Singleton("A"), CR.NonTerm("CasBu"), "".join, sep_first),
    "CasBu" : CR.Union (CR.NonTerm("CasBAu"), CR.Epsilon(""), lambda s : not string_empty(s)),
    "CasBAu" : CR.Prod(CR.Singleton("B"), CR.NonTerm("CasAu"), "".join, sep_first)
}

''' MOTS QUI N'ONT PAS TROIS LETTRES CONSECUTIVES EGALES '''


# # Palindromes sur l'alphabet A, B
# ABPalindrome = {
#     "Pal" : R.UnionRule("Vide", "S", string_empty),
#     "Vide" : R.EpsilonRule(""),
#     "AtomA" : R.SingletonRule("A"),
#     "AtomB" : R.SingletonRule("B"),

#     "S"    : R.UnionRule ("AtomA", "S1", lambda s : s == "A"),
#     "S1"   : R.UnionRule("AtomB", "S2", lambda s : s == "B"),
#     "S2"   : R.UnionRule("ASA", "BSB", lambda s : s[0] == "A"),

#     "ASA"   : R.ProductRule("AtomA", "ASA1", "".join, sep_first),
#     "ASA1"  : R.ProductRule("Pal", "AtomA", "".join, sep_last),
 
#     "BSB"   : R.ProductRule("AtomB", "BSB1", "".join, sep_first),
#     "BSB1"  : R.ProductRule("Pal", "AtomB", "".join, sep_last),
 
# }

# # Palindromes sur l'alphabet A, B, C
# ABCPalindrome = {
#     "Pal" : R.UnionRule("Vide", "S", string_empty),
#     "Vide" : R.EpsilonRule(""),
#     "AtomA" : R.SingletonRule("A"),
#     "AtomB" : R.SingletonRule("B"),
#     "AtomC" : R.SingletonRule("C"),

#     "S"    : R.UnionRule ("AtomA", "S1", lambda s : s == "A"),
#     "S1"   : R.UnionRule("AtomB", "S2", lambda s : s == "B"),
#     "S2"   : R.UnionRule("AtomC", "S3", lambda s : s == "C"),
#     "S3"   : R.UnionRule("ASA", "S4", lambda s: s[0] == "A"),
#     "S4"   : R.UnionRule("BSB", "CSC", lambda s : s[0] == "B"),

#     "ASA"   : R.ProductRule("AtomA", "ASA1", "".join, sep_first),
#     "ASA1"  : R.ProductRule("Pal", "AtomA", "".join, sep_last),
 
#     "BSB"   : R.ProductRule("AtomB", "BSB1", "".join, sep_first),
#     "BSB1"  : R.ProductRule("Pal", "AtomB", "".join, sep_last),

#     "CSC"   : R.ProductRule("AtomC", "CSC1", "".join, sep_first),
#     "CSC1"  : R.ProductRule("Pal", "AtomC", "".join, sep_last),
# }

''' MOTS QUI ONT LE MEME NOMBRE DE A QUE DE B '''

    # "S" : CR.Union(CR.Epsilon(""), CR.Union (CR.NonTerm("ab"), CR.Union(CR.NonTerm("ba"), CR.NonTerm("aMbM"), CR.NonTerm("b#MaM")))),

def count (s, x):
    count = 0
    for c in s:
        if c == x:
            count += 1
    return count

def sep_even (s, sep):
    last_b = False
    print (s, sep)
    for i in range(len(s)):
        print(i, s[i], last_b)
        if last_b and s[i] == sep:
            print ("ici")
            if count(s[:i],'A') == count(s[i:],'A') and count(s[:i],'B') == count(s[i:],'B'):
                return (s[:i], s[i:])
        elif s[i] == sep:
            last_b = True
        else:
            last_b = False
 
EvenGram = {
    "S" : CR.Union(CR.Epsilon(""), CR.NonTerm("S1"), string_empty),
    "S1" : CR.Union(CR.NonTerm("M"), CR.NonTerm("S2"), lambda s : s[0] == 'A' and s[-1] == 'B'),
    "S2" : CR.Union(CR.NonTerm("N"), CR.NonTerm("S3"), lambda s : s[0] == 'B' and s[-1] == 'A'),
    "S3" : CR.Union(CR.NonTerm("MN"), CR.NonTerm("NM"), lambda s : s[0] == 'A'),
    "MN" : CR.Prod(CR.NonTerm("M"), CR.NonTerm("N"), "".join, lambda s : sep_even(s, 'B')),
    "NM" : CR.Prod(CR.NonTerm("N"), CR.NonTerm("M"), "".join, lambda s : sep_even(s, 'A')),
    "M" : CR.Prod(CR.Singleton("A"), CR.NonTerm("Sb"), "".join, sep_first),
    "Sb" : CR.Prod(CR.NonTerm("S"), CR.Singleton("B"), "".join, sep_last),
    "N" : CR.Prod(CR.Singleton("B"), CR.NonTerm("Sa"), "".join, sep_first),
    "Sa" : CR.Prod(CR.NonTerm("S"), CR.Singleton("A"), "".join, sep_last)
} 


EvenGram = {
    
    "S" : CR.Union(CR.Epsilon(""), CR.NonTerm("T"), string_empty),
    "T" : CR.Union(CR.NonTerm("M"), CR.NonTerm("S2"), lambda s : s[0] == 'A' and s[-1] == 'B'),
    "S2" : CR.Union(CR.NonTerm("N"), CR.NonTerm("S3"), lambda s : s[0] == 'B' and s[-1] == 'A'),
    "S3" : CR.Union(CR.NonTerm("MN"), CR.NonTerm("S4"), lambda s : s[0] == 'A'),
    "S4" : CR.Union(CR.NonTerm("NM"), CR.NonTerm("S5")),
    "S5" : CR.Union(CR.NonTerm("AB"), CR.NonTerm("BA")),
    "AB" : CR.Prod(CR.Singleton("A"), CR.Singleton("B"), "".join),
    "BA" : CR.Prod(CR.Singleton("B"), CR.Singleton("A"), "".join),
    "MN" : CR.Prod(CR.NonTerm("M"), CR.NonTerm("N"), "".join, lambda s : sep_even(s, 'B')),
    "NM" : CR.Prod(CR.NonTerm("N"), CR.NonTerm("M"), "".join, lambda s : sep_even(s, 'A')),
    "M" : CR.Prod(CR.Singleton("A"), CR.NonTerm("Tb"), "".join, sep_first),
    "Tb" : CR.Prod(CR.NonTerm("T"), CR.Singleton("B"), "".join, sep_last),
    "N" : CR.Prod(CR.Singleton("B"), CR.NonTerm("Ta"), "".join, sep_first),
    "Ta" : CR.Prod(CR.NonTerm("T"), CR.Singleton("A"), "".join, sep_last)
}

EvenGram = {
    
    "S" : CR.Union(CR.Epsilon(""), CR.NonTerm("T"), string_empty),
    "T" : CR.Union(CR.NonTerm("M"), CR.NonTerm("S2"), lambda s : s[0] == 'A' and s[-1] == 'B'),
    "S2" : CR.Union(CR.NonTerm("N"), CR.NonTerm("S3"), lambda s : s[0] == 'B' and s[-1] == 'A'),
    "S3" : CR.Union(CR.NonTerm("MN"), CR.NonTerm("NM"), lambda s : s[0] == 'A'),
    "AB" : CR.Prod(CR.Singleton("A"), CR.Singleton("B"), "".join),
    "BA" : CR.Prod(CR.Singleton("B"), CR.Singleton("A"), "".join),
    "MN" : CR.Prod(CR.NonTerm("M"), CR.NonTerm("N"), "".join, lambda s : sep_even(s, 'B')),
    "NM" : CR.Prod(CR.NonTerm("N"), CR.NonTerm("M"), "".join, lambda s : sep_even(s, 'A')),
    "M" : CR.Union(CR.NonTerm("mm"), CR.NonTerm("AB")),
    "mm" : CR.Prod(CR.Singleton("A"), CR.NonTerm("Tb"), "".join, sep_first),
    "Tb" : CR.Prod(CR.NonTerm("T"), CR.Singleton("B"), "".join, sep_last),
    "N" : CR.Union(CR.NonTerm("BA"), CR.NonTerm("nn")),
    "nn" : CR.Prod(CR.Singleton("B"), CR.NonTerm("Ta"), "".join, sep_first),
    "Ta" : CR.Prod(CR.NonTerm("T"), CR.Singleton("A"), "".join, sep_last)
}

EvenGram = {
    
    "U" : CR.Union(CR.Epsilon(""), CR.NonTerm("S"), string_empty),
    "S" : CR.Union(CR.NonTerm("aSb"), CR.NonTerm("S2"), lambda s : s[0] == 'A' and s[-1] == 'B'),
    "S2" : CR.Union(CR.NonTerm("bSa"), CR.NonTerm("S3"), lambda s : s[0] == 'B' and s[-1] == 'A'),
    "S3" : CR.Union(CR.NonTerm("abT"), CR.NonTerm("baT"), lambda s : s[0] == 'B' and s[-1] == 'A'),  
    "aSb" : CR.Prod(CR.Singleton("A"), CR.NonTerm("Sb"), "".join),
    "Sb" :  CR.Prod(CR.NonTerm("S"), CR.Singleton("B"), "".join),
    "bSa": CR.Prod(CR.Singleton("B"), CR.NonTerm("Sa"), "".join),
    "Sa" : CR.Prod (CR.NonTerm("S"), CR.Singleton("A"), "".join),
   
    "abT" : CR.Union(CR.NonTerm("AB"), CR.NonTerm("T")),
    "AB" : CR.Prod(CR.Singleton("A"), CR.Singleton("B"), "".join),
    "BA" : CR.Prod(CR.Singleton("B"), CR.Singleton("A"), "".join),
    "baT" : CR.Prod(CR.NonTerm("BA"), CR.NonTerm("T"), "".join),
 
    "T" : CR.Union(CR.NonTerm("S"), CR.Epsilon(""))
}

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
    return num//den

def dyck_count (n):
    if n % 2 == 0:
        return catalan (n//2)
    else:
        return 0

def tree_count (n):
    if n == 0:
        return 0
    else:
        f = math.factorial(n-1)
        return math.factorial(2*(n-1))//(f*f*n)

def palindrome_count (base, n):
    if n == 0:
        return 1
    elif n <= 2:
        return base 
    else:
        return base ** ((n+1)//2)

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

    "EvenGram" : [EvenGram, "U", lambda n : n],
    # "treeGram"  : [treeGram, "Tree", tree_count],
    # "fiboGram"  : [fiboGram, "Fib", lambda n : fibo_count(n+2)],
    # "ABGram"    : [ABGram, "AB", lambda n: 2**n],
    # "DyckGram"  : [DyckGram, "Dyck", dyck_count],
    # "TwoGram"   : [TwoGram, "Two", two_count],
    # "ThreeGram" : [ThreeGram, "Three", three_count ],
    # "ABPalindrome" : [ABPalindrome, "Pal", lambda x : palindrome_count(2, x) ],
    # "ABCPalindrome": [ABCPalindrome, "Pal", lambda x : palindrome_count(3, x)],
 
}

def get_rule_init (g, name):
    return g[name][0][g[name][1]]
