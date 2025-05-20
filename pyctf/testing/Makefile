include ../config/Makefile.config

all: project.so

project.so: project.c
	env PYMODNAME=project PYMODLIBS="" $(MAKE) -f $(CONFDIR)/Makefile.pymod

clean:
	rm -f *~ *.so *.o *.pyc
