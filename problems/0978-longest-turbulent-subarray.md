# 978. Longest Turbulent Subarray

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/longest-turbulent-subarray/>  
- **NeetCode:** <https://neetcode.io/problems/longest-turbulent-subarray>  
- **Video:** <https://www.youtube.com/watch?v=V_iHUhR8Dek>  
- **Video approach:** 4. Sliding Window  

[← Back to index](../INDEX.md)

## 1. Brute Force

A turbulent subarray alternates between increasing and decreasing comparisons. For each starting index, we extend as far as possible while the comparison sign keeps flipping. If two adjacent elements are equal, the turbulent pattern breaks immediately. We track the maximum length found across all starting positions.

```cpp
class Solution {
public:
    int maxTurbulenceSize(vector<int>& arr) {
        int n = arr.size();
        int res = 1;

        for (int i = 0; i < n - 1; i++) {
            if (arr[i] == arr[i + 1]) continue;

            int sign = arr[i] > arr[i + 1] ? 1 : 0;
            int j = i + 1;

            while (j < n - 1) {
                if (arr[j] == arr[j + 1]) break;

                int curSign = arr[j] > arr[j + 1] ? 1 : 0;
                if (sign == curSign) break;

                sign = curSign;
                j++;
            }

            res = max(res, j - i + 1);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## 2. Dynamic Programming (Top-Down)

We can think of this problem recursively: from each position, we try to extend a turbulent subarray by checking if the next comparison matches the expected direction. If we expect a decrease and find one, we flip the expectation and recurse. Memoization prevents redundant calculations by caching results for each `(index, expected sign)` pair.

```cpp
class Solution {
    vector<vector<int>> memo;

public:
    int maxTurbulenceSize(vector<int>& arr) {
        int n = arr.size();
        memo.assign(n, vector<int>(2, -1));

        int maxLen = 1;
        for (int i = 0; i < n; i++) {
            maxLen = max(maxLen, dfs(i, true, arr));
            maxLen = max(maxLen, dfs(i, false, arr));
        }

        return maxLen;
    }

    int dfs(int i, bool sign, vector<int>& arr) {
        int signIndex = sign ? 1 : 0;
        if (i == arr.size() - 1) return 1;
        if (memo[i][signIndex] != -1) {
            return memo[i][signIndex];
        }

        int res = 1;
        if ((sign && arr[i] > arr[i + 1]) ||
            (!sign && arr[i] < arr[i + 1])) {
            res = 1 + dfs(i + 1, !sign, arr);
        }

        memo[i][signIndex] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

Instead of recursion, we build the solution iteratively. At each position, we track two values: the length of the turbulent subarray ending here with an increasing comparison, and the length ending with a decreasing comparison. When we see an increase, we extend the previous decreasing sequence (and vice versa), since turbulence requires alternation.

```cpp
class Solution {
public:
    int maxTurbulenceSize(vector<int>& arr) {
        int n = arr.size();
        if (n == 1) return 1;

        vector<vector<int>> dp(n, vector<int>(2, 1));
        int maxLen = 1;

        for (int i = 1; i < n; ++i) {
            if (arr[i] > arr[i - 1]) {
                dp[i][1] = dp[i - 1][0] + 1;
            } else if (arr[i] < arr[i - 1]) {
                dp[i][0] = dp[i - 1][1] + 1;
            }
            maxLen = max(maxLen, max(dp[i][0], dp[i][1]));
        }

        return maxLen;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Sliding Window ▶ video

We maintain a window that represents a valid turbulent subarray. As we move the `right` pointer, we check if the current comparison alternates from the previous one. If it does, we extend the window. If not (or if elements are equal), we shrink the window by moving the `left` pointer to start fresh from the breaking point.

```cpp
class Solution {
public:
    int maxTurbulenceSize(vector<int>& arr) {
        int l = 0, r = 1, res = 1;
        string prev = "";

        while (r < arr.size()) {
            if (arr[r - 1] > arr[r] && prev != ">") {
                res = max(res, r - l + 1);
                r++;
                prev = ">";
            } else if (arr[r - 1] < arr[r] && prev != "<") {
                res = max(res, r - l + 1);
                r++;
                prev = "<";
            } else {
                r = (arr[r] == arr[r - 1]) ? r + 1 : r;
                l = r - 1;
                prev = "";
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 5. Iteration

We can simplify the sliding window approach by just counting consecutive valid comparisons. We track the current count of alternating comparisons. When we see a comparison that properly alternates from the previous one, we increment the count. Otherwise, we reset to `1` (or `0` if elements are equal). The final answer is the maximum count plus one.

```cpp
class Solution {
public:
    int maxTurbulenceSize(vector<int>& arr) {
        int n = arr.size();
        int res = 0, cnt = 0, sign = -1;

        for (int i = 0; i < n - 1; i++) {
            if (arr[i] > arr[i + 1]) {
                cnt = (sign == 0) ? cnt + 1 : 1;
                sign = 1;
            } else if (arr[i] < arr[i + 1]) {
                cnt = (sign == 1) ? cnt + 1 : 1;
                sign = 0;
            } else {
                cnt = 0;
                sign = -1;
            }

            res = max(res, cnt);
        }

        return res + 1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
