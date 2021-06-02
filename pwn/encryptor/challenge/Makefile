# make sure to activate python virtual environment first

all: ingecryptor venv
	python -m pip wheel ingecryptor/ -w ./ --no-deps

venv:
	python -m pip install -U pip
	python -m pip install -U ninja setuptools wheel
	
clean:
	rm -rf venv
	rm -f ingecryptor-0.0.1-cp38-cp38-linux_x86_64.whl
