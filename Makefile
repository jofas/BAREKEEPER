pep8:
	autopep8 --in-place -r --aggressive --aggressive ./

test:
	pytest

coverage:
	coverage run -m pytest
	coverage report
