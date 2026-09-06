# 2929. Distribute Candies Among Children II

- **Difficulty:** Medium  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/distribute-candies-among-children-ii/>  
- **NeetCode:** <https://neetcode.io/problems/distribute-candies-among-children-ii>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most straightforward approach is to try every possible combination of candies for the three children. We iterate through all values for child A, child B, and child C (each from `0` to the `limit`), and count only those combinations where the total equals exactly `n` candies. While simple to understand, this method checks many invalid combinations.

```cpp
class Solution {
public:
    long long distributeCandies(int n, int limit) {
        long long res = 0;
        for (int a = 0; a <= limit; a++) {
            for (int b = 0; b <= limit; b++) {
                for (int c = 0; c <= limit; c++) {
                    if (a + b + c == n) {
                        res++;
                    }
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(l ^ 3)$
- Space complexity: $O(1)$

> Where $l$ is the given limit.

## 2. Better Approach

We can reduce unnecessary iterations by fixing the first child's amount and only looping through valid values for the second child. Once we know how many candies child A and child B receive, child C's amount is determined: `c = n - a - b`. We simply check if this value is within the allowed `limit`.

```cpp
class Solution {
public:
    long long distributeCandies(int n, int limit) {
        long long res = 0;
        int maxA = min(n, limit);
        for (int a = 0; a <= maxA; a++) {
            int maxB = min(n - a, limit);
            for (int b = 0; b <= maxB; b++) {
                if (n - a - b <= limit) {
                    res++;
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(min(n, limit) ^ 2)$
- Space complexity: $O(1)$

## 3. Enumeration - I

Instead of iterating through every value of `b`, we can directly compute the range of valid values. For a fixed `a`, child B can receive anywhere from `b_min` to `b_max` candies, where `b_max = min(n - a, limit)` and `b_min = max(0, n - a - limit)`. The lower bound ensures child C does not exceed the `limit`. The number of valid `b` values is simply `b_max - b_min + 1`.

```cpp
class Solution {
public:
    long long distributeCandies(int n, int limit) {
        long long res = 0;
        int aMax = min(n, limit);
        for (int a = 0; a <= aMax; ++a) {
            int bMax = min(n - a, limit);
            int bMin = max(0, n - a - limit);
            if (bMax >= bMin) {
                res += (long long)(bMax - bMin + 1);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(min(n, limit))$

## 4. Enumeration - II

This is a slight optimization of the previous approach. We add an early check: if the remaining candies `n - a` exceeds `2 * limit`, it is impossible to distribute them between child B and child C (since each can hold at most `limit`). This allows us to skip invalid values of `a` entirely.

```cpp
class Solution {
public:
    long long distributeCandies(int n, int limit) {
        long long res = 0;
        int maxA = min(n, limit);
        for (int a = 0; a <= maxA; ++a) {
            int rem = n - a;
            if (rem <= 2 * limit) {
                int hi = min(rem, limit);
                int lo = max(0, rem - limit);
                res += (long long)(hi - lo + 1);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(min(n, limit))$

## 5. Inclusion-Exclusion Principle

We can solve this in constant time using combinatorics. The total number of ways to distribute `n` candies among 3 children (without the `limit` constraint) is `C(n+2, 2)`. However, we need to subtract cases where at least one child exceeds the `limit`. Using the inclusion-exclusion principle, we subtract cases where one child exceeds the `limit`, add back cases where two children exceed it (since they were subtracted twice), and subtract cases where all three exceed it.

```cpp
class Solution {
public:
    long long distributeCandies(int n, int limit) {
        int C3[4] = {1, 3, 3, 1};
        long long res = 0;
        for (int j = 0; j < 4; j++) {
            long long m = n - j * (limit + 1);
            if (m < 0) continue;
            long long ways = (m + 2) * (m + 1) / 2;
            int sign = (j % 2 == 0 ? 1 : -1);
            res += sign * C3[j] * ways;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$
