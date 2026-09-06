# 1799. Maximize Score after N Operations

- **Difficulty:** Hard  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximize-score-after-n-operations/>  
- **NeetCode:** <https://neetcode.io/problems/maximize-score-after-n-operations>  
- **Video:** <https://www.youtube.com/watch?v=RRQVDqp5RSE>  

[← Back to index](../INDEX.md)

## 1. Brute Force (Backtracking)

We need to perform exactly `n` operations on an array of `2n` elements, where each operation picks two elements, computes their GCD, and multiplies it by the operation number. Since we want to maximize the total score, we should try all possible ways to pair up elements and track the best result.

The backtracking approach explores every possible pairing. At each step, we pick any two unvisited elements, mark them as used, compute the score for this operation, then recursively solve for the remaining elements. After exploring that path, we backtrack by unmarking those elements and trying different pairs.

```cpp
class Solution {
public:
    int maxScore(vector<int>& nums) {
        int N = nums.size();
        vector<bool> visit(N, false);
        return dfs(nums, visit, 1, N);
    }

private:
    int dfs(vector<int>& nums, vector<bool>& visit, int n, int N) {
        if (n > N / 2) {
            return 0;
        }

        int res = 0;
        for (int i = 0; i < N; i++) {
            if (visit[i]) continue;
            visit[i] = true;
            for (int j = i + 1; j < N; j++) {
                if (visit[j]) continue;
                visit[j] = true;
                int g = gcd(nums[i], nums[j]);
                res = max(res, n * g + dfs(nums, visit, n + 1, N));
                visit[j] = false;
            }
            visit[i] = false;
        }

        return res;
    }

    int gcd(int a, int b) {
        return b == 0 ? a : gcd(b, a % b);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ n * \log m)$
- Space complexity: $O(n)$

> Where $n$ is the size of the array $nums$ and $m$ is the maximum element in the array.

## 2. Bitmask DP (Top-Down) - I

The brute force approach has redundant computation because the same subset of remaining elements can be reached through different pairing sequences. We can optimize by caching results based on which elements have been used.

A bitmask elegantly represents which elements are taken. Each bit position corresponds to an array index: bit `i` being `1` means `nums[i]` is used. Since the operation number can be derived from counting set bits (every `2` used elements means one completed operation), the mask alone uniquely defines the state.

```cpp
class Solution {
public:
    int maxScore(vector<int>& nums) {
        return dfs(0, 1, nums);
    }

private:
    unordered_map<int, int> cache;

    int dfs(int mask, int op, vector<int>& nums) {
        if (cache.count(mask)) {
            return cache[mask];
        }

        int maxScore = 0;
        int n = nums.size();
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) continue;
            for (int j = i + 1; j < n; j++) {
                if ((mask & (1 << j)) != 0) continue;
                int newMask = mask | (1 << i) | (1 << j);
                int score = op * gcd(nums[i], nums[j]) + dfs(newMask, op + 1, nums);
                maxScore = max(maxScore, score);
            }
        }

        return cache[mask] = maxScore;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * 2 ^ n * \log m)$
- Space complexity: $O(2 ^ n)$

> Where $n$ is the size of the array $nums$ and $m$ is the maximum element in the array.

## 3. Bitmask DP (Top-Down) - II

We can further optimize by precomputing all pairwise GCD values. In the previous approach, we recompute `gcd(nums[i], nums[j])` every time we consider that pair. Since the same pair appears in many different states, precomputing these values into a 2D table saves repeated GCD calculations.

Additionally, using an array instead of a hash map for memoization provides faster access since bitmask states are contiguous integers from `0` to `2^n - 1`.

```cpp
class Solution {
public:
    int maxScore(vector<int>& nums) {
        int n = nums.size();
        GCD.assign(n, vector<int>(n, 0));
        dp.assign(1 << n, -1);

        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                GCD[i][j] = gcd(nums[i], nums[j]);
            }
        }

        return dfs(0, 1, nums);
    }

private:
    vector<vector<int>> GCD;
    vector<int> dp;

    int dfs(int mask, int op, vector<int>& nums) {
        if (dp[mask] != -1) return dp[mask];

        int maxScore = 0;
        for (int i = 0; i < nums.size(); i++) {
            if (mask & (1 << i)) continue;
            for (int j = i + 1; j < nums.size(); j++) {
                if (mask & (1 << j)) continue;
                int newMask = mask | (1 << i) | (1 << j);
                maxScore = max(
                    maxScore,
                    op * GCD[i][j] + dfs(newMask, op + 1, nums)
                );
            }
        }
        return dp[mask] = maxScore;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * (2 ^ n + \log m))$
- Space complexity: $O(n ^ 2 + 2 ^ n)$

> Where $n$ is the size of the array $nums$ and $m$ is the maximum element in the array.

## 4. Bitmask DP (Bottom-Up)

Instead of recursion with memoization, we can fill the DP table iteratively. The key observation is that a state with more bits set depends on states with fewer bits set. By iterating from higher masks (more elements used) to lower masks (fewer elements used), we ensure that when we process a state, all states it transitions to are already computed.

The operation number for a given mask is determined by counting how many bits are set and dividing by `2`, then adding `1` for the next operation.

```cpp
class Solution {
public:
    int maxScore(vector<int>& nums) {
        int n = nums.size();
        int N = 1 << n;
        vector<vector<int>> GCD(n, vector<int>(n, 0));

        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                GCD[i][j] = __gcd(nums[i], nums[j]);
            }
        }

        vector<int> dp(N, 0);
        for (int mask = N - 1; mask >= 0; mask--) {
            int bits = __builtin_popcount(mask);
            if (bits % 2 == 1) continue;
            int op = bits / 2 + 1;

            for (int i = 0; i < n; i++) {
                if (mask & (1 << i)) continue;
                for (int j = i + 1; j < n; j++) {
                    if (mask & (1 << j)) continue;
                    int newMask = mask | (1 << i) | (1 << j);
                    dp[mask] = max(dp[mask], op * GCD[i][j] + dp[newMask]);
                }
            }
        }
        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * (2 ^ n + \log m))$
- Space complexity: $O(n ^ 2 + 2 ^ n)$

> Where $n$ is the size of the array $nums$ and $m$ is the maximum element in the array.
