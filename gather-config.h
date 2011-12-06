/* This file is here to prevent a file conflict on multiarch systems.  A
 * conflict will frequently occur because arch-specific build-time
 * configuration options are stored (and used, so they can't just be stripped
 * out) in gather-config.h.  The original gather-config.h has been renamed.
 * DO NOT INCLUDE THE NEW FILE DIRECTLY -- ALWAYS INCLUDE THIS ONE INSTEAD. */

#ifdef gather_config_multilib_redirection_h
#error "Do not define gather_config_multilib_redirection_h!"
#endif
#define gather_config_multilib_redirection_h

#if defined(__i386__)
#include "sblim-gather-i386.h"
#elif defined(__ia64__)
#include "sblim-gather-ia64.h"
#elif defined(__powerpc64__)
#include "sblim-gather-ppc64.h"
#elif defined(__powerpc__)
#include "sblim-gather-ppc.h"
#elif defined(__s390x__)
#include "sblim-gather-s390x.h"
#elif defined(__s390__)
#include "sblim-gather-s390.h"
#elif defined(__x86_64__)
#include "sblim-gather-x86_64.h"
#else
#error "This sblim-gather-devel package does not work your architecture?"
#endif

#undef gather_config_multilib_redirection_h
