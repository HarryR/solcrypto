PYTHON ?= python
SOLJITSU ?= ./node_modules/.bin/soljitsu
SOLC ?= ./solc-static-linux
SOLC_OPTS ?= --optimize
NPM ?= npm

CONTRACTS=UAOSRing MerkleProof AOSRing
CONTRACTS_BIN=$(addprefix build/,$(addsuffix .bin,$(CONTRACTS)))
CONTRACTS_ABI=$(addprefix abi/,$(addsuffix .abi,$(CONTRACTS)))

all: $(CONTRACTS_BIN) $(CONTRACTS_ABI) flatten

build:
	mkdir -p build

flatten: build $(SOLJITSU)
	$(SOLJITSU) combine --src-dir=contracts/ --dest-dir=build/

$(SOLJITSU): node_modules

node_modules:
	$(NPM) install

clean:
	rm -rf build
	find . -name '*.pyc' -exec rm '{}' ';'
	find . -name '__pycache__' -exec rm '{}' ';'

abi:
	mkdir -p abi

abi/%.abi: build/%.abi abi
	cp $< $@

build/%.bin: contracts/%.sol solc-static-linux
	$(SOLC) $(SOLC_OPTS) -o build --asm --bin --overwrite --abi $<

# Retrieve static built solidity compiler for Linux (useful...)
solc-static-linux:
	wget -O $@ "https://github.com/ethereum/solidity/releases/download/v$(shell ./utils/get-package-version.py package.json solc)/solc-static-linux" || rm -f $@
	chmod 755 $@
