/**
 * This library provides glibc symbols required by Oracle Instant Client that
 * are not provided by musl libc, gcompat or other glibc compatibility libs.
 *
 * They will be available in the upcoming gcompat version
 * (https://twitter.com/weh_kaniini/status/1369955979874492426).
 */
#include <resolv.h>
#include <stdlib.h>


extern char *canonicalize_file_name(const char *path) {
	return realpath(path, NULL);
}

extern int __res_nsearch(res_state statp, const char *dname, int class,
                         int type, unsigned char *answer, int anslen) {

	if (statp == NULL) {
		return -1;
	}
	return res_search(dname, class, type, answer, anslen);
}

extern int __dn_skipname(const unsigned char *comp_dn, const unsigned char *eom) {
	return dn_skipname(comp_dn, eom);
}

extern int __dn_expand(const unsigned char *base, const unsigned char *end,
                       const unsigned char *src, char *dest, int space) {

	return dn_expand(base, end, src, dest, space);
}
