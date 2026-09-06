# 2381. Shifting Letters II

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/shifting-letters-ii/>  
- **NeetCode:** <https://neetcode.io/problems/shifting-letters-ii>  
- **Video:** <https://www.youtube.com/watch?v=eEUjVY7wK3k>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The straightforward approach is to apply each shift operation directly. For each shift, we iterate through the specified range and increment or decrement each character. Since characters wrap around the alphabet, we use modulo 26 arithmetic.

This approach is simple but slow because we might repeatedly process the same characters across multiple overlapping shifts.

```cpp
class Solution {
public:
    string shiftingLetters(string s, vector<vector<int>>& shifts) {
        vector<int> letters(s.size());
        for (int i = 0; i < s.size(); i++) {
            letters[i] = s[i] - 'a';
        }

        for (const auto& shift : shifts) {
            int l = shift[0], r = shift[1], d = shift[2];
            for (int i = l; i <= r; i++) {
                letters[i] = (letters[i] + (d == 1 ? 1 : -1) + 26) % 26;
            }
        }

        for (int i = 0; i < s.size(); i++) {
            s[i] = letters[i] + 'a';
        }

        return s;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n)$

> Where $n$ is the length of the string $s$ and $m$ is the size of the array $shifts$.

## 2. Sweep Line Algorithm

Instead of applying each shift individually, we can use a difference array technique. The idea is to mark where shifts begin and end, then compute the cumulative effect as we scan through the string.

For a shift affecting range `[l, r]`, we add the shift value at index `l` and subtract it at index `r + 1`. When we compute the running sum (prefix sum) of this difference array, each position automatically accumulates the total shift from all overlapping operations.

```cpp
class Solution {
public:
    string shiftingLetters(string s, vector<vector<int>>& shifts) {
        int n = s.size();
        vector<int> prefix_diff(n + 1, 0);

        for (auto& shift : shifts) {
            int left = shift[0], right = shift[1], d = shift[2];
            int val = d == 1 ? 1 : -1;
            prefix_diff[left] += val;
            prefix_diff[right + 1] -= val;
        }

        int diff = 0;
        vector<int> res(n);
        for (int i = 0; i < n; ++i) {
            res[i] = s[i] - 'a';
        }

        for (int i = 0; i < n; ++i) {
            diff += prefix_diff[i];
            res[i] = (diff % 26 + res[i] + 26) % 26;
        }

        for (int i = 0; i < n; ++i) {
            s[i] = 'a' + res[i];
        }

        return s;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n)$

> Where $n$ is the length of the string $s$ and $m$ is the size of the array $shifts$.

## 3. Binary Indexed Tree (Fenwick Tree)

A Binary Indexed Tree (BIT) efficiently handles range updates and point queries. For this problem, we use the BIT to support range updates: when we need to add a value to all elements in range `[l, r]`, we update at position `l` and cancel at position `r + 1`.

When querying, the prefix sum at any index gives us the total accumulated shift for that position. This is useful when shifts need to be applied dynamically or when we need to query intermediate results.

```cpp
class BIT {
    vector<int> tree;
    int n;
public:
    BIT(int size) {
        n = size + 2;
        tree.assign(n, 0);
    }

    void update(int index, int delta) {
        index++;
        while (index < n) {
            tree[index] += delta;
            index += index & -index;
        }
    }

    int prefixSum(int index) {
        index++;
        int sum = 0;
        while (index > 0) {
            sum += tree[index];
            index -= index & -index;
        }
        return sum;
    }

    void rangeUpdate(int left, int right, int delta) {
        update(left, delta);
        update(right + 1, -delta);
    }
};

class Solution {
public:
    string shiftingLetters(string s, vector<vector<int>>& shifts) {
        int n = s.size();
        BIT bit(n);

        for (auto& shift : shifts) {
            int left = shift[0], right = shift[1], d = shift[2];
            int delta = d == 1 ? 1 : -1;
            bit.rangeUpdate(left, right, delta);
        }

        string res;
        for (int i = 0; i < n; i++) {
            int shift = bit.prefixSum(i) % 26;
            int code = (s[i] - 'a' + shift + 26) % 26;
            res += char('a' + code);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O((m + n) * \log n)$
- Space complexity: $O(n)$

> Where $n$ is the length of the string $s$ and $m$ is the size of the array $shifts$.
