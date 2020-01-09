include python/examples/Makefile.mk
include python/ola/Makefile.mk

python/PyCompileTest.sh: python/Makefile.mk
	mkdir -p $(top_builddir)/python
	echo "$(PYTHON) -m compileall -f tools scripts python include data; exit \$$?" > $(top_builddir)/python/PyCompileTest.sh
	chmod +x $(top_builddir)/python/PyCompileTest.sh

if BUILD_PYTHON_LIBS
test_scripts += \
    python/PyCompileTest.sh
endif

CLEANFILES += \
    python/PyCompileTest.sh
