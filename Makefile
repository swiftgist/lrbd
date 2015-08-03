

all: rpm

tarball:
	VERSION=`awk '/^Version/ {print $$2}' lrbd.spec`; \
	git archive --prefix lrbd/ -o ~/rpmbuild/SOURCES/lrbd-$$VERSION.tar.gz HEAD

rpm: tarball
	rpmbuild -bb lrbd.spec

