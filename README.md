# ![BAREKEEPER](./barekeeper.gif)

> Thus said the LORD unto Moses, thou shalt not force a software 
> developer to leave their terminal.
>
> Thou shalt not use a mouse, it is of its father the devil.
>
> ~ Exodus 20:27-28

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
