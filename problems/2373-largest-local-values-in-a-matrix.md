# 2373. Largest Local Values in a Matrix

- **Difficulty:** Easy  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/largest-local-values-in-a-matrix/>  
- **NeetCode:** <https://neetcode.io/problems/largest-local-values-in-a-matrix>  
- **Video:** <https://www.youtube.com/watch?v=wdTRu9sarFA>  

[← Back to index](../INDEX.md)

## 1. Iteration

For each position in the output matrix, we need to find the maximum value in the corresponding 3x3 region of the input grid. The output matrix is (n-2) x (n-2) since we cannot center a 3x3 window on the edges. We simply iterate over all valid starting positions and scan the 3x3 window to find the maximum.

```cpp
class Solution {
public:
    vector<vector<int>> largestLocal(vector<vector<int>>& grid) {
        int N = grid.size();
        vector<vector<int>> res(N - 2, vector<int>(N - 2, 0));

        for (int i = 0; i < N - 2; i++) {
            for (int j = 0; j < N - 2; j++) {
                for (int r = i; r < i + 3; r++) {
                    for (int c = j; c < j + 3; c++) {
                        res[i][j] = max(res[i][j], grid[r][c]);
                    }
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n ^ 2)$ for the output array.

## 2. Generalized Approach (Sparse Table)

While the simple iteration works well for a fixed 3x3 window, a Sparse Table allows us to answer any rectangular range maximum query in O(1) time after O(n^2 log^2 n) preprocessing. This is overkill for this specific problem but demonstrates a generalized technique useful when the window size varies or when we need to answer many range queries efficiently.

```cpp
class SparseTable {
public:
    vector<vector<vector<vector<int>>>> sparseTable;
    vector<int> log;
    int n;

    SparseTable(vector<vector<int>>& grid) {
        n = grid.size();
        log.resize(n + 1, 0);
        for (int i = 2; i <= n; i++) {
            log[i] = log[i / 2] + 1;
        }

        int maxLog = log[n];
        sparseTable.resize(n, vector<vector<vector<int>>>(n, vector<vector<int>>(maxLog + 1, vector<int>(maxLog + 1))));

        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                sparseTable[r][c][0][0] = grid[r][c];
            }
        }

        for (int i = 0; i <= maxLog; i++) {
            for (int j = 0; j <= maxLog; j++) {
                for (int r = 0; r + (1 << i) <= n; r++) {
                    for (int c = 0; c + (1 << j) <= n; c++) {
                        if (i == 0 && j == 0) continue;
                        if (i == 0) {
                            sparseTable[r][c][i][j] = max(
                                sparseTable[r][c][i][j - 1],
                                sparseTable[r][c + (1 << (j - 1))][i][j - 1]
                            );
                        } else if (j == 0) {
                            sparseTable[r][c][i][j] = max(
                                sparseTable[r][c][i - 1][j],
                                sparseTable[r + (1 << (i - 1))][c][i - 1][j]
                            );
                        } else {
                            sparseTable[r][c][i][j] = max(
                                max(sparseTable[r][c][i - 1][j - 1], sparseTable[r + (1 << (i - 1))][c][i - 1][j - 1]),
                                max(sparseTable[r][c + (1 << (j - 1))][i - 1][j - 1],
                                    sparseTable[r + (1 << (i - 1))][c + (1 << (j - 1))][i - 1][j - 1])
                            );
                        }
                    }
                }
            }
        }
    }

    int query(int x1, int y1, int x2, int y2) {
        int lx = log[x2 - x1 + 1];
        int ly = log[y2 - y1 + 1];
        return max(
            max(sparseTable[x1][y1][lx][ly], sparseTable[x2 - (1 << lx) + 1][y1][lx][ly]),
            max(sparseTable[x1][y2 - (1 << ly) + 1][lx][ly],
                sparseTable[x2 - (1 << lx) + 1][y2 - (1 << ly) + 1][lx][ly])
        );
    }
};

class Solution {
public:
    vector<vector<int>> largestLocal(vector<vector<int>>& grid) {
        int n = grid.size(), k = 3;
        SparseTable st(grid);
        vector<vector<int>> res(n - k + 1, vector<int>(n - k + 1));

        for (int i = 0; i <= n - k; i++) {
            for (int j = 0; j <= n - k; j++) {
                res[i][j] = st.query(i, j, i + k - 1, j + k - 1);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 \log ^ 2 n)$
- Space complexity:
    - $O(n ^ 2 \log ^ 2 n)$ extra space.
    - $O((n - k) ^ 2)$ for the output matrix.

> Where $n$ is the size of the given square grid and $k$ is the fixed size of the submatrix window.
