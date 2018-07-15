# Copyright (c) 2018 HarryR. All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0+

PYTHON ?= python
SOLJITSU ?= ./node_modules/.bin/soljitsu
SOLC ?= ./solc-static-linux
SOLC_OPTS ?= --optimize
NPM ?= npm

CONTRACTS ?= UAOSRing MerkleProof AOSRing
CONTRACTS_BIN = $(addprefix build/,$(addsuffix .bin,$(CONTRACTS)))
CONTRACTS_ABI = $(addprefix abi/,$(addsuffix .abi,$(CONTRACTS)))

COVERAGE ?= $(PYTHON) -mcoverage run --source=$(PYNAME) -p

PYNAME = pysolcrypto

PYLINT_IGNORE ?= C0330,too-many-arguments,invalid-name,line-too-long,missing-docstring,bad-whitespace,consider-using-ternary,wrong-import-position,wrong-import-order,trailing-whitespace
FLAKE8_IGNORE ?= E501


#######################################################################


all: $(CONTRACTS_BIN) $(CONTRACTS_ABI) flatten

build:
	mkdir -p build

abi:
	mkdir -p abi

node_modules:
	$(NPM) install


#######################################################################
# Solidity tooling
#

flatten: build $(SOLJITSU)
	$(SOLJITSU) combine --src-dir=contracts/ --dest-dir=build/

$(SOLJITSU): node_modules

clean:
	rm -rf build .coverage .coverage.*
	find . -name '*.pyc' -exec rm '{}' ';'
	find . -name '__pycache__' -exec rm '{}' ';'

abi/%.abi: build/%.abi abi
	cp $< $@

build/%.bin: contracts/%.sol solc-static-linux
	$(SOLC) $(SOLC_OPTS) -o build --asm --bin --overwrite --abi $<

# Retrieve static built solidity compiler for Linux (useful...)
solc-static-linux:
	wget -O $@ "https://github.com/ethereum/solidity/releases/download/v$(shell ./utils/get-package-version.py package.json solc)/solc-static-linux" || rm -f $@
	chmod 755 $@


#######################################################################
# Python tooling
#

.PHONY: test
test:
	$(COVERAGE) -m unittest discover test/

requirements:
	$(PYTHON) -mpip install -r requirements.txt

requirements-dev:
	$(PYTHON) -mpip install -r requirements-dev.txt


#######################################################################
# Lint
#

coverage-combine:
	$(PYTHON) -mcoverage combine

coverage-report:
	$(PYTHON) -mcoverage report

coverage-html:
	$(PYTHON) -mcoverage html

# Unused variables, on error - should be fixed.
lint-pyflakes:
	$(PYTHON) -mpyflakes $(PYNAME)

# Vulture finds unused code
lint-vulture:
	$(PYTHON) -mvulture $(PYNAME) || true

# Finds TODO: items, lots of useful stuff
lint-pylint:
	$(PYTHON) -mpylint -d $(PYLINT_IGNORE) $(PYNAME) || true

# PEP8 strictness
lint-flake8:
	$(PYTHON) -mflake8 --ignore=$(FLAKE8_IGNORE) $(PYNAME)

essential-lint: lint-pyflakes lint-flake8

extra-lint: lint-vulture lint-pylint

lint: essential-lint extra-lint
