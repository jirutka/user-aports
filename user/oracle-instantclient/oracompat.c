/**
 * This library provides glibc symbols required by Oracle Instant Client that
 * are not provided by musl libc, gcompat or other glibc compatibility libs.
 *
 * They will be available in the upcoming gcompat version
 * (https://twitter.com/weh_kaniini/status/1369955979874492426).
 */
#include <assert.h>
#include <resolv.h>
#include <stdarg.h>
#include <stdio.h>
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

extern int __printf_chk(__attribute__((unused)) int flag, const char *format, ...) {
	int ret;
	va_list ap;

	assert(format != NULL);

	va_start(ap, format);
	ret = printf(format, ap);
	va_end(ap);

	return ret;
}

extern int __fprintf_chk(FILE *fp, __attribute__((unused)) int flag, const char *format, ...) {
	int ret;
	va_list ap;

	assert(fp != NULL);
	assert(format != NULL);

	va_start(ap, format);
	ret = fprintf(fp, format, ap);
	va_end(ap);

	return ret;
}

extern int __vsprintf_chk(char *s, __attribute__((unused)) int flag,
                          size_t slen, const char *format, va_list ap) {

	assert(s != NULL);
	assert(slen > 0);
	assert(format != NULL);

	return vsnprintf(s, slen, format, ap);
}
