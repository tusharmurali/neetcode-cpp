# 805. Split Array With Same Average

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/split-array-with-same-average/>  
- **NeetCode:** <https://neetcode.io/problems/split-array-with-same-average>  

[← Back to index](../INDEX.md)

## 1. Backtracking

We need to check if we can partition the array into two non-empty groups with equal averages. The naive approach is to try all possible ways to assign each element to group A or group B. For each complete assignment, we verify if both groups are non-empty and have the same average. Two groups have equal averages when `sum(A) * len(B) == sum(B) * len(A)`.

```cpp
class Solution {
public:
    bool splitArraySameAverage(vector<int>& nums) {
        vector<int> A, B;
        return backtrack(nums, 0, A, B);
    }

    bool backtrack(vector<int>& nums, int i, vector<int>& A, vector<int>& B) {
        if (i == nums.size()) {
            if (A.empty() || B.empty()) return false;
            int sumA = accumulate(A.begin(), A.end(), 0);
            int sumB = accumulate(B.begin(), B.end(), 0);
            return sumA * B.size() == sumB * A.size();
        }

        A.push_back(nums[i]);
        if (backtrack(nums, i + 1, A, B)) return true;
        A.pop_back();

        B.push_back(nums[i]);
        bool res = backtrack(nums, i + 1, A, B);
        B.pop_back();

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity: $O(n)$

## 2. Memoization (Brute Force)

The backtracking solution recomputes many states. We can track the state as `(index, size of A, sum of A)` since B is determined by what remains. If A has size `s` and sum `curSum`, then B has size `n - s` and sum `total - curSum`. We check the equal average condition at each step and memoize to avoid redundant work.

```cpp
class Solution {
public:
    bool splitArraySameAverage(vector<int>& nums) {
        int total = accumulate(nums.begin(), nums.end(), 0);
        int n = nums.size();
        unordered_map<string, bool> memo;

        function<bool(int, int, int)> dfs = [&](int i, int size, int currSum) {
            string key = to_string(i) + "," + to_string(size) + "," + to_string(currSum);
            if (memo.count(key)) return memo[key];

            if (size > 0 && size < n && currSum * (n - size) == (total - currSum) * size)
                return true;
            if (i == n) return false;

            if (dfs(i + 1, size + 1, currSum + nums[i]) || dfs(i + 1, size, currSum))
                return memo[key] = true;

            return memo[key] = false;
        };

        return dfs(0, 0, 0);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * s)$
- Space complexity: $O(n ^ 2 * s)$

> Where $n$ is the size of the input array $nums$, and $s$ is the sum of the elements of the array.

## 3. Memoization (Optimal)

For two groups to have the same average as the whole array, we need: `sum(A) / len(A) = total / n`. This means `sum(A) = len(A) * total / n`. We only need to find a subset `A` of size `a` (where `1 <= a <= n/2`) with sum exactly `a * total / n`. This sum must be an integer, so we only check sizes where `a * total` is divisible by `n`.

```cpp
class Solution {
public:
    bool splitArraySameAverage(vector<int>& nums) {
        int n = nums.size();
        int total = accumulate(nums.begin(), nums.end(), 0);

        // len(A) = a, len(B) = b, let a <= b
        // avg(A) = avg(B)
        // sum(A) / a = sum(B) / b = sum(nums) / n
        // sum(A) / a = avg => sum(A) = a * avg
        // sum(A) = a * sum(nums) / n
        // Find if any subset exists with a * sum(nums) / n
        // a is in the range [1, (n//2)]

        vector<vector<vector<int>>> memo(n + 1,
            vector<vector<int>>(n / 2 + 1, vector<int>(total + 1, -1)));

        function<bool(int, int, int)> dfs = [&](int i, int a, int s) -> bool {
            if (a == 0) return s == 0;
            if (i == n || s < 0 || a < 0) return false;
            if (memo[i][a][s] != -1) return memo[i][a][s];

            bool res = dfs(i + 1, a, s) || dfs(i + 1, a - 1, s - nums[i]);
            memo[i][a][s] = res;
            return res;
        };

        for (int a = 1; a <= n / 2; ++a) {
            if ((total * a) % n == 0) {
                int target = (total * a) / n;
                if (dfs(0, a, target)) return true;
            }
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * s)$
- Space complexity: $O(n ^ 2 * s)$

> Where $n$ is the size of the input array $nums$, and $s$ is the sum of the elements of the array.

## 4. Dynamic Programming (Bottom-Up)

We can build all achievable sums for each subset size using dynamic programming. For each element, we update what sums are achievable for each size. We iterate backwards through sizes to avoid using the same element twice. Finally, we check if any valid target sum exists for sizes 1 through n/2.

```cpp
class Solution {
public:
    bool splitArraySameAverage(vector<int>& nums) {
        int n = nums.size();

        // len(A) = a, len(B) = b, let a <= b
        // avg(A) = avg(B)
        // sum(A) / a = sum(B) / b = sum(nums) / n
        // sum(A) / a = avg => sum(A) = a * avg
        // sum(A) = a * sum(nums) / n
        // Find if any subset exists with a * sum(nums) / n
        // a is in the range [1, (n//2)]

        int total = accumulate(nums.begin(), nums.end(), 0);
        vector<unordered_set<int>> dp(n / 2 + 1);
        dp[0].insert(0);

        for (int num : nums) {
            for (int a = n / 2; a >= 1; a--) {
                for (int prev : dp[a - 1]) {
                    dp[a].insert(prev + num);
                }
            }
        }

        for (int a = 1; a <= n / 2; ++a) {
            if ((a * total) % n == 0 && dp[a].count((a * total) / n)) {
                return true;
            }
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * s)$
- Space complexity: $O(n ^ 2 * s)$

> Where $n$ is the size of the input array $nums$, and $s$ is the sum of the elements of the array.
