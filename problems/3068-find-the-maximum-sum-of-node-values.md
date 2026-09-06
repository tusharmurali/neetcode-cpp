# 3068. Find the Maximum Sum of Node Values

- **Difficulty:** Hard  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-the-maximum-sum-of-node-values/>  
- **NeetCode:** <https://neetcode.io/problems/find-the-maximum-sum-of-node-values>  
- **Video:** <https://www.youtube.com/watch?v=bnBp6_b4GCw>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

A key insight is that applying XOR with `k` on an edge affects both endpoints. If we apply the operation on the same edge twice, the effects cancel out. This means we can effectively choose any pair of nodes to XOR (not just adjacent ones) by applying operations along the path between them.

For each node, we have two choices: keep its original value or XOR it with `k`. However, since each operation affects two nodes simultaneously, we must XOR an even number of nodes in total. We use DFS to track two states for each subtree: the maximum sum when an even number of nodes are XORed, and when an odd number are XORed.

```cpp
class Solution {
    vector<vector<int>> adj;

public:
    long long maximumValueSum(vector<int>& nums, int k, vector<vector<int>>& edges) {
        int n = nums.size();
        adj.resize(n);
        for (const auto& edge : edges) {
            adj[edge[0]].push_back(edge[1]);
            adj[edge[1]].push_back(edge[0]);
        }

        return dfs(0, -1, nums, k)[0];
    }

private:
    vector<long long> dfs(int node, int parent, vector<int>& nums, int k) {
        vector<long long> res = { nums[node], nums[node] ^ k };
        for (int child : adj[node]) {
            if (child == parent) continue;

            vector<long long> cur = dfs(child, node, nums, k);
            vector<long long> tmp(2);
            tmp[0] = max(res[0] + cur[0], res[1] + cur[1]);
            tmp[1] = max(res[1] + cur[0], res[0] + cur[1]);
            res = tmp;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down)

Since we must XOR an even number of nodes, we can ignore the tree structure entirely and treat this as a selection problem. For each node, we decide whether to XOR it or not, while tracking whether we have selected an odd or even count so far. This naturally leads to a DP formulation where the state is the current index and the parity of nodes XORed.

```cpp
class Solution {
    vector<vector<long long>> dp;

public:
    long long maximumValueSum(vector<int>& nums, int k, vector<vector<int>>& edges) {
        int n = nums.size();
        dp.assign(n + 1, vector<long long>(2, LLONG_MIN));
        dp[n][0] = 0;
        dp[n][1] = INT_MIN;

        return dfs(0, 0, nums, k);
    }

private:
    long long dfs(int i, int xorCnt, vector<int>& nums, int k) {
        if (dp[i][xorCnt] != LLONG_MIN) {
            return dp[i][xorCnt];
        }

        long long res = nums[i] + dfs(i + 1, xorCnt, nums, k);
        res = max(res, (nums[i] ^ k) + dfs(i + 1, xorCnt ^ 1, nums, k));
        return dp[i][xorCnt] = res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

This is the iterative version of the top-down approach. Instead of using recursion with memoization, we fill the DP table from the end to the beginning. At each position, we compute the best sum for both even and odd XOR counts based on the values already computed for subsequent positions.

```cpp
class Solution {
public:
    long long maximumValueSum(vector<int>& nums, int k, vector<vector<int>>& edges) {
        int n = nums.size();
        vector<vector<long long>> dp(n + 1, vector<long long>(2));
        dp[n][1] = INT_MIN;

        for (int i = n - 1; i >= 0; i--) {
            dp[i][0] = max(nums[i] + dp[i + 1][0], (nums[i] ^ k) + dp[i + 1][1]);
            dp[i][1] = max(nums[i] + dp[i + 1][1], (nums[i] ^ k) + dp[i + 1][0]);
        }

        return dp[0][0];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Space Optimized)

In the bottom-up approach, each state only depends on the immediately next state. This means we do not need to store the entire DP table. We can reduce space by keeping only two variables: one for even parity and one for odd parity, updating them as we process each element.

```cpp
class Solution {
public:
    long long maximumValueSum(vector<int>& nums, int k, vector<vector<int>>& edges) {
        int n = nums.size();
        vector<long long> dp = {0, LLONG_MIN};

        for (int i = n - 1; i >= 0; i--) {
            vector<long long> nextDp(2);
            nextDp[0] = max(nums[i] + dp[0], (nums[i] ^ k) + dp[1]);
            nextDp[1] = max(nums[i] + dp[1], (nums[i] ^ k) + dp[0]);
            dp = nextDp;
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 5. Greedy

For each node, compute the delta: `(nums[i] ^ k) - nums[i]`. A positive delta means XORing that node increases the sum. Since we must XOR an even number of nodes, we greedily pick pairs of nodes with the highest combined deltas. We sort deltas in descending order and take pairs as long as their sum is positive.

```cpp
class Solution {
public:
    long long maximumValueSum(vector<int>& nums, int k, vector<vector<int>>& edges) {
        int n = nums.size();
        vector<int> delta(n);
        long long res = 0;
        for (int i = 0; i < n; i++) {
            res += nums[i];
            delta[i] = (nums[i] ^ k) - nums[i];
        }

        sort(delta.rbegin(), delta.rend());

        for (int i = 0; i + 1 < n; i += 2) {
            int pathDelta = delta[i] + delta[i + 1];
            if (pathDelta <= 0) {
                break;
            }
            res += pathDelta;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 6. Greedy (Optimal)

We can optimize by avoiding sorting. For each node, greedily add whichever is larger: `nums[i]` or `nums[i] ^ k`. Track whether we have XORed an odd or even number of nodes. If odd at the end, we need to undo one operation. The minimum cost to fix parity is the smallest absolute difference `|nums[i] ^ k - nums[i]|` across all nodes.

```cpp
class Solution {
public:
    long long maximumValueSum(vector<int>& nums, int k, vector<vector<int>>& edges) {
        int xorCnt = 0, minDiff = 1 << 30;
        long long res = 0;

        for (int& num : nums) {
            int xorNum = num ^ k;
            if (xorNum > num) {
                res += xorNum;
                xorCnt ^= 1;
            } else {
                res += num;
            }
            minDiff = min(minDiff, abs(xorNum - num));
        }

        return res - (xorCnt * minDiff);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
