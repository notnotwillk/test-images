# OSv runs position-independent Linux executables, so build one. Run this
# before capstan, which copies files but builds nothing.
potato: potato.c
	$(CC) -O2 -Wall -fpie -pie -o $@ $<

clean:
	rm -f potato

.PHONY: clean
