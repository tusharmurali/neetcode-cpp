# 212. Word Search II

- **Difficulty:** Hard  
- **Pattern:** Tries  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/word-search-ii/>  
- **NeetCode:** <https://neetcode.io/problems/search-for-word-ii>  
- **Video:** <https://www.youtube.com/watch?v=asbcE9mZz_U>  

[← Back to index](../INDEX.md)

## 1. Backtracking

For each word, we try to **trace it on the board** by walking through adjacent cells (up/down/left/right).
To avoid using the same cell twice in one word path, we **temporarily mark the cell as visited**, and then restore it after exploring (classic backtracking).

If we can match all characters of a word in order, that word is found and added to the result.

```cpp
class Solution {
public:
    vector<string> findWords(vector<vector<char>>& board, vector<string>& words) {
        int ROWS = board.size(), COLS = board[0].size();
        vector<string> res;

        for (string& word : words) {
            bool flag = false;
            for (int r = 0; r < ROWS && !flag; r++) {
                for (int c = 0; c < COLS; c++) {
                    if (board[r][c] != word[0]) continue;
                    if (backtrack(board, r, c, word, 0)) {
                        res.push_back(word);
                        flag = true;
                        break;
                    }
                }
            }
        }
        return res;
    }

private:
    bool backtrack(vector<vector<char>>& board, int r, int c, string& word, int i) {
        if (i == word.length()) return true;
        if (r < 0 || c < 0 || r >= board.size() ||
            c >= board[0].size() || board[r][c] != word[i])
            return false;

        board[r][c] = '*';
        bool ret = backtrack(board, r + 1, c, word, i + 1) ||
                   backtrack(board, r - 1, c, word, i + 1) ||
                   backtrack(board, r, c + 1, word, i + 1) ||
                   backtrack(board, r, c - 1, word, i + 1);
        board[r][c] = word[i];
        return ret;
    }
};
```

**Complexity**

- Time complexity: $O(w * m * n * 4 * 3 ^ t - 1)$
- Space complexity: $O(t)$

> Where $w$ is the number of words, $m$ is the number of rows, $n$ is the number of columns and $t$ is the maximum length of any word in the array $words$.

## 2. Backtracking (Trie + Hash Set)

Searching each word separately repeats the same work many times.
A **Trie (prefix tree)** lets us share work: while walking on the board, we only continue paths that match **some prefix** of the given words.
So the board `DFS` explores "possible prefixes", and whenever the Trie node says **this prefix is a complete word**, we record it.

We also need to avoid reusing the same cell in a single path, so we keep a **visited set** during the current `DFS` path (and backtrack/remove when returning).

```cpp
class TrieNode {
public:
    unordered_map<char, TrieNode*> children;
    bool isWord;

    TrieNode() : isWord(false) {}

    void addWord(const string& word) {
        TrieNode* cur = this;
        for (char c : word) {
            if (!cur->children.count(c)) {
                cur->children[c] = new TrieNode();
            }
            cur = cur->children[c];
        }
        cur->isWord = true;
    }
};

class Solution {
    unordered_set<string> res;
    vector<vector<bool>> visit;
public:
    vector<string> findWords(vector<vector<char>>& board, vector<string>& words) {
        TrieNode* root = new TrieNode();
        for (const string& word : words) {
            root->addWord(word);
        }

        int ROWS = board.size(), COLS = board[0].size();
        visit.assign(ROWS, vector<bool>(COLS, false));

        for (int r = 0; r < ROWS; ++r) {
            for (int c = 0; c < COLS; ++c) {
                dfs(board, r, c, root, "");
            }
        }
        return vector<string>(res.begin(), res.end());
    }

private:
    void dfs(vector<vector<char>>& board, int r, int c, TrieNode* node, string word) {
        int ROWS = board.size(), COLS = board[0].size();
        if (r < 0 || c < 0 || r >= ROWS ||
            c >= COLS || visit[r][c] ||
            !node->children.count(board[r][c])) {
            return;
        }

        visit[r][c] = true;
        node = node->children[board[r][c]];
        word += board[r][c];
        if (node->isWord) {
            res.insert(word);
        }

        dfs(board, r + 1, c, node, word);
        dfs(board, r - 1, c, node, word);
        dfs(board, r, c + 1, node, word);
        dfs(board, r, c - 1, node, word);

        visit[r][c] = false;
    }
};
```

**Complexity**

- Time complexity: $O(m * n * 4 * 3 ^ {t - 1} + s)$
- Space complexity: $O(s)$

> Where $m$ is the number of rows, $n$ is the number of columns, $t$ is the maximum length of any word in the array $words$ and $s$ is the sum of the lengths of all the words.

## 3. Backtracking (Trie)

We still do `DFS` on the board, but we guide the `DFS` using a **Trie** so we only walk paths that match prefixes of the given words.

This version is faster because it adds **aggressive pruning**:

- Each Trie node keeps `refs` = "how many words in the dictionary still pass through this node".
- When we successfully find one or more words, each `DFS` call returns how many new words it found below its current prefix.
- We subtract that count from `refs` as `DFS` unwinds, removing the found words from every Trie node on their paths.
- If after removal a node's `refs` becomes `0`, that branch is **dead** (no remaining words use it), so we physically cut the pointer from its parent (`prev.children[...] = null`).
  That prevents future `DFS` calls from exploring useless prefixes.

Also, instead of using a visited set, we mark the board in-place:

- Temporarily set `board[r][c] = '*'` while exploring that path.
- Restore it when backtracking.

```cpp
class TrieNode {
public:
    TrieNode* children[26];
    int idx;
    int refs;

    TrieNode() {
        for (int i = 0; i < 26; ++i) {
            children[i] = nullptr;
        }
        idx = -1;
        refs = 0;
    }

    void addWord(const string& word, int i) {
        TrieNode* cur = this;
        cur->refs++;
        for (char c : word) {
            int index = c - 'a';
            if (!cur->children[index]) {
                cur->children[index] = new TrieNode();
            }
            cur = cur->children[index];
            cur->refs++;
        }
        cur->idx = i;
    }
};

class Solution {
public:
    vector<string> res;

    vector<string> findWords(vector<vector<char>>& board, vector<string>& words) {
        TrieNode* root = new TrieNode();
        for (int i = 0; i < words.size(); ++i) {
            root->addWord(words[i], i);
        }

        for (int r = 0; r < board.size(); ++r) {
            for (int c = 0; c < board[0].size(); ++c) {
                root->refs -= dfs(board, root, r, c, words);
            }
        }

        return res;
    }

    int dfs(auto& board, TrieNode* node, int r, int c, auto& words) {
        if (r < 0 || c < 0 || r >= board.size() ||
            c >= board[0].size() || board[r][c] == '*' ||
            !node->children[board[r][c] - 'a']) {
            return 0;
        }

        char temp = board[r][c];
        board[r][c] = '*';
        TrieNode* prev = node;
        node = node->children[temp - 'a'];
        int found = 0;
        if (node->idx != -1) {
            res.push_back(words[node->idx]);
            node->idx = -1;
            found++;
        }

        found += dfs(board, node, r + 1, c, words);
        found += dfs(board, node, r - 1, c, words);
        found += dfs(board, node, r, c + 1, words);
        found += dfs(board, node, r, c - 1, words);

        board[r][c] = temp;
        node->refs -= found;
        if (!node->refs) {
            prev->children[temp - 'a'] = nullptr;
        }
        return found;
    }
};
```

**Complexity**

- Time complexity: $O(m * n * 4 * 3 ^ {t - 1} + s)$
- Space complexity: $O(s)$

> Where $m$ is the number of rows, $n$ is the number of columns, $t$ is the maximum length of any word in the array $words$ and $s$ is the sum of the lengths of all the words.

## Standalone solution file (`cpp/0212-word-search-ii.cpp` in the NeetCode repo)

```cpp
/*
    Given a board of characters & a list of words, return all words on the board

    Implement trie, for search: iterate thru children until isWord, add to result

    Time: O(m x (4 x 3^(l - 1))) -> m = # of cells, l = max length of words
    Space: O(n) -> n = total number of letters in dictionary (no overlap in Trie)
*/

class TrieNode {
public:
    TrieNode* children[26];
    bool isWord;
    
    TrieNode() {
        for (int i = 0; i < 26; i++) {
            children[i] = NULL;
        }
        isWord = false;
    }
};

class Solution {
public:
    vector<string> findWords(vector<vector<char>>& board, vector<string>& words) {
        for (int i = 0; i < words.size(); i++) {
            insert(words[i]);
        }
        
        int m = board.size();
        int n = board[0].size();
        
        TrieNode* node = root;
        vector<string> result;
        
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                search(board, i, j, m, n, node, "", result);
            }
        }
        
        return result;
    }
private:
    TrieNode* root = new TrieNode();
    
    void insert(string word) {
        TrieNode* node = root;
        int curr = 0;
        
        for (int i = 0; i < word.size(); i++) {
            curr = word[i] - 'a';
            if (node->children[curr] == NULL) {
                node->children[curr] = new TrieNode();
            }
            node = node->children[curr];
        }
        
        node->isWord = true;
    }
    
    void search(vector<vector<char>>& board, int i, int j, int m, int n, TrieNode* node, string word, vector<string>& result) {
        if (i < 0 || i >= m || j < 0 || j >= n || board[i][j] == '#') {
            return;
        }
        
        char c = board[i][j];
        
        node = node->children[c - 'a'];
        if (node == NULL) {
            return;
        }
        
        word += board[i][j];
        if (node->isWord) {
            result.push_back(word);
            node->isWord = false;
        }
        
        board[i][j] = '#';
        
        search(board, i - 1, j, m, n, node, word, result);
        search(board, i + 1, j, m, n, node, word, result);
        search(board, i, j - 1, m, n, node, word, result);
        search(board, i, j + 1, m, n, node, word, result);
        
        board[i][j] = c;
    }
};
```
