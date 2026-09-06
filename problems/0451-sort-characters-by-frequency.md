# 451. Sort Characters By Frequency

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/sort-characters-by-frequency/>  
- **NeetCode:** <https://neetcode.io/problems/sort-characters-by-frequency>  
- **Video:** <https://www.youtube.com/watch?v=OXdXc9HTrIg>  

[← Back to index](../INDEX.md)

## 1. Sorting

To sort characters by frequency, we first need to know how often each character appears. Once we have the frequencies, we can sort the entire string using a custom comparator that prioritizes higher frequencies. Characters with the same frequency are sorted alphabetically for consistency.

```cpp
class Solution {
public:
    string frequencySort(string s) {
        vector<int> count(123);
        for (char c : s) {
            count[c]++;
        }

        vector<char> chars(s.begin(), s.end());
        sort(chars.begin(), chars.end(), [&](char a, char b) {
            if (count[b] == count[a]) {
                return a < b;
            }
            return count[b] < count[a];
        });

        return string(chars.begin(), chars.end());
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 2. Frequency Sort

Instead of sorting all characters individually, we can sort the unique characters by their frequencies. This is more efficient because the number of unique characters is bounded (at most 62 for alphanumeric). After sorting the unique characters, we build the result by repeating each character according to its frequency.

```cpp
class Solution {
public:
    string frequencySort(string s) {
        vector<int> count(123, 0);
        for (char c : s) {
            count[c]++;
        }

        vector<pair<char, int>> freq;
        for (int i = 0; i < 123; i++) {
            if (count[i] > 0) {
                freq.emplace_back((char)i, count[i]);
            }
        }

        sort(freq.begin(), freq.end(), [](auto& a, auto& b) {
            if (a.second == b.second) {
                return a.first < b.first;
            }
            return a.second > b.second;
        });

        string res;
        for (const auto& entry : freq) {
            res += string(entry.second, entry.first);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for the output string.

## 3. Bucket Sort

Bucket sort avoids comparison-based sorting entirely. Since frequencies range from 1 to n (the string length), we create buckets indexed by frequency. Each bucket holds characters that appear exactly that many times. By iterating from the highest frequency bucket down to the lowest, we naturally process characters in the required order.

```cpp
class Solution {
public:
    string frequencySort(string s) {
        unordered_map<char, int> count;
        for (char c : s) {
            count[c]++;
        }

        vector<vector<char>> buckets(s.size() + 1);
        for (auto& entry : count) {
            buckets[entry.second].push_back(entry.first);
        }

        string res;
        for (int i = s.size(); i > 0; i--) {
            for (char c : buckets[i]) {
                res += string(i, c);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0451-sort-characters-by-frequency.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    string frequencySort(string s) {
        //count the frequency / the big A and small A are different characters
        //the string cannot not be empty according to the question
        unordered_map<char, int> freq;
        for(char c: s){
            freq[c]++;
        }

        // Move it to the vector so we can sort it easily 
        vector<pair<char, int>> freq_v(freq.begin(), freq.end());
    
        // Sort the vector by the frequency
        sort(freq_v.begin(), freq_v.end(), [](const pair<int, int>& a, const pair<int, int>& b) {
            return a.second > b.second;
        });

        // Create the answer string -> add the chars with their frequency 
        string ans = "";
        for(auto pair: freq_v){
            for(int i = 0; i < pair.second; i++){
                ans += pair.first;
            }
        }
        return ans;
    }
};
```
