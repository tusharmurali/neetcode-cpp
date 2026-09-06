# 1793. Maximum Score of a Good Subarray

- **Difficulty:** Hard  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-score-of-a-good-subarray/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-score-of-a-good-subarray>  
- **Video:** <https://www.youtube.com/watch?v=_K7oyQlAjv4>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A "good" subarray must contain index `k`. The score is the minimum element multiplied by the subarray length. The straightforward approach is to try all possible subarrays that include `k`, tracking the minimum as we extend each one. For each starting point at or before `k`, we extend rightward past `k`, updating the minimum and calculating the score at each step.

```cpp
class Solution {
public:
    int maximumScore(vector<int>& nums, int k) {
        int n = nums.size(), res = 0;

        for (int i = 0; i <= k; i++) {
            int minEle = nums[i];
            for (int j = i; j < n; j++) {
                minEle = min(minEle, nums[j]);
                if (j >= k) {
                    res = max(res, minEle * (j - i + 1));
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## 2. Binary Search

For any subarray containing `k`, the minimum value decreases (or stays the same) as we expand outward from `k`. We can preprocess the array so that `arr[i]` represents the minimum value in the subarray from `i` to `k` (for left side) or from `k` to `i` (for right side). This creates sorted arrays on each side, allowing binary search to quickly find how far we can extend while maintaining at least a given minimum value.

```cpp
class Solution {
public:
    int maximumScore(vector<int>& nums, int k) {
        int n = nums.size(), res = 0;
        vector<int> arr = nums;

        for (int i = k - 1; i >= 0; i--) {
            arr[i] = min(arr[i], arr[i + 1]);
        }
        for (int i = k + 1; i < n; i++) {
            arr[i] = min(arr[i], arr[i - 1]);
        }

        vector<int> leftArr(arr.begin(), arr.begin() + k + 1);
        vector<int> rightArr(arr.begin() + k, arr.end());

        set<int> candidates(arr.begin(), arr.end());
        for (int minVal : candidates) {
            int l = lower_bound(leftArr.begin(), leftArr.end(), minVal) - leftArr.begin();
            int r = findRight(rightArr, minVal);
            res = max(res, minVal * (k - l + 1 + r));
        }
        return res;
    }

private:
    int findRight(vector<int>& arr, int target) {
        int lo = 0, hi = arr.size() - 1, pos = 0;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            if (arr[mid] >= target) {
                pos = mid;
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        return pos;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Binary Search (Overwriting the Input)

This is a space-optimized version of the previous approach. Instead of creating a separate array, we modify the input array directly. The left portion becomes non-decreasing toward `k`, and the right portion becomes non-increasing from `k`. We can then binary search directly on the modified input array.

```cpp
class Solution {
public:
    int maximumScore(vector<int>& nums, int k) {
        int n = nums.size(), res = 0;

        for (int i = k - 1; i >= 0; i--) {
            nums[i] = min(nums[i], nums[i + 1]);
        }
        for (int i = k + 1; i < n; i++) {
            nums[i] = min(nums[i], nums[i - 1]);
        }

        auto findLeft = [&](int target) {
            int lo = 0, hi = k;
            while (lo <= hi) {
                int mid = (lo + hi) / 2;
                if (nums[mid] < target) {
                    lo = mid + 1;
                } else {
                    hi = mid - 1;
                }
            }
            return lo;
        };

        auto findRight = [&](int target) {
            int lo = k, hi = n - 1;
            while (lo <= hi) {
                int mid = (lo + hi) / 2;
                if (nums[mid] >= target) {
                    lo = mid + 1;
                } else {
                    hi = mid - 1;
                }
            }
            return hi;
        };

        set<int> candidates(nums.begin(), nums.end());
        for (int minVal : candidates) {
            int i = findLeft(minVal);
            int j = findRight(minVal);
            res = max(res, minVal * (j - i + 1));
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 4. Monotonic Stack

This problem is related to finding the largest rectangle in a histogram. For each element, we want to know how far left and right it can extend as the minimum. A monotonic stack helps us find the "next smaller element" boundaries efficiently. When we pop an element from the stack, we know its valid range, and we only count it if that range includes index `k`.

```cpp
class Solution {
public:
    int maximumScore(vector<int>& nums, int k) {
        int n = nums.size(), res = 0;
        stack<int> stk;

        for (int i = 0; i <= n; i++) {
            while (!stk.empty() && (i == n || nums[stk.top()] >= nums[i])) {
                int mini = nums[stk.top()];
                stk.pop();
                int j = stk.empty() ? -1 : stk.top();
                if (j < k && k < i) {
                    res = max(res, mini * (i - j - 1));
                }
            }
            stk.push(i);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 5. Greedy + Two Pointers

Start with just the element at index `k` as our subarray. To expand, we have two choices: go left or go right. The key insight is that we should always expand toward the larger neighbor. This greedy choice maximizes the minimum value we can maintain for as long as possible, leading to higher scores. We continue until we have expanded to cover the entire array.

```cpp
class Solution {
public:
    int maximumScore(vector<int>& nums, int k) {
        int l = k, r = k;
        int res = nums[k];
        int curMin = nums[k];
        int n = nums.size();

        while (l > 0 || r < n - 1) {
            int left = (l > 0) ? nums[l - 1] : 0;
            int right = (r < n - 1) ? nums[r + 1] : 0;

            if (left > right) {
                l--;
                curMin = min(curMin, left);
            } else {
                r++;
                curMin = min(curMin, right);
            }

            res = max(res, curMin * (r - l + 1));
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
