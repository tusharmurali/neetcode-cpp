# 920. Number of Music Playlists

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-music-playlists/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-music-playlists>  
- **Video:** <https://www.youtube.com/watch?v=gk4qzZSmyrs>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

We need to count valid playlists of exactly `goal` songs using exactly `n` different songs, where a song can only repeat after `k` other songs have played. At each position in the playlist, we have two choices: add a new song we have not used yet, or replay an old song (if enough songs have been played since its last appearance). The number of ways to add a new song depends on how many songs we have already used, and the number of ways to replay an old song depends on how many songs are eligible for replay.

```cpp
class Solution {
private:
    static const int MOD = 1e9 + 7;
    vector<vector<int>> dp;

    int count(int curGoal, int oldSongs, int n, int k) {
        if (curGoal == 0 && oldSongs == n) return 1;
        if (curGoal == 0 || oldSongs > n) return 0;
        if (dp[curGoal][oldSongs] != -1) return dp[curGoal][oldSongs];

        long long res = (long long)(n - oldSongs) * count(curGoal - 1, oldSongs + 1, n, k) % MOD;
        if (oldSongs > k) {
            res = (res + (long long)(oldSongs - k) * count(curGoal - 1, oldSongs, n, k)) % MOD;
        }
        dp[curGoal][oldSongs] = res;
        return dp[curGoal][oldSongs];
    }

public:
    int numMusicPlaylists(int n, int goal, int k) {
        dp.assign(goal + 1, vector<int>(n + 1, -1));
        return count(goal, 0, n, k);
    }
};
```

**Complexity**

- Time complexity: $O(g * n)$
- Space complexity: $O(g * n)$

> Where $g$ is the number of songs to listen and $n$ is the number of different songs.

## 2. Dynamic Programming (Bottom-Up)

The top-down solution can be converted to a bottom-up approach by iterating through all possible states. We build a 2D table where `dp[i][j]` represents the number of ways to create a playlist of length `i` using exactly `j` distinct songs. We fill this table row by row, starting from the base case and building up to our target state.

```cpp
class Solution {
private:
    static const int MOD = 1e9 + 7;

public:
    int numMusicPlaylists(int n, int goal, int k) {
        vector<vector<int>> dp(goal + 1, vector<int>(n + 1, 0));
        dp[0][0] = 1;

        for (int curGoal = 1; curGoal <= goal; curGoal++) {
            for (int oldSongs = 1; oldSongs <= n; oldSongs++) {
                int res = (long long) dp[curGoal - 1][oldSongs - 1] * (n - oldSongs + 1) % MOD;
                if (oldSongs > k) {
                    res = (res + (long long) dp[curGoal - 1][oldSongs] * (oldSongs - k) % MOD) % MOD;
                }
                dp[curGoal][oldSongs] = res;
            }
        }

        return dp[goal][n];
    }
};
```

**Complexity**

- Time complexity: $O(g * n)$
- Space complexity: $O(g * n)$

> Where $g$ is the number of songs to listen and $n$ is the number of different songs.

## 3. Dynamic Programming (Space Optimized)

Looking at the bottom-up recurrence, each row only depends on the previous row. This means we do not need to store the entire 2D table. Instead, we can use a single 1D array and update it in place, being careful to preserve the previous row's values where needed. This reduces space from `O(goal * n)` to `O(n)`.

```cpp
class Solution {
private:
    static const int MOD = 1e9 + 7;

public:
    int numMusicPlaylists(int n, int goal, int k) {
        vector<int> dp(n + 1);

        for (int curGoal = 1; curGoal <= goal; curGoal++) {
            int prev = curGoal == 1 ? 1: 0;
            for (int oldSongs = 1; oldSongs <= n; oldSongs++) {
                int res = (long long) prev * (n - oldSongs + 1) % MOD;
                if (oldSongs > k) {
                    res = (res + (long long) dp[oldSongs] * (oldSongs - k) % MOD) % MOD;
                }
                prev = dp[oldSongs];
                dp[oldSongs] = res;
            }
        }

        return dp[n];
    }
};
```

**Complexity**

- Time complexity: $O(g * n)$
- Space complexity: $O(n)$

> Where $g$ is the number of songs to listen and $n$ is the number of different songs.
