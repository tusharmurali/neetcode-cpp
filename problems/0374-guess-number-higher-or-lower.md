# 374. Guess Number Higher Or Lower

- **Difficulty:** Easy  
- **Pattern:** Binary Search  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/guess-number-higher-or-lower/>  
- **NeetCode:** <https://neetcode.io/problems/guess-number-higher-or-lower>  
- **Video:** <https://www.youtube.com/watch?v=xW4QsTtaCa4>  

[← Back to index](../INDEX.md)

## 1. Linear Search

The simplest approach is to try every number from `1` to `n` until we find the correct one. Each guess tells us whether we hit the target. While guaranteed to work, this method is slow for large `n` since we might need to check every single number.

```cpp
/**
 * Forward declaration of guess API.
 * @param  num   your guess
 * @return 	     -1 if num is higher than the picked number
 *			      1 if num is lower than the picked number
 *               otherwise return 0
 * int guess(int num);
 */

class Solution {
public:
    int guessNumber(int n) {
        for (int num = 1; num <= n; num++) {
            if (guess(num) == 0) return num;
        }
        return n;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. Binary Search

Since the numbers from `1` to `n` are sorted, we can use binary search to find the target efficiently. The `guess` API tells us whether to search higher or lower, which is exactly the feedback binary search needs to halve the search space with each guess.

```cpp
/**
 * Forward declaration of guess API.
 * @param  num   your guess
 * @return 	     -1 if num is higher than the picked number
 *			      1 if num is lower than the picked number
 *               otherwise return 0
 * int guess(int num);
 */

class Solution {
public:
    int guessNumber(int n) {
        int l = 1, r = n;
        while (true) {
            int m = l + (r - l) / 2;
            int res = guess(m);
            if (res > 0) {
                l = m + 1;
            } else if (res < 0) {
                r = m - 1;
            } else {
                return m;
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 3. Ternary Search

Ternary search divides the search space into three parts instead of two. We pick two midpoints and use the `guess` API on both. Based on the results, we can eliminate either one-third or two-thirds of the search space. While this approach works, it does not improve on binary search for this problem since we need more API calls per iteration.

```cpp
/**
 * Forward declaration of guess API.
 * @param  num   your guess
 * @return 	     -1 if num is higher than the picked number
 *			      1 if num is lower than the picked number
 *               otherwise return 0
 * int guess(int num);
 */

class Solution {
public:
    int guessNumber(int n) {
        int l = 1, r = n;
        while (true) {
            int m1 = l + (r - l) / 3;
            int m2 = r - (r - l) / 3;
            if (guess(m1) == 0) return m1;
            if (guess(m2) == 0) return m2;
            if (guess(m1) + guess(m2) == 0) {
                l = m1 + 1;
                r = m2 - 1;
            } else if (guess(m1) == -1) {
                r = m1 - 1;
            } else {
                l = m2 + 1;
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(\log_3 n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0374-guess-number-higher-or-lower.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int guessNumber(int n) {
        int low = 1;
        int high = n;
        
        while(true) {
            int mid = low + (high - low)/2;
            int myGuess = guess(mid);
            if(myGuess == 1)
                low = mid + 1;
            else if(myGuess == -1)
                high = mid - 1;
            else
                return mid;
        }
    }
};
```
