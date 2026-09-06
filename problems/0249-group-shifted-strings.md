# 249. Group Shifted Strings

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/group-shifted-strings/>  
- **NeetCode:** <https://neetcode.io/problems/group-shifted-strings>  

[← Back to index](../INDEX.md)

## 1. Hashing

Two strings belong to the same shifting sequence if the relative differences between consecutive characters are identical. For example, "abc" and "xyz" both have differences of `+1` between each pair of adjacent letters. By computing these differences for each string and using them as a hash key, we can group all strings that share the same shifting pattern together.

The key insight is that we normalize differences using modulo `26` to handle wrap-around cases (like 'z' shifting to 'a'). This way, strings that can be shifted into one another will produce the same hash key.

```cpp
class Solution {
public:
    string getHash(string &s) {
        string hashKey;
        for (int i = 1; i < s.length(); i++) {
            hashKey += (s[i] - s[i - 1] + 26) % 26 + 'a';
        }

        return hashKey;
    }

    vector<vector<string>> groupStrings(vector<string>& strings) {
        unordered_map<string, vector<string>> mapHashToList;

        // Create a hash_value (hashKey) for each string and append the string
        // to the list of hash values i.e. mapHashToList["cd"] = ["acf", "gil", "xzc"]
        for (string str : strings) {
            string hashKey = getHash(str);
            mapHashToList[hashKey].push_back(str);
        }

        // Iterate over the map, and add the values to groups
        vector<vector<string>> groups;
        for (auto it : mapHashToList) {
            groups.push_back(it.second);
        }

        // Return a list of all of the grouped strings
        return groups;
    }
};
```

**Complexity**

- Time complexity: $O(N \cdot K)$
- Space complexity: $O(N \cdot K)$

> Where $N$ is the length of `strings` and $K$ is the maximum length of a string in `strings`.
