# 1930. Unique Length 3 Palindromic Subsequences

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/unique-length-3-palindromic-subsequences/>  
- **NeetCode:** <https://neetcode.io/problems/unique-length-3-palindromic-subsequences>  
- **Video:** <https://www.youtube.com/watch?v=3THUt0vAFLU>  

[← Back to index](../INDEX.md)

## 1. Brute Force (Recursion)

A length-3 palindrome has the form `aba` where the first and third characters are the same. We can use recursion to generate all subsequences of length 3 and check which ones are palindromes. This explores all possible combinations by either including or excluding each character.

```cpp
class Solution {
public:
    int countPalindromicSubsequence(string s) {
        unordered_set<string> res;
        rec(s, 0, "", res);
        return res.size();
    }

private:
    void rec(const string& s, int i, string cur, unordered_set<string>& res) {
        if (cur.length() == 3) {
            if (cur[0] == cur[2]) {
                res.insert(cur);
            }
            return;
        }
        if (i == s.length()) {
            return;
        }
        rec(s, i + 1, cur, res);
        rec(s, i + 1, cur + s[i], res);
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n + m)$

> Where $n$ is the length of the string $s$ and $m$ is the number of unique three length pallindromic subsequences (26 \* 26 = 676).

## 2. Brute Force

Instead of generating all subsequences recursively, we can use three nested loops to pick positions for the three characters. For indices `i < j < k`, we check if `s[i] == s[k]` to form a palindrome. Using a set ensures we count each unique palindrome only once.

```cpp
class Solution {
public:
    int countPalindromicSubsequence(string s) {
        unordered_set<string> res;

        for (int i = 0; i < s.length() - 2; i++) {
            for (int j = i + 1; j < s.length() - 1; j++) {
                for (int k = j + 1; k < s.length(); k++) {
                    if (s[i] != s[k]) {
                        continue;
                    }
                    res.insert(string() + s[i] + s[j] + s[k]);
                }
            }
        }
        return res.size();
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3)$
- Space complexity: $O(m)$

> Where $n$ is the length of the string $s$ and $m$ is the number of unique three length pallindromic subsequences (26 \* 26 = 676).

## 3. Sequential Matching for Each Palindrome

Since we only have 26 lowercase letters, there are at most 26 \* 26 = 676 possible palindromes of length 3 (26 choices for the end characters, 26 for the middle). We can check each potential palindrome by scanning the string once to see if it exists as a subsequence.

```cpp
class Solution {
public:
    int countPalindromicSubsequence(string s) {
        int res = 0;
        for (char ends = 'a'; ends <= 'z'; ends++) {
            for (char mid = 'a'; mid <= 'z'; mid++) {
                string seq = string() + ends + mid + ends;
                int idx = 0, found = 0;
                for (char& c : s) {
                    if (seq[idx] == c) {
                        idx++;
                        if (idx == 3) {
                            found = 1;
                            break;
                        }
                    }
                }
                res += found;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(1)$

> Where $n$ is the length of the string $s$ and $m$ is the number of unique three length pallindromic subsequences (26 \* 26 = 676).

## 4. Iterate On Middle Characters

Instead of checking all possible palindromes, we can iterate through the string and treat each position as a potential middle character. For each middle position, we need to know which characters appear both before and after it. A palindrome exists if the same character appears on both sides.

```cpp
class Solution {
public:
    int countPalindromicSubsequence(string s) {
        unordered_set<string> res;
        unordered_set<char> left;
        vector<int> right(26, 0);

        for (char c : s) {
            right[c - 'a']++;
        }

        for (int i = 0; i < s.length(); i++) {
            right[s[i] - 'a']--;
            if (right[s[i] - 'a'] == 0) {
                right[s[i] - 'a'] = -1;
            }

            for (int j = 0; j < 26; j++) {
                char c = 'a' + j;
                if (left.count(c) && right[j] > 0) {
                    res.insert(string() + s[i] + c);
                }
            }
            left.insert(s[i]);
        }

        return res.size();
    }
};
```

**Complexity**

- Time complexity: $O(26 * n)$
- Space complexity: $O(m)$

> Where $n$ is the length of the string $s$ and $m$ is the number of unique three length pallindromic subsequences (26 \* 26 = 676).

## 5. Prefix Count

We can precompute prefix counts for each character, allowing us to quickly determine how many of each character appear in any substring. For each possible end character, we find its first and last occurrence, then count distinct middle characters between them using prefix sums.

```cpp
class Solution {
public:
    int countPalindromicSubsequence(string s) {
        int n = s.length();
        vector<vector<int>> prefix(n + 1, vector<int>(26));
        vector<int> firstIndex(26, -1);
        vector<int> lastIndex(26, -1);

        for (int i = 0; i < n; i++) {
            int j = s[i] - 'a';
            if (firstIndex[j] == -1) {
                firstIndex[j] = i;
            }
            lastIndex[j] = i;
            prefix[i + 1] = prefix[i];
            prefix[i + 1][j]++;
        }

        int res = 0;
        for (int ends = 0; ends < 26; ends++) {
            if (firstIndex[ends] == -1 || firstIndex[ends] == lastIndex[ends]) {
                continue;
            }
            int l = firstIndex[ends], r = lastIndex[ends];
            for (int mid = 0; mid < 26; mid++) {
                if (prefix[r][mid] - prefix[l + 1][mid] > 0) {
                    res++;
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(26 * n)$
- Space complexity: $O(26 * n)$

## 6. First And Last Index

For a length-3 palindrome with character `c` at both ends, we need at least two occurrences of `c`. The palindrome can use any character between the first and last occurrence of `c` as the middle. By finding the first and last index of each character, we can count the distinct characters in between.

```cpp
class Solution {
public:
    int countPalindromicSubsequence(string s) {
        int res = 0;

        for (char c = 'a'; c <= 'z'; c++) {
            int l = s.find(c), r = s.rfind(c);
            if (l == -1 || l == r) continue;

            unordered_set<char> mids;
            for (int j = l + 1; j < r; j++) {
                mids.insert(s[j]);
            }
            res += mids.size();
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(26 * n)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

## 7. First And Last Index (Optimal)

The previous approach uses a set to track distinct middle characters, which has some overhead. We can use a bitmask instead, where each bit represents whether a character has been seen. This provides O(1) operations for checking and adding characters.

```cpp
class Solution {
public:
    int countPalindromicSubsequence(string s) {
        vector<int> firstIndex(26, -1);
        vector<int> lastIndex(26, -1);

        for (int i = 0; i < s.size(); i++) {
            int j = s[i] - 'a';
            if (firstIndex[j] == -1) {
                firstIndex[j] = i;
            }
            lastIndex[j] = i;
        }

        int res = 0;
        for (int ends = 0; ends < 26; ends++) {
            if (firstIndex[ends] == -1 || firstIndex[ends] == lastIndex[ends]) {
                continue;
            }
            int l = firstIndex[ends], r = lastIndex[ends];
            int mask = 0;
            for (int i = l + 1; i < r; i++) {
                int c = s[i] - 'a';
                if (mask & (1 << c)) {
                    continue;
                }
                mask |= (1 << c);
                res++;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(26 * n)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

## Standalone solution file (`cpp/1930-unique-length-3-palindromic-subsequences.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int countPalindromicSubsequence(string s) {
        vector<pair<int, int>> v(26, {-1, -1});
        for (int i = 0; i < s.size(); i++) {
            if (v[s[i] - 'a'].first == -1) v[s[i] - 'a'].first = i;
            else v[s[i] - 'a'].second = i;
        }
        
        int res = 0;
        for (int i = 0; i < 26; i++) {
            if (v[i].second != -1) {
                unordered_set<char> tmp;
                for (int j = v[i].first + 1; j < v[i].second; j++) tmp.insert(s[j]);
                res += tmp.size();
            }
        }
        
        return res;
    }
};
```
