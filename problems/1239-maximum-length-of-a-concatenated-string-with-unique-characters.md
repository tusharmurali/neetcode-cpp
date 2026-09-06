# 1239. Maximum Length of a Concatenated String With Unique Characters

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-length-of-a-concatenated-string-with-unique-characters/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-length-of-a-concatenated-string-with-unique-characters>  
- **Video:** <https://www.youtube.com/watch?v=d4SPuvkaeoo>  
- **Video approach:** 1. Backtracking (Hash Set) (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Backtracking (Hash Set) ▶ video

We want to find the longest concatenation of strings where all characters are unique. Since we need to try different combinations of strings, backtracking is a natural fit. For each string, we have two choices: include it (if it doesn't conflict with already chosen characters) or skip it. A hash set helps us efficiently check for character conflicts between the current selection and the next candidate string.

```cpp
class Solution {
public:
    int maxLength(vector<string>& arr) {
        unordered_set<char> charSet;
        return backtrack(0, arr, charSet);
    }

private:
    bool overlap(unordered_set<char>& charSet, const string& s) {
        unordered_set<char> prev;
        for (char c : s) {
            if (charSet.count(c) || prev.count(c)) {
                return true;
            }
            prev.insert(c);
        }
        return false;
    }

    int backtrack(int i, vector<string>& arr, unordered_set<char>& charSet) {
        if (i == arr.size()) {
            return charSet.size();
        }

        int res = 0;
        if (!overlap(charSet, arr[i])) {
            for (char c : arr[i]) {
                charSet.insert(c);
            }
            res = backtrack(i + 1, arr, charSet);
            for (char c : arr[i]) {
                charSet.erase(c);
            }
        }

        return max(res, backtrack(i + 1, arr, charSet));
    }
};
```

**Complexity**

- Time complexity: $O(m * 2 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

> Where $n$ is the number of strings and $m$ is the maximum length of a string.

## 2. Backtracking (Boolean Array)

Since we only deal with lowercase letters, we can replace the hash set with a fixed-size boolean array of length `26`. This provides faster lookups and updates while reducing memory overhead. The overlap check simultaneously marks characters as used, and if a conflict is found, we undo the partial marking before returning.

```cpp
class Solution {
public:
    int maxLength(vector<string>& arr) {
        bool charSet[26] = {false};
        return backtrack(0, arr, charSet);
    }

private:
    int getIdx(char c) {
        return c - 'a';
    }

    bool overlap(bool charSet[], const string& s) {
        for (int i = 0; i < s.length(); i++) {
            int c = getIdx(s[i]);
            if (charSet[c]) {
                for (int j = 0; j < i; j++) {
                    charSet[getIdx(s[j])] = false;
                }
                return true;
            }
            charSet[c] = true;
        }
        return false;
    }

    int backtrack(int i, vector<string>& arr, bool charSet[]) {
        if (i == arr.size()) {
            return 0;
        }

        int res = 0;
        if (!overlap(charSet, arr[i])) {
            res = arr[i].length() + backtrack(i + 1, arr, charSet);
            for (char c : arr[i]) {
                charSet[getIdx(c)] = false;
            }
        }
        return max(res, backtrack(i + 1, arr, charSet));
    }
};
```

**Complexity**

- Time complexity: $O(m * 2 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

> Where $n$ is the number of strings and $m$ is the maximum length of a string.

## 3. Recursion (Bit Mask) - I

We can represent the character set of each string as a bitmask, where bit `i` is set if the character `'a' + i` is present. Two strings conflict if their bitmasks share any set bits (i.e., their AND is non-zero). This allows `O(1)` conflict detection. We preprocess strings to filter out those with internal duplicates and convert valid ones to bitmasks.

```cpp
class Solution {
public:
    int maxLength(vector<string>& arr) {
        vector<pair<int, int>> A;

        for (const string& s : arr) {
            int cur = 0;
            bool valid = true;

            for (char c : s) {
                if (cur & (1 << (c - 'a'))) {
                    valid = false;
                    break;
                }
                cur |= (1 << (c - 'a'));
            }

            if (valid) {
                A.emplace_back(cur, s.length());
            }
        }

        return dfs(0, 0, A);
    }

private:
    int dfs(int i, int subSeq, vector<pair<int, int>>& A) {
        if (i == A.size()) {
            return 0;
        }

        int res = dfs(i + 1, subSeq, A);

        int curSeq = A[i].first, length = A[i].second;
        if ((subSeq & curSeq) == 0) {
            res = max(res, length + dfs(i + 1, subSeq | curSeq, A));
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n + 2 ^ n)$
- Space complexity: $O(n)$

> Where $n$ is the number of strings and $m$ is the maximum length of a string.

## 4. Recursion (Bit Mask) - II

This is a variation of the bitmask recursion that uses a different traversal pattern. Instead of explicitly choosing to skip or include each string, we iterate through all remaining strings and only recurse when we find a compatible one. This approach naturally prunes branches where strings conflict, though the overall complexity remains similar.

```cpp
class Solution {
public:
    int maxLength(vector<string>& arr) {
        vector<pair<int, int>> A;

        for (const string& s : arr) {
            int cur = 0;
            bool valid = true;

            for (char c : s) {
                if (cur & (1 << (c - 'a'))) {
                    valid = false;
                    break;
                }
                cur |= (1 << (c - 'a'));
            }

            if (valid) {
                A.emplace_back(cur, s.length());
            }
        }

        return dfs(0, 0, A);
    }

private:
    int dfs(int i, int subSeq, vector<pair<int, int>>& A) {
        int res = 0;
        for (int j = i; j < A.size(); j++) {
            int curSeq = A[j].first, length = A[j].second;
            if ((subSeq & curSeq) == 0) {
                res = max(res, length + dfs(j + 1, subSeq | curSeq, A));
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * (m  + 2 ^ n))$
- Space complexity: $O(n)$

> Where $n$ is the number of strings and $m$ is the maximum length of a string.

## 5. Dynamic Programming

Instead of recursion, we can build solutions iteratively. We maintain a set of all unique bitmasks we can achieve so far. For each new valid string, we try combining it with every existing bitmask in our set. If they don't conflict, we add the combined mask to our collection. The answer is the maximum number of set bits among all masks.

```cpp
class Solution {
public:
    int maxLength(vector<string>& arr) {
        unordered_set<int> dp;
        dp.insert(0);
        int res = 0;

        for (const string& s : arr) {
            int cur = 0;
            bool valid = true;

            for (char c : s) {
                int bit = 1 << (c - 'a');
                if (cur & bit) {
                    valid = false;
                    break;
                }
                cur |= bit;
            }

            if (!valid) {
                continue;
            }

            unordered_set<int> next_dp(dp);
            for (int seq : dp) {
                if ((seq & cur) || next_dp.count(seq | cur)) {
                    continue;
                }
                next_dp.insert(seq | cur);
                res = max(res, __builtin_popcount(seq | cur));
            }
            dp = next_dp;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * (m  + 2 ^ n))$
- Space complexity: $O(2 ^ n)$

> Where $n$ is the number of strings and $m$ is the maximum length of a string.
