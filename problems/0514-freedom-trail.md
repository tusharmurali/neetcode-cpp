# 514. Freedom Trail

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/freedom-trail/>  
- **NeetCode:** <https://neetcode.io/problems/freedom-trail>  
- **Video:** <https://www.youtube.com/watch?v=NOgnlTXidSs>  

[← Back to index](../INDEX.md)

## 1. Recursion

Imagine a circular dial with letters. To spell a word, we rotate the dial to align each required letter with the top position, then press a button. The challenge is finding the minimum total rotations.

For each character in the key, we might have multiple positions on the ring that match. From our current position, we can rotate clockwise or counterclockwise to reach any matching position. We try all possibilities recursively and take the minimum.

Since the ring is circular, the distance between two positions is the minimum of going directly or wrapping around.

```cpp
class Solution {
public:
    int findRotateSteps(string ring, string key) {
        return dfs(0, 0, ring, key);
    }

private:
    int dfs(int r, int k, const string& ring, const string& key) {
        if (k == key.size()) return 0;

        int res = INT_MAX;
        for (int i = 0; i < ring.size(); i++) {
            if (ring[i] == key[k]) {
                int minDist = min(abs(r - i), int(ring.size()) - abs(r - i));
                res = min(res, minDist + 1 + dfs(i, k + 1, ring, key));
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ m)$
- Space complexity: $O(m)$ for recursion stack.

> Where $n$ is the length of the $ring$ and $m$ is the length of the $key$.

## 2. Dynamic Programming (Top-Down)

The plain recursion has overlapping subproblems. From the same ring position trying to match the same key index, we always get the same answer. Adding memoization avoids recomputing these states.

The state is defined by two parameters: current ring position and current key index. There are at most `n * m` unique states, where `n` is the `ring` length and `m` is the `key` length.

```cpp
class Solution {
    vector<vector<int>> dp;

public:
    int findRotateSteps(string ring, string key) {
        int n = ring.size();
        int m = key.size();
        dp.assign(n, vector<int>(m, -1));
        return dfs(0, 0, ring, key);
    }

private:
    int dfs(int r, int k, string& ring, string& key) {
        if (k == key.size()) return 0;
        if (dp[r][k] != -1) return dp[r][k];

        int res = INT_MAX;
        for (int i = 0; i < ring.size(); i++) {
            if (ring[i] == key[k]) {
                int minDist = min(abs(r - i), int(ring.size()) - abs(r - i));
                res = min(res, minDist + 1 + dfs(i, k + 1, ring, key));
            }
        }

        dp[r][k] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * m)$
- Space complexity: $O(n * m)$

> Where $n$ is the length of the $ring$ and $m$ is the length of the $key$.

## 3. Dynamic Programming (Bottom-Up)

We can convert the top-down solution to bottom-up by filling the DP table iteratively. Process the key from the last character back to the first. For each key character, compute the minimum cost to reach it from every possible ring position.

The value `dp[k][r]` represents the minimum steps to spell `key[k:]` starting from ring position `r`. We build this by using already-computed values for `key[k + 1:]`.

```cpp
class Solution {
public:
    int findRotateSteps(string ring, string key) {
        int n = ring.size();
        int m = key.size();
        vector<vector<int>> dp(m + 1, vector<int>(n, INT_MAX));

        for (int i = 0; i < n; ++i) {
            dp[m][i] = 0;
        }

        for (int k = m - 1; k >= 0; --k) {
            for (int r = 0; r < n; ++r) {
                for (int i = 0; i < n; ++i) {
                    if (ring[i] == key[k]) {
                        int minDist = min(abs(r - i), n - abs(r - i));
                        dp[k][r] = min(dp[k][r], minDist + 1 + dp[k + 1][i]);
                    }
                }
            }
        }
        return dp[0][0];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * m)$
- Space complexity: $O(n * m)$

> Where $n$ is the length of the $ring$ and $m$ is the length of the $key$.

## 4. Dynamic Programming (Space Optimized) - I

Since each DP row only depends on the next row, we can reduce space from O(n \* m) to O(n) by keeping just two arrays: one for the current key index and one for the next.

Additionally, precomputing the positions of each character in the ring using an adjacency list speeds up lookups.

```cpp
class Solution {
public:
    int findRotateSteps(string ring, string key) {
        int n = ring.size();
        int m = key.size();
        vector<int> dp(n, 0);

        vector<vector<int>> adj(26);
        for (int i = 0; i < n; ++i) {
            adj[ring[i] - 'a'].push_back(i);
        }

        for (int k = m - 1; k >= 0; --k) {
            vector<int> nextDp(n, INT_MAX);
            for (int r = 0; r < n; ++r) {
                for (int& i : adj[key[k] - 'a']) {
                    int minDist = min(abs(r - i), n - abs(r - i));
                    nextDp[r] = min(nextDp[r], minDist + 1 + dp[i]);
                }
            }
            dp = nextDp;
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * m)$
- Space complexity: $O(n)$

> Where $n$ is the length of the $ring$ and $m$ is the length of the $key$.

## 5. Dynamic Programming (Space Optimized) - II

Instead of tracking all ring positions, we can focus only on positions that match key characters. The `dp` array stores the minimum cost to reach each ring position after matching some prefix of the key.

Initially, we set `dp[i]` to the distance from position `0` to position `i`. Then for each subsequent key character, we update only the positions that match, computing the minimum cost by considering transitions from positions matching the previous key character.

```cpp
class Solution {
public:
    int findRotateSteps(string ring, string key) {
        int n = ring.size(), m = key.size();
        vector<int> dp(n);

        for (int i = 0; i < n; i++) {
            dp[i] = min(i, n - i);
        }

        vector<vector<int>> adj(26);
        for (int i = 0; i < n; i++) {
            adj[ring[i] - 'a'].push_back(i);
        }

        for (int k = 1; k < m; k++) {
            for (int r : adj[key[k] - 'a']) {
                int minDist = INT_MAX;
                for (int i : adj[key[k - 1] - 'a']) {
                    minDist = min(minDist, min(abs(r - i), n - abs(r - i)) + dp[i]);
                }
                dp[r] = minDist;
            }
        }

        int result = INT_MAX;
        for (int& i : adj[key[m - 1] - 'a']) {
            result = min(result, dp[i]);
        }

        return result + m;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * m)$
- Space complexity: $O(n)$

> Where $n$ is the length of the $ring$ and $m$ is the length of the $key$.

## 6. Dynamic Programming (Optimal)

For each ring position, we only need to consider the closest matching positions in each direction (clockwise and counterclockwise). Using binary search or maintaining sorted position lists, we can find these two candidates in O(1) amortized time per position.

Since the adjacency list positions are naturally sorted by index, we can use a two-pointer technique while iterating through ring positions. For each position, we find the nearest matching character on either side and choose the better option.

```cpp
class Solution {
public:
    int findRotateSteps(string ring, string key) {
        int n = ring.size(), m = key.size();

        vector<int> dp(n, 0);
        vector<int> nextDp(n, 0);
        vector<vector<int>> adj(26);

        for (int i = 0; i < n; i++) {
            adj[ring[i] - 'a'].push_back(i);
        }

        for (int k = m - 1; k >= 0; k--) {
            int c = key[k] - 'a';
            int it = 0, N = adj[c].size();

            for (int r = 0; r < n; r++) {
                if (ring[r] - 'a' != c) {
                    nextDp[r] = INT_MAX;
                    while (it < N && adj[c][it] < r) {
                        it++;
                    }

                    int nextIdx = it < N ? adj[c][it] : adj[c][0];
                    int prevIdx = it > 0 ? adj[c][it - 1] : adj[c][N - 1];

                    nextDp[r] = min(
                        (r > prevIdx ? r - prevIdx : n - (prevIdx - r)) + dp[prevIdx],
                        (nextIdx > r ? nextIdx - r : n - (r - nextIdx)) + dp[nextIdx]
                    );
                } else {
                    nextDp[r] = dp[r];
                }
            }

            dp.swap(nextDp);
        }

        return dp[0] + m;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n)$

> Where $n$ is the length of the $ring$ and $m$ is the length of the $key$.
