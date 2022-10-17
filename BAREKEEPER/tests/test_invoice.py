import sys
from subprocess import Popen, PIPE
from BAREKEEPER import BAREKEEPER


def test_invoice_1():
    BAREKEEPER("examples/invoice_1.json").invoice()


def test_invoice_2():
    p = Popen(["jsonnet", "examples/invoice_2.jsonnet"], stdout=PIPE)
    sys.stdin = p.stdout
    BAREKEEPER().invoice()
