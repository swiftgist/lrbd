

all: rpm

tarball:
	tar -czf ~/rpmbuild/SOURCES/lrbd-0.9.0.tar.gz --exclude .??* -C .. lrbd

rpm: tarball
	rpmbuild -bb lrbd.spec

