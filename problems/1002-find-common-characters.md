# 1002. Find Common Characters

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-common-characters/>  
- **NeetCode:** <https://neetcode.io/problems/find-common-characters>  
- **Video:** <https://www.youtube.com/watch?v=QEESBA2Q_88>  

[← Back to index](../INDEX.md)

## 1. Frequency Count

A character appears in all words only if it exists in every single word. Moreover, if a character appears twice in every word, we can include it twice in our result. The key insight is to track the minimum frequency of each character across all words. We start with the frequency counts from the first word, then for each subsequent word, we reduce each count to the minimum of the current count and that word's count.

```cpp
class Solution {
public:
    vector<string> commonChars(vector<string>& words) {
        vector<int> cnt(26, INT_MAX);

        for (string& word : words) {
            vector<int> curCnt(26, 0);
            for (char c : word) {
                curCnt[c - 'a']++;
            }

            for (int i = 0; i < 26; i++) {
                cnt[i] = min(cnt[i], curCnt[i]);
            }
        }

        vector<string> res;
        for (int i = 0; i < 26; i++) {
            for (int j = 0; j < cnt[i]; j++) {
                res.push_back(string(1, i + 'a'));
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity:
    - $O(1)$ extra space, since we have at most $26$ different characters.
    - $O(n * m)$ space for the output list.

> Where $n$ is the number of words and $m$ is the length of the longest word.
