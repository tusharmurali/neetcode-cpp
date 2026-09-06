# 1913. Maximum Product Difference Between Two Pairs

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-product-difference-between-two-pairs/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-product-difference-between-two-pairs>  
- **Video:** <https://www.youtube.com/watch?v=wBPoEm3r3EA>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The product difference is `(nums[a] * nums[b]) - (nums[c] * nums[d])` where all four indices are distinct. To maximize this, we want the first product as large as possible and the second product as small as possible. The brute force approach tries all valid combinations of four distinct indices.

```cpp
class Solution {
public:
    int maxProductDifference(vector<int>& nums) {
        int n = nums.size(), res = 0;
        for (int a = 0; a < n; a++) {
            for (int b = 0; b < n; b++) {
                if (a == b) continue;
                for (int c = 0; c < n; c++) {
                    if (a == c || b == c) continue;
                    for (int d = 0; d < n; d++) {
                        if (a == d || b == d || c == d) continue;
                        res = max(res, nums[a] * nums[b] - nums[c] * nums[d]);
                    }
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 4)$
- Space complexity: $O(1)$

## 2. Sorting

To maximize the product difference, we need the two largest numbers for the first product and the two smallest numbers for the second product. After sorting, these are simply the last two and first two elements.

```cpp
class Solution {
public:
    int maxProductDifference(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        return nums[nums.size() - 1] * nums[nums.size() - 2] - nums[0] * nums[1];
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 3. Two Maximums and Two Minimums

We only need the two largest and two smallest values, so we can find them in a single pass without sorting the entire array. By tracking these four values as we iterate, we achieve linear time complexity.

```cpp
class Solution {
public:
    int maxProductDifference(vector<int>& nums) {
        int max1 = 0, max2 = 0;
        int min1 = INT_MAX, min2 = INT_MAX;
        for (int num : nums) {
            if (num > max1) {
                max2 = max1;
                max1 = num;
            } else if (num > max2) {
                max2 = num;
            }
            if (num < min1) {
                min2 = min1;
                min1 = num;
            } else if (num < min2) {
                min2 = num;
            }
        }
        return (max1 * max2) - (min1 * min2);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
