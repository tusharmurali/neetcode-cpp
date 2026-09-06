# 50. Pow(x, n)

- **Difficulty:** Medium  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/powx-n/>  
- **NeetCode:** <https://neetcode.io/problems/pow-x-n>  
- **Video:** <https://www.youtube.com/watch?v=g9YQyYi4IQQ>  
- **Video approach:** 2. Binary Exponentiation (Recursive)  

[← Back to index](../INDEX.md)

## 1. Brute Force

We are asked to compute \( x^n \), where:

- `x` is a floating-point number
- `n` can be **positive, zero, or negative**

The most straightforward way to think about exponentiation is:

- multiplying `x` by itself `n` times

This brute force approach directly follows the mathematical definition of power:

- if `n` is positive → multiply `x` repeatedly
- if `n` is zero → the result is always `1`
- if `n` is negative → compute \( x^{|n|} \) and take its reciprocal

Although this method is not efficient for large `n`, it is very easy to understand and is a good starting point.

```cpp
class Solution {
public:
    double myPow(double x, int n) {
        if (x == 0) {
            return 0;
        }
        if (n == 0) {
            return 1;
        }

        double res = 1;
        for (int i = 0; i < abs(n); i++) {
            res *= x;
        }
        return n >= 0 ? res : 1 / res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. Binary Exponentiation (Recursive) ▶ video

Computing \( x^n \) by multiplying `x` repeatedly works, but it becomes very slow when `n` is large.

A much better idea is to use **binary exponentiation**, which is based on these observations:

- If `n` is even:
    - \( x^n = (x^2)^{n/2} \)
- If `n` is odd:
    - \( x^n = x \times (x^2)^{(n-1)/2} \)

This means we can:

- **halve the exponent** at each step
- **square the base** accordingly

By doing this recursively, the number of multiplications reduces from `O(n)` to `O(log n)`.

We also handle negative powers by:

- computing \( x^{|n|} \)
- taking the reciprocal if `n` is negative

```cpp
class Solution {
public:
    double myPow(double x, int n) {
        if (x == 0) {
            return 0;
        }
        if (n == 0) {
            return 1;
        }

        double res = helper(x, abs(static_cast<long>(n)));
        return (n >= 0) ? res : 1 / res;
    }

private:
    double helper(double x, long n) {
        if (n == 0) {
            return 1;
        }
        double half = helper(x, n / 2);
        return (n % 2 == 0) ? half * half : x * half * half;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(\log n)$ for recursion stack.

## 3. Binary Exponentiation (Iterative)

We want to compute \( x^n \) efficiently, even when `n` is very large (positive or negative).

The brute force approach multiplies `x` repeatedly and takes **O(n)** time, which is too slow.
Instead, we use **binary exponentiation**, which reduces the time complexity to **O(log n)**.

The key ideas are:

- Any number `n` can be written in binary
- If the current `power` is **odd**, we must include one extra `x` in the result
- We repeatedly:
    - square the base (`x = x * x`)
    - halve the exponent (`power = power // 2`)

For negative powers:

- \( x^n = \frac{1}{x^{|n|}} \)
- so we compute using `abs(n)` and take the reciprocal at the end if needed

This iterative version avoids recursion and works efficiently with constant extra space.

```cpp
class Solution {
public:
    double myPow(double x, int n) {
        if (x == 0) return 0;
        if (n == 0) return 1;

        double res = 1;
        long power = abs((long)n);

        while (power) {
            if (power & 1) {
                res *= x;
            }
            x *= x;
            power >>= 1;
        }

        return n >= 0 ? res : 1 / res;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0050-powx-n.cpp` in the NeetCode repo)

```cpp
/*
    Implement pow(x, n), which calculates x raised to the power n
    Ex. x = 2 n = 10 -> 1024, x = 2.1 n = 3 -> 9.261, x = 2 n = -2 -> 0.25

    Divide-and-conquer, even x^n = A * A, odd x^n = A * A * x

    Time: O(log n)
    Space: O(1) -> optimized from recursive O(log n) to do iteratively
*/

// class Solution {
// public:
//     double myPow(double x, int n) {
//         long exponent = abs(n);
//         double result = helper(x, exponent);
//         if (n >= 0) {
//             return result;
//         }
//         return 1.0 / result;
//     }
// private:
//     double helper(double x, long n) {
//         if (x == 0.0) {
//             return 0;
//         }
//         if (n == 0) {
//             return 1.0;
//         }
//         double result = helper(x * x, n / 2);
//         if (n % 2 == 0) {
//             return result;
//         }
//         return result * x;
//     }
// };

class Solution {
public:
    double myPow(double x, int n) {
        long exponent = abs(n);
        double curr = x;
        double result = 1.0;
        
        for (long i = exponent; i > 0; i /= 2) {
            if (i % 2 == 1) {
                result *= curr;
            }
            curr *= curr;
        }
        
        if (n < 0) {
            return 1.0 / result;
        }
        return result;
    }
};
```
