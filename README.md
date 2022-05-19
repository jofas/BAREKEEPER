# ![BAREKEEPER](./barekeeper.gif)

Generates invoice PDFs from structured data using a LaTeX template.
The data is provided by a `json/jsonnet` file.
Also supports the generation of business letters.


## Example

The example documents in the `examples/` dir are generated via:

```bash
sh generate_examples.sh
```

**Note:** the number in the filename of the generated PDF comes from
the `invoice_nr`/`letter_nr` provided by the `json` input.


## Dependencies

* `tex-live (linux/macOs)` or `MikeTeX (Windows)` with
  `lualatex` installed

* `python 3`

* the `jinja2` and `fire` python packages


## TODO

* [ ] move to new repo

* [ ] archive `invoice_generator`

* [ ] installation script (and maybe single distribution with
  dependencies included?)

* [ ] `JSONNET_PATH` for importing the `.libsonnet` files

* [ ] replace `pdflatex` with `reportlab` or some other python native
  pdf generator

* [ ] time management

* [ ] offer generator

* [ ] cost management
