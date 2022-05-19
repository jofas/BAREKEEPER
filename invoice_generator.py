import sys
import pathlib
import subprocess
import locale
import json
from types import SimpleNamespace

from jinja2 import Environment, PackageLoader
import fire

from _types import Invoice, Letter


def invoice(filename="-"):
    locale.setlocale(locale.LC_ALL, locale="de_DE.UTF-8")

    env = Environment(
        loader=PackageLoader(__name__),
    )

    template = env.get_template("invoice.tex")

    if filename == "-":
        stream = sys.stdin.read()
    else:
        with open(filename) as file:
            stream = file.read()

    invoice = Invoice.fromNamespace(json.loads(
        stream,
        object_hook=lambda d: SimpleNamespace(**d),
    ))

    sum_ = sum([entry.price for entry in invoice.entries])
    tax = sum_ * 0.19

    pathlib.Path("./build").mkdir(exist_ok=True)

    filename = "./build/invoice_nr_{}.tex".format(invoice.invoice_nr)

    with open(filename, "w") as file:
        file.write(template.render(
            sender=invoice.sender,
            tax_id=invoice.tax_id,
            payment_details=invoice.payment_details,
            invoice_nr=invoice.invoice_nr,
            invoice_date=invoice.invoice_date,
            recipient=invoice.recipient,
            entries=invoice.entries,
            tax=tax,
            sum_=sum_,
            locale=locale,
        ))

    _build(filename)


def letter(filename="-"):
    env = Environment(
        loader=PackageLoader(__name__),
    )

    template = env.get_template("letter.tex")

    if filename == "-":
        stream = sys.stdin.read()
    else:
        with open(filename) as file:
            stream = file.read()

    letter = Letter.fromNamespace(json.loads(
        stream,
        object_hook=lambda d: SimpleNamespace(**d),
    ))

    pathlib.Path("./build").mkdir(exist_ok=True)

    filename = "./build/letter_nr_{}.tex".format(letter.letter_nr)

    with open(filename, "w") as file:
        file.write(template.render(
            sender=letter.sender,
            letter_date=letter.letter_date,
            recipient=letter.recipient,
            headline=letter.headline,
            content=letter.content,
            closing=letter.closing,
        ))

    _build(filename)


def _build(filename):
    # run two times to make sure everything is build correctly
    # (e.g. latex needs two compilations to get the table of contents
    # right)
    subprocess.run(
        ["lualatex", "--output-directory=./build", filename])
    subprocess.run(
        ["lualatex", "--output-directory=./build", filename])


if __name__ == "__main__":
    fire.Fire()
