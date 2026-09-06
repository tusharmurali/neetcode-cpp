# 1984. Minimum Difference Between Highest And Lowest of K Scores

- **Difficulty:** Easy  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-difference-between-highest-and-lowest-of-k-scores/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-difference-between-highest-and-lowest-of-k-scores>  
- **Video:** <https://www.youtube.com/watch?v=JU5XdBZZtlk>  

[← Back to index](../INDEX.md)

## 1. Sorting + Sliding Window

When we need to minimize the difference between the highest and lowest values among any `k` chosen elements, sorting the array first is key. After sorting, the smallest possible range of `k` elements will always be a contiguous segment. Why? Because picking non-adjacent elements after sorting would only increase the gap between `max` and `min`. So, we sort the array and then slide a window of size `k` across it, tracking the minimum difference between the first and last element of each window.

```cpp
class Solution {
public:
    int minimumDifference(vector<int>& nums, int k) {
        sort(nums.begin(), nums.end());
        int l = 0, r = k - 1, res = INT_MAX;
        while (r < nums.size()) {
            res = min(res, nums[r] - nums[l]);
            l++;
            r++;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## Standalone solution file (`cpp/1984-minimum-difference-between-highest-and-lowest-of-k-scores.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int minimumDifference(vector<int>& nums, int k) {
        sort(nums.begin(), nums.end());
        int l = 0, r = k - 1;
        int res = INT_MAX;
        
        while(r < nums.size()) {
            res = min(res, nums[r] - nums[l]);
            l = l + 1;
            r = r + 1;
        }
        return res;
    }
};
```
