g++ -DHAVE_CONFIG_H -I. -I../../../ode/src  -I/Users/jbongard/Downloads/ode-0.12/include -DDRAWSTUFF_TEXTURE_PATH="\"/Users/jbongard/Downloads/ode-0.12/drawstuff/textures\"" -DdTRIMESH_ENABLED -DdDOUBLE  -g -O2 -MT demo_buggy.o -MD -MP -c -o demo_buggy.o demo_buggy.cpp
/bin/sh ../../../libtool --tag=CXX   --mode=link g++  -g -O2   -o demo_buggy demo_buggy.o ../../../drawstuff/src/libdrawstuff.la ../../../ode/src/libode.la -framework OpenGL -framework GLUT  -lm  -lpthread
