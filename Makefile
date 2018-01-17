SOLJITSU=./node_modules/.bin/soljitsu
SOLC=solc --optimize

CONTRACTS=UAOSRing MerkleProof AOSRing
CONTRACTS_BIN=$(addprefix build/,$(addsuffix .bin,$(CONTRACTS)))
CONTRACTS_ABI=$(addprefix abi/,$(addsuffix .abi,$(CONTRACTS)))

all: $(CONTRACTS_BIN) $(CONTRACTS_ABI) flatten

build:
	mkdir -p build

flatten: build $(SOLJITSU)
	$(SOLJITSU) combine --src-dir=contracts/ --dest-dir=build/

$(SOLJITSU):
	yarn

clean:
	rm -rf build
	find . -name '*.pyc' -exec rm '{}' ';'

abi:
	mkdir -p abi

abi/%.abi: build/%.abi abi
	cp $< $@

build/%.bin: contracts/%.sol
	$(SOLC) -o build --asm --bin --overwrite --abi $<
