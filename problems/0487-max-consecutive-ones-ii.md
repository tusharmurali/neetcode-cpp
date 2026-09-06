# 487. Max Consecutive Ones II

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/max-consecutive-ones-ii/>  
- **NeetCode:** <https://neetcode.io/problems/max-consecutive-ones-ii>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest approach is to try every possible starting position and extend the window as far as we can while allowing at most one zero to be flipped. For each starting index, we scan forward and count zeros. As long as we have seen at most one zero, the current window is valid. Once we encounter a second zero, we stop extending and record the maximum length found so far. This guarantees we consider all possible substrings but results in checking many overlapping ranges.

```cpp
class Solution {
public:
    int findMaxConsecutiveOnes(vector<int>& nums) {
        int longestSequence = 0;

        for (int left = 0; left < nums.size(); left++) {
            int numZeroes = 0;

            //Check every consecutive sequence
            for (int right = left; right < nums.size(); right++) {

                // Count how many 0's
                if (nums[right] == 0) {
                    numZeroes += 1;
                }

                // Update answer if it's valid
                if (numZeroes <= 1) {
                    longestSequence = max(longestSequence, right - left + 1);
                }
            }
        }

        return longestSequence;
    }
};
```

**Complexity**

- Time complexity: $O(n^2)$
- Space complexity: $O(1)$ constant space used

> Where $n$ is the length of the input array `nums`.

## 2. Sliding Window

Instead of restarting from every position, we can use a sliding window that grows and shrinks dynamically. The key insight is that we only need to shrink the window when we have more than one zero inside it. By maintaining a count of zeros in the current window, we expand by moving the `right` pointer and contract by moving the `left` pointer whenever the window becomes invalid. This way, each element is visited at most twice, making the solution linear.

```cpp
class Solution {
public:
    int findMaxConsecutiveOnes(vector<int>& nums) {
        int longestSequence = 0;
        int left = 0;
        int right = 0;
        int numZeroes = 0;

        // While our window is in bounds
        while (right < nums.size()) {

            // Increase numZeroes if the rightmost element is 0
            if (nums[right] == 0) {
                numZeroes++;
            }

            //If our window is invalid, contract our window
            while (numZeroes == 2) {
                if (nums[left] == 0) {
                    numZeroes--;
                }
                left++;
            }

            // Update our longest sequence answer
            longestSequence = max(longestSequence, right - left + 1);

            // Expand our window
            right++;
        }

        return longestSequence;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ constant space used

> Where $n$ is the length of the input array `nums`.
