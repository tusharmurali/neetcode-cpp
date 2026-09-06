# 338. Counting Bits

- **Difficulty:** Easy  
- **Pattern:** Bit Manipulation  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/counting-bits/>  
- **NeetCode:** <https://neetcode.io/problems/counting-bits>  
- **Video:** <https://www.youtube.com/watch?v=RyBM56RIWrM>  
- **Video approach:** 4. Bit Manipulation (DP)  

[← Back to index](../INDEX.md)

## 1. Bit Manipulation - I

For every number from `0` to `n`, we want to compute how many `1` bits appear in its binary representation.

This **bit manipulation** approach checks each bit position individually:

- Integers are typically represented using **32 bits**
- For each number, we test whether the bit at position `i` is set using a bit mask

Although this solution is not optimal, it clearly demonstrates how bitwise operations work at a low level.

```cpp
class Solution {
public:
    vector<int> countBits(int n) {
        vector<int> res(n + 1);
        for (int num = 1; num <= n; num++) {
            for (int i = 0; i < 32; i++) {
                if (num & (1 << i)) {
                    res[num]++;
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output array.

## 2. Bit Manipulation - II

To count the number of `1` bits efficiently, we can use **Brian Kernighan’s Algorithm**.

The key observation:

- The operation `n & (n - 1)` **removes the lowest set bit** from `n`
- Repeating this until `n` becomes `0` counts how many `1` bits are present

This avoids checking all 32 bits for every number.

```cpp
class Solution {
public:
    vector<int> countBits(int n) {
        vector<int> res(n + 1, 0);
        for (int i = 1; i <= n; i++) {
            int num = i;
            while (num != 0) {
                res[i]++;
                num &= (num - 1);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output array.

## 3. In-Built Function

We need to compute the number of set bits (`1`s) in the binary representation of **every number from `0` to `n`**.

Instead of manually counting bits using bit manipulation or dynamic programming, many programming languages provide **built-in ways to convert numbers to binary or directly count set bits**. Using these built-in features allows us to write a very concise and readable solution.

This approach is especially useful when:

- `n` is small to moderate
- clarity is more important than optimal performance
- we want a quick and reliable implementation

```cpp
class Solution {
public:
    vector<int> countBits(int n) {
        vector<int> res(n + 1, 0);
        for (int i = 0; i <= n; i++) {
            res[i] = __builtin_popcount(i);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output array.

## 4. Bit Manipulation (DP) ▶ video

We want to compute the number of set bits (`1`s) for **all numbers from `0` to `n`** efficiently.

A key observation from binary representation is:

- Numbers repeat their bit patterns every time we reach a **power of two**
- When a number is a power of two, it has **exactly one `1` bit**
- Any number `i` can be written as:
  **`i = highestPowerOfTwo ≤ i + remainder`**

So, the number of set bits in `i` is:

> **1 (for the highest power of two) + number of set bits in the remainder**

This allows us to build the solution incrementally using **Dynamic Programming**, reusing results we have already computed.

```cpp
class Solution {
public:
    vector<int> countBits(int n) {
        vector<int> dp(n + 1);
        int offset = 1;

        for (int i = 1; i <= n; i++) {
            if (offset * 2 == i) {
                offset = i;
            }
            dp[i] = 1 + dp[i - offset];
        }
        return dp;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output array.

## 5. Bit Manipulation (Optimal)

We want to find the number of set bits (`1`s) in every number from `0` to `n`.

A very important observation from binary representation is:

- Right-shifting a number by 1 (`i >> 1`) removes the **least significant bit**
- `(i & 1)` tells us whether the last bit of `i` is `1` or `0`

So, the number of set bits in `i` can be built from a **smaller number**:

> **setBits(i) = setBits(i >> 1) + (i & 1)**

This means each result depends only on a previously computed value, making it a perfect fit for **Dynamic Programming**.

```cpp
class Solution {
public:
    vector<int> countBits(int n) {
        vector<int> dp(n + 1);
        for (int i = 1; i <= n; i++) {
            dp[i] = dp[i >> 1] + (i & 1);
        }
        return dp;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output array.

## Standalone solution file (`cpp/0338-counting-bits.cpp` in the NeetCode repo)

```cpp
/*
    Given int, return array: for each i, ans[i] is # of 1's
    Ex. n = 2 -> [0,1,1], 0 = 0 has 0, 1 = 1 has 1, 2 = 10 has 1

    x = 1001011101 = 605
    x'= 0100101110 = 302
    Differ by 1 bit, by removing LSB: f(x) = f(x / 2) + (x mod 2)

    Time: O(n)
    Space: O(1), the output array does not count towards space
*/

class Solution {
public:
    vector<int> countBits(int n) {
        vector<int> result(n + 1, 0);
        
        for (int i = 1; i <= n; i++) {
            //                 i / 2      i % 2
            result[i] = result[i >> 1] + (i & 1);
        }
        
        return result;
    }
};
```
