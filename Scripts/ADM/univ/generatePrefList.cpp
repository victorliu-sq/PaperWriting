#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>  // Include for std::sort, std::unique, and std::shuffle
#include <random>     // Include for std::default_random_engine
#include <chrono>     // Include for std::chrono::system_clock
#include <cstdlib>    // For std::exit()

// Function to remove double quotes from a string
void removeQuotes(std::string& s) {
    s.erase(remove(s.begin(), s.end(), '\"'), s.end());
}

int main() {
    std::string filename = "/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/ADM/univ/Grouped_Students.csv";
    std::ifstream file(filename);

    if (!file.is_open()) {
        std::cerr << "Error: Could not open the file." << std::endl;
        return 1;
    }

    std::string line;
    std::vector<int> driverIDs;
    std::vector<int> tempGroup; // Temporary vector to hold and shuffle group IDs
    int lineNumber = 0;

    // Setup random number generator
    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::default_random_engine engine(seed);

    // Read lines from the file
    while (getline(file, line)) {
        if (lineNumber++ == 0) continue; // Skip the header line if there is one

        std::stringstream ss(line);
        std::string cell;
        int cellNumber = 0;

        // Read each cell in the line
        while (getline(ss, cell, ',')) {
            if (cellNumber++ == 0) continue; // Skip the first column

            std::stringstream idStream(cell);
            std::string id;
            tempGroup.clear(); // Clear previous group data

            // Parse all driver IDs
            while (getline(idStream, id, ',')) {
                try {
                    if (!id.empty()) {
                        removeQuotes(id);
                        tempGroup.push_back(std::stoi(id));
                    }
                } catch (const std::invalid_argument& ia) {
                    std::cerr << "Invalid argument: " << ia.what() << " at line " << lineNumber << " with ID '" << id << "'" << std::endl;
                    file.close();
                    std::exit(EXIT_FAILURE);
                } catch (const std::out_of_range& oor) {
                    std::cerr << "Out of range: " << oor.what() << " at line " << lineNumber << " with ID '" << id << "'" << std::endl;
                    file.close();
                    std::exit(EXIT_FAILURE);
                }
            }
            // Shuffle the current group's IDs before adding to the main vector
            std::shuffle(tempGroup.begin(), tempGroup.end(), engine);
            driverIDs.insert(driverIDs.end(), tempGroup.begin(), tempGroup.end());
        }
    }
    file.close();

    // Verify all IDs from 0 to 19999 are present
    std::sort(driverIDs.begin(), driverIDs.end());
    auto unique_end = std::unique(driverIDs.begin(), driverIDs.end());
    driverIDs.erase(unique_end, driverIDs.end()); // Remove duplicate entries

    if (driverIDs.size() != 20000) {
        std::cerr << "Error: Total driver IDs read (" << driverIDs.size() << ") does not match expected count of 20000." << std::endl;
        return 1;
    }

    for (int i = 0; i < 20000; ++i) {
        if (driverIDs[i] != i) {
            std::cerr << "Error: Missing driver ID " << i << std::endl;
            return 1;
        }
    }

    std::cout << "All driver IDs from 0 to 19999 are present and correctly ordered." << std::endl;

    return 0;
}
