# 1590. Make Sum Divisible by P

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/make-sum-divisible-by-p/>  
- **NeetCode:** <https://neetcode.io/problems/make-sum-divisible-by-p>  
- **Video:** <https://www.youtube.com/watch?v=tZXsLAyE0SE>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We need to find the shortest subarray to remove so that the remaining elements sum to a multiple of `p`. The brute force approach tries every possible subarray length starting from 1. For each length, we slide a window across the array and check if removing that window leaves a sum divisible by `p`. We return the first (smallest) length `l` that works.

```cpp
class Solution {
public:
    int minSubarray(vector<int>& nums, int p) {
        int n = nums.size();
        long long totSum = 0;
        for (int num : nums) totSum += num;

        if (totSum % p == 0) return 0;

        for (int l = 1; l < n; l++) {
            long long curSum = 0;
            for (int i = 0; i < n; i++) {
                curSum += nums[i];
                if (i >= l) curSum -= nums[i - l];

                long long remainSum = totSum - curSum;
                if (remainSum % p == 0) return l;
            }
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Prefix Sum

If the total sum has remainder `r` when divided by `p`, we need to remove a subarray whose sum also has remainder `r` (mod `p`). This transforms the problem into finding the shortest subarray with a specific remainder. Using prefix sums, if the current prefix has remainder `curSum`, we look for an earlier prefix with remainder `(curSum - r + p) % p`. A hash map stores the most recent index for each remainder, allowing `O(1)` lookups.

```cpp
class Solution {
public:
    int minSubarray(vector<int>& nums, int p) {
        long total = 0;
        for (int num : nums) total += num;
        int remain = total % p;
        if (remain == 0) return 0;

        int res = nums.size();
        long curSum = 0;
        unordered_map<int, int> map;
        map[0] = -1;

        for (int i = 0; i < nums.size(); i++) {
            curSum = (curSum + nums[i]) % p;
            int prefix = (curSum - remain + p) % p;
            if (map.count(prefix)) {
                res = min(res, i - map[prefix]);
            }
            map[curSum] = i;
        }

        return res == nums.size() ? -1 : res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
