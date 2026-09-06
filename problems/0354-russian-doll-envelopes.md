# 354. Russian Doll Envelopes

- **Difficulty:** Hard  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/russian-doll-envelopes/>  
- **NeetCode:** <https://neetcode.io/problems/russian-doll-envelopes>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

This problem is essentially finding the longest chain of envelopes where each envelope strictly contains the previous one. If we sort envelopes by width, we only need to find the longest increasing subsequence (`LIS`) of heights. The trick is to sort by width ascending, but when widths are equal, sort by height descending. This prevents envelopes with the same width from being part of the same chain, since we need strictly greater dimensions for both.

```cpp
class Solution {
    vector<int> nums, memo;
    int n;

    int dfs(int i) {
        if (memo[i] != -1) return memo[i];
        int lis = 1;
        for (int j = i + 1; j < n; j++) {
            if (nums[i] < nums[j]) {
                lis = max(lis, 1 + dfs(j));
            }
        }
        return memo[i] = lis;
    }

public:
    int maxEnvelopes(vector<vector<int>>& envelopes) {
        n = envelopes.size();
        sort(envelopes.begin(), envelopes.end(), [](auto &a, auto &b) {
            if (a[0] != b[0]) return a[0] < b[0];
            return a[1] > b[1];
        });
        nums.resize(n);
        for (int i = 0; i < n; i++) nums[i] = envelopes[i][1];
        memo.assign(n, -1);

        int result = 0;
        for (int i = 0; i < n; i++) {
            result = max(result, dfs(i));
        }
        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Bottom-Up)

Instead of using recursion, we can build the solution iteratively from right to left. For each position, we compute the length of the longest increasing subsequence starting from that position by looking at all valid successors. This bottom-up approach avoids the overhead of recursion and explicitly fills a `DP` table.

```cpp
class Solution {
public:
    int maxEnvelopes(vector<vector<int>>& envelopes) {
        int n = envelopes.size();
        sort(envelopes.begin(), envelopes.end(),
             [](const vector<int>& a, const vector<int>& b) {
                 if (a[0] != b[0]) return a[0] < b[0];
                 return a[1] > b[1];
             });
        vector<int> heights(n);
        for (int i = 0; i < n; ++i) heights[i] = envelopes[i][1];
        vector<int> LIS(n, 1);
        int ans = 0;
        for (int i = n - 1; i >= 0; --i) {
            for (int j = i + 1; j < n; ++j) {
                if (heights[i] < heights[j]) {
                    LIS[i] = max(LIS[i], 1 + LIS[j]);
                }
            }
            ans = max(ans, LIS[i]);
        }
        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 3. Dynamic Programming + Binary Search

The standard `LIS` problem can be solved in O(n log n) using binary search. We maintain a list where each position stores the smallest ending value of all increasing subsequences of that length. For each new element, we either extend the longest subsequence or replace an existing ending value to allow for potentially longer subsequences later. Binary search finds the correct position efficiently.

```cpp
class Solution {
public:
    int maxEnvelopes(vector<vector<int>>& envelopes) {
        int n = envelopes.size();
        vector<int> nums(n);
        sort(envelopes.begin(), envelopes.end(), [](auto &a, auto &b) {
            if (a[0] != b[0]) return a[0] < b[0];
            return a[1] > b[1];
        });
        for (int i = 0; i < n; i++) nums[i] = envelopes[i][1];

        vector<int> dp;
        dp.push_back(nums[0]);

        int LIS = 1;
        for (int i = 1; i < n; i++) {
            if (dp.back() < nums[i]) {
                dp.push_back(nums[i]);
                LIS++;
                continue;
            }

            int idx = lower_bound(dp.begin(),
                                  dp.end(), nums[i]) - dp.begin();
            dp[idx] = nums[i];
        }

        return LIS;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 4. Segment Tree

A segment tree can efficiently answer range maximum queries, which helps compute `LIS`. For each height, we query the maximum `LIS` length among all smaller heights, add one, and update the tree with this new value. Coordinate compression reduces the height values to a manageable range. This approach achieves the same O(n log n) complexity as binary search but offers a different perspective using range queries.

```cpp
class SegmentTree {
public:
    int n;
    vector<int> tree;

    SegmentTree(int N) {
        n = N;
        while (n & (n - 1)) {
            n++;
        }
        tree.resize(2 * n);
    }

    void update(int i, int val) {
        tree[n + i] = val;
        int j = (n + i) >> 1;
        while (j >= 1) {
            tree[j] = max(tree[j << 1], tree[j << 1 | 1]);
            j >>= 1;
        }
    }

    int query(int l, int r) {
        if (l > r) {
            return 0;
        }
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
        return res;
    }
};

class Solution {
    int lis(vector<int>& nums) {
        vector<int> sortedArr = nums;
        sort(sortedArr.begin(), sortedArr.end());
        sortedArr.erase(unique(sortedArr.begin(),
                        sortedArr.end()), sortedArr.end());

        vector<int> order(nums.size());
        for (int i = 0; i < nums.size(); i++) {
            order[i] = lower_bound(sortedArr.begin(), sortedArr.end(),
                                   nums[i]) - sortedArr.begin();
        }

        int n = sortedArr.size();
        SegmentTree segTree(n);

        int LIS = 0;
        for (int num : order) {
            int curLIS = segTree.query(0, num - 1) + 1;
            segTree.update(num, curLIS);
            LIS = max(LIS, curLIS);
        }
        return LIS;
    }

public:
    int maxEnvelopes(vector<vector<int>>& envelopes) {
        int n = envelopes.size();
        sort(envelopes.begin(), envelopes.end(),
             [](const vector<int>& a, const vector<int>& b) {
                 if (a[0] != b[0]) return a[0] < b[0];
                 return a[1] > b[1];
             });
        vector<int> heights(n);
        for (int i = 0; i < n; ++i) heights[i] = envelopes[i][1];
        return lis(heights);
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$
