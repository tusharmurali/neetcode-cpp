# 120. Triangle

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/triangle/>  
- **NeetCode:** <https://neetcode.io/problems/triangle>  
- **Video:** <https://www.youtube.com/watch?v=OM1MTokvxs4>  

[← Back to index](../INDEX.md)

## 1. Recursion

Starting from the top of the triangle, at each position we can move either directly down or diagonally down-right. We want to find the path from top to bottom with the minimum sum.

This naturally leads to a recursive approach: from position `(row, col)`, we add the current value and recurse to both possible next positions, taking the minimum result. The base case is reaching past the bottom row, where we return `0`.

```cpp
class Solution {
public:
    int minimumTotal(vector<vector<int>>& triangle) {
        return dfs(0, 0, triangle);
    }

private:
    int dfs(int row, int col, vector<vector<int>>& triangle) {
        if (row >= triangle.size()) {
            return 0;
        }
        return triangle[row][col] + min(dfs(row + 1, col, triangle), dfs(row + 1, col + 1, triangle));
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Dynamic Programming (Top-Down)

The recursive solution recomputes the same subproblems many times. For example, position `(2, 1)` might be reached from both `(1, 0)` and `(1, 1)`. We can use memoization to store results once computed.

By caching the minimum path sum from each position, we ensure each subproblem is solved only once. This transforms the exponential time complexity into polynomial.

```cpp
class Solution {
public:
    int minimumTotal(vector<vector<int>>& triangle) {
        vector<vector<int>> memo(triangle.size(), vector<int>(0));
        int INF = INT_MAX;
        for (int r = 0; r < triangle.size(); ++r) {
            memo[r].resize(triangle[r].size(), INF);
        }

        return dfs(0, 0, triangle, memo);
    }

private:
    int dfs(int row, int col, vector<vector<int>>& triangle, vector<vector<int>>& memo) {
        if (row >= triangle.size()) {
            return 0;
        }
        if (memo[row][col] != INT_MAX) {
            return memo[row][col];
        }

        memo[row][col] = triangle[row][col] + min(dfs(row + 1, col, triangle, memo), dfs(row + 1, col + 1, triangle, memo));
        return memo[row][col];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Dynamic Programming (Bottom-Up)

Instead of recursing from top to bottom, we can build the solution from the bottom up. Starting from the last row (where the values are the path sums themselves), we work upward. At each cell, we add the minimum of the two cells below it.

This eliminates recursion overhead and naturally fills the `dp` table in the correct order. By the time we reach the top, `dp[0][0]` contains the minimum path sum.

```cpp
class Solution {
public:
    int minimumTotal(vector<vector<int>>& triangle) {
        int n = triangle.size();
        vector<vector<int>> dp(n, vector<int>(n, 0));
        for (int col = 0; col < triangle[n - 1].size(); ++col) {
            dp[n - 1][col] = triangle[n - 1][col];
        }

        for (int row = n - 2; row >= 0; --row) {
            for (int col = 0; col < triangle[row].size(); ++col) {
                dp[row][col] = triangle[row][col] + min(dp[row + 1][col], dp[row + 1][col + 1]);
            }
        }

        return dp[0][0];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 4. Dynamic Programming (Space Optimized) - I

When building top-down, we only need the previous row to compute the current row. We can use a single array that grows as we move down the triangle, updating values as we go.

The tricky part is handling the edges correctly. The leftmost element of each row can only come from the leftmost element above. The rightmost can only come from the rightmost above. Middle elements take the minimum of their two parents.

```cpp
class Solution {
public:
    int minimumTotal(vector<vector<int>>& triangle) {
        int n = triangle.size();
        vector<int> dp = triangle[0];

        for (int row = 1; row < n; row++) {
            vector<int> nxtDp(row + 1, 0);
            nxtDp[0] = dp[0] + triangle[row][0];
            for (int col = 1; col < row; col++) {
                nxtDp[col] = triangle[row][col] + min(dp[col], dp[col - 1]);
            }
            nxtDp[row] = dp[row - 1] + triangle[row][row];
            dp = nxtDp;
        }

        return *min_element(dp.begin(), dp.end());
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$ extra space.

## 5. Dynamic Programming (Space Optimized) - II

Working bottom-up with space optimization is cleaner because we process elements left to right, and each cell only depends on cells to its right in the row below. This means we can safely overwrite values as we go without corrupting data we still need.

We start with the bottom row and repeatedly update each position with the minimum path sum from that point down. The final answer ends up in `dp[0]`.

```cpp
class Solution {
public:
    int minimumTotal(vector<vector<int>>& triangle) {
        int n = triangle.size();
        vector<int> dp(triangle.back());

        for (int row = n - 2; row >= 0; --row) {
            for (int col = 0; col < triangle[row].size(); ++col) {
                dp[col] = triangle[row][col] + min(dp[col], dp[col + 1]);
            }
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$ extra space.

## 6. Dynamic Programming (In-Place)

If we are allowed to modify the input triangle, we can skip creating a separate DP array entirely. We use the triangle itself to store intermediate results, applying the same bottom-up logic.

This approach uses constant extra space but modifies the input data. Each cell in the triangle gets replaced with the minimum path sum from that cell to the bottom.

```cpp
class Solution {
public:
    int minimumTotal(vector<vector<int>>& triangle) {
        for (int row = triangle.size() - 2; row >= 0; row--) {
            for (int col = 0; col < triangle[row].size(); col++) {
                triangle[row][col] += min(triangle[row + 1][col], triangle[row + 1][col + 1]);
            }
        }
        return triangle[0][0];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## Standalone solution file (`cpp/0120-triangle.cpp` in the NeetCode repo)

```cpp
class Solution{    
    public:    
        int minimumTotal(vector<vector<int>>& triangle){            
            for(int i = 0; i < triangle.size() - 1; i++){                
                for(int k = 0; k < triangle[i + 1].size(); k++){                    
                    if(k == 0){                        
                        triangle[i + 1][0] = triangle[i + 1][0] + triangle[i][0];                    
                    }
                    else{                        
                        if(k == triangle[i + 1].size() - 1){                           
                            triangle[i + 1][k] = triangle[i + 1][k] + triangle[i][k - 1];                           
                        }
                        else{                            
                            triangle[i + 1][k] = triangle[i + 1][k] + min(triangle[i][k - 1], triangle[i][k]);                            
                        }                       
                    }                    
                }                
            }            
            return *min_element(triangle[triangle.size() - 1].begin(), triangle[triangle.size() - 1].end());        
        }    
};
```
