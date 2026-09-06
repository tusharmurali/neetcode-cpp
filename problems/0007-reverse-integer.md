# 7. Reverse Integer

- **Difficulty:** Medium  
- **Pattern:** Bit Manipulation  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/reverse-integer/>  
- **NeetCode:** <https://neetcode.io/problems/reverse-integer>  
- **Video:** <https://www.youtube.com/watch?v=HAgLH58IgJQ>  
- **Video approach:** 3. Iteration  

[← Back to index](../INDEX.md)

## 1. Brute Force

We want to reverse the digits of an integer `x` (for example, `123 -> 321`, `-120 -> -21`).

A very simple way to do this is:

- ignore the sign for a moment and work with the absolute value
- convert the number to a string so digits become easy to manipulate
- reverse the string and convert it back to an integer
- restore the original sign if `x` was negative

Finally, the problem usually requires that the answer must fit in a **32-bit signed integer** range:

- from `-2^31` to `2^31 - 1`
  If the reversed number goes outside this range, we return `0`.

This approach is beginner-friendly because it uses direct operations on strings instead of manual digit math.

```cpp
class Solution {
public:
    int reverse(int x) {
        int org = x;
        x = abs(x);
        string strX = to_string(x);
        std::reverse(strX.begin(), strX.end());
        long long res = stoll(strX);
        if (org < 0) {
            res *= -1;
        }
        if (res < -(1LL << 31) || res > (1LL << 31) - 1) {
            return 0;
        }
        return static_cast<int>(res);
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 2. Recursion

We want to reverse the digits of an integer while **preserving its sign** and ensuring the result fits within the **32-bit signed integer range**.

Instead of reversing digits using strings, this approach uses **pure arithmetic** and **recursion**.
The idea is simple:

- Take the last digit of the number
- Append it to a running reversed value
- Remove the last digit from the number
- Repeat until the number becomes `0`

Recursion naturally fits this process because each step reduces the problem size by one digit.

```cpp
class Solution {
public:
    int reverse(int x) {
        long res = rec(abs(x), 0) * (x < 0 ? -1 : 1);
        if (res < INT_MIN || res > INT_MAX) {
            return 0;
        }
        return (int)res;
    }

private:
    long rec(int n, long rev) {
        if (n == 0) {
            return rev;
        }
        rev = rev * 10 + n % 10;
        return rec(n / 10, rev);
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 3. Iteration ▶ video

We want to reverse the digits of an integer **without using strings**, while also ensuring the result fits within the **32-bit signed integer range**.

The key idea is to build the reversed number **digit by digit**:

- Repeatedly take the **last digit** of the number
- Append it to the end of a running `res`
- Remove the last digit from the original number

However, before appending a new digit, we must **check for overflow**.
If multiplying `res` by `10` (and adding the new digit) would exceed the 32-bit signed integer limits, we immediately return `0`.

This approach closely matches how integer reversal works at a low level and is both **efficient and safe**.

```cpp
class Solution {
public:
    int reverse(int x) {
        const int MIN = -2147483648; // -2^31
        const int MAX = 2147483647;  // 2^31 - 1

        int res = 0;
        while (x != 0) {
            int digit = x % 10;
            x /= 10;

            if (res > MAX / 10 || (res == MAX / 10 && digit > MAX % 10))
                return 0;
            if (res < MIN / 10 || (res == MIN / 10 && digit < MIN % 10))
                return 0;
            res = (res * 10) + digit;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0007-reverse-integer.cpp` in the NeetCode repo)

```cpp
/*
    Given a signed 32-bit integer, return it with its digits reversed
    Ex. x = 123 -> 321, x = -123 -> -321, x = 120 -> 21

    Reverse bit-by-bit starting from right, shift right off every time

    Time: O(log x)
    Space: O(1)
*/

class Solution {
public:
    int reverse(int x) {
        int rev = 0;
        while (x != 0) {
            int temp = x % 10;
            x /= 10;
            if (rev > INT_MAX / 10 || (rev == INT_MAX / 10 && temp > 7)) {
                return 0;
            }
            if (rev < INT_MIN / 10 || (rev == INT_MIN / 10 && temp < -8)) {
                return 0;
            }
            rev = rev * 10 + temp;
        }
        return rev;
    }
};
```
