#ifndef	_SYS_SOCKET_H
#define	_SYS_SOCKET_H	1
#include <stdint.h>
typedef uint8_t sa_family_t;
typedef uint32_t socklen_t;

struct iovec {
  void  *iov_base;
  size_t iov_len;
};

/* Socket protocol types (TCP/UDP/RAW) */
#define SOCK_STREAM     1
#define SOCK_DGRAM      2
#define SOCK_RAW        3

#define SOCK_CLOEXEC    02000000

#define IOCPARM_MASK    0x7fUL          /* parameters must be < 128 bytes */
#define IOC_VOID        0x20000000UL    /* no parameters */
#define IOC_OUT         0x40000000UL    /* copy out parameters */
#define IOC_IN          0x80000000UL    /* copy in parameters */
#define IOC_INOUT       (IOC_IN|IOC_OUT)
                                        /* 0x20000000 distinguishes new &
                                           old ioctl's */
#define _IO(x,y)        ((long)(IOC_VOID|((x)<<8)|(y)))

#define _IOR(x,y,t)     ((long)(IOC_OUT|((sizeof(t)&IOCPARM_MASK)<<16)|((x)<<8)|(y)))

#define _IOW(x,y,t)     ((long)(IOC_IN|((sizeof(t)&IOCPARM_MASK)<<16)|((x)<<8)|(y)))

#endif
