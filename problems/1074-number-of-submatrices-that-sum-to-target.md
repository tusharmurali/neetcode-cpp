# 1074. Number of Submatrices that Sum to Target

- **Difficulty:** Hard  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-submatrices-that-sum-to-target/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-submatrices-that-sum-to-target>  
- **Video:** <https://www.youtube.com/watch?v=43DRBP2DUHg>  
- **Video approach:** 3. Horizontal 1D Prefix Sum (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Brute Force

We consider every possible submatrix by fixing all four corners (top-left and bottom-right). For each submatrix, we sum all its elements and check if it equals the target. This is the most straightforward approach but very slow.

```cpp
class Solution {
public:
    int numSubmatrixSumTarget(vector<vector<int>>& matrix, int target) {
        int ROWS = matrix.size(), COLS = matrix[0].size();
        int res = 0;

        for (int r1 = 0; r1 < ROWS; r1++) {
            for (int r2 = r1; r2 < ROWS; r2++) {
                for (int c1 = 0; c1 < COLS; c1++) {
                    for (int c2 = c1; c2 < COLS; c2++) {
                        int subSum = 0;
                        for (int r = r1; r <= r2; r++) {
                            for (int c = c1; c <= c2; c++) {
                                subSum += matrix[r][c];
                            }
                        }
                        if (subSum == target) {
                            res++;
                        }
                    }
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m ^ 3 * n ^ 3)$
- Space complexity: $O(1)$ extra space.

> Where $m$ is the number of rows and $n$ is the number of columns of the given matrix.

## 2. Two Dimensional Prefix Sum

By precomputing a 2D prefix sum, any submatrix sum can be calculated in `O(1)` using inclusion-exclusion. We still enumerate all submatrix boundaries, but computing each sum is now constant time instead of proportional to the submatrix size.

```cpp
class Solution {
public:
    int numSubmatrixSumTarget(vector<vector<int>>& matrix, int target) {
        int ROWS = matrix.size(), COLS = matrix[0].size();
        vector<vector<int>> subSum(ROWS, vector<int>(COLS, 0));

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                int top = (r > 0) ? subSum[r - 1][c] : 0;
                int left = (c > 0) ? subSum[r][c - 1] : 0;
                int topLeft = (min(r, c) > 0) ? subSum[r - 1][c - 1] : 0;
                subSum[r][c] = matrix[r][c] + top + left - topLeft;
            }
        }

        int res = 0;
        for (int r1 = 0; r1 < ROWS; r1++) {
            for (int r2 = r1; r2 < ROWS; r2++) {
                for (int c1 = 0; c1 < COLS; c1++) {
                    for (int c2 = c1; c2 < COLS; c2++) {
                        int top = (r1 > 0) ? subSum[r1 - 1][c2] : 0;
                        int left = (c1 > 0) ? subSum[r2][c1 - 1] : 0;
                        int topLeft = (min(r1, c1) > 0) ? subSum[r1 - 1][c1 - 1] : 0;
                        int curSum = subSum[r2][c2] - top - left + topLeft;
                        if (curSum == target) {
                            res++;
                        }
                    }
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m ^ 2 * n ^ 2)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns of the given matrix.

## 3. Horizontal 1D Prefix Sum ▶ video

We reduce the 2D problem to multiple 1D subarray sum problems. After fixing a row range `(r1 to r2)`, the submatrix sum becomes a horizontal prefix sum across columns. We apply the classic technique of using a hash map to count how many previous prefix sums differ by exactly the target.

```cpp
class Solution {
public:
    int numSubmatrixSumTarget(vector<vector<int>>& matrix, int target) {
        int ROWS = matrix.size(), COLS = matrix[0].size();
        vector<vector<int>> subSum(ROWS, vector<int>(COLS, 0));

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                int top = (r > 0) ? subSum[r - 1][c] : 0;
                int left = (c > 0) ? subSum[r][c - 1] : 0;
                int topLeft = (min(r, c) > 0) ? subSum[r - 1][c - 1] : 0;
                subSum[r][c] = matrix[r][c] + top + left - topLeft;
            }
        }

        int res = 0;
        for (int r1 = 0; r1 < ROWS; r1++) {
            for (int r2 = r1; r2 < ROWS; r2++) {
                unordered_map<int, int> count;
                count[0] = 1;
                for (int c = 0; c < COLS; c++) {
                    int curSum = subSum[r2][c] - (r1 > 0 ? subSum[r1 - 1][c] : 0);
                    res += count[curSum - target];
                    count[curSum]++;
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m ^ 2 * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns of the given matrix.

## 4. Vertical 1D Prefix Sum

Similar to the horizontal approach, but we fix column bounds instead of row bounds. For each pair of columns `(c1 to c2)`, we maintain a running row sum and apply the hash map technique vertically. This can be more efficient when there are fewer columns than rows.

```cpp
class Solution {
public:
    int numSubmatrixSumTarget(vector<vector<int>>& matrix, int target) {
        int ROWS = matrix.size(), COLS = matrix[0].size(), res = 0;

        for (int c1 = 0; c1 < COLS; c1++) {
            vector<int> rowPrefix(ROWS, 0);
            for (int c2 = c1; c2 < COLS; c2++) {
                for (int r = 0; r < ROWS; r++) {
                    rowPrefix[r] += matrix[r][c2];
                }

                unordered_map<int, int> count;
                count[0] = 1;
                int curSum = 0;
                for (int r = 0; r < ROWS; r++) {
                    curSum += rowPrefix[r];
                    res += count[curSum - target];
                    count[curSum]++;
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n ^ 2)$
- Space complexity: $O(m)$

> Where $m$ is the number of rows and $n$ is the number of columns of the given matrix.
