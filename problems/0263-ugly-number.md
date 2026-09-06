# 263. Ugly Number

- **Difficulty:** Easy  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/ugly-number/>  
- **NeetCode:** <https://neetcode.io/problems/ugly-number>  
- **Video:** <https://www.youtube.com/watch?v=M0Zay1Qr9ws>  
- **Video approach:** 1. Math (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Math ▶ video

An ugly number has only 2, 3, and 5 as prime factors. This means if we keep dividing the number by 2, 3, and 5 (as long as it is divisible), we should eventually reach 1. If any other prime factor exists, the number will not reduce to 1.

```cpp
class Solution {
public:
    bool isUgly(int n) {
        if (n <= 0) return false;

        for (int p = 2; p <= 5 && n > 0; p++) {
            while (n % p == 0) {
                n /= p;
            }
        }

        return n == 1;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0263-ugly-number.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    bool isUgly(int n) {
        if(n <= 0)
            return false;
        
        for(int p: {2, 3, 5})
            while(n % p == 0)
                n = n / p;
        return n == 1;
    }
};
```
