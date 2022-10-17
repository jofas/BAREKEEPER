import json
import sys
import pathlib
import subprocess
import locale
from datetime import datetime
import importlib
import importlib.util
import os

from jinja2 import Environment, PackageLoader
import fire

from src.time import TimeEntry
from src.doc_gen import Invoice, Letter
import src.query_language as ql
import src.grouping_language as gl
from src.util import fmt_date


class BAREKEEPER:
    def __init__(self, filename="-"):
        if filename == "-":
            self.stream = sys.stdin.read()
        else:
            with open(filename) as file:
                self.stream = file.read()

    def time(self, filter=None, group_by=None, transformer="tf.no_tf"):
        entries = [TimeEntry(**e) for e in json.loads(self.stream)]

        if filter is not None:
            q = ql.parse(filter)
            entries = [e for e in entries if q(e)]

        if os.path.isfile(transformer):
            spec = importlib.util.spec_from_file_location(
                "tf.custom", transformer,
            )
            t = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(t)
        else:
            t = importlib.import_module(transformer)

        if group_by is not None:
            if isinstance(group_by, tuple):
                group_by = ",".join(group_by)

            apply_grouping = gl.parse(group_by)
        else:
            apply_grouping = None

        g = gl.Grouping(entries, apply_grouping)

        for k, entries in g.groups():
            g[k] = t.execute(entries)

        g.as_csv(sys.stdout)

    def invoice(self):
        locale.setlocale(locale.LC_ALL, locale="de_DE.UTF-8")

        invoice = Invoice(**json.loads(self.stream))

        env = Environment(
            loader=PackageLoader(__name__),
        )

        template = env.get_template("invoice.tex")

        pathlib.Path("./build").mkdir(exist_ok=True)

        filename = "./build/invoice_nr_{}.tex".format(invoice.invoice_nr)

        # TODO: just provide invoice to template engine
        with open(filename, "w") as file:
            file.write(template.render(
                sender=invoice.sender,
                tax_id=invoice.tax_id,
                payment_details=invoice.payment_details,
                invoice_nr=invoice.invoice_nr,
                invoice_date=invoice.invoice_date,
                recipient=invoice.recipient,
                entries=invoice.entries,
                tax=invoice.tax,
                sum_=invoice.total,
                locale=locale,
            ))

        self._gen_doc(filename)

    def letter(self):
        letter = Letter(**json.loads(self.stream))

        env = Environment(
            loader=PackageLoader(__name__),
        )

        template = env.get_template("letter.tex")

        pathlib.Path("./build").mkdir(exist_ok=True)

        filename = "./build/letter_nr_{}.tex".format(letter.letter_nr)

        # TODO: just provide letter to template engine
        with open(filename, "w") as file:
            file.write(template.render(
                sender=letter.sender,
                letter_date=letter.letter_date,
                recipient=letter.recipient,
                headline=letter.headline,
                content=letter.content,
                closing=letter.closing,
            ))

        self._gen_doc(filename)

    def _gen_doc(self, filename):
        # run two times to make sure everything is build correctly
        # (e.g. latex needs two compilations to get the table of contents
        # right)
        subprocess.run(
            ["lualatex", "--output-directory=./build", filename])
        subprocess.run(
            ["lualatex", "--output-directory=./build", filename])


if __name__ == "__main__":
    fire.Fire(BAREKEEPER)
