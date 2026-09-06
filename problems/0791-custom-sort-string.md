# 791. Custom Sort String

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/custom-sort-string/>  
- **NeetCode:** <https://neetcode.io/problems/custom-sort-string>  

[← Back to index](../INDEX.md)

## 1. Custom Comparator

We want to reorder string `s` so that characters appear in the same relative order as they do in `order`. The key insight is that we can assign each character a rank based on its position in `order`. Characters not in `order` can be assigned a high rank (like `26`) so they appear at the end. By sorting `s` using these ranks as the comparison key, characters will naturally arrange themselves according to the custom ordering.

```cpp
class Solution {
public:
    string customSortString(string order, string s) {
        vector<int> rank(26, 26);
        for (int i = 0; i < order.size(); ++i) {
            rank[order[i] - 'a'] = i;
        }

        sort(s.begin(), s.end(), [&](char a, char b) {
            return rank[a - 'a'] < rank[b - 'a'];
        });

        return s;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 2. Frequency Count

Instead of sorting, we can build the result string directly by counting character frequencies. Since we know the desired order of characters, we first iterate through `order` and append each character as many times as it appears in `s`. Then we handle any remaining characters not in `order` by iterating through the alphabet. This avoids the `O(n log n)` sorting overhead.

```cpp
class Solution {
public:
    string customSortString(string order, string s) {
        vector<int> count(26, 0);
        for (char c : s) {
            count[c - 'a']++;
        }

        string res;
        for (char c : order) {
            int idx = c - 'a';
            while (count[idx] > 0) {
                res += c;
                count[idx]--;
            }
        }

        for (int idx = 0; idx < 26; ++idx) {
            char c = 'a' + idx;
            while (count[idx] > 0) {
                res += c;
                count[idx]--;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
