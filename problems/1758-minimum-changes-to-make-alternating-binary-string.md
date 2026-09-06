# 1758. Minimum Changes To Make Alternating Binary String

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-changes-to-make-alternating-binary-string/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-changes-to-make-alternating-binary-string>  
- **Video:** <https://www.youtube.com/watch?v=9vAQdmVU2ds>  

[← Back to index](../INDEX.md)

## 1. Start with Zero and One

An alternating binary string must follow one of two patterns: starting with '0' (like "010101...") or starting with '1' (like "101010..."). We simply count how many characters differ from each pattern and return the smaller count.

We use XOR to toggle the expected character at each position. Starting with 0, we XOR with 1 after each character to alternate between expecting 0 and 1.

```cpp
class Solution {
public:
    int minOperations(string s) {
        int cur = 0, cnt1 = 0;
        for (char c : s) {
            if (c - '0' != cur) {
                cnt1++;
            }
            cur ^= 1;
        }

        cur = 1;
        int cnt2 = 0;
        for (char c : s) {
            if (c - '0' != cur) {
                cnt2++;
            }
            cur ^= 1;
        }

        return min(cnt1, cnt2);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. Start with Zero or One

We can optimize by counting mismatches for only one pattern. Notice that if a position mismatches the "start with 1" pattern, it must match the "start with 0" pattern, and vice versa. So the count for one pattern plus the count for the other equals the string length.

We count mismatches for the "start with 1" pattern (where even indices should be '1' and odd indices should be '0'). The count for the "start with 0" pattern is simply `length - count`.

```cpp
class Solution {
public:
    int minOperations(string s) {
        int count = 0;

        for (int i = 0; i < s.size(); i++) {
            if (i % 2 == 0) {
                if (s[i] == '0') {
                    count++;
                }
            } else {
                if (s[i] == '1') {
                    count++;
                }
            }
        }

        return min(count, (int)s.size() - count);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
