# 265. Paint House II

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/paint-house-ii/>  
- **NeetCode:** <https://neetcode.io/problems/paint-house-ii>  

[← Back to index](../INDEX.md)

## 1. Memoization

This is a generalization of the Paint House problem where we now have `k` colors instead of just 3. The core constraint remains the same: no two adjacent houses can have the same color.

We recursively try each valid color for the current house and find the minimum cost to paint all remaining houses. Since the same subproblems are solved multiple times, we use memoization to cache results.

```cpp
class Solution {
private:
    int n, k;
    vector<vector<int>> costs;
    unordered_map<string, int> memo;

    int memoSolve(int houseNumber, int color) {
        if (houseNumber == n - 1) {
            return costs[houseNumber][color];
        }

        string key = to_string(houseNumber) + " " + to_string(color);
        if (memo.find(key) != memo.end()) {
            return memo[key];
        }

        int minRemainingCost = INT_MAX;
        for (int nextColor = 0; nextColor < k; nextColor++) {
            if (color == nextColor) continue;
            int currentRemainingCost = memoSolve(houseNumber + 1, nextColor);
            minRemainingCost = min(currentRemainingCost, minRemainingCost);
        }
        int totalCost = costs[houseNumber][color] + minRemainingCost;
        memo[key] = totalCost;
        return totalCost;
    }

public:
    int minCostII(vector<vector<int>>& costs) {
        if (costs.empty()) return 0;
        this->costs = costs;
        n = costs.size();
        k = costs[0].size();

        int minCost = INT_MAX;
        for (int color = 0; color < k; color++) {
            minCost = min(minCost, memoSolve(0, color));
        }
        return minCost;
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot k^2)$

- Space complexity: $O(n \cdot k)$

> Where $n$ is the number of houses in a row, and $k$ is the number of colors available for painting.

## 2. Dynamic Programming

We can solve this iteratively by building up the minimum costs house by house. For each house and each color, we need the minimum cost from the previous house excluding that same color.

The straightforward approach checks all `k` colors from the previous row to find the minimum, giving O(k) work per cell and O(n \* k^2) overall.

```cpp
class Solution {
public:
    int minCostII(vector<vector<int>>& costs) {
        if (costs.empty()) return 0;
        int k = costs[0].size();
        int n = costs.size();

        for (int house = 1; house < n; house++) {
            for (int color = 0; color < k; color++) {
                int minCost = INT_MAX;
                for (int previousColor = 0; previousColor < k; previousColor++) {
                    if (color == previousColor) continue;
                    minCost = min(minCost, costs[house - 1][previousColor]);
                }
                costs[house][color] += minCost;
            }
        }

        int minVal = INT_MAX;
        for (int c : costs[n - 1]) {
            minVal = min(minVal, c);
        }
        return minVal;
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot k^2)$

- Space complexity: $O(1)$ if done in-place, $O(n \cdot k)$ if input is copied.

> Where $n$ is the number of houses in a row, and $k$ is the number of colors available for painting.

## 3. Dynamic Programming with O(k) additional Space

The previous solution modifies the input array. If we want to preserve it, we can use a separate array of size `k` to track the costs from the previous row.

This approach maintains the same logic but uses an auxiliary array instead of modifying the input directly.

```cpp
class Solution {
public:
    int minCostII(vector<vector<int>>& costs) {
        if (costs.empty()) return 0;
        int k = costs[0].size();
        int n = costs.size();

        vector<int> previousRow = costs[0];

        for (int house = 1; house < n; house++) {
            vector<int> currentRow(k, 0);
            for (int color = 0; color < k; color++) {
                int minCost = INT_MAX;
                for (int previousColor = 0; previousColor < k; previousColor++) {
                    if (color == previousColor) continue;
                    minCost = min(minCost, previousRow[previousColor]);
                }
                currentRow[color] = costs[house][color] + minCost;
            }
            previousRow = currentRow;
        }

        int minVal = INT_MAX;
        for (int c : previousRow) {
            minVal = min(minVal, c);
        }
        return minVal;
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot k^2)$

- Space complexity: $O(k)$

> Where $n$ is the number of houses in a row, and $k$ is the number of colors available for painting.

## 4. Dynamic programming with Optimized Time

The O(k^2) time per house comes from finding the minimum in the previous row for each color. But notice: for all colors except one, we just need the global minimum of the previous row. The exception is when the current color matches the minimum color from the previous row, in which case we need the second minimum.

By precomputing the minimum and second minimum colors from each row, we can update each cell in O(1) time, reducing the overall complexity to O(n \* k).

```cpp
class Solution {
public:
    int minCostII(vector<vector<int>>& costs) {
        if (costs.size() == 0) return 0;

        int k = costs[0].size();
        int n = costs.size();

        for (int house = 1; house < n; house++) {
            // Find the minimum and second minimum color in the PREVIOUS row.
            int minColor = -1;
            int secondMinColor = -1;

            for (int color = 0; color < k; color++) {
                int cost = costs[house - 1][color];

                if (minColor == -1 || cost < costs[house - 1][minColor]) {
                    secondMinColor = minColor;
                    minColor = color;
                } else if (secondMinColor == -1 || cost < costs[house - 1][secondMinColor]) {
                    secondMinColor = color;
                }
            }

            // And now calculate the new costs for the current row.
            for (int color = 0; color < k; color++) {
                if (color == minColor) {
                    costs[house][color] += costs[house - 1][secondMinColor];
                } else {
                    costs[house][color] += costs[house - 1][minColor];
                }
            }
        }

        // Find the minimum in the last row.
        int min = INT_MAX;
        for (int c : costs[n - 1]) {
            min = std::min(min, c);
        }

        return min;
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot k)$

- Space complexity: $O(1)$

> Where $n$ is the number of houses in a row, and $k$ is the number of colors available for painting.

## 5. Dynamic programming with Optimized Time and Space

Building on the previous optimization, we realize we do not actually need to store the entire previous row. We only need three pieces of information: the minimum cost, the second minimum cost, and which color achieved the minimum.

By tracking just these three values as we process each house, we can compute everything in O(1) space while maintaining O(n \* k) time complexity.

```cpp
class Solution {
public:
    int minCostII(vector<vector<int>>& costs) {
        if (costs.empty()) return 0;
        int k = costs[0].size();
        int n = costs.size();

        int prevMin = -1, prevSecondMin = -1, prevMinColor = -1;
        for (int color = 0; color < k; color++) {
            int cost = costs[0][color];
            if (prevMin == -1 || cost < prevMin) {
                prevSecondMin = prevMin;
                prevMinColor = color;
                prevMin = cost;
            } else if (prevSecondMin == -1 || cost < prevSecondMin) {
                prevSecondMin = cost;
            }
        }

        for (int house = 1; house < n; house++) {
            int minCost = -1, secondMin = -1, minColor = -1;
            for (int color = 0; color < k; color++) {
                int cost = costs[house][color];
                if (color == prevMinColor) {
                    cost += prevSecondMin;
                } else {
                    cost += prevMin;
                }
                if (minCost == -1 || cost < minCost) {
                    secondMin = minCost;
                    minColor = color;
                    minCost = cost;
                } else if (secondMin == -1 || cost < secondMin) {
                    secondMin = cost;
                }
            }
            prevMin = minCost;
            prevSecondMin = secondMin;
            prevMinColor = minColor;
        }

        return prevMin;
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot k)$

- Space complexity: $O(1)$

> Where $n$ is the number of houses in a row, and $k$ is the number of colors available for painting.
