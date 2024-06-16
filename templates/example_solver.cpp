#include <iostream>
#include <fstream>

struct Answer {
    int value;

    int calc_score() {
        return value * value;
    }
};

// Solve a problem and return the score
int solve() {
    int a, b;
    std::cin >> a >> b;
    Answer ans{a + b};
    std::cout << ans.value << std::endl;
    return ans.calc_score();
};

int main(int argc, char *argv[]) {
    int score = solve();

    // Here is an example of how to pass the score to cp-heuristics-adapter.
    if (argc != 1) {
        // Destination file path is passed as the first argument.
        std::ofstream score_file_stream(argv[1]);
        // Print the score in a line.
        score_file_stream << score << std::endl;
    }
    return 0;
}
