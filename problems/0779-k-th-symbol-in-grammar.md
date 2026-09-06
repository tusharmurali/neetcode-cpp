# 779. K-th Symbol in Grammar

- **Difficulty:** Medium  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/k-th-symbol-in-grammar/>  
- **NeetCode:** <https://neetcode.io/problems/k-th-symbol-in-grammar>  
- **Video:** <https://www.youtube.com/watch?v=pmD2HCKaqRQ>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The problem generates rows where each row is built from the previous one: `0` becomes `01` and `1` becomes `10`. The most straightforward approach is to actually build each row until we reach row `n`, then return the character at position `k`. While simple to understand, this approach becomes impractical for large `n` since each row doubles in size.

```cpp
class Solution {
public:
    int kthGrammar(int n, int k) {
        vector<char> prev = {'0'};
        for (int i = 2; i <= n; i++) {
            vector<char> cur;
            for (char c : prev) {
                if (c == '0') {
                    cur.push_back('0');
                    cur.push_back('1');
                } else {
                    cur.push_back('1');
                    cur.push_back('0');
                }
            }
            prev = cur;
        }
        return prev[k - 1] - '0';
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(2 ^ n)$

## 2. Binary Tree Traversal (Recursion)

We can visualize the grammar as a binary tree where each node generates two children. The key insight is that the position `k` in row `n` has a parent at position `ceil(k/2)` in row `n-1`. If `k` is in the left half of the current row, it inherits the parent's value directly. If `k` is in the right half, its value is the flip of the parent. This lets us trace from position `k` back to the root without building any rows.

```cpp
class Solution {
public:
    int kthGrammar(int n, int k) {
        return dfs(n, k, 0);
    }

    int dfs(int n, int k, int root){
        if (n == 1) return root;

        int total = 1 << (n - 1);
        if (k > total / 2) {
            return dfs(n - 1, k - total / 2, root ^ 1);
        } else {
            return dfs(n - 1, k, root);
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 3. Binary Tree Traversal (Iteration)

This is the iterative version of the binary tree approach. Instead of recursion, we use a loop to perform binary search on the position. We maintain a range `[left, right]` representing the current segment and track whether the value flips as we narrow down to position `k`. Each iteration halves the search space until we've processed all `n - 1` levels.

```cpp
class Solution {
public:
    int kthGrammar(int n, int k) {
        int cur = 0;
        int left = 1, right = 1 << (n - 1);

        for (int i = 0; i < n - 1; i++) {
            int mid = (left + right) / 2;
            if (k <= mid) {
                right = mid;
            } else {
                left = mid + 1;
                cur = (cur == 0) ? 1 : 0;
            }
        }

        return cur;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 4. Recursion (Traverse Towards Root)

Each position in row `n` comes from a parent position in row `n-1`. If position `k` is odd, it's a left child and has the same value as its parent at position `(k+1)/2`. If `k` is even, it's a right child and has the opposite value. We recursively trace back to row 1 (which is always `0`) and determine the value based on how many flips occurred.

```cpp
class Solution {
public:
    int kthGrammar(int n, int k) {
        if (n == 1) {
            return 0;
        }
        if (k & 1) {
            return kthGrammar(n - 1, (k + 1) / 2);
        }
        return kthGrammar(n - 1, k / 2) ^ 1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 5. Math

There's an elegant mathematical pattern here. The value at position `k` depends on how many times we flip while tracing from `k` back to the root. Each flip happens when we're a right child, which corresponds to a `1` bit in the binary representation of `k - 1`. So the answer is simply the parity (odd or even) of the number of `1` bits in `k - 1`.

```cpp
class Solution {
public:
    int kthGrammar(int n, int k) {
        return __builtin_popcount(k - 1) & 1;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$ or $O(\log n)$ depending on the language.
