# 1547. Minimum Cost to Cut a Stick

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-cost-to-cut-a-stick/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-cost-to-cut-a-stick>  
- **Video:** <https://www.youtube.com/watch?v=EVxTO5I0d7w>  

[← Back to index](../INDEX.md)

## 1. Recursion

Each cut costs the length of the current stick segment. The order of cuts matters because earlier cuts determine the lengths of segments for later cuts. We need to try all possible orderings of cuts and find the one with minimum total cost. For a segment from position `l` to `r`, we try each valid cut point, pay the segment length, then recursively solve the resulting sub-segments.

```cpp
class Solution {
public:
    int minCost(int n, vector<int>& cuts) {
        return dfs(0, n, cuts);
    }

private:
    int dfs(int l, int r, vector<int>& cuts) {
        if (r - l == 1) {
            return 0;
        }
        int res = INT_MAX;
        for (int c : cuts) {
            if (l < c && c < r) {
                res = min(res, (r - l) + dfs(l, c, cuts) + dfs(c, r, cuts));
            }
        }
        return res == INT_MAX ? 0 : res;
    }
};
```

**Complexity**

- Time complexity: $O(m ^ N)$
- Space complexity: $O(N)$ for recursion stack.

> Where $m$ is the size of the $cuts$ array, $n$ is the length of the stick, and $N = min(n, m)$.

## 2. Dynamic Programming (Top-Down) - I

The recursive solution has overlapping subproblems since many segment pairs `(l, r)` are computed multiple times. By caching results for each unique `(l, r)` pair, we avoid redundant computation. The state depends only on the segment boundaries, not on how we arrived at that segment.

```cpp
class Solution {
public:
    int minCost(int n, vector<int>& cuts) {
        return dfs(0, n, cuts);
    }

private:
    unordered_map<string, int> dp;

    int dfs(int l, int r, vector<int>& cuts) {
        if (r - l == 1) {
            return 0;
        }
        string key = to_string(l) + "," + to_string(r);
        if (dp.find(key) != dp.end()) {
            return dp[key];
        }

        int res = INT_MAX;
        for (int c : cuts) {
            if (l < c && c < r) {
                res = min(res, (r - l) + dfs(l, c, cuts) + dfs(c, r, cuts));
            }
        }
        res = res == INT_MAX ? 0 : res;
        dp[key] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * N ^ 2)$
- Space complexity: $O(N ^ 2)$

> Where $m$ is the size of the $cuts$ array, $n$ is the length of the stick, and $N = min(n, m)$.

## 3. Dynamic Programming (Top-Down) - II

Instead of using arbitrary segment boundaries, we can index by cut positions. After sorting cuts, we define states by cut indices rather than positions. This reduces the state space from potentially O(n^2) to O(m^2) where `m` is the number of cuts. We pass indices `i` and `j` representing the range of cuts to consider, plus the actual segment boundaries `l` and `r`.

```cpp
class Solution {
private:
    vector<vector<int>> dp;

public:
    int minCost(int n, vector<int>& cuts) {
        int m = cuts.size();
        sort(cuts.begin(), cuts.end());
        dp = vector<vector<int>>(m + 1, vector<int>(m + 1, -1));
        return dfs(0, n, 0, m - 1, cuts);
    }

private:
    int dfs(int l, int r, int i, int j, vector<int>& cuts) {
        if (i > j) return 0;
        if (dp[i][j] != -1) return dp[i][j];

        int res = INT_MAX;
        for (int mid = i; mid <= j; mid++) {
            int cur = (r - l) + dfs(l, cuts[mid], i, mid - 1, cuts) + dfs(cuts[mid], r, mid + 1, j, cuts);
            res = min(res, cur);
        }

        dp[i][j] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m\log m + m ^ 3)$
- Space complexity: $O(m ^ 2)$

> Where $m$ is the size of the $cuts$ array and $n$ is the length of the stick.

## 4. Dynamic Programming (Bottom-Up)

We can solve this iteratively by building up from smaller segments to larger ones. First, add `0` and `n` as boundary points to the sorted cuts. Then `dp[i][j]` represents the minimum cost to cut the segment between `cuts[i]` and `cuts[j]`. We fill the table by increasing segment length, since longer segments depend on solutions for shorter ones.

```cpp
class Solution {
public:
    int minCost(int n, vector<int>& cuts) {
        int m = cuts.size();
        cuts.push_back(0);
        cuts.push_back(n);
        sort(cuts.begin(), cuts.end());

        vector<vector<int>> dp(m + 2, vector<int>(m + 2, 0));

        for (int length = 2; length <= m + 1; length++) {
            for (int i = 0; i + length <= m + 1; i++) {
                int j = i + length;
                dp[i][j] = INT_MAX;
                for (int mid = i + 1; mid < j; mid++) {
                    dp[i][j] = min(dp[i][j],
                        cuts[j] - cuts[i] + dp[i][mid] + dp[mid][j]);
                }
            }
        }

        return dp[0][m + 1];
    }
};
```

**Complexity**

- Time complexity: $O(m\log m + m ^ 3)$
- Space complexity: $O(m ^ 2)$

> Where $m$ is the size of the $cuts$ array and $n$ is the length of the stick.
