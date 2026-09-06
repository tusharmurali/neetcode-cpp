# 441. Arranging Coins

- **Difficulty:** Easy  
- **Pattern:** Binary Search  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/arranging-coins/>  
- **NeetCode:** <https://neetcode.io/problems/arranging-coins>  
- **Video:** <https://www.youtube.com/watch?v=5rHz_6s2Buw>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We are building a staircase where row 1 needs 1 coin, row 2 needs 2 coins, and so on. The question is: how many complete rows can we build with `n` coins?

The simplest approach is to simulate the process. Keep adding rows one by one, subtracting the required coins from `n` until we cannot complete another row.

```cpp
class Solution {
public:
    int arrangeCoins(int n) {
        int row = 0;
        while (n - row > 0) {
            row++;
            n -= row;
        }
        return row;
    }
};
```

**Complexity**

- Time complexity: $O(\sqrt {n})$
- Space complexity: $O(1)$

## 2. Binary Search

Building rows one by one is slow for large `n`. Instead, we can use the formula for the sum of first `k` integers: `k * (k + 1) / 2`. If this sum is at most `n`, we can build `k` complete rows.

This creates a monotonic condition perfect for binary search. We search for the largest `k` such that `k * (k + 1) / 2 <= n`.

```cpp
class Solution {
public:
    int arrangeCoins(int n) {
        long long l = 1, r = n, res = 0;

        while (l <= r) {
            long long mid = l + (r - l) / 2;
            long long coins = (mid * (mid + 1)) / 2;
            if (coins > n) {
                r = mid - 1;
            } else {
                l = mid + 1;
                res = max(res, mid);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 3. Binary Search (Optimal)

We can optimize the binary search by tightening the upper bound. Since `k * (k + 1) / 2 <= n`, we know `k` is roughly `sqrt(2n)`. A safe upper bound is `n / 2 + 1` for `n > 3`, which reduces the search space.

We also simplify the binary search by finding the first `k` where the condition fails, then returning `k - 1`.

```cpp
class Solution {
public:
    int arrangeCoins(int n) {
        if (n <= 3) {
            return n == 1 ? 1 : n - 1;
        }

        int l = 1, r = (n / 2) + 1;
        while (l < r) {
            int mid = l + (r - l) / 2;
            long long coins = (mid * (mid + 1LL)) / 2;
            if (coins <= n) {
                l = mid + 1;
            } else {
                r = mid;
            }
        }

        return l - 1;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 4. Bit Manipulation

We can build the answer bit by bit, from the most significant bit down. For each bit position, we tentatively set it and check if the resulting number of rows is valid. If valid, we keep the bit; otherwise, we clear it.

Since `n` fits in 32 bits and `k` is roughly `sqrt(n)`, we only need about 16 bits to represent the answer.

```cpp
class Solution {
public:
    int arrangeCoins(int n) {
        int mask = 1 << 15;
        int rows = 0;
        while (mask > 0) {
            rows |= mask;
            long long coins = (long long) rows * (rows + 1) / 2;
            if (coins > n) {
                rows ^= mask;
            }
            mask >>= 1;
        }
        return rows;
    }
};
```

**Complexity**

- Time complexity: $O(1)$ since we iterate $15$ times.
- Space complexity: $O(1)$

## 5. Math

We can solve this directly with algebra. We need the largest `k` where `k * (k + 1) / 2 <= n`. Rearranging: `k^2 + k - 2n <= 0`. Using the quadratic formula, `k = (-1 + sqrt(1 + 8n)) / 2`.

Simplifying gives us `k = sqrt(2n + 0.25) - 0.5`. We take the floor of this value to get the answer.

```cpp
class Solution {
public:
    int arrangeCoins(int n) {
        return (int)(sqrt(2.0 * n + 0.25) - 0.5);
    }
};
```

**Complexity**

- Time complexity: $O(1)$ or $O(\sqrt {n})$ depending on the language.
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0441-arranging-coins.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int arrangeCoins(int n) {
        int l=1,r = n,answer=1;
        long long sum,m;

        // binary search the values
        while(l<=r){
            m = l + (r-l)/2;

            sum = m * (m+1)/2;

            if(sum==n){
                return (int)m;
            }
            else if(n<sum){
                r = m -1;
            }
            else{
                answer = (int)m;
                l = m + 1;
            }
        }

        return answer;
    }
};
```
