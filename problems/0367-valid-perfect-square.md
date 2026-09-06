# 367. Valid Perfect Square

- **Difficulty:** Easy  
- **Pattern:** Binary Search  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/valid-perfect-square/>  
- **NeetCode:** <https://neetcode.io/problems/valid-perfect-square>  
- **Video:** <https://www.youtube.com/watch?v=Cg_wWPHJ2Sk>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most straightforward approach is to try every integer starting from 1 and check if its square equals the input number. We keep incrementing until either we find a match (perfect square) or the square exceeds the input (not a perfect square). Since we only need to check up to the square root of the number, this terminates reasonably quickly.

```cpp
class Solution {
public:
    bool isPerfectSquare(int num) {
        for (long long i = 1; i <= num; i++) {
            long long sq = i * i;
            if (sq > num) {
                return false;
            }
            if (sq == num) {
                return true;
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(\sqrt {n})$
- Space complexity: $O(1)$

## 2. In-Built Function

Most programming languages provide a built-in square root function. We can use it to compute the square root, truncate it to an integer, and then verify by squaring it back. If the squared result equals the original number, it is a perfect square. This leverages optimized library implementations for a quick solution.

```cpp
class Solution {
public:
    bool isPerfectSquare(int num) {
        int sqRoot = (int) sqrt(num);
        return sqRoot * sqRoot == num;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 3. Binary Search

Instead of checking every number sequentially, we can use binary search to find the square root more efficiently. The search space is from 1 to num. For each midpoint, we compute its square: if it is too large, search the left half; if too small, search the right half; if equal, we found a perfect square. This reduces the number of checks from O(sqrt(n)) to O(log n).

```cpp
class Solution {
public:
    bool isPerfectSquare(int num) {
        long long l = 1, r = num;

        while (l <= r) {
            long long m = l + (r - l) / 2;
            long long sq = m * m;
            if (sq > num) {
                r = m - 1;
            } else if (sq < num) {
                l = m + 1;
            } else {
                return true;
            }
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 4. Math

There is a beautiful mathematical property: perfect squares can be expressed as the sum of consecutive odd numbers. For example, 1 = 1, 4 = 1+3, 9 = 1+3+5, 16 = 1+3+5+7, and so on. We can repeatedly subtract consecutive odd numbers from the input. If we eventually reach exactly zero, the number is a perfect square.

```cpp
class Solution {
public:
    bool isPerfectSquare(int num) {
        int i = 1;
        while (num > 0) {
            num -= i;
            i += 2;
        }
        return num == 0;
    }
};
```

**Complexity**

- Time complexity: $O(\sqrt {n})$
- Space complexity: $O(1)$

## 5. Newton's Method

Newton's method is a fast iterative technique for finding roots of equations. To find the square root of num, we want to solve x^2 = num, or equivalently find the root of f(x) = x^2 - num. Newton's method gives us the iteration formula: x_new = (x + num/x) / 2. Starting from an initial guess (the number itself), each iteration brings us closer to the actual square root. Once converged, we check if the result squared equals the input.

```cpp
class Solution {
public:
    bool isPerfectSquare(int num) {
        long long r = num;
        while (r * r > num) {
            r = (r + num / r) / 2;
        }
        return r * r == num;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 6. Bit Manipulation

We can construct the square root bit by bit, from the most significant bit to the least significant. For a 32-bit integer, the square root fits in at most 16 bits. We try setting each bit position and check if the resulting number squared is still within bounds. If setting a bit makes the square too large, we clear that bit; otherwise, we keep it. This builds the largest integer whose square does not exceed the input.

```cpp
class Solution {
public:
    bool isPerfectSquare(int num) {
        int r = 0, mask = 1 << 15;

        while (mask > 0) {
            r |= mask;
            if (r > (num / r)) {
                r ^= mask;
            }
            mask >>= 1;
        }

        return r * r == num;
    }
};
```

**Complexity**

- Time complexity: $O(1)$ since we iterate at most $15$ times.
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0367-valid-perfect-square.cpp` in the NeetCode repo)

```cpp
/*
Approach: Binary search the number such that divind num by that number gives the number itself

Time Complexity: log(n)
Space Complexity: O(1)
*/
class Solution {
public:
    bool isPerfectSquare(int num) {
        if(num ==1) {return true;}
        int l = 0,r = num;
        while(l<r){
            int m = l + (r-l)/2;
            float x = (float)num / (float)m;
            if(x==m){
                return true;
            }
            else if (x<m){
                r = m;
            }
            else {
                l = m +1;
            }
        }

        return false;
    }
};
```
