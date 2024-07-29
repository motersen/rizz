DESTDIR=$(HOME)/bin

install: rosin rosin-tune.pl rosin-play.py
	install -Dm755 rosin-tune.pl rosin-play.py rosin $(DESTDIR)

uninstall:
	rm -rf $(DESTDIR)/rosin-tune.pl $(DESTDIR)/rosin-play.py $(DESTDIR)/rosin
