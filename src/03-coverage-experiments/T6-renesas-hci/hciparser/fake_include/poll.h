#define POLLIN     0x1
#define POLLOUT    0x2
#define POLLERR    0x4
#define POLLNVAL   0x8
#define POLLRDNORM 0x10
#define POLLRDBAND 0x20
#define POLLPRI    0x40
#define POLLWRNORM 0x80
#define POLLWRBAND 0x100
#define POLLHUP    0x200
typedef unsigned int nfds_t;
struct pollfd
{
  int fd;
  short events;
  short revents;
};
