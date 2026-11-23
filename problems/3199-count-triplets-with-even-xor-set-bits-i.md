# 3199. Count Triplets with Even XOR Set Bits I

- **Difficulty:** Easy  
- **Pattern:** Bit Manipulation  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/count-triplets-with-even-xor-set-bits-i/>  
- **NeetCode:** <https://neetcode.io/problems/count-triplets-with-even-xor-set-bits-i>  

[← Back to index](../INDEX.md)

## 1. Brute Force

```cpp
class Solution {
public:
    int tripletCount(vector<int>& a, vector<int>& b, vector<int>& c) {
        int res = 0;
        for (int x : a) {
            for (int y : b) {
                for (int z : c) {
                    if (__builtin_popcount(x ^ y ^ z) % 2 == 0) {
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

- Time complexity: $O(n ^ 3 \log m)$
- Space complexity: $O(1)$

> Where $n$ is the maximum length of the arrays $a$, $b$, $c$ and $m$ is the maximum value in them.

## 2. Hash Map

```cpp
class Solution {
public:
    int tripletCount(vector<int>& a, vector<int>& b, vector<int>& c) {
        unordered_map<int, int> countA = count(a), countB = count(b), countC = count(c);
        int res = 0;
        for (auto& [x, p] : countA) {
            for (auto& [y, q] : countB) {
                for (auto& [z, r] : countC) {
                    if (__builtin_popcount(x ^ y ^ z) % 2 == 0) {
                        res += p * q * r;
                    }
                }
            }
        }
        return res;
    }

private:
    unordered_map<int, int> count(vector<int>& arr) {
        unordered_map<int, int> mp;
        for (int x : arr) {
            mp[x]++;
        }
        return mp;
    }
};
```

**Complexity**

- Time complexity: $O(n + d ^ 3 \log m)$
- Space complexity: $O(d)$

> Where $n$ is the maximum length of the arrays $a$, $b$, $c$, $d$ is the number of distinct values in an array ($d \le 101$) and $m$ is the maximum value.

## 3. Bit Manipulation

```cpp
class Solution {
public:
    int tripletCount(vector<int>& a, vector<int>& b, vector<int>& c) {
        auto [evenA, oddA] = count(a);
        auto [evenB, oddB] = count(b);
        auto [evenC, oddC] = count(c);
        return evenA * evenB * evenC + evenA * oddB * oddC +
               oddA * evenB * oddC + oddA * oddB * evenC;
    }

private:
    pair<int, int> count(vector<int>& arr) {
        int odd = 0;
        for (int x : arr) {
            odd += __builtin_popcount(x) % 2;
        }
        return {(int)arr.size() - odd, odd};
    }
};
```

**Complexity**

- Time complexity: $O(n \log m)$
- Space complexity: $O(1)$

> Where $n$ is the maximum length of the arrays $a$, $b$, $c$ and $m$ is the maximum value in them.
