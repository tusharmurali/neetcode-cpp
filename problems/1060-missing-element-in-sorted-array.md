# 1060. Missing Element in Sorted Array

- **Difficulty:** Medium  
- **Pattern:** Binary Search  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/missing-element-in-sorted-array/>  
- **NeetCode:** <https://neetcode.io/problems/missing-element-in-sorted-array>  

[← Back to index](../INDEX.md)

## 1. Iteration

Since the array is sorted and strictly increasing, any missing numbers must fall in the gaps between consecutive elements. For each pair of adjacent elements, we can calculate how many numbers are missing by looking at the difference minus one. As we scan through the array, we count missing numbers until we accumulate at least `k` of them. Once we find the gap that contains the `k`-th missing number, we can compute its exact value.

```cpp
class Solution {
public:
    int missingElement(vector<int>& nums, int k) {
        int n = nums.size();

        for (int i = 1; i < n; ++i) {
            int missedInGap = nums[i] - nums[i - 1] - 1;
            if (missedInGap >= k) {
                return nums[i - 1] + k;
            }
            k -= missedInGap;
        }

        return nums[n - 1] + k;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ constant space

> Where $n$ is the length of the input array `nums`.

## 2. Binary Search

Instead of scanning linearly, we can use binary search to find the position where the `k`-th missing number falls. The key observation is that for any index `i`, the count of missing numbers up to that point equals `nums[i] - nums[0] - i`. This formula works because in a complete sequence starting from `nums[0]`, we would expect `nums[0] + i` at index `i`. The difference tells us how many numbers were skipped. Since this count is monotonically increasing, binary search applies naturally.

```cpp
class Solution {
public:
    int missingElement(vector<int>& nums, int k) {
        int n = nums.size();
        int left = 0, right = n - 1;

        while (left < right) {
            int mid = right - (right - left) / 2;
            if (nums[mid] - nums[0] - mid < k) {
                left = mid;
            } else{
                right = mid - 1;
            }
        }

        return nums[0] + k + left;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$ constant space

> Where $n$ is the length of the input array `nums`.
