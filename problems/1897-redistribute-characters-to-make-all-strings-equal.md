# 1897. Redistribute Characters to Make All Strings Equal

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/redistribute-characters-to-make-all-strings-equal/>  
- **NeetCode:** <https://neetcode.io/problems/redistribute-characters-to-make-all-strings-equal>  
- **Video:** <https://www.youtube.com/watch?v=a3SmUiimBi8>  

[← Back to index](../INDEX.md)

## 1. Frequency Count (Hash Map)

To make all strings equal, each character must be evenly distributed across all `n` strings. This means the total count of each character across all words must be divisible by `n`.

Think of it this way: if we have 6 occurrences of the letter 'a' and 3 words, each word can have exactly 2 'a's. But if we have 7 occurrences of 'a' and 3 words, there is no way to distribute them evenly.

The order of characters within each string does not matter since we can move characters freely. We only need to verify that redistribution is mathematically possible.

```cpp
class Solution {
public:
    bool makeEqual(vector<string>& words) {
        unordered_map<char, int> charCnt;

        for (const string& w : words) {
            for (char c : w) {
                charCnt[c]++;
            }
        }

        for (const auto& entry : charCnt) {
            if (entry.second % words.size() != 0) {
                return false;
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

> Where $n$ is the number of words and $m$ is the average length of each word.

## 2. Frequency Count (Array)

This approach uses the same divisibility principle but with a clever optimization. Instead of storing full counts and checking divisibility at the end, we track counts modulo `n` and use a flag counter to know whether all characters are evenly distributable.

When a character's frequency becomes divisible by `n`, it means that character can be perfectly distributed. We increment a flag when this happens and decrement it when a new character appears (since it starts at count 1, which is not divisible by `n` unless `n = 1`). At the end, if the flag is 0, all characters are evenly distributable.

```cpp
class Solution {
public:
    bool makeEqual(vector<string>& words) {
        vector<int> freq(26, 0);
        int flag = 0;
        int n = words.size();

        for (const string& w : words) {
            for (char c : w) {
                int i = c - 'a';
                if (freq[i] != 0) {
                    freq[i]++;
                    if (freq[i] % n == 0) {
                        flag++;
                    }
                } else {
                    freq[i]++;
                    if (freq[i] % n != 0) {
                        flag--;
                    }
                }
                freq[i] %= n;
            }
        }

        return flag == 0;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

> Where $n$ is the number of words and $m$ is the average length of each word.
