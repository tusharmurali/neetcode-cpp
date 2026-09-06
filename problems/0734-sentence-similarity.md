# 734. Sentence Similarity

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/sentence-similarity/>  
- **NeetCode:** <https://neetcode.io/problems/sentence-similarity>  

[← Back to index](../INDEX.md)

## 1. Using Hash Map and Hash Set

Two sentences are similar if they have the same length and each pair of corresponding words is either identical or defined as similar in the given pairs. To check similarity efficiently, we build a lookup structure: a hash map where each word maps to a set of its similar words. Since similarity is symmetric, we add both directions for each pair. Then we simply iterate through both sentences and verify each word pair using `wordToSimilarWords`.

```cpp
class Solution {
public:
    bool areSentencesSimilar(vector<string>& sentence1, vector<string>& sentence2,
                             vector<vector<string>>& similarPairs) {
        if (sentence1.size() != sentence2.size()) {
            return false;
        }
        unordered_map<string, unordered_set<string>> wordToSimilarWords;
        for (auto& pair : similarPairs) {
            wordToSimilarWords[pair[0]].insert(pair[1]);
            wordToSimilarWords[pair[1]].insert(pair[0]);
        }

        for (int i = 0; i < sentence1.size(); i++) {
            // If the words are equal, continue.
            if (sentence1[i] == sentence2[i]) {
                continue;
            }
            // If the words form a similar pair, continue.
            if (wordToSimilarWords[sentence1[i]].count(sentence2[i])) {
                continue;
            }
            return false;
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O((n + k) \cdot m)$
- Space complexity: $O(k\cdot m)$

> Where $n$ is the number of words in `sentence1` and `sentence2`, $k$ is the length of `similarPairs`, and $m$ is the average length of words in `sentence1` as well as `similarPairs`.
