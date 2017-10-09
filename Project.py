from abc import ABCMeta, abstractmethod


class AbstractRule:
    __metaclass__ = ABCMeta

    def __init__(self):
        self._grammar = {}

    def _set_grammar(self, gram):
        self._grammar = gram


class ConstantRule(AbstractRule):
    def __init__(self):
        super(ConstantRule, self).__init__()
        self._object = self


class ConstructorRule(AbstractRule):
    def __init__(self, value):
        super(ConstructorRule, self).__init__()
        self._valuation = float('inf')
        self._parameters = value

    def valuation(self):
        return self._valuation

    @abstractmethod
    def _calc_valuation(self):
        """update valuation"""

    def _update_valuation(self):
        self._grammar[self._parameters[0]]._update_valuation()


class UnionRule(ConstructorRule):
    def __init__(self, value):
        super(UnionRule, self).__init__(value)


assert issubclass(ConstantRule, AbstractRule)

b = ConstantRule()
c = ConstantRule()

b._grammar = "test dict"
print c._grammar
