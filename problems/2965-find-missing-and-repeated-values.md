# 2965. Find Missing and Repeated Values

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-missing-and-repeated-values/>  
- **NeetCode:** <https://neetcode.io/problems/find-missing-and-repeated-values>  
- **Video:** <https://www.youtube.com/watch?v=LQGmWiDuTw8>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The grid contains numbers from `1` to `n*n`, but one number appears twice (repeated) and one is missing. The simplest approach is to check each number individually by scanning the entire grid for every possible value. For each number from `1` to `n*n`, we count how many times it appears. If a number appears twice, it is the repeated value. If it appears zero times, it is the missing value.

```cpp
class Solution {
public:
    vector<int> findMissingAndRepeatedValues(vector<vector<int>>& grid) {
        int n = grid.size();
        int doubleVal = 0, missing = 0;

        for (int num = 1; num <= n * n; num++) {
            int cnt = 0;
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    if (grid[i][j] == num) {
                        cnt++;
                    }
                }
            }

            if (cnt == 2) {
                doubleVal = num;
            } else if (cnt == 0) {
                missing = num;
            }
        }

        return {doubleVal, missing};
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 4)$
- Space complexity: $O(1)$

## 2. Hash Map

Instead of rescanning the grid for every number, we can count all occurrences in a single pass using a hash map. First, we iterate through the grid once and record how many times each value appears. Then, we check each number from `1` to `n*n` in the map: a frequency of `2` indicates the repeated number, and a frequency of `0` indicates the missing number.

```cpp
class Solution {
public:
    vector<int> findMissingAndRepeatedValues(vector<vector<int>>& grid) {
        int N = grid.size();
        unordered_map<int, int> count;

        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                count[grid[i][j]]++;
            }
        }

        int doubleVal = 0, missing = 0;

        for (int num = 1; num <= N * N; num++) {
            int freq = count[num];
            if (freq == 0) missing = num;
            if (freq == 2) doubleVal = num;
        }

        return {doubleVal, missing};
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Hash Set

A hash set can detect duplicates efficiently. As we scan the grid, we add each number to a set. If we try to add a number that already exists in the set, we have found the repeated value. After processing the grid, we iterate from `1` to `n*n` and check which number is not in the set; that is the missing value.

```cpp
class Solution {
public:
    vector<int> findMissingAndRepeatedValues(vector<vector<int>>& grid) {
        int N = grid.size();
        unordered_set<int> seen;
        int doubleVal = 0, missing = 0;

        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                if (seen.count(grid[i][j])) {
                    doubleVal = grid[i][j];
                }
                seen.insert(grid[i][j]);
            }
        }

        for (int num = 1; num <= N * N; num++) {
            if (!seen.count(num)) {
                missing = num;
                break;
            }
        }

        return {doubleVal, missing};
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 4. Math

We can solve this without extra data structures using mathematical formulas. Let `a` be the repeated number and `b` be the missing number. The sum of the grid differs from the expected sum (`1 + 2 + ... + n*n`) by exactly `a - b`. Similarly, the sum of squares differs by `a^2 - b^2`. From these two equations, we can derive `a + b` (since `a^2 - b^2 = (a - b)(a + b)`), and then solve for both values.

```cpp
class Solution {
public:
    vector<int> findMissingAndRepeatedValues(vector<vector<int>>& grid) {
        int N = grid.size();
        long long gridSum = 0;
        long long gridSqSum = 0;

        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                gridSum += grid[i][j];
                gridSqSum += 1LL * grid[i][j] * grid[i][j];
            }
        }

        long long totSum = 1LL * N * N * (N * N + 1) / 2;
        long long diff = gridSum - totSum; // a - b

        long long totSqSum = 1LL * N * N * (N * N + 1) * (2 * N * N + 1) / 6;
        long long sqDiff = gridSqSum - totSqSum; // (a^2) - (b^2)

        long long sum = sqDiff / diff; // a + b

        int a = (sum + diff) / 2;
        int b = sum - a;

        return {a, b};
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$
