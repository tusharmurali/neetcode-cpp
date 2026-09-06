# 567. Permutation In String

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/permutation-in-string/>  
- **NeetCode:** <https://neetcode.io/problems/permutation-string>  
- **Video:** <https://www.youtube.com/watch?v=UbyhOgBN834>  
- **Video approach:** 3. Sliding Window  

[← Back to index](../INDEX.md)

## 1. Brute Force

The brute-force approach tries every possible substring of `s2` and checks whether it is a permutation of `s1`.
To do this, we sort `s1` once, and then for each substring of `s2`, we sort it and compare.
If the sorted substring matches the sorted `s1`, it means the substring contains exactly the same characters.
This method is simple to understand but very slow because it examines all substrings and sorts each one.

```cpp
class Solution {
public:
    bool checkInclusion(std::string s1, std::string s2) {
        sort(s1.begin(), s1.end());

        for (int i = 0; i < s2.length(); i++) {
            for (int j = i; j < s2.length(); j++) {
                string subStr = s2.substr(i, j - i + 1);
                sort(subStr.begin(), subStr.end());

                if (subStr == s1) {
                    return true;
                }
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3 \log n)$
- Space complexity: $O(n)$

## 2. Hash Table

We first count the characters in `s1`, since any valid substring in `s2` must match these exact frequencies.
Then, for every starting point in `s2`, we build a frequency map as we extend the substring.
If we ever exceed the needed count for a character, we stop early because the substring can no longer be a valid permutation.
If all character counts match exactly, we have found a valid permutation.
This method is much cleaner than brute force but still slow because it restarts counting for each position.

```cpp
class Solution {
public:
    bool checkInclusion(string s1, string s2) {
        unordered_map<char, int> count1;
        for (char c : s1) {
            count1[c]++;
        }

        int need = count1.size();
        for (int i = 0; i < s2.length(); i++) {
            unordered_map<char, int> count2;
            int cur = 0;
            for (int j = i; j < s2.length(); j++) {
                char c = s2[j];
                count2[c]++;

                if (count1[c] < count2[c]) {
                    break;
                }

                if (count1[c] == count2[c]) {
                    cur++;
                }

                if (cur == need) {
                    return true;
                }
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

> Where $n$ is the length of the string1 and $m$ is the length of string2.

## 3. Sliding Window ▶ video

Since a permutation of `s1` must have the **same character counts**, we can use a fixed-size sliding window over `s2` whose length is exactly `len(s1)`.
We maintain two frequency arrays:

- one for `s1`
- one for the current window in `s2`

If these two arrays ever match, the window is a valid permutation.
As we slide the window forward, we update counts by removing the left character and adding the new right character — no need to rebuild the counts each time.
This makes the solution fast and efficient.

```cpp
class Solution {
public:
    bool checkInclusion(string s1, string s2) {
        if (s1.length() > s2.length()) {
            return false;
        }

        vector<int> s1Count(26, 0);
        vector<int> s2Count(26, 0);
        for (int i = 0; i < s1.length(); i++) {
            s1Count[s1[i] - 'a']++;
            s2Count[s2[i] - 'a']++;
        }

        int matches = 0;
        for (int i = 0; i < 26; i++) {
            if (s1Count[i] == s2Count[i]) {
                matches++;
            }
        }

        int l = 0;
        for (int r = s1.length(); r < s2.length(); r++) {
            if (matches == 26) {
                return true;
            }

            int index = s2[r] - 'a';
            s2Count[index]++;
            if (s1Count[index] == s2Count[index]) {
                matches++;
            } else if (s1Count[index] + 1 == s2Count[index]) {
                matches--;
            }

            index = s2[l] - 'a';
            s2Count[index]--;
            if (s1Count[index] == s2Count[index]) {
                matches++;
            } else if (s1Count[index] - 1 == s2Count[index]) {
                matches--;
            }
            l++;
        }
        return matches == 26;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0567-permutation-in-string.cpp` in the NeetCode repo)

```cpp
/*
    Given 2 strings, return true if s2 contains permutation of s1
    Ex. s1 = "ab", s2 = "eidbaooo" -> true, s2 contains "ba"

    Sliding window, expand + count down char, contract + count up char

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    bool checkInclusion(string s1, string s2) {
        int m = s1.size();
        int n = s2.size();
        if (m > n) {
            return false;
        }
        
        vector<int> count(26);
        for (int i = 0; i < m; i++) {
            count[s1[i] - 'a']++;
            count[s2[i] - 'a']--;
        }
        if (isPermutation(count)) {
            return true;
        }
        
        for (int i = m; i < n; i++) {
            count[s2[i] - 'a']--;
            count[s2[i - m] - 'a']++;
            if (isPermutation(count)) {
                return true;
            }
        }
        
        return false;
    }
private:
    bool isPermutation(vector<int>& count) {
        for (int i = 0; i < 26; i++) {
            if (count[i] != 0) {
                return false;
            }
        }
        return true;
    }
};
```
