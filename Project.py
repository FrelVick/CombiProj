# -*- coding: utf-8 -*
import math
import Rules as R
import Tree
import GrammarsC
import CRules as CR

class IncorrectGrammar(Exception):

    def __init__(self, message):
        super(IncorrectGrammar, self).__init__(message)
    
'''Vérifie que tous les non-terminaux apparaissant dans 
les règles sont bien définis dans la grammaire '''
def check_defined_rules (grammar):
    for rule_id in grammar:
        rule = grammar[rule_id]
        if isinstance(rule, R.ConstructorRule):
            fst, snd = rule._parameters
            if not (fst in grammar):
                raise IncorrectGrammar(fst+" rule not defined in grammar")
            if not ( snd in grammar):
               raise IncorrectGrammar(snd+" rule not defined in grammar")
            

# Sets grammar for each rule, computes valuations, checks grammar
def init_grammar (grammar):

    for rule_id in grammar:
        grammar[rule_id]._set_grammar(grammar)

    check_defined_rules(grammar)

    ''' Pour le calcul des valuations on a besoin de comparer 
    les résultats de l'itération courante avec ceux de l'itération précédente,
    on stocke donc les valuations calculées dans les dictionnaires val_before 
    et val_after'''

    val_before, val_after = {}, {}

    for rule in grammar.values():
        if isinstance(rule, R.ConstructorRule):
            val_before[rule] = rule.valuation() 
            val_after [rule] = 0

    # Tant que l'on n'a pas atteint le point fixe, on met à jour les valuations 
    while (val_before != val_after):
        val_before = val_after.copy()
        for rule in val_after:
            rule._update_valuation()
            val_after[rule] = rule.valuation()
   
    # Si on atteint un point fixe pour lequel une des règles à une valuation infine,
    # la grammaire est mal construite
    for rule_id in grammar:
        if grammar[rule_id].valuation() == float('inf'):
            raise IncorrectGrammar("Rule "+rule_id+" is incorrect (inf valuation)")

   


"""
TESTS
"""

"""
grammars est un dictionnaire qui associe au nom d'une grammaire 
une liste qui contient la grammaire, le symbole de départ, et une
fonction qui calcule la taille du langage engendré en fonction de n
(pour les tests)
"""

grammars = GrammarsC.grammars

# Récupérer un dictionnaire associant à chaque règle de la grammaire
# sa valuation
def get_valuation(gram):
    d = {}
    for rule_name in gram:
        d[rule_name] = gram[rule_name].valuation()
    return d
    
# On teste si la valuation et le nombre d'objets calculés à partir
# de l'ensemble de règles correspond aux résultats obtenus à 
# partir de formules.
def tests (name, gram, rule_init, card_fun, n, valuation = []):
    print ("\nTests on "+name)
    rule = gram[rule_init]
    try:

        # V A L U A T I O N 

        if len(valuation) != 0:
            print ("Valuation:")
            assert (valuation == get_valuation(gram))
            print ("Passed")

        # C A R D I N A L I T Y

        print ("\nCardinality:")
        for i in range(n):
            count = rule.count(i)
            # assert (count == card_fun(i))
            assert (count == len(rule.list(i)))
        print ("Passed")

        # R A N K

        try:
            print ("\nRank:")
            assert([rule.rank(i) for i in rule.list(n)] == list(range(rule.count(n))))
            print ("Passed")
        except NotImplementedError:
            print ("Rank not available for this grammar")
        # U N R A N K

        print("\nUnrank:")
        assert(rule.list(n) == [rule.unrank(n, i) for i in list(range(rule.count(n)))])
        print("Passed")

        # V A L U A T I O N  &  C O U N T

        ''' La valuation correspond au plus petit mot qu'une règle peut produire :
        on vérifie donc pour chaque règle que la valeur de la valuation calculée correspond au plus 
        petit produit par la règle'''
        
        print("\nValuation & Count:")
        valuation = get_valuation(gram)
        for rule_name in gram:
            i = 0
            while gram[rule_name].count(i) == 0:
                i += 1
            assert(i == valuation[rule_name])
        print ("Passed")
        
    except AssertionError:
        print ("Not passed")


for g in grammars:
    print (grammars[g][0])
    grammars[g][0] = CR.dvp_gram(grammars[g][0])
    init_grammar(grammars[g][0])
    tests(g, grammars[g][0], grammars[g][1], grammars[g][2], 4)
    # print (get_valuation(grammars[g][0]))
    # print ((grammars[g][0][grammars[g][1]]).list(1))

# g = "EvenGram"
# grammars[g][0] = CR.dvp_gram(grammars[g][0])
# init_grammar(grammars[g][0])
# for i in range (10):
#     d = {}
#     l = (grammars[g][0]["S"].list(i))
#     print (len(l))
#     for i in range(len(l)):
#         if i not in d:
#             d[i] = l[i]
#         else:
#             raise ValueError("doublon")

        
''' CACHING :
pour les tests sur toutes les gram taille 7 15s vs 18s
pour les test sur toutes les gram taille 8  1m20 vs 1m40'''

''' TESTS GRAMMAIRE CONDENSEE ''' 

ng = {"Tree" : CR.Union (CR.Singleton (Tree.Leaf), 
                         CR.Prod(CR.NonTerm ("Tree"), CR.NonTerm ("Tree"), 
                                 lambda l : Tree.Node(l)))}

# Version condensée
DyckGram = {
    "Dyck" : CR.Union(CR.Epsilon(""), CR.Prod(CR.NonTerm("Dyck"), CR.NonTerm("Cas(u"), "".join)), 
    "Cas(u" : CR.Prod(CR.Singleton("("), CR.NonTerm("Casu)"), "".join),
    "Casu)" :CR.Prod(CR.NonTerm("Dyck"), CR.Singleton(")"), "".join)
}

# Version condensée avec Sequence
DyckGram = {
    "Dyck" : CR.Sequence ("Cas(u", "", "".join),
    "Cas(u" : CR.Prod(CR.Singleton("("), CR.NonTerm("Casu)"), "".join),
    "Casu)" :CR.Prod(CR.NonTerm("Dyck"), CR.Singleton(")"), "".join)
}

g = CR.dvp_gram(DyckGram)

for k in g:
    print (k, str(g[k]))

init_grammar(g)

print(g["Dyck"].list(6))

''' TESTS GRAMMAIRE CONDENSEE '''

''' TESTS BOUND '''

''' TEST SEQUENCE ''' 
