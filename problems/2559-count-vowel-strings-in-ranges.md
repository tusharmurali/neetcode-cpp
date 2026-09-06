# 2559. Count Vowel Strings in Ranges

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/count-vowel-strings-in-ranges/>  
- **NeetCode:** <https://neetcode.io/problems/count-vowel-strings-in-ranges>  
- **Video:** <https://www.youtube.com/watch?v=TLJd7W-z-yc>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A word is a "vowel string" if it starts and ends with a vowel (a, e, i, o, u). For each query, we need to count how many words in the given range satisfy this condition. The straightforward approach is to iterate through the range for each query and check each word.

```cpp
class Solution {
public:
    vector<int> vowelStrings(vector<string>& words, vector<vector<int>>& queries) {
        unordered_set<char> vowels = {'a', 'e', 'i', 'o', 'u'};
        vector<int> res;

        for (auto& q : queries) {
            int start = q[0], end = q[1], count = 0;

            for (int i = start; i <= end; i++) {
                if (vowels.count(words[i][0]) && vowels.count(words[i].back())) {
                    count++;
                }
            }

            res.push_back(count);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(m)$ space for the output list.

> Where $n$ is the number of words, and $m$ is the number of queries.

## 2. Prefix Sum + Hash Set

The brute force approach recomputes the count for overlapping or similar ranges repeatedly. We can precompute a prefix sum array where `prefix[i]` stores the count of vowel strings from index `0` to `i-1`. Then any range query `(l, r)` can be answered in O(1) time as `prefix[r+1] - prefix[l]`.

```cpp
class Solution {
public:
    vector<int> vowelStrings(vector<string>& words, vector<vector<int>>& queries) {
        unordered_set<char> vowels = {'a', 'e', 'i', 'o', 'u'};
        int n = words.size();
        vector<int> prefixCnt(n + 1, 0);

        for (int i = 0; i < n; i++) {
            prefixCnt[i + 1] = prefixCnt[i];
            if (vowels.count(words[i][0]) && vowels.count(words[i].back())) {
                prefixCnt[i + 1]++;
            }
        }

        vector<int> res;
        for (auto& q : queries) {
            int l = q[0], r = q[1];
            res.push_back(prefixCnt[r + 1] - prefixCnt[l]);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity:
    - $O(n)$ extra space.
    - $O(m)$ space for the output list.

> Where $n$ is the number of words, and $m$ is the number of queries.

## 3. Prefix Sum + Bitmask

Instead of using a hash set to check vowels, we can use a bitmask. Since there are only 5 vowels and 26 letters, we can represent which characters are vowels using a single integer where bit `i` is set if the character at position `i` (`'a' + i`) is a vowel. Checking if a character is a vowel becomes a simple bitwise AND operation.

```cpp
class Solution {
public:
    vector<int> vowelStrings(vector<string>& words, vector<vector<int>>& queries) {
        int vowels = 0;
        for (char c : string("aeiou")) {
            vowels |= (1 << (c - 'a'));
        }

        int n = words.size();
        vector<int> prefix(n + 1);
        for (int i = 0; i < n; i++) {
            int f = words[i][0] - 'a';
            int l = words[i].back() - 'a';
            int isVowel = ((1 << f) & vowels) && ((1 << l) & vowels);
            prefix[i + 1] = prefix[i] + isVowel;
        }

        vector<int> res;
        for (auto& q : queries) {
            int l = q[0], r = q[1];
            res.push_back(prefix[r + 1] - prefix[l]);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity:
    - $O(n)$ extra space.
    - $O(m)$ space for the output list.

> Where $n$ is the number of words, and $m$ is the number of queries.
