OBJ = progress
CFLAGS ?= -g
override CFLAGS += -Wall -D_FILE_OFFSET_BITS=64
override LDFLAGS += -lm
UNAME := $(shell uname)
PKG_CONFIG ?= pkg-config
ifeq ($(UNAME), Linux)
    ifeq (, $(shell which $(PKG_CONFIG) 2> /dev/null))
    $(error "pkg-config command not found")
    endif
    ifeq (, $(shell $(PKG_CONFIG) ncursesw --libs 2> /dev/null))
    $(error "ncurses package not found")
    endif
    override LDFLAGS += $(shell $(PKG_CONFIG) ncursesw --libs)
endif
ifeq ($(UNAME), Darwin)
    override LDFLAGS += -lncurses
endif
ifeq ($(UNAME), FreeBSD)
    override LDFLAGS += -lncurses -lprocstat
endif
PREFIX ?= /usr/local
BINDIR = $(PREFIX)/bin
MANDIR = $(PREFIX)/share/man/man1

$(OBJ) : progress.o sizes.o hlist.o
	$(CC) -Wall $^ -o $@ $(LDFLAGS)
%.o : %.c
	$(CC) $(CFLAGS) -c $^
clean :
	rm -f *.o $(OBJ)
install : $(OBJ)
	@echo "Installing program to $(DESTDIR)$(BINDIR) ..."
	@mkdir -p $(DESTDIR)$(BINDIR)
	@install -pm0755 $(OBJ) $(DESTDIR)$(BINDIR)/$(TARGET) || \
	echo "Failed. Try "make PREFIX=~ install" ?"
	@echo "Installing manpage to $(DESTDIR)$(MANDIR) ..."
	@mkdir -p $(DESTDIR)$(MANDIR)
	@install -pm0644 $(OBJ).1 $(DESTDIR)$(MANDIR)/ || \
	echo "Failed. Try "make PREFIX=~ install" ?"
uninstall :
	@rm -f $(DESTDIR)$(BINDIR)/$(OBJ)
	@rm -f $(DESTDIR)$(MANDIR)/$(OBJ).1
