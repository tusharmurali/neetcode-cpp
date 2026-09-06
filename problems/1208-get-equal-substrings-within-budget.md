# 1208. Get Equal Substrings Within Budget

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/get-equal-substrings-within-budget/>  
- **NeetCode:** <https://neetcode.io/problems/get-equal-substrings-within-budget>  
- **Video:** <https://www.youtube.com/watch?v=3lsT1Le526U>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We want to find the longest substring where the total transformation cost stays within the budget. The transformation cost at each position is the absolute difference between the ASCII values of the corresponding characters. By checking every possible substring and tracking its cost, we can find the maximum valid length.

```cpp
class Solution {
public:
    int equalSubstring(string s, string t, int maxCost) {
        int n = s.size();
        int res = 0;

        for (int i = 0; i < n; i++) {
            int curCost = 0;
            for (int j = i; j < n; j++) {
                curCost += abs(t[j] - s[j]);
                if (curCost > maxCost) {
                    break;
                }
                res = max(res, j - i + 1);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Sliding Window

Since we want the longest contiguous substring within a cost budget, a sliding window is ideal. We expand the window by moving the right pointer and shrink it from the left when the cost exceeds the budget. This efficiently explores all valid windows in linear time.

```cpp
class Solution {
public:
    int equalSubstring(string s, string t, int maxCost) {
        int curCost = 0, l = 0, res = 0;

        for (int r = 0; r < s.length(); r++) {
            curCost += abs(s[r] - t[r]);
            while (curCost > maxCost) {
                curCost -= abs(s[l] - t[l]);
                l++;
            }
            res = max(res, r - l + 1);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 3. Sliding Window (Optimal)

We can simplify the sliding window by never shrinking it more than one position at a time. Once we find a valid window of size `k`, we only care about finding windows of size `k+1` or larger. If the current window is invalid, we slide both pointers together, maintaining the window size. The final answer is derived from the position of the left pointer `l`.

```cpp
class Solution {
public:
    int equalSubstring(string s, string t, int maxCost) {
        int l = 0;
        for (int r = 0; r < s.length(); r++) {
            maxCost -= abs(s[r] - t[r]);
            if (maxCost < 0) {
                maxCost += abs(s[l] - t[l]);
                l++;
            }
        }
        return s.length() - l;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
