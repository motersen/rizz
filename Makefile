DESTDIR=$(HOME)/bin

install: rizz rizz-up.py
	install -Dm755 rizz rizz-up.py $(DESTDIR)

uninstall:
	rm -rf $(DESTDIR)/rizz $(DESTDIR)/rizz-up.py
