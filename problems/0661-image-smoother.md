# 661. Image Smoother

- **Difficulty:** Easy  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/image-smoother/>  
- **NeetCode:** <https://neetcode.io/problems/image-smoother>  
- **Video:** <https://www.youtube.com/watch?v=xa83GG1RIOY>  

[← Back to index](../INDEX.md)

## 1. Iteration (Using Extra Matrix)

For each cell, we need to compute the average of all valid neighbors (including itself) within a 3x3 window.
We check all 9 potential neighbors, skip those outside the matrix bounds, sum the valid values, and divide by the count.
Since we need the original values to compute neighbors, we store results in a separate matrix.

```cpp
class Solution {
public:
    vector<vector<int>> imageSmoother(vector<vector<int>>& img) {
        int ROWS = img.size(), COLS = img[0].size();
        vector<vector<int>> res(ROWS, vector<int>(COLS, 0));

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                int total = 0, count = 0;
                for (int i = r - 1; i <= r + 1; i++) {
                    for (int j = c - 1; j <= c + 1; j++) {
                        if (i >= 0 && i < ROWS && j >= 0 && j < COLS) {
                            total += img[i][j];
                            count++;
                        }
                    }
                }
                res[r][c] = total / count;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n * m)$

> Where $n$ is the number of rows and $m$ is the number of columns of the matrix.

## 2. Iteration (Using Extra Row)

We can reduce space by only keeping track of the previous row's original values.
As we process row by row, we modify cells in place.
For neighbors in the current row, we use a copy saved before modification.
For the previous row, we use the saved copy.
For the next row, we use the original matrix values (not yet modified).

```cpp
class Solution {
public:
    vector<vector<int>> imageSmoother(vector<vector<int>>& img) {
        int ROWS = img.size(), COLS = img[0].size();
        vector<int> prevRow = img[0];

        for (int r = 0; r < ROWS; r++) {
            vector<int> currRow = img[r];

            for (int c = 0; c < COLS; c++) {
                int total = 0, count = 0;
                for (int i = max(0, r - 1); i < min(ROWS, r + 2); i++) {
                    for (int j = max(0, c - 1); j < min(COLS, c + 2); j++) {
                        if (i == r) {
                            total += currRow[j];
                        } else if (i == r - 1) {
                            total += prevRow[j];
                        } else {
                            total += img[i][j];
                        }
                        count++;
                    }
                }
                img[r][c] = total / count;
            }

            prevRow = currRow;
        }

        return img;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n)$ extra space.

> Where $n$ is the number of rows and $m$ is the number of columns of the matrix.

## 3. Iteration (Without Extra Space)

Since pixel values are at most 255, we can encode both the original value and the new average in a single integer.
We store the new average in the upper bits (by multiplying by 256) and keep the original in the lower bits.
During computation, we extract the original value using modulo 256.
After processing all cells, we extract the new values by dividing by 256.

```cpp
class Solution {
public:
    vector<vector<int>> imageSmoother(vector<vector<int>>& img) {
        int ROWS = img.size(), COLS = img[0].size();
        int LIMIT = 256;

        for (int r = 0; r < ROWS; ++r) {
            for (int c = 0; c < COLS; ++c) {
                int total = 0, count = 0;
                for (int i = max(0, r - 1); i < min(ROWS, r + 2); ++i) {
                    for (int j = max(0, c - 1); j < min(COLS, c + 2); ++j) {
                        total += img[i][j] % LIMIT;
                        count++;
                    }
                }
                img[r][c] += (total / count) * LIMIT;
            }
        }

        for (int r = 0; r < ROWS; ++r) {
            for (int c = 0; c < COLS; ++c) {
                img[r][c] /= LIMIT;
            }
        }

        return img;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(1)$ extra space.

> Where $n$ is the number of rows and $m$ is the number of columns of the matrix.

## 4. Bit Mask

This approach is similar to the previous one but uses bit manipulation instead of multiplication and division.
We use XOR and bit shifting to store the new average in the upper 8 bits.
The original value occupies the lower 8 bits (since values are 0 to 255).
This is slightly more efficient as bit operations are faster than arithmetic operations.

```cpp
class Solution {
public:
    vector<vector<int>> imageSmoother(vector<vector<int>>& img) {
        int ROWS = img.size(), COLS = img[0].size();

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                int total = 0, cnt = 0;
                for (int i = r - 1; i <= r + 1; i++) {
                    for (int j = c - 1; j <= c + 1; j++) {
                        if (i < 0 || i >= ROWS || j < 0 || j >= COLS) {
                            continue;
                        }
                        total += img[i][j] % 256;
                        cnt++;
                    }
                }
                img[r][c] ^= ((total / cnt) << 8);
            }
        }

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                img[r][c] >>= 8;
            }
        }
        return img;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(1)$ extra space.

> Where $n$ is the number of rows and $m$ is the number of columns of the matrix.
