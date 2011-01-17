from sympy import symbols, Integer

from sympy.physics.quantum.dagger import Dagger
from sympy.physics.quantum.anticommutator import AntiCommutator as AComm
from sympy.physics.quantum.operator import Operator


a, b, c = symbols('abc')
A, B, C, D = symbols('ABCD', commutative=False)


def test_anticommutator():
    ac = AComm(A,B)
    assert isinstance(ac, AComm)
    assert ac.is_commutative == False
    assert ac.subs(A,C) == AComm(C,B)

def test_commutator_identities():
    assert AComm(a*A,b*B) == a*b*AComm(A,B)
    assert AComm(A, A) == 2*A**2
    assert AComm(A, B) == AComm(B, A)
    assert AComm(a, b) == 2*a*b
    assert AComm(A,B).doit() == A*B + B*A


def test_anticommutator_dagger():
    assert Dagger(AComm(A, B)) == AComm(Dagger(A),Dagger(B))


class Foo(Operator):

    def _eval_anticommutator_Bar(self, bar):
        return Integer(0)


class Bar(Operator):
    pass


class Tam(Operator):

    def _eval_anticommutator_Foo(self, foo):
        return Integer(1)


def test_eval_commutator():
    F = Foo('F')
    B = Bar('B')
    T = Tam('T')
    assert AComm(F,B).doit() == 0
    assert AComm(B,F).doit() == 0
    assert AComm(F,T).doit() == 1
    assert AComm(T,F).doit() == 1
    assert AComm(B,T).doit() == B*T + T*B