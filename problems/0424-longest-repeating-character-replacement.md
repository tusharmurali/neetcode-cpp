# 424. Longest Repeating Character Replacement

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/longest-repeating-character-replacement/>  
- **NeetCode:** <https://neetcode.io/problems/longest-repeating-substring-with-replacement>  
- **Video:** <https://www.youtube.com/watch?v=gqXU1UyA8pk>  
- **Video approach:** 3. Sliding Window (Optimal)  

[← Back to index](../INDEX.md)

## 1. Brute Force

The brute-force idea is to try every possible substring starting at every index.
For each start point, we expand the substring and keep track of how many times each character appears.
A substring is valid if we can make all its characters the same by replacing at most `k` of them.
To check this, we track the **most frequent character** inside the substring — everything else would need to be replaced.
If the number of replacements needed is within `k`, we update the answer.
This works but is slow because it checks many overlapping substrings.

```cpp
class Solution {
public:
    int characterReplacement(string s, int k) {
        int res = 0;
        for (int i = 0; i < s.size(); i++) {
            unordered_map<char, int> count;
            int maxf = 0;
            for (int j = i; j < s.size(); j++) {
                count[s[j]]++;
                maxf = max(maxf, count[s[j]]);
                if ((j - i + 1) - maxf <= k) {
                    res = max(res, j - i + 1);
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(m)$

> Where $n$ is the length of the string and $m$ is the total number of unique characters in the string.

## 2. Sliding Window

We try to make a valid window where **all characters become the same**, but instead of checking every substring, we fix a target character `c` and ask:

"How long can the window be if we want the entire window to become `c` using at most `k` replacements?"

We slide a window across the string and count how many characters inside it already match `c`.
If the number of characters that **don't** match `c` is more than `k`, the window is invalid, so we shrink it from the left.
By doing this for every possible character, we find the longest valid window.

This idea is simple and beginner-friendly because we only track:

- how many characters match `c`
- how many replacements are needed

```cpp
class Solution {
public:
    int characterReplacement(std::string s, int k) {
        int res = 0;
        unordered_set<char> charSet(s.begin(), s.end());

        for (char c : charSet) {
            int count = 0, l = 0;
            for (int r = 0; r < s.size(); r++) {
                if (s[r] == c) {
                    count++;
                }

                while ((r - l + 1) - count > k) {
                    if (s[l] == c) {
                        count--;
                    }
                    l++;
                }

                res = std::max(res, r - l + 1);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m)$

> Where $n$ is the length of the string and $m$ is the total number of unique characters in the string.

## 3. Sliding Window (Optimal) ▶ video

We want the longest window where we can make all characters the same using at most `k` replacements.
Using the true current maximum frequency, the window is valid as long as:

**window size – count of the most frequent character ≤ k**

Why?
Because the characters that _aren't_ the most frequent are the ones we would need to replace.

So while expanding the window, we track:

- the frequency of each character,
- the highest frequency we have seen in the window as it grows (`maxf`).

After we shrink from the left, `maxf` may be stale because we do not decrease it.
That can temporarily make the current window look valid even when its true current maximum frequency is smaller.
This is still correct because such a stale value never increases the answer beyond a window length that was already achievable when `maxf` was accurate.

If the window is too large under this tracked `maxf`, we shrink it from the left.
This gives us one clean sliding window pass.

```cpp
class Solution {
public:
    int characterReplacement(std::string s, int k) {
        unordered_map<char, int> count;
        int res = 0;

        int l = 0, maxf = 0;
        for (int r = 0; r < s.size(); r++) {
            count[s[r]]++;
            maxf = max(maxf, count[s[r]]);

            while ((r - l + 1) - maxf > k) {
                count[s[l]]--;
                l++;
            }
            res = max(res, r - l + 1);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(m)$

> Where $n$ is the length of the string and $m$ is the total number of unique characters in the string.

## Standalone solution file (`cpp/0424-longest-repeating-character-replacement.cpp` in the NeetCode repo)

```cpp
/*
    Given a string s & an int k, can change any char k times:
    Return length of longest substring containing same letter
    Ex. s = "ABAB" k = 2 -> 4 "AAAA", s = "AABABBA" k = 1 -> 4

    Sliding window, expand if can change char, contract if > k

    Time: O(n)
    Space: O(26)
*/

class Solution {
public:
    int characterReplacement(string s, int k) {
        vector<int> count(26);
        int maxCount = 0;
        
        int i = 0;
        int j = 0;
        
        int result = 0;
        
        while (j < s.size()) {
            count[s[j] - 'A']++;
            maxCount = max(maxCount, count[s[j] - 'A']);
            if (j - i + 1 - maxCount > k) {
                count[s[i] - 'A']--;
                i++;
            }
            result = max(result, j - i + 1);
            j++;
        }
        
        return result;
    }
};
```
