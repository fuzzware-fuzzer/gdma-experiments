#ifndef DMA_TEST_PW_CHECK
#define DMA_TEST_PW_CHECK

#define EXPORT_DMA_BUFFER_ALIAS(name) \
  extern __typeof(name) __attribute__ ((alias (#name))) dma_buf;

#define EXPORT_DMA_BUFFER_ALIAS_NUM(name, num) \
  extern __typeof(name) __attribute__ ((alias (#name))) dma_buf_##num;

#define PASSWORD_CHECK_LEN 8
#define CRASH_ADDR 0x77889900
__attribute__ ((noinline)) void pwcheck_success() {
  *((unsigned int *)(CRASH_ADDR)) = 0x13371337;
}

static const char password[PASSWORD_CHECK_LEN] = {'P', 'a', 's', 's', 'w', 'o', 'r', 'd'};
/* num_correct is incremented to create a side effect such that the checking is
   not inlined. This sticks around as its exported, but would not survive LTO? */
int num_correct = 0;
__attribute__ ((noinline)) void pwcheck_passed_1() {++num_correct;}
__attribute__ ((noinline)) void pwcheck_passed_2() {++num_correct;}
__attribute__ ((noinline)) void pwcheck_passed_3() {++num_correct;}
__attribute__ ((noinline)) void pwcheck_passed_4() {++num_correct;}
__attribute__ ((noinline)) void pwcheck_passed_5() {++num_correct;}
__attribute__ ((noinline)) void pwcheck_passed_6() {++num_correct;}
__attribute__ ((noinline)) void pwcheck_passed_7() {++num_correct;}
__attribute__ ((noinline)) void pwcheck_passed_8() {++num_correct;}

/* noclone makes sure the argument does not get constprop'ed */
__attribute__((noinline,noclone)) void check_password(void *buf) {
  num_correct = 0;
  if (((char *)buf)[0] == password[0]) {
    pwcheck_passed_1();
    if (((char *)buf)[1] == password[1]) {
      pwcheck_passed_2();
      if (((char *)buf)[2] == password[2]) {
        pwcheck_passed_3();
        if (((char *)buf)[3] == password[3]) {
          pwcheck_passed_4();
          if (((char *)buf)[4] == password[4]) {
            pwcheck_passed_5();
            if (((char *)buf)[5] == password[5]) {
              pwcheck_passed_6();
              if (((char *)buf)[6] == password[6]) {
                pwcheck_passed_7();
                if (((char *)buf)[7] == password[7]) {
                  pwcheck_passed_8();
                  pwcheck_success();
                }
              }
            }
          }
        }
      }
    }
  }
}

/* noclone makes sure the arguments do not get constprop'ed */
__attribute__ ((noinline,noclone)) void check_password_scatter_gather(void *buf1, void *buf2) {
  num_correct = 0;
  if (((char *)buf1)[0] == password[0]) {
    pwcheck_passed_1();
    if (((char *)buf2)[0] == password[4]) {
      pwcheck_passed_2();
      if (((char *)buf1)[1] == password[1]) {
        pwcheck_passed_3();
        if (((char *)buf2)[1] == password[5]) {
          pwcheck_passed_4();
          if (((char *)buf1)[2] == password[2]) {
            pwcheck_passed_5();
            if (((char *)buf2)[2] == password[6]) {
              pwcheck_passed_6();
              if (((char *)buf1)[3] == password[3]) {
                pwcheck_passed_7();
                if (((char *)buf2)[3] == password[7]) {
                  pwcheck_passed_8();
                  pwcheck_success();
                }
              }
            }
          }
        }
      }
    }
  }
}

__attribute__ ((noinline)) void fuzzing_exit(void) {
  while(1);
}

#endif

