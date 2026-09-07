#include <iostream>
#include <string>

std::string noxen_core(const std::string& input) {
    return "NOXEN C++ Core: " + input;
}

int main(int argc, char* argv[]) {
    std::string input = argc > 1 ? argv[1] : "System Ready";
    std::cout << noxen_core(input) << std::endl;
    return 0;
}
