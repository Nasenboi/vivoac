cmake -S . -B build
cmake --build build
cd build && cpack -G productbuild