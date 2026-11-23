# 1099. Two Sum Less Than K

- **Difficulty:** Easy  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/two-sum-less-than-k/>  
- **NeetCode:** <https://neetcode.io/problems/two-sum-less-than-k>  

[← Back to index](../INDEX.md)

## 1. Brute Force

```cpp
class Solution {
public:
    int twoSumLessThanK(vector<int>& nums, int k) {
        int res = -1;
        int n = nums.size();
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                int total = nums[i] + nums[j];
                if (total < k) {
                    res = max(res, total);
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Sorting + Binary Search

```cpp
class Solution {
public:
    int twoSumLessThanK(vector<int>& nums, int k) {
        sort(nums.begin(), nums.end());
        int res = -1;
        int n = nums.size();
        for (int i = 0; i < n; i++) {
            int target = k - nums[i];
            int l = i + 1, r = n - 1, j = -1;
            while (l <= r) {
                int m = l + (r - l) / 2;
                if (nums[m] < target) {
                    j = m;
                    l = m + 1;
                } else {
                    r = m - 1;
                }
            }
            if (j != -1) {
                res = max(res, nums[i] + nums[j]);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 3. Sorting + Two Pointers

```cpp
class Solution {
public:
    int twoSumLessThanK(vector<int>& nums, int k) {
        sort(nums.begin(), nums.end());
        int res = -1;
        int l = 0, r = nums.size() - 1;
        while (l < r) {
            int total = nums[l] + nums[r];
            if (total < k) {
                res = max(res, total);
                l++;
            } else {
                r--;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 4. Counting Sort

```cpp
class Solution {
public:
    int twoSumLessThanK(vector<int>& nums, int k) {
        vector<int> count(1001, 0);
        for (int num : nums) {
            count[num]++;
        }

        int res = -1;
        int lo = 1, hi = 1000;
        while (lo <= hi) {
            if (lo + hi >= k || count[hi] == 0) {
                hi--;
            } else {
                if (count[lo] > (lo < hi ? 0 : 1)) {
                    res = max(res, lo + hi);
                }
                lo++;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(m)$

> Where $n$ is the length of the array $nums$ and $m$ is the range of values in $nums$ ($m = 1000$).
