# 1626. Best Team with no Conflicts

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/best-team-with-no-conflicts/>  
- **NeetCode:** <https://neetcode.io/problems/best-team-with-no-conflicts>  
- **Video:** <https://www.youtube.com/watch?v=7kURH3btcV4>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

A conflict happens when a younger player has a higher score than an older player. To handle this cleanly, we sort players by score (and by age as a tiebreaker). After sorting, as we iterate through players in order, we only need to check if a new player's age is compatible with the last player we picked. If the current player has an equal or higher age than the last picked player, there is no conflict since the scores are already in non-decreasing order. We use recursion with memoization to explore all valid team combinations and find the maximum total score.

```cpp
class Solution {
private:
    vector<pair<int, int>> pairs;
    vector<vector<int>> dp;

public:
    int bestTeamScore(vector<int>& scores, vector<int>& ages) {
        int n = scores.size();
        pairs.resize(n);
        for (int i = 0; i < n; i++) {
            pairs[i] = {scores[i], ages[i]};
        }
        sort(pairs.begin(), pairs.end());

        dp = vector<vector<int>>(n, vector<int>(n + 1, -1));
        return dfs(0, -1);
    }

private:
    int dfs(int i, int j) {
        if (i == pairs.size()) {
            return 0;
        }
        if (dp[i][j + 1] != -1) {
            return dp[i][j + 1];
        }

        int mScore = j >= 0 ? pairs[j].first : 0;
        int mAge = j >= 0 ? pairs[j].second : 0;
        int score = pairs[i].first;
        int age = pairs[i].second;

        int res = 0;
        if (!(score > mScore && age < mAge)) {
            res = dfs(i + 1, i) + score;
        }
        dp[i][j + 1] = max(res, dfs(i + 1, j));
        return dp[i][j + 1];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 2. Dynamic Programming (Bottom-Up)

Instead of recursion, we can build the solution iteratively. After sorting players by score, for each player we look at all previous players and check if we can extend their team. If the current player's age is greater than or equal to a previous player's age, we can add the current player to that team without causing a conflict. We track the maximum score ending at each player position.

```cpp
class Solution {
public:
    int bestTeamScore(vector<int>& scores, vector<int>& ages) {
        int n = scores.size();
        vector<pair<int, int>> pairs(n);
        for (int i = 0; i < n; i++) {
            pairs[i] = {scores[i], ages[i]};
        }
        sort(pairs.begin(), pairs.end());

        vector<int> dp(n);
        for (int i = 0; i < n; i++) {
            dp[i] = pairs[i].first;
        }

        for (int i = 0; i < n; i++) {
            int mScore = pairs[i].first, mAge = pairs[i].second;
            for (int j = 0; j < i; j++) {
                int score = pairs[j].first, age = pairs[j].second;
                if (mAge >= age) {
                    dp[i] = max(dp[i], mScore + dp[j]);
                }
            }
        }

        return *max_element(dp.begin(), dp.end());
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Segment Tree)

The bottom-up approach has O(n^2) complexity because we check all previous players for each new player. We can optimize this using a segment tree. Since we only care about players with ages less than or equal to the current player's age, we can query the segment tree for the maximum `dp` value among all ages in the range `[0, current_age]`. After processing each player, we update the segment tree with the new `dp` value at that age index.

```cpp
class SegmentTree {
private:
    int n;
    vector<int> tree;

public:
    SegmentTree(int N) {
        n = N;
        while ((n & (n - 1)) != 0) {
            n++;
        }
        build();
    }

    void build() {
        tree.resize(2 * n, 0);
    }

    void update(int i, int val) {
        int pos = n + i;
        tree[pos] = max(tree[pos], val);
        pos >>= 1;
        while (pos >= 1) {
            tree[pos] = max(tree[pos << 1], tree[pos << 1 | 1]);
            pos >>= 1;
        }
    }

    int query(int l, int r) {
        int res = 0;
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
public:
    int bestTeamScore(vector<int>& scores, vector<int>& ages) {
        int n = scores.size();
        vector<pair<int, int>> pairs(n);
        for (int i = 0; i < n; i++) {
            pairs[i] = {scores[i], ages[i]};
        }
        sort(pairs.begin(), pairs.end());

        vector<int> dp(n);
        for (int i = 0; i < n; i++) {
            dp[i] = pairs[i].first;
        }

        set<int> uniqueAgesSet;
        for (auto& pair : pairs) {
            uniqueAgesSet.insert(pair.second);
        }
        vector<int> uniqueAges(uniqueAgesSet.begin(), uniqueAgesSet.end());
        map<int, int> ageId;
        for (int i = 0; i < uniqueAges.size(); i++) {
            ageId[uniqueAges[i]] = i;
        }

        SegmentTree segtree(uniqueAges.size());

        int res = 0;
        for (int i = 0; i < n; i++) {
            int mScore = pairs[i].first;
            int mAge = pairs[i].second;
            int idx = ageId[mAge];
            int j = segtree.query(0, idx);
            dp[i] = j + mScore;
            segtree.update(idx, dp[i]);
            res = max(res, dp[i]);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$
