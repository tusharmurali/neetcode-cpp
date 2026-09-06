# 1436. Destination City

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/destination-city/>  
- **NeetCode:** <https://neetcode.io/problems/destination-city>  
- **Video:** <https://www.youtube.com/watch?v=Hi8vMnnTZHE>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The destination city is a city that appears as an endpoint but never as a starting point in any path. For each destination in the paths, we can check whether it ever appears as a starting city. The city that never starts a path is our answer.

```cpp
class Solution {
public:
    string destCity(vector<vector<string>>& paths) {
        for (int i = 0; i < paths.size(); i++) {
            bool flag = true;
            for (int j = 0; j < paths.size(); j++) {
                if (paths[i][1] == paths[j][0]) {
                    flag = false;
                    break;
                }
            }
            if (flag) {
                return paths[i][1];
            }
        }
        return "";
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Hash Set

Instead of checking each destination against all starting points in O(n) time, we can store all starting cities in a hash set for O(1) lookup. Any destination city that is not in the set of starting cities must be the final destination.

```cpp
class Solution {
public:
    string destCity(vector<vector<string>>& paths) {
        unordered_set<string> s;
        for (auto& p : paths) {
            s.insert(p[0]);
        }

        for (auto& p : paths) {
            if (s.find(p[1]) == s.end()) {
                return p[1];
            }
        }
        return "";
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Hash Map

We can model the paths as a linked chain where each city points to its next destination. By building this chain in a hash map and following the links from any starting city, we will eventually reach the final destination, which has no outgoing path.

```cpp
class Solution {
public:
    string destCity(vector<vector<string>>& paths) {
        unordered_map<string, string> mp;
        for (auto& p : paths) {
            mp[p[0]] = p[1];
        }

        string start = paths[0][0];
        while (mp.find(start) != mp.end()) {
            start = mp[start];
        }
        return start;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
