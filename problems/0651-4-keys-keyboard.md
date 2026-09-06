# 651. 4 Keys Keyboard

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/4-keys-keyboard/>  
- **NeetCode:** <https://neetcode.io/problems/4-keys-keyboard>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming

With `n` key presses, we want to maximize the number of 'A's on screen. At any point, we can either type 'A' or use Ctrl-A, Ctrl-C, then Ctrl-V to copy and paste. The key observation is that after pressing 'A' some number of times, it becomes more efficient to copy what we have and paste it multiple times. For a given number of 'A's, using Ctrl-A + Ctrl-C + `k` pastes multiplies the count by `k + 1` (original + `k` copies). We use dynamic programming where `dp[i]` represents the maximum 'A's achievable with exactly `i` key presses.

```cpp
class Solution {
public:
    int maxA(int n) {
        vector<int> dp(n + 1);
        iota(dp.begin(), dp.end(), 0);
        
        for (int i = 0; i <= n - 3; i++) {
            for (int j = i + 3; j <= min(n, i + 6); j++) {
                dp[j] = max(dp[j], (j - i - 1) * dp[i]);
            }
        }

        return dp[n];
    }
};
```

**Complexity**

- Time complexity: $O(n)$

- Space complexity: $O(n)$

>  Where $n$ is the maximum number of key presses allowed.
