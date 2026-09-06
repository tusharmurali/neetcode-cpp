# 916. Word Subsets

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/word-subsets/>  
- **NeetCode:** <https://neetcode.io/problems/word-subsets>  
- **Video:** <https://www.youtube.com/watch?v=LFX61XMU22c>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A word from `words1` is "universal" if every word in `words2` is a subset of it. For a word to be a subset of another, every character must appear at least as many times in the target word. The straightforward approach is to check each word in `words1` against all words in `words2`, comparing character frequencies to determine if all `words2` words are subsets of `words1`.

```cpp
class Solution {
public:
    vector<string> wordSubsets(vector<string>& words1, vector<string>& words2) {
        vector<string> res;

        for (const string& w1 : words1) {
            vector<int> count1(26, 0);
            for (char c : w1) count1[c - 'a']++;

            bool isSubset = true;
            for (const string& w2 : words2) {
                vector<int> count2(26, 0);
                for (char c : w2) count2[c - 'a']++;

                for (int i = 0; i < 26; i++) {
                    if (count2[i] > count1[i]) {
                        isSubset = false;
                        break;
                    }
                }

                if (!isSubset) break;
            }

            if (isSubset) res.push_back(w1);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(N * n + N * M * m)$
- Space complexity:
    - $O(1)$ extra space, since we have at most $26$ different characters.
    - $O(N * n)$ space for the output list.

> Where $N$ is the size of the array $words1$, $n$ is the length of the longest word in $words1$, $M$ is the size of the array $words2$, and $m$ is the length of the longest word in $words2$.

## 2. Greedy + Hash Map

Instead of checking every word in `words2` for each candidate, we can precompute a single "maximum requirement" array. The key insight is that if a word is universal, it must satisfy all words in `words2` simultaneously. This means for each character, we only need the maximum count required across all words in `words2`. By merging all requirements into one frequency map, we reduce the problem to a single comparison per candidate `word`.

```cpp
class Solution {
public:
    vector<string> wordSubsets(vector<string>& words1, vector<string>& words2) {
        vector<int> count2(26, 0);
        for (string& w : words2) {
            vector<int> countW(26, 0);
            for (char c : w) countW[c - 'a']++;
            for (int i = 0; i < 26; ++i)
                count2[i] = max(count2[i], countW[i]);
        }

        vector<string> res;
        for (string& w : words1) {
            vector<int> countW(26, 0);
            for (char c : w) countW[c - 'a']++;

            bool flag = true;
            for (int i = 0; i < 26; ++i) {
                if (countW[i] < count2[i]) {
                    flag = false;
                    break;
                }
            }

            if (flag) res.push_back(w);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(N * n + M * m)$
- Space complexity:
    - $O(1)$ extra space, since we have at most $26$ different characters.
    - $O(N * n)$ space for the output list.

> Where $N$ is the size of the array $words1$, $n$ is the length of the longest word in $words1$, $M$ is the size of the array $words2$, and $m$ is the length of the longest word in $words2$.
