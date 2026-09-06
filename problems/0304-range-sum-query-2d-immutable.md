# 304. Range Sum Query 2D Immutable

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/range-sum-query-2d-immutable/>  
- **NeetCode:** <https://neetcode.io/problems/range-sum-query-2d-immutable>  
- **Video:** <https://www.youtube.com/watch?v=KE8MQuwE2yA>  
- **Video approach:** 3. Two Dimensional Prefix Sum  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most straightforward approach is to iterate through every cell in the specified rectangular region and sum up all the values. For each query, we simply loop from the top-left corner to the bottom-right corner and accumulate the result. While this is easy to implement, it becomes slow when we have many queries or large regions to sum.

```cpp
class NumMatrix {
private:
    vector<vector<int>> matrix;

public:
    NumMatrix(vector<vector<int>>& matrix) {
        this->matrix = matrix;
    }

    int sumRegion(int row1, int col1, int row2, int col2) {
        int res = 0;
        for (int r = row1; r <= row2; r++) {
            for (int c = col1; c <= col2; c++) {
                res += matrix[r][c];
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$ for each query.
- Space complexity: $O(1)$

> Where $m$ is the number of rows and $n$ is the number of columns in the matrix.

## 2. One Dimensional Prefix Sum

Instead of summing every cell for each query, we can precompute prefix sums for each row. Each `prefixSum[row][col]` stores the sum of all elements from `matrix[row][0]` to `matrix[row][col]`. This way, finding the sum of any range within a single row takes constant time. For a rectangular region spanning multiple rows, we sum each row's contribution using its prefix sum.

```cpp
class NumMatrix {
private:
    vector<vector<int>> prefixSum;

public:
    NumMatrix(vector<vector<int>>& matrix) {
        int rows = matrix.size(), cols = matrix[0].size();
        prefixSum = vector<vector<int>>(rows, vector<int>(cols, 0));

        for (int row = 0; row < rows; row++) {
            prefixSum[row][0] = matrix[row][0];
            for (int col = 1; col < cols; col++) {
                prefixSum[row][col] = prefixSum[row][col - 1] + matrix[row][col];
            }
        }
    }

    int sumRegion(int row1, int col1, int row2, int col2) {
        int res = 0;
        for (int row = row1; row <= row2; row++) {
            if (col1 > 0) {
                res += prefixSum[row][col2] - prefixSum[row][col1 - 1];
            } else {
                res += prefixSum[row][col2];
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the matrix.

## 3. Two Dimensional Prefix Sum ▶ video

We can extend prefix sums to two dimensions. The idea is to precompute `sumMat[r][c]` as the sum of all elements in the rectangle from `(0, 0)` to `(r - 1, c - 1)`. To find the sum of any rectangular region, we use the inclusion-exclusion principle: take the sum up to the bottom-right corner, subtract the regions above and to the left, then add back the top-left corner (which was subtracted twice).

```cpp
class NumMatrix {
private:
    vector<vector<int>> sumMat;

public:
    NumMatrix(vector<vector<int>>& matrix) {
        int ROWS = matrix.size(), COLS = matrix[0].size();
        sumMat = vector<vector<int>>(ROWS + 1, vector<int>(COLS + 1, 0));

        for (int r = 0; r < ROWS; r++) {
            int prefix = 0;
            for (int c = 0; c < COLS; c++) {
                prefix += matrix[r][c];
                int above = sumMat[r][c + 1];
                sumMat[r + 1][c + 1] = prefix + above;
            }
        }
    }

    int sumRegion(int row1, int col1, int row2, int col2) {
        row1++; col1++; row2++; col2++;
        int bottomRight = sumMat[row2][col2];
        int above = sumMat[row1 - 1][col2];
        int left = sumMat[row2][col1 - 1];
        int topLeft = sumMat[row1 - 1][col1 - 1];
        return bottomRight - above - left + topLeft;
    }
};
```

**Complexity**

- Time complexity: $O(1)$ for each query.
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the matrix.

## Standalone solution file (`cpp/0304-range-sum-query-2d-immutable.cpp` in the NeetCode repo)

```cpp
class NumMatrix {
public:

    vector<vector<int>> dp;

    NumMatrix(vector<vector<int>>& matrix) {
        int r = matrix.size(),c = matrix[0].size();
        dp = matrix;

        for(int i =0;i<r;i++){
            for(int j =0;j<c;j++){
                if(i>0) dp[i][j] += dp[i-1][j]; // add prev row
                if(j>0) dp[i][j] += dp[i][j-1]; // add prev col

                // remove diagonal as it is added twice above
                if(i>0&&j>0) dp[i][j] -= dp[i-1][j-1];
            }
        }
    }
    
    int sumRegion(int row1, int col1, int row2, int col2) {
        int answer = dp[row2][col2];

        if(row1>0) answer -= dp[row1-1][col2];  // remove prev row on col1
        if(col1>0) answer -= dp[row2][col1-1]; // remo prev col on row2

        // add prev diagonal as pre row and prev col both contains that value
        if(row1>0&&col1>0) answer += dp[row1-1][col1-1];
        return answer;
    }
};

/**
 * Your NumMatrix object will be instantiated and called as such:
 * NumMatrix* obj = new NumMatrix(matrix);
 * int param_1 = obj->sumRegion(row1,col1,row2,col2);
 */
```
