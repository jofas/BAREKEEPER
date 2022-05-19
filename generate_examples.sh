python3 invoice_generator.py invoice examples/invoice_1.json
cp build/invoice_nr_1.pdf examples/invoice_1.pdf

jsonnet examples/invoice_2.jsonnet | python3 invoice_generator.py invoice -
cp build/invoice_nr_2.pdf examples/invoice_2.pdf

python3 invoice_generator.py letter examples/letter_1.json
cp build/letter_nr_1.pdf examples/letter_1.pdf

jsonnet examples/letter_2.jsonnet | python3 invoice_generator.py letter -
cp build/letter_nr_2.pdf examples/letter_2.pdf
