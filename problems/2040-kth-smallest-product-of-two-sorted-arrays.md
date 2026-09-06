# 2040. Kth Smallest Product of Two Sorted Arrays

- **Difficulty:** Hard  
- **Pattern:** Binary Search  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/kth-smallest-product-of-two-sorted-arrays/>  
- **NeetCode:** <https://neetcode.io/problems/kth-smallest-product-of-two-sorted-arrays>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most direct approach computes all possible products by multiplying each element in the first array with each element in the second. After generating all products, we sort them and return the k-th smallest. While simple, this requires `O(m * n)` space and time for generation, plus `O(m * n * log(m * n))` for sorting, making it impractical for large inputs.

```cpp
class Solution {
public:
    long long kthSmallestProduct(vector<int>& nums1, vector<int>& nums2, long long k) {
        int n = nums1.size(), m = nums2.size();
        vector<long long> prod;
        prod.reserve((size_t)n * m);
        for (int x : nums1) {
            for (int y : nums2) {
                prod.push_back(1LL * x * y);
            }
        }
        sort(prod.begin(), prod.end());
        return prod[k - 1];
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ and $n$ are the lengths of the arrays $nums1$ and $nums2$, respectively.

## 2. Binary Search

Instead of enumerating all products, we can binary search on the answer. For a candidate product value, we count how many products are less than or equal to it. If the count is less than `k`, we need a larger product; otherwise, we search smaller. The counting function leverages the sorted nature of both arrays: for positive numbers in `nums1`, we use upper bound on `nums2`; for negative numbers, we use lower bound with adjusted logic.

```cpp
class Solution {
public:
    long long kthSmallestProduct(vector<int>& nums1, vector<int>& nums2, long long k) {
        long long left = -10000000000LL, right = 10000000000LL;
        while (left <= right) {
            long long mid = left + (right - left) / 2;
            if (count(nums1, nums2, mid) < k) left = mid + 1;
            else right = mid - 1;
        }
        return left;
    }

private:
    long long count(vector<int>& nums1, vector<int>& nums2, long long prod) {
        long long cnt = 0;
        int n2 = nums2.size();
        for (int a : nums1) {
            if (a > 0) {
                long long bound = prod >= 0
                    ? prod / a
                    : -(( -prod + a - 1) / a);
                cnt += upper_bound(nums2.begin(), nums2.end(), bound) - nums2.begin();
            } else if (a < 0) {
                long long threshold = (long long)ceil((long double)prod / a);
                cnt += n2 - (lower_bound(nums2.begin(), nums2.end(), threshold) - nums2.begin());
            } else {
                if (prod >= 0) cnt += n2;
            }
        }
        return cnt;
    }
};
```

**Complexity**

- Time complexity: $O(m \log (\log N))$
- Space complexity: $O(1)$

> Where $m$ and $n$ are the lengths of the arrays $nums1$ and $nums2$, respectively. $N$ is the size of the range of the product.

## 3. Binary Search + Two Pointers

We can optimize the counting step using two pointers instead of binary search for each element. By separating negative and non-negative numbers in both arrays, we handle four cases: negative times negative (positive result), positive times positive, negative times positive, and positive times negative. For each case, two pointers can efficiently count products less than or equal to the target by exploiting monotonicity.

```cpp
class Solution {
public:
    long long kthSmallestProduct(vector<int>& nums1, vector<int>& nums2, long long k) {
        int n1 = nums1.size(), n2 = nums2.size();
        int pos1 = 0; // first non-negative in nums1
        while (pos1 < n1 && nums1[pos1] < 0) {
            pos1++;
        }
        int pos2 = 0; // first non-negative in nums2
        while (pos2 < n2 && nums2[pos2] < 0) {
            pos2++;
        }

        long long left = -10000000000LL, right = 10000000000LL;
        while (left <= right) {
            long long mid = left + (right - left) / 2;
            if (count(nums1, nums2, pos1, pos2, n1, n2, mid) < k) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return left;
    }

private:
    long long count(const vector<int>& nums1, const vector<int>& nums2,
                    int pos1, int pos2, int n1, int n2,
                    long long prod) {
        long long cnt = 0;

        // negative * negative -> positive
        int i = 0, j = pos2 - 1;
        while (i < pos1 && j >= 0) {
            if ((long long)nums1[i] * nums2[j] > prod) {
                i++;
            } else {
                cnt += (pos1 - i);
                j--;
            }
        }

        // positive * positive -> positive
        i = pos1; j = n2 - 1;
        while (i < n1 && j >= pos2) {
            if ((long long)nums1[i] * nums2[j] > prod) {
                j--;
            } else {
                cnt += (j - pos2 + 1);
                i++;
            }
        }

        // negative * positive -> negative
        i = 0; j = pos2;
        while (i < pos1 && j < n2) {
            if ((long long)nums1[i] * nums2[j] > prod) {
                j++;
            } else {
                cnt += (n2 - j);
                i++;
            }
        }

        // positive * negative -> negative
        i = pos1; j = 0;
        while (i < n1 && j < pos2) {
            if ((long long)nums1[i] * nums2[j] > prod) {
                i++;
            } else {
                cnt += (n1 - i);
                j++;
            }
        }

        return cnt;
    }
};
```

**Complexity**

- Time complexity: $O((m + n) \log N)$
- Space complexity: $O(1)$

> Where $m$ and $n$ are the lengths of the arrays $nums1$ and $nums2$, respectively. $N$ is the size of the range of the product.
