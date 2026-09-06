# 1442. Count Triplets That Can Form Two Arrays of Equal XOR

- **Difficulty:** Medium  
- **Pattern:** Bit Manipulation  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/count-triplets-that-can-form-two-arrays-of-equal-xor/>  
- **NeetCode:** <https://neetcode.io/problems/count-triplets-that-can-form-two-arrays-of-equal-xor>  
- **Video:** <https://www.youtube.com/watch?v=e4Yx9KjqzQ8>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We need to find triplets `(i, j, k)` where `a = arr[i] XOR arr[i+1] XOR ... XOR arr[j-1]` equals `b = arr[j] XOR arr[j+1] XOR ... XOR arr[k]`. The most direct approach is to try all valid combinations of `i`, `j`, and `k`, compute both XOR values for each triplet, and count when they match.

```cpp
class Solution {
public:
    int countTriplets(vector<int>& arr) {
        int N = arr.size();
        int res = 0;

        for (int i = 0; i < N - 1; ++i) {
            for (int j = i + 1; j < N; ++j) {
                for (int k = j; k < N; ++k) {
                    int a = 0, b = 0;
                    for (int idx = i; idx < j; ++idx) {
                        a ^= arr[idx];
                    }
                    for (int idx = j; idx <= k; ++idx) {
                        b ^= arr[idx];
                    }
                    if (a == b) {
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

- Time complexity: $O(n ^ 4)$
- Space complexity: $O(1)$ extra space.

## 2. Brute Force (Optimized)

Instead of recomputing the XOR values from scratch for each triplet, we can build them incrementally. As we move `j` forward, we can extend `a` by XORing the next element. Similarly, as we move `k` forward, we can extend `b` by XORing the next element. This eliminates the innermost loops for computing XOR values.

```cpp
class Solution {
public:
    int countTriplets(vector<int>& arr) {
        int N = arr.size();
        int res = 0;

        for (int i = 0; i < N - 1; ++i) {
            int a = 0;
            for (int j = i + 1; j < N; ++j) {
                a ^= arr[j - 1];
                int b = 0;
                for (int k = j; k < N; ++k) {
                    b ^= arr[k];
                    if (a == b) {
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

- Time complexity: $O(n ^ 3)$
- Space complexity: $O(1)$ extra space.

## 3. Math + Bitwise XOR

The key insight is that if `a == b`, then `a XOR b == 0`, which means `arr[i] XOR arr[i+1] XOR ... XOR arr[k] == 0`. So we need to find subarrays where the XOR of all elements is `0`. For any such subarray from index `i` to `k`, we can place `j` at any position from `i+1` to `k`, giving us `k - i` valid triplets. This reduces the problem to finding pairs `(i, k)` where the subarray XOR is `0`.

```cpp
class Solution {
public:
    int countTriplets(vector<int>& arr) {
        int N = arr.size();
        int res = 0;

        for (int i = 0; i < N - 1; ++i) {
            int curXor = arr[i];
            for (int k = i + 1; k < N; ++k) {
                curXor ^= arr[k];
                if (curXor == 0) {
                    res += k - i;
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## 4. Math + Bitwise XOR (Optimal)

We can use prefix XOR to find subarrays with XOR equal to `0` in linear time. If `prefix[i] == prefix[k+1]`, then the XOR from index `i` to `k` is `0`. For each prefix value, we track how many times we have seen it and the sum of indices where it occurred. When we see the same prefix again at index `k`, the contribution to the result is `k * count - sum_of_indices`, where `count` is how many times this prefix appeared before, and the formula accounts for all `k - i` values.

```cpp
class Solution {
public:
    int countTriplets(vector<int>& arr) {
        int N = arr.size(), res = 0, prefix = 0;
        unordered_map<int, int> count; // number of prefixes
        unordered_map<int, int> indexSum; // sum of indices with that prefix
        count[0] = 1;

        for (int i = 0; i < N; i++) {
            prefix ^= arr[i];
            if (count.count(prefix)) {
                res += i * count[prefix] - indexSum[prefix];
            }
            count[prefix]++;
            indexSum[prefix] += i + 1;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
