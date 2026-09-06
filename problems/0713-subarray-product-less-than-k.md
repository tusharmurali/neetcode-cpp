# 713. Subarray Product Less Than K

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/subarray-product-less-than-k/>  
- **NeetCode:** <https://neetcode.io/problems/subarray-product-less-than-k>  
- **Video:** <https://www.youtube.com/watch?v=Cg6_nF7YIks>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most straightforward approach is to check every possible subarray. For each starting index, extend the subarray one element at a time while tracking the running product. If the product stays below `k`, count it. Once the product reaches or exceeds `k`, no further extensions from this starting point will work (since all elements are positive, the product only grows).

```cpp
class Solution {
public:
    int numSubarrayProductLessThanK(vector<int>& nums, int k) {
        int n = nums.size(), res = 0;

        for (int i = 0; i < n; i++) {
            int curProd = 1;
            for (int j = i; j < n; j++) {
                curProd *= nums[j];
                if (curProd >= k) break;
                res++;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Binary Search

Products grow multiplicatively, which makes binary search tricky with raw values. However, taking logarithms converts products into sums: `log(a * b) = log(a) + log(b)`. This means we can build a prefix sum of logarithms and binary search for the rightmost position where the prefix sum difference is less than `log(k)`. For each starting index, we find how many valid ending positions exist.

```cpp
class Solution {
public:
    int numSubarrayProductLessThanK(vector<int>& nums, int k) {
        if (k <= 1) return 0;
        int n = nums.size();
        vector<double> logs(n + 1, 0.0);
        double logK = log(k);
        for (int i = 0; i < n; i++) {
            logs[i + 1] = logs[i] + log(nums[i]);
        }
        int res = 0;
        for (int i = 0; i < n; i++) {
            int l = i + 1, r = n + 1;
            while (l < r) {
                int mid = (l + r) >> 1;
                if (logs[mid] < logs[i] + logK - 1e-12) {
                    l = mid + 1;
                } else {
                    r = mid;
                }
            }
            res += l - (i + 1);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Sliding Window

Since all numbers are positive, the product of a subarray increases as we add elements and decreases as we remove them. This monotonic property makes sliding window ideal. We maintain a window [l, r] where the product is less than `k`. When adding `nums[r]` causes the product to exceed or equal `k`, we shrink from the left until the product drops below `k` again. Each valid window ending at `r` contributes `r - l + 1` new subarrays.

```cpp
class Solution {
public:
    int numSubarrayProductLessThanK(vector<int>& nums, int k) {
        int res = 0, l = 0;
        long long product = 1;
        for (int r = 0; r < nums.size(); r++) {
            product *= nums[r];
            while (l <= r && product >= k) {
                product /= nums[l++];
            }
            res += (r - l + 1);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
