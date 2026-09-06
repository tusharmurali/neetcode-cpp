# 3133. Minimum Array End

- **Difficulty:** Medium  
- **Pattern:** Bit Manipulation  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/minimum-array-end/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-array-end>  
- **Video:** <https://www.youtube.com/watch?v=4pP-0UpEok4>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We need to build an array of `n` elements where the AND of all elements equals `x`, and the array is strictly increasing. The smallest such array starts with `x` as the first element. Each subsequent element must be greater than the previous one and still have `x` as a subset of its bits (so the AND remains `x`).

To find the next valid number after `res`, we add 1 and then OR with `x`. Adding 1 ensures the number increases, and ORing with `x` ensures all bits of `x` are set (preserving the AND property).

```cpp
class Solution {
public:
    long long minEnd(int n, int x) {
        long long res = x;
        for (int i = 0; i < n - 1; i++) {
            res = (res + 1) | x;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. Binary Representation And Bit Manipulation

The brute force iterates `n - 1` times, which is too slow for large `n`. Instead, we can directly compute the answer using bit manipulation. The key insight is that the answer must have all bits of `x` set, and we need to "count" to `n - 1` using only the bit positions where `x` has 0s.

Think of it as embedding the binary representation of `n - 1` into the zero-bit positions of `x`. The bits of `x` stay fixed at 1, while the zero positions of `x` are filled with the bits of `n - 1` in order.

```cpp
class Solution {
public:
    long long minEnd(int n, int x) {
        long long res = 0;
        n -= 1;

        vector<int> x_bin(64, 0); // Binary representation of x
        vector<int> n_bin(64, 0); // Binary representation of n-1

        for (int i = 0; i < 32; i++) {
            x_bin[i] = (x >> i) & 1;
            n_bin[i] = (n >> i) & 1;
        }

        int i_x = 0;
        int i_n = 0;
        while (i_x < 63) {
            while (i_x < 63 && x_bin[i_x] != 0) {
                i_x++;
            }
            x_bin[i_x] = n_bin[i_n];
            i_x++;
            i_n++;
        }

        for (int i = 0; i < 64; i++) {
            if (x_bin[i] == 1) {
                res += (1LL << i);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(\log n)$

## 3. Bit Manipulation

We can optimize further by avoiding explicit binary arrays. Using bit masks, we iterate through bit positions. For each zero-bit position in `x`, we check if the corresponding bit in `n - 1` is set, and if so, set that bit in our result.

We use two pointers: one for positions in the result (`i_x`) and one for bits of `n - 1` (`i_n`). Whenever we find a zero-bit in `x`, we potentially copy a bit from `n - 1` to the result.

```cpp
class Solution {
public:
    long long minEnd(int n, int x) {
        long long res = x;
        long long i_x = 1;
        long long i_n = 1; // for n - 1

        while (i_n <= n - 1) {
            if ((i_x & x) == 0) {
                if (i_n & (n - 1)) {
                    res = res | i_x;
                }
                i_n = i_n << 1;
            }
            i_x = i_x << 1;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$
