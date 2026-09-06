# 76. Minimum Window Substring

- **Difficulty:** Hard  
- **Pattern:** Sliding Window  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/minimum-window-substring/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-window-with-characters>  
- **Video:** <https://www.youtube.com/watch?v=jSto0O4AJbM>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We want the smallest substring of `s` that contains all characters of `t` (with the right counts).
The brute-force way is to try **every possible substring** of `s` and check whether it covers all the characters in `t`.
For each starting index, we expand the end index and keep a frequency map for the current substring.
Whenever the substring has all required characters, we see if it's the smallest one so far.
This is simple to understand but very slow because we check many overlapping substrings.

```cpp
class Solution {
public:
    string minWindow(string s, string t) {
        if (t.empty()) return "";

        unordered_map<char, int> countT;
        for (char c : t) {
            countT[c]++;
        }

        pair<int, int> res = {-1, -1};
        int resLen = INT_MAX;

        for (int i = 0; i < s.length(); i++) {
            unordered_map<char, int> countS;
            for (int j = i; j < s.length(); j++) {
                countS[s[j]]++;

                bool flag = true;
                for (auto &[c, cnt] : countT) {
                    if (countS[c] < cnt) {
                        flag = false;
                        break;
                    }
                }

                if (flag && (j - i + 1) < resLen) {
                    resLen = j - i + 1;
                    res = {i, j};
                }
            }
        }

        return resLen == INT_MAX ? "" : s.substr(res.first, resLen);
    }
};
```

**Complexity**

- Time complexity: $O(m + n ^ 2 * u)$
- Space complexity: $O(k)$

> Where $n$ is the length of the string $s$, $m$ is the length of the string $t$, $u$ is the number of unique characters in $t$, and $k$ is the total number of unique characters in $s$ and $t$.

## 2. Sliding Window

We want the **smallest window in `s`** that contains all characters of `t` (with the right counts).
Instead of checking all substrings, we use a **sliding window**:

- Expand the window by moving the right pointer `r` and adding characters into a `window` map.
- Once the window has all required characters (i.e., it "covers" `t`), we try to **shrink it from the left** with pointer `l` to make it as small as possible while still valid.

During this process, we keep track of the best (smallest) window seen so far.
This way, we only scan each character at most two times, making it efficient and still easy to follow.

```cpp
class Solution {
public:
    string minWindow(string s, string t) {
        if (t.empty()) return "";

        unordered_map<char, int> countT, window;
        for (char c : t) {
            countT[c]++;
        }

        int have = 0, need = countT.size();
        pair<int, int> res = {-1, -1};
        int resLen = INT_MAX;
        int l = 0;

        for (int r = 0; r < s.length(); r++) {
            char c = s[r];
            window[c]++;

            if (countT.count(c) && window[c] == countT[c]) {
                have++;
            }

            while (have == need) {
                if ((r - l + 1) < resLen) {
                    resLen = r - l + 1;
                    res = {l, r};
                }

                window[s[l]]--;
                if (countT.count(s[l]) && window[s[l]] < countT[s[l]]) {
                    have--;
                }
                l++;
            }
        }

        return resLen == INT_MAX ? "" : s.substr(res.first, resLen);
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(k)$

> Where $n$ is the length of the string $s$, $m$ is the length of the string $t$, and $k$ is the total number of unique characters in $s$ and $t$.
>
> Building the frequency map takes $O(m)$ time. During the sliding-window pass, the right pointer traverses $s$ once and the left pointer advances at most $n$ times in total, so this pass takes $O(2n) = O(n)$ time.

## Standalone solution file (`cpp/0076-minimum-window-substring.cpp` in the NeetCode repo)

```cpp
/*
    Given 2 strings s & t, return min window substring
    of s such that all chars in t are included in window
    Ex. s = "ADOBECODEBANC" t = "ABC" -> "BANC"

    Sliding window + hash map {char -> count}
    Move j until valid, move i to find smaller

    Time: O(m + n)
    Space: O(m + n)
*/

class Solution {
public:
    string minWindow(string s, string t) {
        // count of char in t
        unordered_map<char, int> m;
        for (int i = 0; i < t.size(); i++) {
            m[t[i]]++;
        }
        
        int i = 0;
        int j = 0;
        
        // # of chars in t that must be in s
        int counter = t.size();
        
        int minStart = 0;
        int minLength = INT_MAX;
        
        while (j < s.size()) {
            // if char in s exists in t, decrease
            if (m[s[j]] > 0) {
                counter--;
            }
            // if char doesn't exist in t, will be -'ve
            m[s[j]]--;
            // move j to find valid window
            j++;
            
            // when window found, move i to find smaller
            while (counter == 0) {
                if (j - i < minLength) {
                    minStart = i;
                    minLength = j - i;
                }
                
                m[s[i]]++;
                // when char exists in t, increase
                if (m[s[i]] > 0) {
                    counter++;
                }
                i++;
            }
        }
        
        if (minLength != INT_MAX) {
            return s.substr(minStart, minLength);
        }
        return "";
    }
};
```
