# 642. Design Search Autocomplete System

- **Difficulty:** Hard  
- **Pattern:** Tries  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/design-search-autocomplete-system/>  
- **NeetCode:** <https://neetcode.io/problems/design-search-autocomplete-system>  

[← Back to index](../INDEX.md)

## 1. Trie

Autocomplete works by finding sentences that share a common prefix with what the user has typed so far. A trie is ideal for prefix-based lookups. We build a trie where each node stores all sentences that pass through it along with their frequencies. As the user types, we walk down the trie character by character. At any node, we have direct access to all matching sentences and can sort them by frequency (highest first) and then alphabetically to return the top 3 results.

```cpp
class TrieNode {
public:
    unordered_map<char, TrieNode*> children;
    unordered_map<string, int> sentences;
};

class AutocompleteSystem {
private:
    TrieNode* root;
    TrieNode* currNode;
    TrieNode* dead;
    string currSentence;

    void addToTrie(const string& sentence, int count) {
        TrieNode* node = root;
        for (char c : sentence) {
            if (node->children.find(c) == node->children.end()) {
                node->children[c] = new TrieNode();
            }
            node = node->children[c];
            node->sentences[sentence] += count;
        }
    }

public:
    AutocompleteSystem(vector<string>& sentences, vector<int>& times) {
        root = new TrieNode();
        dead = new TrieNode();
        currNode = root;
        currSentence = "";

        for (int i = 0; i < sentences.size(); i++) {
            addToTrie(sentences[i], times[i]);
        }
    }

    vector<string> input(char c) {
        if (c == '#') {
            addToTrie(currSentence, 1);
            currSentence = "";
            currNode = root;
            return {};
        }

        currSentence += c;
        if (currNode->children.find(c) == currNode->children.end()) {
            currNode = dead;
            return {};
        }

        currNode = currNode->children[c];
        vector<pair<int, string>> items;
        for (const auto& [sentence, count] : currNode->sentences) {
            items.push_back({-count, sentence});
        }

        sort(items.begin(), items.end());

        vector<string> ans;
        for (int i = 0; i < min(3, (int)items.size()); i++) {
            ans.push_back(items[i].second);
        }
        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot k + m \cdot (n + \frac{m}{k}) \cdot \log(n + \frac{m}{k}))$

    `constructor`:
    - We initialize the trie, which costs $O(n \cdot k)$ as we iterate over each character in each sentence.

    `input`:
    - We add a character to `currSentence` and the trie, both cost $O(1)$. Next, we fetch and sort the sentences in the current node. Initially, a node could hold $O(n)$ sentences. After we call `input` $m$ times, we could add $\frac{m}{k}$ new sentences. Overall, there could be up to $O(n + \frac{m}{k})$ sentences, so a sort would cost $O((n + \frac{m}{k}) \cdot \log(n + \frac{m}{k}))$.
    - The work done in the other cases (like adding a new sentence to the trie) will be dominated by this sort.
    - `input` is called $m$ times, which gives us a total of $O(m \cdot (n + \frac{m}{k}) \cdot \log(n + \frac{m}{k}))$

- Space complexity: $O(k \cdot (n \cdot k + m))$

> Where $n$ is the length of `sentences`, $k$ is the average length of all sentences, and $m$ is the number of times `input` is called.

## 2. Optimize with Heap

Sorting all matching sentences every time is expensive when there are many matches. Since we only need the top 3 results, we can use a heap to find them more efficiently. By building a min-heap of size 3, we process each sentence once and keep only the best candidates. In languages with linear-time heapify (like Python's `heapq.nsmallest`), this gives a performance boost over full sorting.

```cpp
class TrieNode {
public:
    unordered_map<char, TrieNode*> children;
    unordered_map<string, int> sentences;

    TrieNode() {}
};

class AutocompleteSystem {
private:
    TrieNode* root;
    TrieNode* currNode;
    TrieNode* dead;
    string currSentence;

    void addToTrie(const string& sentence, int count) {
        TrieNode* node = root;
        for (char c : sentence) {
            if (node->children.find(c) == node->children.end()) {
                node->children[c] = new TrieNode();
            }
            node = node->children[c];
            node->sentences[sentence] -= count;
        }
    }

public:
    AutocompleteSystem(vector<string>& sentences, vector<int>& times) {
        root = new TrieNode();
        dead = new TrieNode();
        currNode = root;
        currSentence = "";

        for (int i = 0; i < sentences.size(); i++) {
            addToTrie(sentences[i], times[i]);
        }
    }

    vector<string> input(char c) {
        if (c == '#') {
            addToTrie(currSentence, 1);
            currSentence = "";
            currNode = root;
            return {};
        }

        currSentence += c;
        if (currNode->children.find(c) == currNode->children.end()) {
            currNode = dead;
            return {};
        }

        currNode = currNode->children[c];

        vector<pair<int, string>> items;
        for (const auto& [sentence, count] : currNode->sentences) {
            items.push_back({count, sentence});
        }

        // O(n log n) sort instead of O(n) heapify - main performance difference from Python
        sort(items.begin(), items.end(), [](const pair<int, string>& a, const pair<int, string>& b) {
            if (a.first != b.first) return a.first < b.first;
            return a.second < b.second;
        });

        vector<string> ans;
        for (int i = 0; i < min(3, (int)items.size()); i++) {
            ans.push_back(items[i].second);
        }
        return ans;
    }
};
```

**Complexity**

> This analysis will assume that you have access to a linear time heapify method, like in the Python implementation.

- Time complexity: $O(n \cdot k + m \cdot (n + \frac{m}{k}))$

    `constructor`:
    - We initialize the trie, which costs $O(n \cdot k)$ as we iterate over each character in each sentence.

    `input`:
    - We add a character to `currSentence` and the trie, both cost $O(1)$. Next, we fetch the sentences in the current node. Initially, a node could hold $O(n)$ sentences. After we call `input` $m$ times, we could add $\frac{m}{k}$ new sentences. Overall, there could be up to $O(n + \frac{m}{k})$ sentences. We heapify these sentences and find the best 3 in linear time, which costs $O(n + \frac{m}{k})$.
    - The work done in the other cases (like adding a new sentence to the trie) will be dominated by this.
    - `input` is called $m$ times, which gives us a total of $O(m \cdot (n + \frac{m}{k}))$.

- Space complexity: $O(k \cdot (n \cdot k + m))$

> Where $n$ is the length of `sentences`, $k$ is the average length of all sentences, and $m$ is the number of times `input` is called.
