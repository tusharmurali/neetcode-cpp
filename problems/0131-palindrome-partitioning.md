# 131. Palindrome Partitioning

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/palindrome-partitioning/>  
- **NeetCode:** <https://neetcode.io/problems/palindrome-partitioning>  
- **Video:** <https://www.youtube.com/watch?v=3jvWodd7ht0>  
- **Video approach:** 2. Backtracking - II  

[← Back to index](../INDEX.md)

## 1. Backtracking - I

We want to split the string into **pieces**, but we only keep a split if **every piece is a palindrome**.

Think of placing “cuts” in the string:

- Start at some index `j` (start of the next piece).
- Try to extend the end index `i` to form a substring `s[j..i]`.
- If `s[j..i]` is a palindrome, we **choose it** (put it into `part`) and then restart from the next position (`i+1`) to build the next piece.
- Whether or not it was a palindrome, we can also **extend further** by moving `i` to `i+1` (trying a longer substring from the same start `j`).

Backtracking means:

- When we choose a palindrome piece, we go deeper.
- After returning, we remove that piece and try other possibilities.

```cpp
class Solution {
    vector<vector<string>> res;
public:
    vector<vector<string>> partition(string s) {
        vector<string> part;
        dfs(0, 0, s, part);
        return res;
    }

    void dfs(int j, int i, string &s, vector<string> &part) {
        if (i >= s.size()) {
            if (i == j) {
                res.push_back(part);
            }
            return;
        }

        if (isPali(s, j, i)) {
            part.push_back(s.substr(j, i - j + 1));
            dfs(i + 1, i + 1, s, part);
            part.pop_back();
        }

        dfs(j, i + 1, s, part);
    }

    bool isPali(string &s, int l, int r) {
        while (l < r) {
            if (s[l] != s[r]) {
                return false;
            }
            l++;
            r--;
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity:
    - $O(n)$ extra space.
    - $O(n * 2 ^ n)$ space for the output list.

## 2. Backtracking - II ▶ video

We build the partition **from left to right**.

At any starting index `i`, we have a simple question:

> “Where should I cut next?”

So we try **every possible end index `j`** from `i` to end:

- If `s[i..j]` is a palindrome, it can be the **next piece**.
- Choose it (add to `part`), then recursively solve the rest starting at `j + 1`.
- After coming back, undo the choice (pop) and try a different `j`.

This guarantees:

- We only add **palindrome pieces**.
- We explore **all valid ways** to cut the string.

```cpp
class Solution {
public:
    vector<vector<string>> partition(string s) {
        vector<vector<string>> res;
        vector<string> part;
        dfs(0, s, part, res);
        return res;
    }

private:
    void dfs(int i, const string& s, vector<string>& part, vector<vector<string>>& res) {
        if (i >= s.length()) {
            res.push_back(part);
            return;
        }
        for (int j = i; j < s.length(); j++) {
            if (isPali(s, i, j)) {
                part.push_back(s.substr(i, j - i + 1));
                dfs(j + 1, s, part, res);
                part.pop_back();
            }
        }
    }

    bool isPali(const string& s, int l, int r) {
        while (l < r) {
            if (s[l] != s[r]) {
                return false;
            }
            l++;
            r--;
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity:
    - $O(n)$ extra space.
    - $O(n * 2 ^ n)$ space for the output list.

## 3. Backtracking (DP)

In plain backtracking, we **repeatedly check** whether substrings are palindromes, which costs extra time.  
To optimize this, we **precompute all palindrome substrings once** using Dynamic Programming (DP).

Idea:

- First, build a DP table `dp[i][j]` that tells whether `s[i..j]` is a palindrome.
- Then use backtracking just like before, but instead of checking palindromes on the fly, we **directly look up `dp[i][j]`**.

This makes backtracking faster because palindrome checks become **O(1)**.

```cpp
class Solution {
    vector<vector<bool>> dp;
public:
    vector<vector<string>> partition(string s) {
        int n = s.length();
        dp.resize(n, vector<bool>(n));
        for (int l = 1; l <= n; l++) {
            for (int i = 0; i <= n - l; i++) {
                dp[i][i + l - 1] = (s[i] == s[i + l - 1] &&
                                    (i + 1 > (i + l - 2) ||
                                    dp[i + 1][i + l - 2]));
            }
        }

        vector<vector<string>> res;
        vector<string> part;
        dfs(0, s, part, res);
        return res;
    }

private:
    void dfs(int i, const string& s, vector<string>& part, vector<vector<string>>& res) {
        if (i >= s.length()) {
            res.push_back(part);
            return;
        }
        for (int j = i; j < s.length(); j++) {
            if (dp[i][j]) {
                part.push_back(s.substr(i, j - i + 1));
                dfs(j + 1, s, part, res);
                part.pop_back();
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity:
    - $O(n ^ 2)$ extra space.
    - $O(n * 2 ^ n)$ space for the output list.

## 4. Recursion

This approach combines **Dynamic Programming** and **pure recursion (return-based)**.

- We first **precompute all palindromic substrings** using DP.
- Then we use recursion where each recursive call:
    - **returns all valid palindrome partitions** starting from a given index.
- Instead of maintaining a global result or path, each recursive call builds and **returns its own list of partitions**, which makes the logic clean and declarative.

Think of it as:

> “All partitions starting at index `i` =  
> choose a palindrome `s[i..j]` + all partitions starting at `j + 1`”

```cpp
class Solution {
public:
    vector<vector<string>> partition(string s) {
        int n = s.size();
        vector<vector<bool>> dp(n, vector<bool>(n, false));
        for (int l = 1; l <= n; l++) {
            for (int i = 0; i <= n - l; i++) {
                dp[i][i + l - 1] = (s[i] == s[i + l - 1] &&
                                    (i + 1 > (i + l - 2) ||
                                    dp[i + 1][i + l - 2]));
            }
        }

        return dfs(s, dp, 0);
    }

    vector<vector<string>> dfs(string& s, vector<vector<bool>>& dp, int i) {
        if (i >= s.size()) {
            return {{}};
        }

        vector<vector<string>> ret;
        for (int j = i; j < s.size(); j++) {
            if (dp[i][j]) {
                auto nxt = dfs(s, dp, j + 1);
                for (auto& part : nxt) {
                    vector<string> cur;
                    cur.push_back(s.substr(i, j - i + 1));
                    cur.insert(cur.end(), part.begin(), part.end());
                    ret.push_back(cur);
                }
            }
        }
        return ret;
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity:
    - $O(n ^ 2)$ extra space.
    - $O(n * 2 ^ n)$ space for the output list.

## Standalone solution file (`cpp/0131-palindrome-partitioning.cpp` in the NeetCode repo)

```cpp
/*
    Given a string, partition such that every substring is a palindrome, return all possible ones
    Ex. s = "aab" -> [["a","a","b"],["aa","b"]], s = "a" -> [["a"]]

    Generate all possible substrings at idx, if palindrome potential candidate, backtrack after

    Time: O(n x 2^n)
    Space: O(n)
*/

class Solution {
public:
    vector<vector<string>> partition(string s) {
        vector<string> curr;
        vector<vector<string>> result;
        dfs(s, 0, curr, result);
        return result;
    }
private:
    void dfs(string s, int start, vector<string>& curr, vector<vector<string>>& result) {
        if (start == s.size()) {
            result.push_back(curr);
            return;
        }
        for (int i = start; i < s.size(); i++) {
            if (isPalindrome(s, start, i)) {
                string str = s.substr(start, i - start + 1);
                curr.push_back(str);
                dfs(s, i + 1, curr, result);
                curr.pop_back();
            }
        }
    }
    bool isPalindrome(string s, int left, int right) {
        while (left < right) {
            if (s[left] != s[right]) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }
};
```
