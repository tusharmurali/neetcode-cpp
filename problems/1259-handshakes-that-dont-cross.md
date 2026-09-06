# 1259. Handshakes That Don't Cross

- **Difficulty:** Hard  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/handshakes-that-dont-cross/>  
- **NeetCode:** <https://neetcode.io/problems/handshakes-that-dont-cross>  

[← Back to index](../INDEX.md)

## 1. Bottom-Up Dynamic Programming

Consider people standing in a circle. If person `0` shakes hands with person `k` (where `k` is odd, since we need an even number of people on each side), the circle splits into two independent groups: people between `0` and `k`, and people between `k` and the last person. The total ways for this configuration is the product of ways to arrange handshakes in both groups.

By summing over all valid choices for person `0`'s partner, we get a recurrence relation. This is precisely the Catalan number recurrence, which counts non-crossing pair arrangements.

```cpp
class Solution {
    const static int m = 1'000'000'007;

public:
    int numberOfWays(int numPeople) {
        vector<int> dp(numPeople / 2 + 1);
        dp[0] = 1;

        for (int i = 1; i <= numPeople / 2; i++) {
            for (int j = 0; j < i; j++) {
                (dp[i] += (long long)dp[j] * dp[i - j - 1] % m) %= m;
            }
        }

        return dp[numPeople / 2];
    }
};
```

**Complexity**

- Time complexity: $O(numPeople^2)$

- Space complexity: $O(numPeople)$

## 2. Top-Down Dynamic Programming (Memoization)

The same recurrence relation can be computed recursively with memoization. Instead of building up from smaller subproblems, we start from the target and recursively compute smaller cases as needed, caching results to avoid redundant work.

This approach is often more intuitive since it directly mirrors the problem structure: to solve for `n` pairs, we try all ways to pair the first person and recursively solve the resulting subproblems.

```cpp
class Solution {
    const static int m = 1'000'000'007;

public:
    int numberOfWays(int numPeople) {
        vector<int> dp(numPeople / 2 + 1, -1);
        dp[0] = 1;

        function<int(int)> calculateDP = [&](int i) -> int {
            if (dp[i] != -1) {
                return dp[i];
            }
            dp[i] = 0;
            for (int j = 0; j < i; j++) {
                (dp[i] += (long long)calculateDP(j) * calculateDP(i - j - 1) % m) %= m;
            }
            return dp[i];
        };

        return calculateDP(numPeople / 2);
    }
};
```

**Complexity**

- Time complexity: $O(numPeople^2)$

- Space complexity: $O(numPeople)$

## 3. Catalan Numbers

The number of non-crossing handshake arrangements is exactly the n-th Catalan number, where `n = numPeople/2`. Catalan numbers have a closed-form formula that can be computed iteratively without solving the full recurrence.

Using the formula `C(n) = C(n-1) * 2(2n-1) / (n+1)`, we can compute the result in linear time with constant extra space (aside from precomputing modular inverses).

```cpp
class Solution {
    const int m = 1'000'000'007;
    int mul(int a, int b) { return (long long)a * b % m; }

public:
    int numberOfWays(int numPeople) {
        int n = numPeople / 2;
        vector<int> inv(n + 2);
        inv[1] = 1;
        for (int i = 2; i < n + 2; i++) {
            int k = m / i, r = m % i;
            inv[i] = m - mul(k, inv[r]);
        }

        int C = 1;
        for (int i = 0; i < n; i++) {
            C = mul(mul(2 * (2 * i + 1), inv[i + 2]), C);
        }

        return C;
    }
};
```

**Complexity**

- Time complexity: $O(numPeople)$

- Space complexity: $O(numPeople)$
