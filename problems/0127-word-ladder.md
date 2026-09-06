# 127. Word Ladder

- **Difficulty:** Hard  
- **Pattern:** Graphs  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/word-ladder/>  
- **NeetCode:** <https://neetcode.io/problems/word-ladder>  
- **Video:** <https://www.youtube.com/watch?v=h9iTnkgv05E>  
- **Video approach:** 3. Breadth First Search - III  

[← Back to index](../INDEX.md)

## 1. Breadth First Search - I

This problem can be modeled as finding the shortest path in an unweighted graph where each word is a node and edges connect words that differ by exactly one character. We precompute the adjacency list by comparing all pairs of words. BFS naturally finds the shortest path because it explores all nodes at distance `k` before any node at distance `k+1`.

```cpp
class Solution {
public:
    int ladderLength(string beginWord, string endWord, vector<string>& wordList) {
        if (find(wordList.begin(), wordList.end(), endWord) == wordList.end() ||
            beginWord == endWord) {
            return 0;
        }

        int n = wordList.size();
        int m = wordList[0].size();
        vector<vector<int>> adj(n);
        unordered_map<string, int> mp;
        for (int i = 0; i < n; i++) {
            mp[wordList[i]] = i;
        }

        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                int cnt = 0;
                for (int k = 0; k < m; k++) {
                    if (wordList[i][k] != wordList[j][k]) {
                        cnt++;
                    }
                }
                if (cnt == 1) {
                    adj[i].push_back(j);
                    adj[j].push_back(i);
                }
            }
        }

        queue<int> q;
        int res = 1;
        unordered_set<int> visit;

        for (int i = 0; i < m; i++) {
            for (char c = 'a'; c <= 'z'; c++) {
                if (c == beginWord[i]) {
                    continue;
                }
                string word = beginWord.substr(0, i) + c + beginWord.substr(i + 1);
                if (mp.find(word) != mp.end() && visit.find(mp[word]) == visit.end()) {
                    q.push(mp[word]);
                    visit.insert(mp[word]);
                }
            }
        }

        while (!q.empty()) {
            res++;
            int size = q.size();
            for (int i = 0; i < size; i++) {
                int node = q.front();
                q.pop();
                if (wordList[node] == endWord) {
                    return res;
                }
                for (int nei : adj[node]) {
                    if (visit.find(nei) == visit.end()) {
                        visit.insert(nei);
                        q.push(nei);
                    }
                }
            }
        }

        return 0;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * m)$
- Space complexity: $O(n ^ 2)$

> Where $n$ is the number of words and $m$ is the length of the word.

## 2. Breadth First Search - II

Instead of precomputing the entire adjacency graph, we can generate neighbors on the fly. For each word, we try replacing each character with all 26 letters. If the resulting word exists in our word set, it is a valid neighbor. This approach trades precomputation time for potentially more neighbor generation during `BFS`.

```cpp
class Solution {
public:
    int ladderLength(string beginWord, string endWord, vector<string>& wordList) {
        unordered_set<string> words(wordList.begin(), wordList.end());
        if (words.find(endWord) == words.end() || beginWord == endWord) return 0;
        int res = 0;
        queue<string> q;
        q.push(beginWord);

        while (!q.empty()) {
            res++;
            int len = q.size();
            for (int i = 0; i < len; i++) {
                string node = q.front();
                q.pop();
                if (node == endWord) return res;
                for (int j = 0; j < node.length(); j++) {
                    char original = node[j];
                    for (char c = 'a'; c <= 'z'; c++) {
                        if (c == original) continue;
                        node[j] = c;
                        if (words.find(node) != words.end()) {
                            q.push(node);
                            words.erase(node);
                        }
                    }
                    node[j] = original;
                }
            }
        }
        return 0;
    }
};
```

**Complexity**

- Time complexity: $O(m ^ 2 * n)$
- Space complexity: $O(m ^ 2 * n)$

> Where $n$ is the number of words and $m$ is the length of the word.

## 3. Breadth First Search - III ▶ video

We can use wildcard patterns to efficiently group words that are one character apart. For each word, create patterns by replacing each character with a wildcard. Words sharing the same pattern are neighbors. This precomputation allows `O(1)` neighbor lookup during `BFS`, as we only need to check the pattern buckets.

```cpp
class Solution {
public:
    int ladderLength(string beginWord, string endWord, vector<string>& wordList) {
        if (endWord.empty() || find(wordList.begin(), wordList.end(), endWord) == wordList.end()) {
            return 0;
        }

        unordered_map<string, vector<string>> nei;
        wordList.push_back(beginWord);
        for (const string& word : wordList) {
            for (int j = 0; j < word.size(); ++j) {
                string pattern = word.substr(0, j) + "*" + word.substr(j + 1);
                nei[pattern].push_back(word);
            }
        }

        unordered_set<string> visit{beginWord};
        queue<string> q;
        q.push(beginWord);
        int res = 1;
        while (!q.empty()) {
            int size = q.size();
            for (int i = 0; i < size; ++i) {
                string word = q.front();
                q.pop();
                if (word == endWord) {
                    return res;
                }
                for (int j = 0; j < word.size(); ++j) {
                    string pattern = word.substr(0, j) + "*" + word.substr(j + 1);
                    for (const string& neiWord : nei[pattern]) {
                        if (visit.find(neiWord) == visit.end()) {
                            visit.insert(neiWord);
                            q.push(neiWord);
                        }
                    }
                }
            }
            ++res;
        }
        return 0;
    }
};
```

**Complexity**

- Time complexity: $O(m ^ 2 * n)$
- Space complexity: $O(m ^ 2 * n)$

> Where $n$ is the number of words and $m$ is the length of the word.

## 4. Meet In The Middle (BFS)

Standard `BFS` explores exponentially more nodes as distance increases. By running two `BFS` searches simultaneously from `beginWord` and `endWord`, we can meet in the middle, effectively halving the search depth and dramatically reducing the search space. At each step, we expand the smaller frontier to balance the workload.

```cpp
class Solution {
public:
    int ladderLength(string beginWord, string endWord, vector<string>& wordList) {
        if (find(wordList.begin(), wordList.end(), endWord) == wordList.end() ||
            beginWord == endWord)
            return 0;
        int m = wordList[0].size();
        unordered_set<string> wordSet(wordList.begin(), wordList.end());
        queue<string> qb, qe;
        unordered_map<string, int> fromBegin, fromEnd;
        qb.push(beginWord);
        qe.push(endWord);
        fromBegin[beginWord] = 1;
        fromEnd[endWord] = 1;

        while (!qb.empty() && !qe.empty()) {
            if (qb.size() > qe.size()) {
                swap(qb, qe);
                swap(fromBegin, fromEnd);
            }
            int size = qb.size();
            for (int k = 0; k < size; k++) {
                string word = qb.front();
                qb.pop();
                int steps = fromBegin[word];
                for (int i = 0; i < m; i++) {
                    for (char c = 'a'; c <= 'z'; c++) {
                        if (c == word[i])
                            continue;
                        string nei = word.substr(0, i) +
                                     c + word.substr(i + 1);
                        if (!wordSet.count(nei))
                            continue;
                        if (fromEnd.count(nei))
                            return steps + fromEnd[nei];
                        if (!fromBegin.count(nei)) {
                            fromBegin[nei] = steps + 1;
                            qb.push(nei);
                        }
                    }
                }
            }
        }
        return 0;
    }
};
```

**Complexity**

- Time complexity: $O(m ^ 2 * n)$
- Space complexity: $O(m ^ 2 * n)$

> Where $n$ is the number of words and $m$ is the length of the word.

## Standalone solution file (`cpp/0127-word-ladder.cpp` in the NeetCode repo)

```cpp
/*
    Given 2 words & a dictionary, return min # of words to transform b/w them
    Ex. begin = "hit", end = "cog", dict = ["hot","dot","dog","lot","log","cog"] -> 5
    "hit" -> "hot" -> "dot" -> "dog" -> "cog"

    BFS, change 1 letter at a time (neighbors), if in dict add to queue, else skip

    Time: O(m^2 x n) -> m = length of each word, n = # of words in input word list
    Space: O(m^2 x n)
*/

class Solution {
public:
    int ladderLength(string beginWord, string endWord, vector<string>& wordList) {
        unordered_set<string> dict;
        for (int i = 0; i < wordList.size(); i++) {
            dict.insert(wordList[i]);
        }
        
        queue<string> q;
        q.push(beginWord);
        
        int result = 1;
        
        while (!q.empty()) {
            int count = q.size();
            
            for (int i = 0; i < count; i++) {
                string word = q.front();
                q.pop();
                
                if (word == endWord) {
                    return result;
                }
                dict.erase(word);
                
                for (int j = 0; j < word.size(); j++) {
                    char c = word[j];
                    for (int k = 0; k < 26; k++) {
                        word[j] = k + 'a';
                        if (dict.find(word) != dict.end()) {
                            q.push(word);
                            dict.erase(word);
                        }
                        word[j] = c;
                    }
                }
            }
            
            result++;
        }
        
        return 0;
    }
};
```
