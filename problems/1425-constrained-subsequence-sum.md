# 1425. Constrained Subsequence Sum

- **Difficulty:** Hard  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/constrained-subsequence-sum/>  
- **NeetCode:** <https://neetcode.io/problems/constrained-subsequence-sum>  
- **Video:** <https://www.youtube.com/watch?v=-IYZv-nOSys>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

We want to find the maximum sum of a subsequence where consecutive elements are at most `k` indices apart. For each index, we can either start a new subsequence there or extend a previous subsequence. Using recursion with memoization, we explore starting from each position and try extending to any position within the next `k` indices, taking the maximum result.

```cpp
class Solution {
public:
    int constrainedSubsetSum(vector<int>& nums, int k) {
        vector<int> memo(nums.size(), INT_MIN);
        int ans = INT_MIN;
        for (int i = 0; i < nums.size(); i++) {
            ans = max(ans, dfs(nums, memo, k, i));
        }
        return ans;
    }

private:
    int dfs(vector<int>& nums, vector<int>& memo, int k, int i) {
        if (memo[i] != INT_MIN) {
            return memo[i];
        }

        int res = nums[i];
        for (int j = i + 1; j < nums.size() && j - i <= k; j++) {
            res = max(res, nums[i] + dfs(nums, memo, k, j));
        }

        memo[i] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Bottom-Up)

Instead of recursion, we can solve this iteratively. We define `dp[i]` as the maximum sum of a constrained subsequence ending at index `i`. For each position, we look back at the previous `k` elements and take the best one to extend from (if it improves our sum).

```cpp
class Solution {
public:
    int constrainedSubsetSum(vector<int>& nums, int k) {
        int n = nums.size();
        vector<int> dp(nums.begin(), nums.end());

        for (int i = 1; i < n; i++) {
            for (int j = max(0, i - k); j < i; j++) {
                dp[i] = max(dp[i], nums[i] + dp[j]);
            }
        }

        return *max_element(dp.begin(), dp.end());
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(n)$

## 3. Dynamic Programming + Segment Tree

The bottleneck in the previous approach is finding the maximum DP value in a sliding window of size `k`. A segment tree can answer range maximum queries in `O(log n)` time, allowing us to efficiently find the best previous subsequence to extend from.

```cpp
class SegmentTree {
public:
    int n;
    vector<int> tree;

    SegmentTree(int N) {
        n = N;
        while ((n & (n - 1)) != 0) {
            n++;
        }
        tree.assign(2 * n, INT_MIN);
    }

    void update(int i, int val) {
        i += n;
        tree[i] = val;
        while (i > 1) {
            i >>= 1;
            tree[i] = max(tree[i << 1], tree[i << 1 | 1]);
        }
    }

    int query(int l, int r) {
        int res = INT_MIN;
        l += n;
        r += n + 1;
        while (l < r) {
            if (l & 1) {
                res = max(res, tree[l]);
                l++;
            }
            if (r & 1) {
                r--;
                res = max(res, tree[r]);
            }
            l >>= 1;
            r >>= 1;
        }
        return max(0, res);
    }
};

class Solution {
public:
    int constrainedSubsetSum(vector<int>& nums, int k) {
        int n = nums.size();
        SegmentTree maxSegTree(n);
        maxSegTree.update(0, nums[0]);
        int res = nums[0];

        for (int i = 1; i < n; i++) {
            int cur = nums[i] + maxSegTree.query(max(0, i - k), i - 1);
            maxSegTree.update(i, cur);
            res = max(res, cur);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 4. Max-Heap

We can use a max-heap to efficiently track the maximum DP value among the previous `k` elements. The heap stores pairs of (dp value, index). Before using the top of the heap, we remove any entries that are outside our window (more than `k` positions behind).

```cpp
class Solution {
public:
    int constrainedSubsetSum(vector<int>& nums, int k) {
        int res = nums[0];
        priority_queue<pair<int, int>> maxHeap; // max_sum, index
        maxHeap.emplace(nums[0], 0);

        for (int i = 1; i < nums.size(); i++) {
            while (i - maxHeap.top().second > k) {
                maxHeap.pop();
            }

            int curMax = max(nums[i], nums[i] + maxHeap.top().first);
            res = max(res, curMax);
            maxHeap.emplace(curMax, i);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 5. Monotonic Deque

A monotonic decreasing deque provides `O(1)` access to the maximum value in a sliding window. We maintain a deque where values are in decreasing order. The front always holds the maximum DP value within our window, and we remove elements from the back that are smaller than the current value (since they will never be useful).

```cpp
class Solution {
public:
    int constrainedSubsetSum(vector<int>& nums, int k) {
        int n = nums.size();
        deque<pair<int, int>> dq{{0, nums[0]}};
        int res = nums[0];

        for (int i = 1; i < n; i++) {
            if (!dq.empty() && dq.front().first < i - k) {
                dq.pop_front();
            }

            int cur = max(0, dq.front().second) + nums[i];
            while (!dq.empty() && cur > dq.back().second) {
                dq.pop_back();
            }

            dq.emplace_back(i, cur);
            res = max(res, cur);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(k)$
