# 1524. Number of Sub-arrays With Odd Sum

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-sub-arrays-with-odd-sum/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-sub-arrays-with-odd-sum>  
- **Video:** <https://www.youtube.com/watch?v=AIlI-24oC6Q>  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each possible subarray, compute its sum and check if it is odd. We try every starting index and extend to every possible ending index, accumulating the sum incrementally.

```cpp
class Solution {
public:
    int numOfSubarrays(vector<int>& arr) {
        int n = arr.size(), res = 0;
        int mod = 1e9 + 7;

        for (int i = 0; i < n; i++) {
            int curSum = 0;
            for (int j = i; j < n; j++) {
                curSum += arr[j];
                if (curSum % 2 != 0) {
                    res = (res + 1) % mod;
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Dynamic Programming (Top-Down)

We use memoization to count subarrays ending at each position. For a subarray starting at index `i`, the parity of its sum depends on the running parity as we extend rightward. By caching results for each `(index, parity)` state, we avoid redundant calculations.

```cpp
class Solution {
public:
    int mod = 1e9 + 7;
    vector<vector<int>> memo;
    vector<int> arr;

    int numOfSubarrays(vector<int>& arr) {
        this->arr = arr;
        int n = arr.size();
        memo.assign(n, vector<int>(2, -1));

        int res = 0;
        for (int i = 0; i < n; i++) {
            res = (res + dp(i, 0)) % mod;
        }
        return res;
    }

    int dp(int i, int parity) {
        if (i == arr.size()) return 0;
        if (memo[i][parity] != -1) return memo[i][parity];

        int newParity = (parity + arr[i]) % 2;
        int res = newParity + dp(i + 1, newParity);
        return memo[i][parity] = res % mod;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

We can convert the top-down approach to bottom-up by processing indices from right to left. For each position, we compute how many odd-sum subarrays can be formed starting there, given either even or odd running parity.

```cpp
class Solution {
public:
    int numOfSubarrays(vector<int>& arr) {
        int n = arr.size(), mod = 1e9 + 7;
        vector<vector<int>> dp(n + 1, vector<int>(2, 0));

        for (int i = n - 1; i >= 0; i--) {
            for (int parity = 0; parity <= 1; parity++) {
                int newParity = (parity + arr[i]) % 2;
                dp[i][parity] = (newParity + dp[i + 1][newParity]) % mod;
            }
        }

        int res = 0;
        for (int i = 0; i < n; i++) {
            res = (res + dp[i][0]) % mod;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Prefix Sum - I

A subarray has an odd sum when its prefix sum parity differs from the prefix sum at its starting point. If the current prefix sum is odd, pairing it with any previous even prefix sum yields an odd subarray. We track counts of odd and even prefix sums seen so far.

```cpp
class Solution {
public:
    int numOfSubarrays(vector<int>& arr) {
        long long curSum = 0, oddCnt = 0, evenCnt = 0, res = 0;
        const int MOD = 1e9 + 7;

        for (int n : arr) {
            curSum += n;
            if (curSum % 2 != 0) {
                res = (res + 1 + evenCnt) % MOD;
                oddCnt++;
            } else {
                res = (res + oddCnt) % MOD;
                evenCnt++;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 5. Prefix Sum - II

We only need to track the parity of the prefix sum (`0` for even, `1` for odd). A count array of size `2` stores how many prefix sums of each parity we have seen. For each new element, we look up the count of the opposite parity to find valid subarrays.

```cpp
class Solution {
public:
    int numOfSubarrays(vector<int>& arr) {
        int count[2] = {1, 0};
        int prefix = 0, res = 0;
        const int MOD = 1e9 + 7;

        for (int num : arr) {
            prefix = (prefix + num) % 2;
            res = (res + count[1 - prefix]) % MOD;
            count[prefix]++;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
