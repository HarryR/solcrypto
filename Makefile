SOLJITSU=./node_modules/.bin/soljitsu

build:
	mkdir -p build

flatten: build $(SOLJITSU)
	$(SOLJITSU) combine --src-dir=contracts/ --dest-dir=build/

$(SOLJITSU):
	yarn

clean:
	rm -rf build
	find . -name '*.pyc' -exec rm '{}' ';'