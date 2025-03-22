#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <unordered_map>
#include <set>
#include <algorithm>
#include <regex>

using namespace std;

// Function to find all repeating substrings
vector<string> find_repeating_substrings(const vector<string>& strings) {
    unordered_map<string, int> substring_count;
    set<string> repeating_substrings;

    for (const string& s : strings) {
        set<string> seen_in_current;
        int length = s.size();

        for (int i = 0; i < length; ++i) {
            for (int j = i + 1; j <= length; ++j) {
                string sub = s.substr(i, j - i);
                
                if (seen_in_current.find(sub) != seen_in_current.end()) {
                    repeating_substrings.insert(sub);
                } else {
                    substring_count[sub]++;
                    if (substring_count[sub] > 1) {
                        repeating_substrings.insert(sub);
                    }
                    seen_in_current.insert(sub);
                }
            }
        }
    }

    // Sort substrings from longest to shortest
    vector<string> sorted_repeating(repeating_substrings.begin(), repeating_substrings.end());
    sort(sorted_repeating.begin(), sorted_repeating.end(), 
         [](const string& a, const string& b) { return a.size() > b.size(); });

    return sorted_repeating;
}

// Function to replace substrings using regex
string regex_replace_substrings(const string& s, const unordered_map<string, string>& replacement_map) {
    string result = s;
    
    for (const auto& [sub, replacement] : replacement_map) {
        result = regex_replace(result, regex(sub), replacement);
    }
    
    return result;
}

// Main function to replace repeating substrings with numbered placeholders
pair<vector<string>, unordered_map<string, string>> replace_with_numbers(const vector<string>& strings) {
    vector<string> repeating_substrings = find_repeating_substrings(strings);
    unordered_map<string, string> substring_to_number;

    // Assign numbers to repeating substrings
    for (size_t i = 0; i < repeating_substrings.size(); ++i) {
        substring_to_number[repeating_substrings[i]] = "{" + to_string(i) + "}";
    }

    vector<string> compressed_strings;
    for (const string& s : strings) {
        compressed_strings.push_back(regex_replace_substrings(s, substring_to_number));
    }

    return {compressed_strings, substring_to_number};
}

vector<string> get_lines() {
    std::string filename = "mit_verses_flat.txt";
    std::vector<std::string> lines;
    std::string line;

    std::ifstream inputFile(filename);

    if (inputFile.is_open()) {
        while (std::getline(inputFile, line)) {
            lines.push_back(line);
        }
        inputFile.close();

        // // Now 'lines' vector contains each line from the file
        // for (const auto& singleLine : lines) {
        //     std::cout << singleLine << std::endl;
        // }

        return lines;
    } else {
        std::cerr << "Unable to open file: " << filename << std::endl;
        throw string("Unable to open file");
    }
}

// Driver code
int main() {
    // vector<string> strings = {"banana", "anaban", "nabanan"};
    vector<string> strings = get_lines();

    cout<<"Loaded "<<strings.size()<<" lines."<<endl;
    cout<<"Processing..."<<endl;

    auto [compressed, mapping] = replace_with_numbers(strings);

    cout << "Compressed Strings:\n";
    for (const string& s : compressed) {
        cout << s << endl;
    }

    cout << "\nSubstring Mapping:\n";
    for (const auto& [sub, num] : mapping) {
        cout << num << ": " << sub << endl;
    }

    return 0;
}
