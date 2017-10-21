import Rules as R
import Tree
import math



# Exception thrown if the valuation of the rule
# of a nonterminal symbol is inf

class IncorrectGrammar(Exception):

    def __init__(self, rule):
        message = "Rule "+ rule + " is incorrect"
        super(IncorrectGrammar, self).__init__(message)

# Sets grammar for each rule, computes valuations, checks grammar
def init_grammar (grammar):

    for rule_id in grammar:
        grammar[rule_id]._set_grammar(grammar)

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
            raise IncorrectGrammar(rule_id)
   
   

"""
GRAMMARS
"""

treeGram = {"Tree" : R.UnionRule("Node", "Leaf"),
            "Node" : R.ProductRule("Tree", "Tree",
            lambda (a, b) : Node(a, b)),
            "Leaf" : R.SingletonRule(Tree.Leaf)}

fiboGram = { "Fib"   : R.UnionRule("Vide", "Cas1"),
             "Cas1"  : R.UnionRule("CasAu", "Cas2"),
             "Cas2"  : R.UnionRule("AtomB", "CasBAu"),
             "Vide"  : R.EpsilonRule(""),
             "CasAu" : R.ProductRule("AtomA", "Fib", "".join),
             "AtomA" : R.SingletonRule("A"),
             "AtomB" : R.SingletonRule("B"),
             "CasBAu": R.ProductRule("AtomB", "CasAu", "".join)}

init_grammar(treeGram)
init_grammar(fiboGram)

"""
TESTS
"""

# From TP3
def tree_cardinality(n):
    """
    Return the cardinality of the set
    """
    f = math.factorial(n)
    return math.factorial(2*n)/(f*f*(n+1))

""" Cardinality of fibonacci words of length n  
is fibonacci(n + 2)""" 
def fibo_words_cardinality(n, d = {}):
    if (n < 0):
        raise ValueError("Negative number")
    elif (n <= 1):
        return n
    else:
        if not n - 1 in d:
            d[n - 1] = fibo_words_cardinality(n - 1, d)
        if not n - 2 in d:
            d[n - 2] = fibo_words_cardinality(n - 2, d) 
        return d[n - 1] + d[n - 2]

def test_cardinality_tree (n, T):
    if n == 0:
        assert (0 == T.count(n))
    else:
        assert(tree_cardinality(n-1) == T.count(n))

def test_cardinality_fibo (n, F):
    assert(fibo_words_cardinality(n + 2) == F.count(n))
        
def get_valuation(gram):
    d = {}
    for rule_name in gram:
        d[rule_name] = gram[rule_name].valuation()
    return d

def tests (name, gram, rule_init, valuation, card_fun):
    print ("\nTests on "+name)
    try:
        print ("Valuation:")
        assert (valuation == get_valuation(gram))
        print ("Passed")
        print ("Cardinality:")
        for i in range(10):
            card_fun(i, gram[rule_init])
        print ("Passed")
    except AssertionError:
        print ("Not passed")

tests("treeGram", treeGram, "Tree", 
      {"Tree" : 1, "Leaf" : 1, "Node" : 2}, test_cardinality_tree)


tests("fiboGram", fiboGram, "Fib",
      {"Fib" : 0, "Cas1" : 1, "Cas2" : 1, "Vide" : 0,
       "CasAu" : 1, "AtomA" : 1, "AtomB" : 1, "CasBAu" : 2}, 
      test_cardinality_fibo)

