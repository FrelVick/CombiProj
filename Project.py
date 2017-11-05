# -*- coding: utf-8 -*
import math
import Rules as R
import Tree
import Grammars


class IncorrectGrammar(Exception):

    def __init__(self, message):
        super(IncorrectGrammar, self).__init__(message)
    
# Vérifie que tous les non-terminaux apparaissant dans 
# les règles sont bien définis dans la grammaire

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

    constr_before, constr_after = {}, {}
    for rule in grammar.values():
        if isinstance(rule, R.ConstructorRule):
            constr_before [rule] = rule.valuation() 
            constr_after [rule] = 0

    while (constr_before != constr_after):
        constr_before = constr_after.copy()
        for rule in constr_after:
            rule._update_valuation()
            constr_after[rule] = rule.valuation()
   
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

grammars = Grammars.grammars

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
def tests (name, gram, rule_init, card_fun, valuation = []):
    print ("\nTests on "+name)
    try:
        if len(valuation) != 0:
            print ("Valuation:")
            assert (valuation == get_valuation(gram))
            print ("Passed")
        print ("Cardinality:")
        for i in range(10):
            count = gram[rule_init].count(i)
            assert (count == card_fun(i))
            assert (count == len(gram[rule_init].list(i)))
        print ("Passed")
    except AssertionError:
        print ("Not passed")


for g in grammars:
    init_grammar(grammars[g][0])
    tests(g, grammars[g][0], grammars[g][1], grammars[g][2])
    print (get_valuation(grammars[g][0]))
    print ((grammars[g][0][grammars[g][1]]).list(1))

print("\nTest unrank:")
gram = "ABCPalindrome"
rule = "Pal"
l = grammars[gram][0][rule].list(5)
print (l)
for i in l:
    print(i, grammars[gram][0][rule].rank(i))

print(grammars[gram][0][rule].random(10))

# print("AB",grammars["ABGram"][0]["AB"].rank("AB"))

# for i in range(30):
#     print(grammars["EvenGram"][0]["S"].count(i))
