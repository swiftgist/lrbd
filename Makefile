

all: rpm

rpm: tarball
	rpmbuild -bb lrbd.spec

tarball: tests
	VERSION=`awk '/^Version/ {print $$2}' lrbd.spec`; \
	git archive --prefix lrbd/ -o ~/rpmbuild/SOURCES/lrbd-$$VERSION.tar.gz HEAD

tests:
	@ln -sf lrbd lrbd.py
	@nosetests 
	@rm -f lrbd.py*

