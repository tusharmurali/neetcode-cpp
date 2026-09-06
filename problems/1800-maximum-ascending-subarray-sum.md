# 1800. Maximum Ascending Subarray Sum

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-ascending-subarray-sum/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-ascending-subarray-sum>  
- **Video:** <https://www.youtube.com/watch?v=NcsmaL_e_Zg>  

[← Back to index](../INDEX.md)

## 1. Brute Force

An ascending subarray is a contiguous sequence where each element is strictly greater than the previous. We want the maximum sum among all such subarrays.

The brute force approach considers every possible starting position. From each start, we extend the subarray as long as elements keep increasing, accumulating the sum. We track the maximum sum seen across all starting positions.

```cpp
class Solution {
public:
    int maxAscendingSum(vector<int>& nums) {
        int res = 0;
        for (int i = 0; i < nums.size(); i++) {
            int curSum = nums[i];
            for (int j = i + 1; j < nums.size(); j++) {
                if (nums[j] <= nums[j - 1]) {
                    break;
                }
                curSum += nums[j];
            }
            res = max(res, curSum);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Iteration

We can solve this in a single pass. As we scan through the array, we maintain a running sum of the current ascending subarray. Whenever we encounter an element that does not continue the ascending pattern, we reset the running sum and start a new subarray from that element.

This works because ascending subarrays are naturally separated by positions where the ascending condition breaks.

```cpp
class Solution {
public:
    int maxAscendingSum(vector<int>& nums) {
        int res = nums[0], curSum = nums[0];

        for (int i = 1; i < nums.size(); i++) {
            if (nums[i] <= nums[i - 1]) {
                curSum = 0;
            }
            curSum += nums[i];
            res = max(res, curSum);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
