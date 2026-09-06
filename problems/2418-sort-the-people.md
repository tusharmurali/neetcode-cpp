# 2418. Sort the People

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/sort-the-people/>  
- **NeetCode:** <https://neetcode.io/problems/sort-the-people>  
- **Video:** <https://www.youtube.com/watch?v=Zv_gXqqslbw>  

[← Back to index](../INDEX.md)

## 1. Hash Map

Since all heights are distinct, we can use each height as a unique key to look up the corresponding person's name. By building a hash map from height to name, we can then sort the heights in descending order and retrieve names in the correct sequence.

```cpp
class Solution {
public:
    vector<string> sortPeople(vector<string>& names, vector<int>& heights) {
        unordered_map<int, string> map;
        for (int i = 0; i < heights.size(); i++) {
            map[heights[i]] = names[i];
        }

        sort(heights.begin(), heights.end());
        vector<string> res;
        for (int i = heights.size() - 1; i >= 0; i--) {
            res.push_back(map[heights[i]]);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 2. Sorting the Pairs

Instead of using a hash map, we can pair each height with its corresponding name directly. By creating an array of (height, name) pairs and sorting them by height in descending order, we keep the relationship intact throughout the sorting process.

```cpp
class Solution {
public:
    vector<string> sortPeople(vector<string>& names, vector<int>& heights) {
        vector<pair<int, string>> arr;
        for (int i = 0; i < names.size(); i++) {
            arr.emplace_back(heights[i], names[i]);
        }

        sort(arr.begin(), arr.end(), [](auto& a, auto& b) {
            return a.first > b.first;
        });

        vector<string> res;
        for (auto& [_, name] : arr) {
            res.push_back(name);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Sorting the Indices

Rather than copying data into pairs, we can sort an array of indices based on the heights they point to. This approach is memory efficient when names are long strings, since we only move integers during sorting rather than entire strings.

```cpp
class Solution {
public:
    vector<string> sortPeople(vector<string>& names, vector<int>& heights) {
        int n = names.size();
        vector<int> indices(n);
        iota(indices.begin(), indices.end(), 0);

        sort(indices.begin(), indices.end(), [&](int a, int b) {
            return heights[a] > heights[b];
        });

        vector<string> res;
        for (int i : indices) {
            res.push_back(names[i]);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$
