# 1624. Largest Substring Between Two Equal Characters

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/largest-substring-between-two-equal-characters/>  
- **NeetCode:** <https://neetcode.io/problems/largest-substring-between-two-equal-characters>  
- **Video:** <https://www.youtube.com/watch?v=66b2V_rCuJw>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We need to find two equal characters and maximize the number of characters between them. The straightforward approach checks every pair of indices to see if they contain the same character, then computes the distance between them.

```cpp
class Solution {
public:
    int maxLengthBetweenEqualCharacters(string s) {
        int n = s.size();
        int res = -1;

        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (s[i] == s[j]) {
                    res = max(res, j - i - 1);
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. First And Last Index

To maximize the distance between two equal characters, we want the first occurrence and the last occurrence of each character. By recording both indices for every character, we can compute the maximum span in a single pass through the string, followed by a pass through the recorded data.

```cpp
class Solution {
public:
    int maxLengthBetweenEqualCharacters(string s) {
        unordered_map<char, int> firstIdx, lastIdx;
        int res = -1;

        for (int i = 0; i < s.size(); i++) {
            if (firstIdx.find(s[i]) == firstIdx.end()) {
                firstIdx[s[i]] = i;
            } else {
                lastIdx[s[i]] = i;
            }
        }

        for (auto& [c, idx] : lastIdx) {
            res = max(res, lastIdx[c] - firstIdx[c] - 1);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

## 3. First Index (Hash Map)

We only need to track the first occurrence of each character. As we encounter a character again, we can immediately compute the distance from its first occurrence. This approach uses a single hash map and computes the answer in one pass.

```cpp
class Solution {
public:
    int maxLengthBetweenEqualCharacters(string s) {
        unordered_map<char, int> charIndex;
        int res = -1;

        for (int i = 0; i < s.size(); i++) {
            if (charIndex.find(s[i]) != charIndex.end()) {
                res = max(res, i - charIndex[s[i]] - 1);
            } else {
                charIndex[s[i]] = i;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

## 4. First Index (Array)

Since the input contains only lowercase letters, we can replace the hash map with a fixed-size array of `26` elements. This provides constant-time lookups and slightly better cache performance.

```cpp
class Solution {
public:
    int maxLengthBetweenEqualCharacters(string s) {
        int firstIdx[26];
        fill(begin(firstIdx), end(firstIdx), -1);
        int res = -1;

        for (int i = 0; i < s.size(); i++) {
            int j = s[i] - 'a';
            if (firstIdx[j] != -1) {
                res = max(res, i - firstIdx[j] - 1);
            } else {
                firstIdx[j] = i;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.
