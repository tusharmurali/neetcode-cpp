# 799. Champagne Tower

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/champagne-tower/>  
- **NeetCode:** <https://neetcode.io/problems/champagne-tower>  
- **Video:** <https://www.youtube.com/watch?v=LQ8TuG_QADM>  

[← Back to index](../INDEX.md)

## 1. Recursion

Each glass receives champagne from the two glasses directly above it (its "parents"). When a glass overflows, half of the excess spills to each child below. We can recursively compute how much champagne flows into any glass by summing the overflow from its two parent glasses. The base case is the top glass, which receives all the poured champagne.

```cpp
class Solution {
public:
    double champagneTower(int poured, int query_row, int query_glass) {
        return min(1.0, rec(poured, query_row, query_glass));
    }

private:
    double rec(int poured, int row, int glass) {
        if (row < 0 || glass < 0 || glass > row) {
            return 0;
        }

        if (row == 0 && glass == 0) {
            return poured;
        }

        double leftParent = max(0.0, rec(poured, row - 1, glass - 1) - 1);
        double rightParent = max(0.0, rec(poured, row - 1, glass) - 1);

        return (leftParent + rightParent) / 2;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$

> Where $n$ is the given $queryRow$.

## 2. Dynamic Programming (Top-Down)

The recursive solution recalculates the same glasses many times. By storing computed values in a memoization table, we avoid redundant work. Each glass only needs to be computed once since its inflow depends only on the glasses above it.

```cpp
class Solution {
public:
    double champagneTower(int poured, int query_row, int query_glass) {
        vector<vector<double>> memo(query_row + 5);
        for (int i = 0; i <= query_row + 4; i++) {
            memo[i].resize(i + 1, -1);
        }

        memo[0][0] = poured;
        return min(1.0, rec(memo, query_row, query_glass));
    }

private:
    double rec(vector<vector<double>>& memo, int row, int glass) {
        if (row < 0 || glass < 0 || glass > row) {
            return 0;
        }

        if (memo[row][glass] != -1) {
            return memo[row][glass];
        }

        double leftParent = max(0.0, rec(memo, row - 1, glass - 1) - 1);
        double rightParent = max(0.0, rec(memo, row - 1, glass) - 1);

        memo[row][glass] = (leftParent + rightParent) / 2;
        return memo[row][glass];
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n * m)$

> Where $n$ is the given $queryRow$ and $m$ is the given $queryGlass$.

## 3. Dynamic Programming (Bottom-Up)

Instead of working backwards from the query position, we can simulate the pouring process from top to bottom. We track how much champagne flows into each glass. When a glass overflows (has more than 1 unit), we distribute the excess equally to the two glasses below it.

```cpp
class Solution {
public:
    double champagneTower(int poured, int query_row, int query_glass) {
        vector<vector<double>> dp(query_row + 5);
        for (int i = 0; i <= query_row + 4; i++) {
            dp[i].resize(i + 1, 0);
        }

        dp[0][0] += poured;

        for (int row = 0; row < min(99, query_row + 1); row++) {
            for (int glass = 0; glass <= row; glass++) {
                double excess = (dp[row][glass] - 1.0) / 2.0;
                if (excess > 0) {
                    dp[row + 1][glass] += excess;
                    dp[row + 1][glass + 1] += excess;
                }
            }
        }

        return min(1.0, dp[query_row][query_glass]);
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n * m)$

> Where $n$ is the given $queryRow$ and $m$ is the given $queryGlass$.

## 4. Dynamic Programming (Space Optimized)

Since each row only depends on the row directly above it, we do not need to store the entire 2D table. We can use two 1D arrays: one for the previous row and one for the current row being computed. After processing each row, the current row becomes the previous row for the next iteration.

```cpp
class Solution {
public:
    double champagneTower(int poured, int query_row, int query_glass) {
        vector<double> prev_row = {double(poured)};  // Flow

        for (int row = 1; row <= query_row; row++) {
            vector<double> cur_row(row + 1, 0);
            for (int i = 0; i < row; i++) {
                double extra = prev_row[i] - 1;
                if (extra > 0) {
                    cur_row[i] += 0.5 * extra;
                    cur_row[i + 1] += 0.5 * extra;
                }
            }
            prev_row = cur_row;
        }

        return min(1.0, prev_row[query_glass]);
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n)$

> Where $n$ is the given $queryRow$ and $m$ is the given $queryGlass$.

## 5. Dynamic Programming (Optimal)

We can further optimize by using a single 1D array, processing from right to left within each row. This ensures we do not overwrite values we still need. Each position updates itself with half its excess, while contributing the other half to the next position.

```cpp
class Solution {
public:
    double champagneTower(int poured, int query_row, int query_glass) {
        vector<double> dp(query_row + 1, 0);
        dp[0] = poured;

        for (int row = 1; row <= query_row; row++) {
            for (int i = row - 1; i >= 0; i--) {
                double extra = dp[i] - 1;
                if (extra > 0) {
                    dp[i] = 0.5 * extra;
                    dp[i + 1] += 0.5 * extra;
                } else {
                    dp[i] = 0;
                }
            }
        }

        return min(1.0, dp[query_glass]);
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n)$

> Where $n$ is the given $queryRow$ and $m$ is the given $queryGlass$.
