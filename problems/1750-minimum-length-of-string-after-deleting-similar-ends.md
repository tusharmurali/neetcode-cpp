# 1750. Minimum Length of String after Deleting Similar Ends

- **Difficulty:** Medium  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-length-of-string-after-deleting-similar-ends/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-length-of-string-after-deleting-similar-ends>  
- **Video:** <https://www.youtube.com/watch?v=318hrWVr_5U>  
- **Video approach:** 1. Greedy + Two Pointers (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Greedy + Two Pointers ▶ video

We can repeatedly trim matching characters from both ends of the string. The operation requires the prefix and suffix to consist of the same character, and we must remove at least one character from each end.

Using two pointers starting at opposite ends, we check if both point to the same character. If they do, we greedily remove all consecutive occurrences of that character from both ends. This greedy choice is optimal because removing more characters now can only help (or not hurt) future operations.

```cpp
class Solution {
public:
    int minimumLength(string s) {
        int l = 0, r = s.length() - 1;

        while (l < r && s[l] == s[r]) {
            char tmp = s[l];
            while (l <= r && s[l] == tmp) {
                l++;
            }
            while (l <= r && s[r] == tmp) {
                r--;
            }
        }
        return r - l + 1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
