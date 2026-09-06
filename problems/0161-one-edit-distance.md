# 161. One Edit Distance

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/one-edit-distance/>  
- **NeetCode:** <https://neetcode.io/problems/one-edit-distance>  

[← Back to index](../INDEX.md)

## 1. One Pass Algorithm

Two strings are one edit distance apart if we can transform one into the other with exactly one operation: insert, delete, or replace a single character. The key insight is that the length difference between the strings tells us which operation is possible.

If the lengths differ by more than `1`, it is impossible to make them equal with one edit. If they have the same length, we need exactly one replacement. If they differ by `1`, we need exactly one insertion or deletion.

We scan both strings in parallel. When we find the first mismatch, we check if the remaining portions match according to the appropriate rule.

```cpp
class Solution {
public:
    bool isOneEditDistance(string s, string t) {
        int ns = s.size();
        int nt = t.size();

        // Ensure that s is shorter than t.
        if (ns > nt) return isOneEditDistance(t, s);

        // The strings are NOT one edit away distance
        // if the length diff is more than 1.
        if (nt - ns > 1) return false;

        for (int i = 0; i < ns; i++)
            if (s[i] != t[i])
                // if strings have the same length
                if (ns == nt) return s.substr(i + 1) == t.substr(i + 1);
                // If strings have different lengths
                else
                    return s.substr(i) == t.substr(i + 1);

        // If there are no diffs in ns distance
        // The strings are one edit away only if
        // t has one more character.
        return (ns + 1 == nt);
    }
};
```

**Complexity**

- Time complexity: $O(N)$ in the worst case when string lengths are close enough `abs(ns - nt) <= 1`. $O(1)$ in the best case when `abs(ns - nt) > 1`
- Space complexity: $O(N)$ extra space used

> where $N$ is the number of characters in the longest string
