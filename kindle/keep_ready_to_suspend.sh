#!/bin/sh

# cf. http://www.mobileread.com/forums/archive/index.php/t-221497.html
/usr/bin/powerd_test -s; lipc-set-prop com.lab126.powerd deferSuspend 3000000
while [ $? -ne 0 ]; do
  sleep 3
  /usr/bin/powerd_test -s; lipc-set-prop com.lab126.powerd deferSuspend 3000000
done
