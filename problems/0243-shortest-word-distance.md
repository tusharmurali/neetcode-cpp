# 243. Shortest Word Distance

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/shortest-word-distance/>  
- **NeetCode:** <https://neetcode.io/problems/shortest-word-distance>  

[← Back to index](../INDEX.md)

## 1. Brute Force

```cpp
class Solution {
public:
    int shortestDistance(vector<string>& wordsDict, string word1, string word2) {
        int n = wordsDict.size();
        int res = n;
        for (int i = 0; i < n; i++) {
            if (wordsDict[i] == word1) {
                for (int j = 0; j < n; j++) {
                    if (wordsDict[j] == word2) {
                        res = min(res, abs(i - j));
                    }
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 \cdot m)$
- Space complexity: $O(1)$

> Where $n$ is the number of words in $wordsDict$ and $m$ is the maximum length of a word.

## 2. Two Pointers

```cpp
class Solution {
public:
    int shortestDistance(vector<string>& wordsDict, string word1, string word2) {
        vector<int> idx1, idx2;
        for (int i = 0; i < wordsDict.size(); i++) {
            if (wordsDict[i] == word1) {
                idx1.push_back(i);
            } else if (wordsDict[i] == word2) {
                idx2.push_back(i);
            }
        }

        int res = wordsDict.size();
        int i = 0, j = 0;
        while (i < idx1.size() && j < idx2.size()) {
            res = min(res, abs(idx1[i] - idx2[j]));
            if (idx1[i] < idx2[j]) {
                i++;
            } else {
                j++;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot m)$
- Space complexity: $O(n)$

> Where $n$ is the number of words in $wordsDict$ and $m$ is the maximum length of a word.

## 3. Iteration - I

```cpp
class Solution {
public:
    int shortestDistance(vector<string>& wordsDict, string word1, string word2) {
        int i1 = -1, i2 = -1;
        int res = wordsDict.size();
        for (int i = 0; i < wordsDict.size(); i++) {
            if (wordsDict[i] == word1) {
                i1 = i;
            } else if (wordsDict[i] == word2) {
                i2 = i;
            }

            if (i1 != -1 && i2 != -1) {
                res = min(res, abs(i1 - i2));
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot m)$
- Space complexity: $O(1)$

> Where $n$ is the number of words in $wordsDict$ and $m$ is the maximum length of a word.

## 4. Iteration - II

```cpp
class Solution {
public:
    int shortestDistance(vector<string>& wordsDict, string word1, string word2) {
        int prev = -1;
        int res = wordsDict.size();
        for (int i = 0; i < wordsDict.size(); i++) {
            if (wordsDict[i] == word1 || wordsDict[i] == word2) {
                if (prev != -1 && wordsDict[prev] != wordsDict[i]) {
                    res = min(res, i - prev);
                }
                prev = i;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot m)$
- Space complexity: $O(1)$

> Where $n$ is the number of words in $wordsDict$ and $m$ is the maximum length of a word.
