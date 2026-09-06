# 69. Sqrt(x)

- **Difficulty:** Easy  
- **Pattern:** Binary Search  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/sqrtx/>  
- **NeetCode:** <https://neetcode.io/problems/sqrtx>  
- **Video:** <https://www.youtube.com/watch?v=zdMhGxRWutQ>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The square root of a number `x` is the largest integer `i` such that `i * i <= x`. We can find this by simply checking each integer starting from `1` until squaring it exceeds `x`. The answer is the last integer whose square did not exceed `x`.

```cpp
class Solution {
public:
    int mySqrt(int x) {
        if (x == 0) {
            return 0;
        }

        int res = 1;
        for (int i = 1; i <= x; i++) {
            if ((long long) i * i > x) {
                return res;
            }
            res = i;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(\sqrt {n})$
- Space complexity: $O(1)$

## 2. In-Built Function

Most programming languages provide a built-in square root function that computes the result efficiently using optimized mathematical algorithms (often Newton's method or similar). We can leverage this and simply truncate the result to get the integer floor of the square root.

```cpp
class Solution {
public:
    int mySqrt(int x) {
        return (int) sqrt(x);
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 3. Binary Search

Since we are looking for the largest integer whose square is at most `x`, and the squares of integers are monotonically increasing, we can use binary search. The search space is `[0, x]`, and we narrow it down by checking if the middle value squared is less than, greater than, or equal to `x`.

```cpp
class Solution {
public:
    int mySqrt(int x) {
        int l = 0, r = x;
        int res = 0;

        while (l <= r) {
            int m = l + (r - l) / 2;
            if ((long long) m * m > x) {
                r = m - 1;
            } else if ((long long) m * m < x) {
                l = m + 1;
                res = m;
            } else {
                return m;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 4. Recursion

We can exploit a mathematical property: `sqrt(x) = 2 * sqrt(x / 4)`. By right-shifting `x` by 2 bits (dividing by 4), we recursively compute the square root of a smaller number. Then we left-shift the result by 1 (multiply by 2) to scale it back up. Finally, we check if incrementing by 1 still gives a valid square root.

```cpp
class Solution {
public:
    int mySqrt(int x) {
        if (x < 2) {
            return x;
        }

        int l = mySqrt(x >> 2) << 1;
        int r = l + 1;
        return (long long) r * r > x ? l : r;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(\log n)$ for recursion stack.

## 5. Newton's Method

Newton's method is a numerical technique for finding roots of equations. To find `sqrt(x)`, we solve `r^2 = x`, or equivalently find the root of `f(r) = r^2 - x`. Newton's iteration formula gives us `r_new = (r + x/r) / 2`. Starting with an initial guess of `x`, we repeatedly apply this formula until `r^2 <= x`, which converges quickly to the answer.

```cpp
class Solution {
public:
    int mySqrt(int x) {
        long long r = x;
        while (r * r > x) {
            r = (r + x / r) >> 1;
        }
        return r;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0069-sqrtx.cpp` in the NeetCode repo)

```cpp
/*
  Given a non-negative integer x, return the square root of x rounded down to the nearest integer. The returned integer should be non-negative as well.
  You must not use any built-in exponent function or operator.

  For example, do not use pow(x, 0.5) in c++ or x ** 0.5 in python.

  Ex. Input: x = 4
      Output: 2
      Explanation: The square root of 4 is 2, so we return 2.

  Time  : O(log N)
  Space : O(1)
*/

class Solution {
public:
    int mySqrt(int x) {
        if(x == 0 || x == 1)
            return x;
            
        long long beg = 0, mid = 0, end = x/2;
        while(beg <= end) {
            mid = (beg + end)/2;
            if(mid * mid < x) {
                if((mid + 1) * (mid + 1) > x)
                    return mid;
                beg = mid+1;
            } else if(mid * mid > x) {
                if( (mid - 1) * (mid - 1) < x)
                    return mid-1;
                end = mid - 1;
            } else 
                return mid;
        }
        return mid;
    }
};
```
