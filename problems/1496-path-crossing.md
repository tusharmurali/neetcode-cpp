# 1496. Path Crossing

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/path-crossing/>  
- **NeetCode:** <https://neetcode.io/problems/path-crossing>  
- **Video:** <https://www.youtube.com/watch?v=VWRJBNP7uH8>  

[← Back to index](../INDEX.md)

## 1. Hash Set

We start at the origin and follow the path character by character. At each step, we move in the indicated direction. The path crosses itself if we visit a position we've been to before. A hash set provides O(1) lookups to check if a coordinate has been visited.

```cpp
class Solution {
public:
    bool isPathCrossing(string path) {
        unordered_set<string> visit;
        int x = 0, y = 0;
        visit.insert(to_string(x) + "," + to_string(y));

        for (char c : path) {
            if (c == 'N') y++;
            else if (c == 'S') y--;
            else if (c == 'E') x++;
            else if (c == 'W') x--;

            string pos = to_string(x) + "," + to_string(y);
            if (visit.count(pos)) return true;
            visit.insert(pos);
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Hash Set (Custom Hash)

Instead of storing coordinates as strings or tuples, we can encode them into a single integer. By shifting one coordinate (e.g., `x << 32`) and adding the other, we create a unique hash for each position. This can improve performance by avoiding string concatenation overhead.

```cpp
class Solution {
public:
    bool isPathCrossing(string path) {
        unordered_set<pair<int, int>, pair_hash> visit;
        int x = 0, y = 0;
        visit.insert({x, y});

        for (char c : path) {
            if (c == 'N') y++;
            else if (c == 'S') y--;
            else if (c == 'E') x++;
            else if (c == 'W') x--;

            if (visit.count({x, y})) return true;
            visit.insert({x, y});
        }

        return false;
    }

private:
    struct pair_hash {
        template <class T1, class T2>
        size_t operator()(const pair<T1, T2>& p) const {
            return (hash<T1>()(p.first) << 32) + hash<T2>()(p.second);
        }
    };
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
