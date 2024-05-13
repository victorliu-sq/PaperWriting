#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>
#include <ctime>
#include <cstdlib>

// Function to split a string by a delimiter into a vector
std::vector<std::string> split(const std::string& str, char delimiter) {
    std::vector<std::string> tokens;
    std::string token;
    std::istringstream tokenStream(str);
    while (std::getline(tokenStream, token, delimiter)) {
        tokens.push_back(token);
    }
    return tokens;
}

// Main function
int main() {
    std::ifstream file("inverse_expanded_driver_groups_by_average_score.csv");
    std::string line;
    std::vector<std::vector<std::string>> allDriverIDs;

    if (!file.is_open()) {
        std::cerr << "Error opening file." << std::endl;
        return 1;
    }

    // Seed the random number generator
    std::srand(unsigned(std::time(nullptr)));

    // Skip the header line
    std::getline(file, line);

    // Read each line from the CSV file
    while (std::getline(file, line)) {
        // Split each line into average score bin and driver IDs
        std::vector<std::string> lineData = split(line, ',');
        if (lineData.size() < 2) continue; // Skip malformed lines

        // Extract driver IDs and randomize them
        std::vector<std::string> driverIDs = split(lineData[1], ',');
        std::random_shuffle(driverIDs.begin(), driverIDs.end());

        // Add randomized list to the main list
        allDriverIDs.push_back(driverIDs);
    }

    file.close();

    // Printing all driver IDs in the order of highest to lowest score
    for (const auto& group : allDriverIDs) {
        for (const auto& id : group) {
            std::cout << id << std::endl;
        }
    }

    return 0;
}
