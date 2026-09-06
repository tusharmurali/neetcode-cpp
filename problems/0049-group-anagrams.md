# 49. Group Anagrams

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/group-anagrams/>  
- **NeetCode:** <https://neetcode.io/problems/anagram-groups>  
- **Video:** <https://www.youtube.com/watch?v=vzdNOK2oB2E>  

[← Back to index](../INDEX.md)

## 1. Sorting

Anagrams become identical when their characters are sorted.  
For example, `"eat"`, `"tea"`, and `"ate"` all become `"aet"` after sorting.  
By using the sorted version of each string as a key, we can group all anagrams together.  
Strings that share the same sorted form must be anagrams, so placing them in the same group is both natural and efficient.

```cpp
class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        unordered_map<string, vector<string>> res;
        for (const auto& s : strs) {
            string sortedS = s;
            sort(sortedS.begin(), sortedS.end());
            res[sortedS].push_back(s);
        }
        vector<vector<string>> result;
        for (auto& pair : res) {
            result.push_back(pair.second);
        }
        return result;
    }
};
```

**Complexity**

- Time complexity: $O(m * n \log n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of strings and $n$ is the length of the longest string.

## 2. Hash Table

Instead of sorting each string, we can represent every string by the frequency of its characters.
Since the problem uses lowercase English letters, a fixed-size array of length `26` can capture how many times each character appears.
Two strings are anagrams if and only if their frequency arrays are identical.
By using this frequency array (converted to a tuple so it can be a dictionary key), we can group all strings that share the same character counts.

```cpp
class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        unordered_map<string, vector<string>> res;
        for (const auto& s : strs) {
            vector<int> count(26, 0);
            for (char c : s) {
                count[c - 'a']++;
            }
            string key = to_string(count[0]);
            for (int i = 1; i < 26; ++i) {
                key += ',' + to_string(count[i]);
            }
            res[key].push_back(s);
        }
        vector<vector<string>> result;
        for (const auto& pair : res) {
            result.push_back(pair.second);
        }
        return result;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity:
    - $O(m)$ auxiliary space, excluding the returned output.
    - $O(m * n)$ total space if the output groups are counted.

> Where $m$ is the number of strings and $n$ is the length of the longest string.

## Standalone solution file (`cpp/0049-group-anagrams.cpp` in the NeetCode repo)

```cpp
/*
    Given array of strings, group anagrams together (same letters diff order)
    Ex. strs = ["eat","tea","tan","ate","nat","bat"] -> [["bat"],["nat","tan"],["ate","eat","tea"]]

    Count chars, for each string use total char counts (naturally sorted) as key

    Time: O(n x l) -> n = length of strs, l = max length of a string in strs
    Space: O(n x l)
*/

class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        unordered_map<string, vector<string>> m;
        for (int i = 0; i < strs.size(); i++) {
            string key = getKey(strs[i]);
            m[key].push_back(strs[i]);
        }
        
        vector<vector<string>> result;
        for (auto it = m.begin(); it != m.end(); it++) {
            result.push_back(it->second);
        }
        return result;
    }
private:
    string getKey(string str) {
        vector<int> count(26);
        for (int j = 0; j < str.size(); j++) {
            count[str[j] - 'a']++;
        }
        
        string key = "";
        for (int i = 0; i < count.size(); i++) {
            key.append(to_string(count[i]) + '#');
        }
        return key;
    }
};
```
