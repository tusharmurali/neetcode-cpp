# 163. Missing Ranges

- **Difficulty:** Easy  
- **Pattern:** Intervals  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/missing-ranges/>  
- **NeetCode:** <https://neetcode.io/problems/missing-ranges>  

[← Back to index](../INDEX.md)

## 1. Linear Scan

We need to identify all gaps in the range `[lower, upper]` that are not covered by the sorted array `nums`. There are three places where gaps can occur: before the first element, between consecutive elements, and after the last element. By checking each of these locations, we can collect all missing ranges in a single pass.

```cpp
class Solution {
public:
    vector<vector<int>> findMissingRanges(vector<int>& nums, int lower,
                                          int upper) {
        int n = nums.size();
        vector<vector<int>> missingRanges;
        if (n == 0) {
            missingRanges.push_back(vector<int>{lower, upper});
            return missingRanges;
        }

        // Check for any missing numbers between the lower bound and nums[0].
        if (lower < nums[0]) {
            missingRanges.push_back(vector<int>{lower, nums[0] - 1});
        }

        // Check for any missing numbers between successive elements of nums.
        for (int i = 0; i < n - 1; i++) {
            if (nums[i + 1] - nums[i] <= 1) {
                continue;
            }
            missingRanges.push_back(vector<int>{nums[i] + 1, nums[i + 1] - 1});
        }

        // Check for any missing numbers between the last element of nums and
        // the upper bound.
        if (upper > nums[n - 1]) {
            missingRanges.push_back(vector<int>{nums[n - 1] + 1, upper});
        }

        return missingRanges;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ constant space

> Where $n$ is the number of elements in `nums`.
