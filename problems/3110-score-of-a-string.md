# 3110. Score of a String

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/score-of-a-string/>  
- **NeetCode:** <https://neetcode.io/problems/score-of-a-string>  
- **Video:** <https://www.youtube.com/watch?v=imbrLFL20tQ>  

[← Back to index](../INDEX.md)

## 1. Iteration

The score of a string is defined as the sum of absolute differences between adjacent characters' ASCII values. Since we need to compare each character with its neighbor, we simply walk through the string once, computing the difference between consecutive characters and accumulating the result in `res`.

```cpp
class Solution {
public:
    int scoreOfString(string s) {
        int res = 0;
        for (int i = 0; i < s.length() - 1; i++) {
            res += abs(s[i] - s[i + 1]);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
