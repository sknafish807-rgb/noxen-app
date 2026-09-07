#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "NOXEN C++ Core: No input";
        return 0;
    }

    std::cout << "NOXEN C++ Core: " << argv[1];
    return 0;
}
