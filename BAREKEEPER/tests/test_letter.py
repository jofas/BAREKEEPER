import sys
from subprocess import Popen, PIPE
from BAREKEEPER import BAREKEEPER


def test_letter_1():
    BAREKEEPER("examples/letter_1.json").letter();


def test_letter_2():
    p = Popen(["jsonnet", "examples/letter_2.jsonnet"], stdout=PIPE)
    sys.stdin = p.stdout
    BAREKEEPER().letter();
