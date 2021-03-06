/**
 * This library provides glibc symbols required by Oracle Instant Client that
 * are not provided by musl libc, gcompat or other glibc compatibility libs.
 */
#include <resolv.h>
#include <stdlib.h>


extern char *canonicalize_file_name(const char *path) {
	return realpath(path, NULL);
}

extern int __res_nsearch(__attribute__((unused)) res_state statep, const char *dname, int class, int type, unsigned char *answer, int anslen) {
	return res_search(dname, class, type, answer, anslen);
}

extern int __dn_skipname(const unsigned char *comp_dn, const unsigned char *eom) {
	return dn_skipname(comp_dn, eom);
}

// Copied from https://elixir.bootlin.com/musl/v1.0.5/source/src/network/dn_expand.c
extern int __dn_expand(const unsigned char *base, const unsigned char *end, const unsigned char *src, char *dest, int space) {
	const unsigned char *p = src;
	char *dend, *dbegin = dest;
	int len = -1, i, j;
	if (p==end || space <= 0) return -1;
	dend = dest + (space > 254 ? 254 : space);
	/* detect reference loop using an iteration counter */
	for (i=0; i < end-base; i+=2) {
		/* loop invariants: p<end, dest<dend */
		if (*p & 0xc0) {
			if (p+1==end) return -1;
			j = ((p[0] & 0x3f) << 8) | p[1];
			if (len < 0) len = p+2-src;
			if (j >= end-base) return -1;
			p = base+j;
		} else if (*p) {
			if (dest != dbegin) *dest++ = '.';
			j = *p++;
			if (j >= end-p || j >= dend-dest) return -1;
			while (j--) *dest++ = *p++;
		} else {
			*dest = 0;
			if (len < 0) len = p+1-src;
			return len;
		}
	}
	return -1;
}
