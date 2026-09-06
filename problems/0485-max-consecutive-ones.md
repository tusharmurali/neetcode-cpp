# 485. Max Consecutive Ones

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/max-consecutive-ones/>  
- **NeetCode:** <https://neetcode.io/problems/max-consecutive-ones>  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each position in the array, we count how many consecutive `1`s start from that position. We scan forward until we hit a `0` or the end of the array, then track the maximum count seen. This straightforward approach checks every possible starting position.

```cpp
class Solution {
public:
    int findMaxConsecutiveOnes(vector<int>& nums) {
        int n = nums.size(), res = 0;
        for (int i = 0; i < n; i++) {
            int cnt = 0;
            for (int j = i; j < n; j++) {
                if (nums[j] == 0) break;
                cnt++;
            }
            res = max(res, cnt);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Iteration - I

We only need one pass through the array. Maintain a running count of consecutive `1`s. When we see a `1`, increment the count. When we see a `0`, compare the current count with the maximum, then reset the count to `0`. After the loop, we do one final comparison since the longest sequence might end at the last element.

```cpp
class Solution {
public:
    int findMaxConsecutiveOnes(vector<int>& nums) {
        int res = 0, cnt = 0;
        for (int num : nums) {
            if (num == 0) {
                res = max(res, cnt);
                cnt = 0;
            } else {
                cnt++;
            }
        }
        return max(res, cnt);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 3. Iteration - II

We can simplify the logic by updating the maximum inside the loop at every step. If we see a `1`, we increment the count; otherwise, we reset it to `0`. After each element, we update the result. This eliminates the need for a final comparison after the loop.

```cpp
class Solution {
public:
    int findMaxConsecutiveOnes(vector<int>& nums) {
        int res = 0, cnt = 0;
        for (int num : nums) {
            cnt = num ? cnt + 1 : 0;
            res = max(res, cnt);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
