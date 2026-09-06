# 1220. Count Vowels Permutation

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/count-vowels-permutation/>  
- **NeetCode:** <https://neetcode.io/problems/count-vowels-permutation>  
- **Video:** <https://www.youtube.com/watch?v=VUVpTZVa7Ls>  

[← Back to index](../INDEX.md)

## 1. Recursion

We need to count strings of length n where each vowel can only be followed by specific vowels. The rules are: 'a' can be followed by 'e'; 'e' can be followed by 'a' or 'i'; 'i' can be followed by any vowel except itself; 'o' can be followed by 'i' or 'u'; 'u' can be followed by 'a'. We can solve this by exploring all valid paths using recursion, starting from each vowel.

```cpp
class Solution {
    const int MOD = 1e9 + 7;
    unordered_map<char, vector<char>> follows = {
        {'a', {'e'}},
        {'e', {'a', 'i'}},
        {'i', {'a', 'e', 'o', 'u'}},
        {'o', {'i', 'u'}},
        {'u', {'a'}}
    };

public:
    int countVowelPermutation(int n) {

        int res = 0;
        for (char vowel : string("aeiou")) {
            res = (res + dfs(1, vowel, n)) % MOD;
        }
        return res;
    }

private:
    int dfs(int i, char v, int n) {
        if (i == n) {
            return 1;
        }

        int total = 0;
        for (char& next : follows[v]) {
            total = (total + dfs(i + 1, next, n)) % MOD;
        }
        return total;
    }
};
```

**Complexity**

- Time complexity: $O(4 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Dynamic Programming (Top-Down)

The plain recursion recomputes the same subproblems many times. For example, counting strings starting with `'e'` at position `5` is computed multiple times. We can add memoization to cache results for each `(position, vowel)` pair. This reduces the time complexity dramatically since there are only `O(n * 5)` unique states.

```cpp
class Solution {
private:
    static const int MOD = 1e9 + 7;
    vector<vector<int>> dp;
    vector<vector<int>> follows = {
        {1},          // 'a' -> 'e'
        {0, 2},       // 'e' -> 'a', 'i'
        {0, 1, 3, 4}, // 'i' -> 'a', 'e', 'o', 'u'
        {2, 4},       // 'o' -> 'i', 'u'
        {0}           // 'u' -> 'a'
    };

    int dfs(int i, int v, int n) {
        if (i == n) return 1;
        if (dp[i][v] != -1) return dp[i][v];

        int total = 0;
        for (int next : follows[v]) {
            total = (total + dfs(i + 1, next, n)) % MOD;
        }
        return dp[i][v] = total;
    }

public:
    int countVowelPermutation(int n) {
        dp.assign(n, vector<int>(5, -1));

        int res = 0;
        for (int vowel = 0; vowel < 5; vowel++) {
            res = (res + dfs(1, vowel, n)) % MOD;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

Instead of recursion with memoization, we can build the solution iteratively from the base case. We use a 2D DP table where `dp[i][v]` represents the count of valid strings of length `i` ending with vowel `v`. We start with length `1` (each vowel has count `1`) and build up to length `n` by considering which vowels can precede each vowel.

```cpp
class Solution {
private:
    static const int MOD = 1e9 + 7;

public:
    int countVowelPermutation(int n) {
        vector<vector<int>> dp(n + 1, vector<int>(5, 0));
        vector<vector<int>> follows = {
            {1},          // 'a' -> 'e'
            {0, 2},       // 'e' -> 'a', 'i'
            {0, 1, 3, 4}, // 'i' -> 'a', 'e', 'o', 'u'
            {2, 4},       // 'o' -> 'i', 'u'
            {0}           // 'u' -> 'a'
        };

        for (int v = 0; v < 5; v++) {
            dp[1][v] = 1;
        }

        for (int i = 2; i <= n; i++) {
            for (int v = 0; v < 5; v++) {
                for (int nextV : follows[v]) {
                    dp[i][v] = (dp[i][v] + dp[i - 1][nextV]) % MOD;
                }
            }
        }

        int result = 0;
        for (int v = 0; v < 5; v++) {
            result = (result + dp[n][v]) % MOD;
        }
        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Space Optimized)

In the bottom-up approach, we only need the previous row to compute the current row. This means we can reduce space from `O(n)` to `O(1)` by using just two arrays of size 5 (or even one array with careful updates). We alternate between the current and previous state arrays.

```cpp
class Solution {
private:
    static const int MOD = 1e9 + 7;

public:
    int countVowelPermutation(int n) {
        vector<vector<int>> follows = {
            {1},          // 'a' -> 'e'
            {0, 2},       // 'e' -> 'a', 'i'
            {0, 1, 3, 4}, // 'i' -> 'a', 'e', 'o', 'u'
            {2, 4},       // 'o' -> 'i', 'u'
            {0}           // 'u' -> 'a'
        };

        vector<int> dp(5, 1);

        for (int i = 2; i <= n; i++) {
            vector<int> nextDp(5, 0);
            for (int v = 0; v < 5; v++) {
                for (int nextV : follows[v]) {
                    nextDp[v] = (nextDp[v] + dp[nextV]) % MOD;
                }
            }
            dp = nextDp;
        }

        int result = 0;
        for (int count : dp) {
            result = (result + count) % MOD;
        }
        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since we used array of size $5$.

## 5. Matrix Exponentiation

The transition between states can be represented as a matrix multiplication. If we define a transition matrix `T` where `T[i][j] = 1` if vowel `j` can follow vowel `i`, then multiplying the state vector by `T` gives the next state. To get the state after `n-1` transitions, we compute `T^(n-1)`. Matrix exponentiation allows us to compute this in `O(log n)` time instead of `O(n)`.

```cpp
class Solution {
    static const int MOD = 1e9 + 7;

    struct M {
        vector<vector<int>> a;

        M(int n) {
            a.resize(n, vector<int>(n, 0));
        }

        M operator*(const M& other) const {
            int n = a.size();
            M product(n);

            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    for (int k = 0; k < n; k++) {
                        product.a[i][k] = (product.a[i][k] + a[i][j] * 1LL * other.a[j][k]) % MOD;
                    }
                }
            }
            return product;
        }
    };

    M matrixExpo(M base, int exp) {
        int n = base.a.size();
        M result(n);

        for (int i = 0; i < n; i++) {
            result.a[i][i] = 1;
        }

        while (exp > 0) {
            if (exp % 2 == 1) {
                result = result * base;
            }
            base = base * base;
            exp /= 2;
        }

        return result;
    }

public:
    int countVowelPermutation(int n) {
        vector<vector<int>> follows = {
            {0, 1, 0, 0, 0},  // 'a' -> 'e'
            {1, 0, 1, 0, 0},  // 'e' -> 'a', 'i'
            {1, 1, 0, 1, 1},  // 'i' -> 'a', 'e', 'o', 'u'
            {0, 0, 1, 0, 1},  // 'o' -> 'i', 'u'
            {1, 0, 0, 0, 0}   // 'u' -> 'a'
        };

        M base(5);
        base.a = follows;

        M result = matrixExpo(base, n - 1);

        int ans = 0;
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                ans = (ans + result.a[i][j]) % MOD;
            }
        }

        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(m ^ 3 \log n)$
- Space complexity: $O(m ^ 2)$

> Where $m$ is the size of the matrix used in matrix exponentiation $(5 X 5)$ and $n$ is the length of the permutation.

## Standalone solution file (`cpp/1220-count-vowels-permutation.cpp` in the NeetCode repo)

```cpp
/*
Given an integer n, our task is to count how many strings of length n can be formed under the following rules:

Each character is a lower case vowel ('a', 'e', 'i', 'o', 'u')
Each vowel 'a' may only be followed by an 'e'.
Each vowel 'e' may only be followed by an 'a' or an 'i'.
Each vowel 'i' may not be followed by another 'i'.
Each vowel 'o' may only be followed by an 'i' or a 'u'.
Each vowel 'u' may only be followed by an 'a'.
Since the answer may be too large, we have to return it modulo 10^9 + 7.

Example. For n = 2, Output = 10
	 
	Explanation: All possible strings of length 2 that can be formed as per the given rules are: "ae", "ea", "ei", "ia", "ie", "io", "iu",
	"oi", "ou" and "ua".
	So we return 10 as our answer. 


Time: O(n)
Space: O(1)

*/


class Solution {
const unsigned int mod = 1e9+7;
public:
    int countVowelPermutation(int n) {
        vector<int> prev(5,1), curr(5, 0);
        for(int i=1; i<n; i++) {
            curr[0] = prev[1] % mod;
            curr[1] = (prev[0] + prev[2]) % mod;
            curr[2] = ((prev[0] % mod) + (prev[1] % mod) + (prev[3] % mod) + (prev[4] % mod)) % mod;
            curr[3] = (prev[4] + prev[2]) % mod;
            curr[4] = prev[0] % mod;
            prev = curr;
        }
        int ans = 0;
        for(auto &a:prev) ans = (ans + a) % mod;
        return ans;
    }
};
```
