#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>
#include <random>
#include <chrono>
#include <thread>
#include <mutex>
#include <vector>

using PreferenceLists = std::vector<std::vector<int> >;

// Function to remove double quotes from a string
void removeQuotes(std::string& s) {
    s.erase(remove(s.begin(), s.end(), '\"'), s.end());
}

// Thread function to generate preference lists
void generateLists(const std::vector<std::vector<int> >& groups, PreferenceLists& preferenceLists, int start, int end, int thread_id) {
    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count() + thread_id;
    std::default_random_engine engine(seed);

    for (int i = start; i < end; ++i) {
        std::vector<int> preferenceList;
        for (auto& group : groups) {
            std::vector<int> shuffledGroup = group;
            std::shuffle(shuffledGroup.begin(), shuffledGroup.end(), engine);
            preferenceList.insert(preferenceList.end(), shuffledGroup.begin(), shuffledGroup.end());
        }
        preferenceLists[i] = preferenceList;
    }
}

// Function to read the initial groups from the file
std::vector<std::vector<int> > readGroups(const std::string& filename) {
    std::ifstream file(filename);
    std::vector<std::vector<int> > groups;
    std::string line;

    if (!file.is_open()) {
        std::cerr << "Error: Could not open the file." << std::endl;
        std::exit(EXIT_FAILURE);
    }

    int lineNumber = 0;
    while (getline(file, line)) {
        if (lineNumber++ == 0) continue; // Skip header

        std::vector<int> group;
        std::stringstream ss(line);
        std::string cell;
        int cellNumber = 0;

        while (getline(ss, cell, ',')) {
            if (cellNumber++ == 0) continue; // Skip the first column

            std::stringstream idStream(cell);
            std::string id;
            while (getline(idStream, id, ',')) {
                if (!id.empty()) {
                    removeQuotes(id);
                    group.push_back(std::stoi(id));
                }
            }
        }
        groups.push_back(group);
    }
    file.close();
    return groups;
}

int main() {
    std::string filename = "/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/JOB/hr/grouped_applicants.csv";
    int numLists = 20000;
    int numThreads = 4; // Adjust based on your hardware capabilities
    PreferenceLists preferenceLists(numLists);

    std::vector<std::thread> threads;
    std::vector<std::vector<int> > groups = readGroups(filename);

    int chunkSize = numLists / numThreads;
    for (int i = 0; i < numThreads; ++i) {
        int start = i * chunkSize;
        int end = (i == numThreads - 1) ? numLists : start + chunkSize;
        threads.emplace_back(generateLists, std::ref(groups), std::ref(preferenceLists), start, end, i);
    }

    for (auto& thread : threads) {
        thread.join();
    }

    std::cout << "Generated " << preferenceLists.size() << " preference lists." << std::endl;
    std::cout << "First list size: " << preferenceLists[0].size() << std::endl;

    return 0;
}
