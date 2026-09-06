# 1856. Maximum Subarray Min Product

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-subarray-min-product/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-subarray-min-product>  
- **Video:** <https://www.youtube.com/watch?v=YLesLbNkyjA>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The min-product of a subarray is defined as the minimum element multiplied by the sum of all elements. For each possible subarray, we need to track both the running minimum and the running sum. By trying all subarrays starting from each index, we can compute every possible min-product and find the maximum.

```cpp
class Solution {
public:
    int maxSumMinProduct(vector<int>& nums) {
        long long res = 0, MOD = 1000000007;
        for (int i = 0; i < nums.size(); i++) {
            long long total_sum = 0, mini = INT_MAX;
            for (int j = i; j < nums.size(); j++) {
                mini = min(mini, (long long)nums[j]);
                total_sum += nums[j];
                long long cur = (mini * total_sum) % MOD;
                res = max(res, cur);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## 2. Divide And Conquer (Brute Force)

For any subarray, the minimum element defines the "bottleneck." If we know the minimum element's position, the optimal subarray with that element as minimum spans as far as possible in both directions. This leads to a divide and conquer approach: find the minimum in the current range, calculate the score for the entire range using that minimum, then recursively solve for the left and right portions (excluding the minimum).

```cpp
class Solution {
public:
    int maxSumMinProduct(vector<int>& nums) {
        const int MOD = 1e9 + 7;
        return rec(nums, 0, nums.size() - 1) % MOD;
    }

private:
    long long rec(vector<int>& nums, int l, int r) {
        if (l > r) return 0;

        int minIdx = l;
        long long totalSum = 0;
        for (int i = l; i <= r; i++) {
            totalSum += nums[i];
            if (nums[i] < nums[minIdx]) {
                minIdx = i;
            }
        }

        long long cur = totalSum * nums[minIdx];
        long long left = rec(nums, l, minIdx - 1);
        long long right = rec(nums, minIdx + 1, r);

        return max(cur, max(left, right));
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$ for recursion stack.

## 3. Divide And Conquer (Segment Tree)

The brute force divide and conquer spends O(n) time finding the minimum in each range, leading to O(n^2) worst case. We can optimize this using a segment tree that answers range minimum queries in O(log n). Combined with a prefix sum array for O(1) range sum queries, this reduces the overall complexity significantly.

```cpp
class SegmentTree {
    int n;
    vector<pair<int, long long>> tree;

public:
    SegmentTree(int n, vector<int>& nums) : n(n) {
        while ((this->n & (this->n - 1)) != 0) this->n++;
        build(n, nums);
    }

    void build(int n, vector<int>& nums) {
        tree.resize(2 * this->n, {-1, LLONG_MAX});
        for (int i = 0; i < n; i++) {
            tree[this->n + i] = {i, nums[i]};
        }
        for (int i = this->n - 1; i > 0; i--) {
            tree[i] = min(tree[i << 1], tree[i << 1 | 1], [](auto& a, auto& b) { return a.second < b.second; });
        }
    }

    int query(int l, int r) {
        pair<int, long long> res = {-1, LLONG_MAX};
        l += this->n;
        r += this->n + 1;
        while (l < r) {
            if (l & 1) res = min(res, tree[l++], [](auto& a, auto& b) { return a.second < b.second; });
            if (r & 1) res = min(res, tree[--r], [](auto& a, auto& b) { return a.second < b.second; });
            l >>= 1;
            r >>= 1;
        }
        return res.first;
    }
};

class Solution {
public:
    int maxSumMinProduct(vector<int>& nums) {
        const int MOD = 1e9 + 7;
        SegmentTree segTree(nums.size(), nums);
        vector<long long> prefixSum(nums.size() + 1, 0);
        for (int i = 0; i < nums.size(); i++) {
            prefixSum[i + 1] = prefixSum[i] + nums[i];
        }

        return rec(0, nums.size() - 1, nums, prefixSum, segTree) % MOD;
    }

private:
    long long rec(int l, int r, vector<int>& nums, vector<long long>& prefixSum, SegmentTree& segTree) {
        if (l > r) return 0;
        int minIdx = segTree.query(l, r);
        long long totalSum = prefixSum[r + 1] - prefixSum[l];
        long long cur = totalSum * nums[minIdx];
        long long left = rec(l, minIdx - 1, nums, prefixSum, segTree);
        long long right = rec(minIdx + 1, r, nums, prefixSum, segTree);
        return max(cur, max(left, right));
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 4. Monotonic Stack

For each element, we want to find the maximum subarray where that element is the minimum. This means finding the nearest smaller elements on both sides. A monotonic stack efficiently computes these boundaries in linear time. With prefix sums for fast range sums, we can evaluate each element's contribution and find the global maximum.

```cpp
class Solution {
public:
    int maxSumMinProduct(vector<int>& nums) {
        int n = nums.size();
        vector<long long> prefixSum(n + 1, 0);
        for (int i = 0; i < n; i++) {
            prefixSum[i + 1] = prefixSum[i] + nums[i];
        }

        vector<int> prevMin(n, -1), nxtMin(n, n);
        stack<int> stack;

        for (int i = 0; i < n; i++) {
            while (!stack.empty() && nums[stack.top()] >= nums[i]) {
                stack.pop();
            }
            if (!stack.empty()) {
                prevMin[i] = stack.top();
            }
            stack.push(i);
        }

        while (!stack.empty()) stack.pop();
        for (int i = n - 1; i >= 0; i--) {
            while (!stack.empty() && nums[stack.top()] >= nums[i]) {
                stack.pop();
            }
            if (!stack.empty()) {
                nxtMin[i] = stack.top();
            }
            stack.push(i);
        }

        long long res = 0;
        int MOD = 1e9 + 7;
        for (int i = 0; i < n; i++) {
            int l = prevMin[i] + 1, r = nxtMin[i] - 1;
            long long totalSum = prefixSum[r + 1] - prefixSum[l];
            res = max(res, nums[i] * totalSum);
        }

        return res % MOD;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 5. Monotonic Stack (Space Optimized) - I

We can avoid storing separate boundary arrays by processing elements as they are popped from the stack. When an element is popped (because a smaller element is found), we immediately know its right boundary. The left boundary is the element currently at the top of the stack. We also track the starting index of each element's potential range as we push to the stack.

```cpp
class Solution {
public:
    int maxSumMinProduct(vector<int>& nums) {
        int n = nums.size();
        vector<long long> prefix(n + 1, 0);
        for (int i = 0; i < n; i++) {
            prefix[i + 1] = prefix[i] + nums[i];
        }

        long long res = 0;
        stack<pair<int, int>> stack;
        for (int i = 0; i < n; i++) {
            int newStart = i;
            while (!stack.empty() && stack.top().second > nums[i]) {
                auto [start, val] = stack.top();
                stack.pop();
                long long total = prefix[i] - prefix[start];
                res = max(res, val * total);
                newStart = start;
            }
            stack.push({newStart, nums[i]});
        }

        while (!stack.empty()) {
            auto [start, val] = stack.top();
            stack.pop();
            long long total = prefix[n] - prefix[start];
            res = max(res, val * total);
        }

        return res % 1000000007;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 6. Monotonic Stack (Space Optimized) - II

This variation uses an index-only stack and processes all elements in a single pass by treating the position after the array as a sentinel. When we pop an element, the current position is its right boundary, and the new stack top (or -1) is its left boundary. This eliminates the need to store value pairs in the stack.

```cpp
class Solution {
public:
    int maxSumMinProduct(vector<int>& nums) {
        int n = nums.size();
        vector<long long> prefixSum(n + 1, 0);
        for (int i = 0; i < n; i++) {
            prefixSum[i + 1] = prefixSum[i] + nums[i];
        }

        long long res = 0;
        const int mod = 1e9 + 7;
        stack<int> st;
        for (int i = 0; i <= n; i++) {
            while (!st.empty() && (i == n || nums[i] < nums[st.top()])) {
                int j = st.top();
                st.pop();
                int start = st.empty() ? 0 : st.top() + 1;
                res = max(res, (long long) nums[j] * (prefixSum[i] - prefixSum[start]));
            }
            st.push(i);
        }

        return res % mod;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
