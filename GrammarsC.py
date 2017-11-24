# -*- coding: utf-8 -*
import CRules as CR
import Tree
import math
import Grammars as G

"""
GRAMMAIRES
"""

''' ARBRES BINAIRES '''

treeGram = {
    "Tree" : CR.Union(CR.Prod(CR.NonTerm("Tree"), CR.NonTerm("Tree"),
                               lambda a : Tree.Node(a[0], a[1]), lambda t : (t.left(), t.right())),
                      CR.Singleton(Tree.Leaf), lambda t: not (t.is_leaf()))
}

''' MOTS DE FIBONNACI '''

fiboGram = {
    "Fib" : CR.Union(CR.Epsilon(""), CR.NonTerm("Cas1"), G.string_empty),
    "Cas1" : CR.Union(CR.NonTerm("CasAu"), CR.NonTerm("Cas2"), lambda s : s[0] == "A"),
    "Cas2"  : CR.Union(CR.Singleton("B"), CR.Prod(CR.Singleton("B"), CR.NonTerm("CasAu"), "".join, G.sep_first), lambda s : s == "B"),
    "CasAu" : CR.Prod(CR.Singleton("A"), CR.NonTerm("Fib"), "".join, G.sep_first)
}

''' MOTS SUR L'ALPHABET A, B '''

ABGram = {
    "AB" : CR.Union(CR.Epsilon(""), CR.NonTerm("CasAB"), G.string_empty),
    "CasAB" : CR.Union(CR.NonTerm ("CasAu"), CR.NonTerm("CasBu"), lambda s :  s[0] == 'A'),
    "CasAu" : CR.Prod(CR.Singleton("A"), CR.NonTerm("AB"), "".join, G.sep_first),
    "CasBu" : CR.Prod(CR.Singleton("B"), CR.NonTerm("AB"), "".join, G.sep_first)
}

''' MOTS DE DYCK '''


# DyckGram = {
#     "Dyck" : CR.Union(CR.Epsilon(""), CR.NonTerm("Casuu"), G.string_empty),
#     "Casuu" : CR.Prod(CR.NonTerm("Dyck"), CR.NonTerm("Cas(u"), "".join, G.sep_dyck),
#     "Cas(u" : CR.Prod(CR.Singleton("("), CR.NonTerm("Casu)"), "".join, G.sep_first),
#     "Casu)" : CR.Prod(CR.NonTerm("Dyck"), CR.Singleton(")"), "".join, G.sep_last)
# }

DyckGram = {
    "Dyck" : CR.Sequence ("Cas(u", "", "".join, G.string_empty, G.sep_dyck),
    "Cas(u" : CR.Prod(CR.Singleton("("), CR.NonTerm("Casu)"), "".join, G.sep_first),
    "Casu)" :CR.Prod(CR.NonTerm("Dyck"), CR.Singleton(")"), "".join, G.sep_last)
}


''' MOTS QUI N'ONT PAS DEUX LETTRES CONSECUTIVES EGALES '''

TwoGram = {
    "Two" : CR.Union(CR.NonTerm("CasAu"), CR.NonTerm("CasBAu"), lambda s: s=='' or s[0] == 'A'),
    "CasAu" : CR.Union (CR.Epsilon(""), CR.NonTerm("CasABu"), G.string_empty),
    "CasABu": CR.Prod(CR.Singleton("A"), CR.NonTerm("CasBu"), "".join, G.sep_first),
    "CasBu" : CR.Union (CR.NonTerm("CasBAu"), CR.Epsilon(""), lambda s : not G.string_empty(s)),
    "CasBAu" : CR.Prod(CR.Singleton("B"), CR.NonTerm("CasAu"), "".join, G.sep_first)
}

''' MOTS QUI N'ONT PAS TROIS LETTRES CONSECUTIVES EGALES '''

ThreeGram = {
    "Three" : CR.Union(CR.Epsilon(""), CR.NonTerm("S"), G.string_empty),
    "AA"   : CR.Prod(CR.Singleton("A"), CR.Singleton("A"), "".join, G.sep_first),
    "BB"   : CR.Prod(CR.Singleton("B"), CR.Singleton("B"), "".join, G.sep_first),
    "S"    : CR.Union (CR.NonTerm("U"), CR.NonTerm("T"), lambda s : s[0] == 'A'),
    
    "U"    : CR.Union(CR.Singleton("A"), CR.NonTerm("U1"), lambda s : s=='A'),
    "U1"   : CR.Union(CR.NonTerm("AA"), CR.NonTerm("U2"), lambda s : s =="AA"),
    "U2"   : CR.Union(CR.NonTerm("AT"), CR.NonTerm("AAT"), lambda s : s[0] == "A" and s[1] == "B"),
    "AT"   : CR.Prod(CR.Singleton("A"), CR.NonTerm("T"), "".join, G.sep_first),
    "AAT"  : CR.Prod(CR.Singleton("A"), CR.NonTerm("AT"), "".join, G.sep_first),
    "T"    : CR.Union(CR.Singleton("B"), CR.NonTerm("T1"), lambda s : s == "B"),
    "T1"   : CR.Union(CR.NonTerm("BB"), CR.NonTerm("T2"), lambda s : s == "BB"),
    "T2"   : CR.Union(CR.NonTerm("BU"), CR.NonTerm("BBU"), lambda s : s[0] == "B" and s[1] == "A"),
    "BU"   : CR.Prod(CR.Singleton("B"), CR.NonTerm("U"), "".join, G.sep_first),
    "BBU"  : CR.Prod(CR.Singleton("B"), CR.NonTerm("BU"), "".join, G.sep_first),
}

''' PALINDROMES SUR L'ALPHABET A, B '''

ABPalindrome = {
    "Pal" : CR.Union(CR.Epsilon(""), CR.NonTerm("S"), G.string_empty),

    "S"    : CR.Union (CR.Singleton("A"),  CR.NonTerm("S1"), lambda s : s == "A"),
    "S1"   : CR.Union (CR.Singleton("B"),  CR.NonTerm("S2"), lambda s : s == "B"),
    
    "S2"   : CR.Union(CR.NonTerm("ASA"), CR.NonTerm("BSB"), lambda s : s[0] == "A"),

    "ASA"   : CR.Prod(CR.Singleton("A"),
                      CR.Prod(CR.NonTerm("Pal"), CR.Singleton("A"), "".join, G.sep_last), "".join, G.sep_first),
 
    "BSB"   : CR.Prod(CR.Singleton("B"),
                      CR.Prod(CR.NonTerm("Pal"), CR.Singleton("B"), "".join, G.sep_last), "".join, G.sep_first),
}

''' PALINDROMES SUR L'ALPHABET A, B, C '''

ABCPalindrome = {
    "Pal" : CR.Union(CR.Epsilon(""), CR.NonTerm("S"), G.string_empty),

    "S"    : CR.Union (CR.Singleton("A"),  CR.NonTerm("S1"), lambda s : s == "A"),
    "S1"   : CR.Union (CR.Singleton("B"),  CR.NonTerm("S2"), lambda s : s == "B"),
    "S2"   : CR.Union (CR.Singleton("C"),  CR.NonTerm("S3"), lambda s : s == "C"),
    "S3"   : CR.Union (CR.NonTerm("ASA"),
                       CR.Union (CR.NonTerm("BSB"), CR.NonTerm("CSC"), lambda s : s[0] == "B"),
                       lambda s: s[0] == "A"),

    "ASA"   : CR.Prod (CR.Singleton("A"),
                       CR.Prod (CR.NonTerm("Pal"), CR.Singleton("A"), "".join, G.sep_last), "".join, G.sep_first),

    "BSB"   : CR.Prod (CR.Singleton("B"),
                       CR.Prod (CR.NonTerm("Pal"), CR.Singleton("B"), "".join, G.sep_last), "".join, G.sep_first),

    "CSC"   : CR.Prod (CR.Singleton("C"),
                       CR.Prod (CR.NonTerm("Pal"), CR.Singleton("C"), "".join, G.sep_last), "".join, G.sep_first)
}

''' MOTS QUI ONT LE MEME NOMBRE DE A QUE DE B '''


EqualGram = {
    "S" : CR.Union(CR.Epsilon(""), CR.Union(CR.NonTerm("aTbS"), CR.NonTerm("bUaS"))),
    "T" : CR.Union(CR.NonTerm("aTbT"), CR.Epsilon("")),
    "U" : CR.Union(CR.NonTerm("bUaU"), CR.Epsilon("")),
    
    "aTbS" : CR.Prod(CR.Singleton("A"), CR.Prod(CR.NonTerm("T"), CR.Prod(CR.Singleton("B"), CR.NonTerm("S"), "".join), "".join), "".join),
    "bUaS" : CR.Prod(CR.Singleton("B"), CR.Prod(CR.NonTerm("U"), CR.Prod(CR.Singleton("A"), CR.NonTerm("S"), "".join), "".join), "".join),
    "aTbT" : CR.Prod(CR.Singleton("A"), CR.Prod(CR.NonTerm("T"), CR.Prod(CR.Singleton("B"), CR.NonTerm("T"), "".join), "".join), "".join),
    "bUaU" : CR.Prod(CR.Singleton("B"), CR.Prod(CR.NonTerm("U"), CR.Prod(CR.Singleton("A"), CR.NonTerm("U"), "".join), "".join), "".join),

}



grammarsC = {
    "EqualGram" : [EqualGram, "S", G.equal_count],
    "treeGram"  : [treeGram, "Tree", G.tree_count],
    "fiboGram"  : [fiboGram, "Fib", lambda n : G.fibo_count(n+2)],
    "ABGram"    : [ABGram, "AB", lambda n: 2**n],
    "DyckGram"  : [DyckGram, "Dyck", G.dyck_count],
    "TwoGram"   : [TwoGram, "Two", G.two_count],
    "ThreeGram" : [ThreeGram, "Three", G.three_count ],
    "ABPalindrome" : [ABPalindrome, "Pal", lambda x : G.palindrome_count(2, x) ],
    "ABCPalindrome": [ABCPalindrome, "Pal", lambda x : G.palindrome_count(3, x)] 
}

