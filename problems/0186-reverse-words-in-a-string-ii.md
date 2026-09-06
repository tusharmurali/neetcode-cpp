# 186. Reverse Words in a String II

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/reverse-words-in-a-string-ii/>  
- **NeetCode:** <https://neetcode.io/problems/reverse-words-in-a-string-ii>  

[← Back to index](../INDEX.md)

## 1. Reverse the Whole String and Then Reverse Each Word

Reversing the word order might seem complex, but there is a clever trick: reverse the entire string first, then reverse each individual word. When we reverse the whole string, the words end up in the correct order but each word itself is spelled backward. By reversing each word individually, we fix the spelling while preserving the new word order. This two-pass approach elegantly solves the problem in place.

```cpp
class Solution {
public:
    void reverseWords(vector<char>& s) {
        reverse(s.begin(), s.end());

        // 'start' points to the beginning of the current word
        // 'end' points to the position just after the current word
        int start = 0, end = 0;
        int n = s.size();

        while (start < n) {

            // Move 'right' to the position just after the current word
            while (end < n && s[end] != ' ')
                end++;

            // Note: in C++, reverse() operates on [start, end)
            // In other words, the leftmost element is included, while the rightmost element is not
            reverse(s.begin() + start, s.begin() + end);

            // Move 'start' and 'end' to the beginning of the next word
            end++;
            start = end;
        }
    }
};
```

**Complexity**

- Time complexity: $O(N)$, it's two passes along the string.
- Space complexity: $O(1)$ constant space used

> where $N$ is the length of the input `s`
