SHELL = /bin/sh

andorbind: andorbind.cpp
	g++ -O3 -Wall -Werror -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) andorbind.cpp -o libandorbind.so
	g++ -O3 -Wall -Werror -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` -I python3 -I . andorbind.cpp -o andorbind`python3-config --extension-suffix` -L. -landorbind -landor -Wl,-rpath,.


