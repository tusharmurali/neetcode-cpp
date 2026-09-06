# 204. Count Primes

- **Difficulty:** Medium  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/count-primes/>  
- **NeetCode:** <https://neetcode.io/problems/count-primes>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most straightforward way to count primes is to check each number individually. A number is prime if it has no divisors other than 1 and itself. We can optimize the divisibility check by only testing divisors up to the square root of the number, since if a number has a factor larger than its square root, it must also have a corresponding factor smaller than its square root.

```cpp
class Solution {
public:
    int countPrimes(int n) {
        int res = 0;
        for (int num = 2; num < n; num++) {
            bool isPrime = true;
            for (int i = 2; i * i <= num; i++) {
                if (num % i == 0) {
                    isPrime = false;
                    break;
                }
            }
            if (isPrime) res++;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \sqrt {n})$
- Space complexity: $O(1)$

## 2. Sieve of Eratosthenes

Instead of checking each number for primality, we can use the Sieve of Eratosthenes to efficiently mark composite numbers. The key insight is that when we find a prime number, all of its multiples must be composite. By marking these multiples, we eliminate the need to check them later. We start marking from the square of each prime because smaller multiples would have already been marked by smaller primes.

```cpp
class Solution {
public:
    int countPrimes(int n) {
        vector<bool> sieve(n, false);
        int res = 0;
        for (int num = 2; num < n; num++) {
            if (!sieve[num]) {
                res++;
                for (long long i = 1LL * num * num; i < n; i += num) {
                    sieve[i] = true;
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log (\log n))$
- Space complexity: $O(n)$
