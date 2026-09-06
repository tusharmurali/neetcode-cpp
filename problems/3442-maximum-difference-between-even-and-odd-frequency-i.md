# 3442. Maximum Difference Between Even and Odd Frequency I

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-difference-between-even-and-odd-frequency-i/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-difference-between-even-and-odd-frequency-i>  

[← Back to index](../INDEX.md)

## 1. Counting

We want to maximize `(frequency of some character with odd count) - (frequency of some character with even count)`. The straightforward approach is to count how often each character appears, then check all pairs where one has an odd frequency and the other has an even frequency. We take the maximum difference among all valid pairs.

```cpp
class Solution {
public:
    int maxDifference(string s) {
        vector<int> count(26, 0);
        for (char c : s) {
            count[c - 'a']++;
        }

        int res = INT_MIN;
        for (int odd : count) {
            if (odd == 0 || odd % 2 == 0) continue;
            for (int even : count) {
                if (even == 0 || even % 2 == 1) continue;
                res = max(res, odd - even);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

## 2. Counting (Optimal)

Instead of checking all pairs, we can observe that to maximize `odd - even`, we should pick the largest odd frequency and the smallest even frequency. This gives us the optimal answer in a single pass through the frequency counts.

```cpp
class Solution {
public:
    int maxDifference(string s) {
        vector<int> count(26, 0);
        for (char c : s) {
            count[c - 'a']++;
        }

        int oddMax = 0, evenMin = s.length();
        for (int c : count) {
            if (c & 1) {
                oddMax = max(oddMax, c);
            } else if (c > 0) {
                evenMin = min(evenMin, c);
            }
        }

        return oddMax - evenMin;
    }
};
```

**Complexity**

* Time complexity: $O(n)$
* Space complexity: $O(1)$ since we have at most $26$ different characters.
