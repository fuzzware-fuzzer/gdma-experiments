#include <byteswap.h>
#define ntohs(x) bswap_16(x)
#define htons(x) bswap_16(x)
#define ntohl(x) bswap_32(x)
#define htonl(x) bswap_32(x)
