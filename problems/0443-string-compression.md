# 443. String Compression

- **Difficulty:** Medium  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/string-compression/>  
- **NeetCode:** <https://neetcode.io/problems/string-compression>  

[← Back to index](../INDEX.md)

## 1. Using Extra Space

The idea is to traverse the array and group consecutive identical characters together. For each group, we write the character followed by its count (only if count > 1). We first build the compressed string in a separate buffer, then copy it back to the original array. This approach is straightforward but uses extra space proportional to the output size.

```cpp
class Solution {
public:
    int compress(vector<char>& chars) {
        int n = chars.size();
        string s = "";

        int i = 0;
        while (i < n) {
            s += chars[i];
            int j = i + 1;
            while (j < n && chars[i] == chars[j]) {
                j++;
            }

            if (j - i > 1) {
                s += to_string(j - i);
            }
            i = j;
        }

        for (i = 0; i < s.size(); i++) {
            chars[i] = s[i];
        }
        return s.size();
    }
};
```

**Complexity**

- Time complexity: $O(n)$ or $O(n ^ 2)$ depending on the language.
- Space complexity: $O(n)$

## 2. Two Pointers

We can compress the array in-place using two pointers: one for reading (`i`) and one for writing (`k`). Since the compressed form is never longer than the original (a character followed by its count takes at most as much space as the repeated characters), we can safely overwrite the array as we go. This eliminates the need for extra space.

```cpp
class Solution {
public:
    int compress(vector<char>& chars) {
        int n = chars.size(), k = 0, i = 0;

        while (i < n) {
            chars[k++] = chars[i];
            int j = i + 1;
            while (j < n && chars[i] == chars[j]) {
                j++;
            }

            if (j - i > 1) {
                string cnt = to_string(j - i);
                for (char c : cnt) {
                    chars[k++] = c;
                }
            }
            i = j;
        }

        return k;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
