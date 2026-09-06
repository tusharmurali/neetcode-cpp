# 948. Bag of Tokens

- **Difficulty:** Medium  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/bag-of-tokens/>  
- **NeetCode:** <https://neetcode.io/problems/bag-of-tokens>  
- **Video:** <https://www.youtube.com/watch?v=prI82maTivg>  

[← Back to index](../INDEX.md)

## 1. Greedy + Two Pointers

To maximize our score, we should be strategic about which tokens we play face-up (losing power, gaining score) versus face-down (gaining power, losing score). The key insight is that when gaining score, we want to spend as little power as possible, and when gaining power, we want to gain as much as possible. Sorting the tokens lets us always play the smallest token face-up and the largest token face-down.

```cpp
class Solution {
public:
    int bagOfTokensScore(vector<int>& tokens, int power) {
        sort(tokens.begin(), tokens.end());
        int res = 0, score = 0, l = 0, r = tokens.size() - 1;

        while (l <= r) {
            if (power >= tokens[l]) {
                power -= tokens[l++];
                score++;
                res = max(res, score);
            } else if (score > 0) {
                power += tokens[r--];
                score--;
            } else {
                break;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.
