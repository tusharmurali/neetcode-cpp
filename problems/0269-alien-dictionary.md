# 269. Alien Dictionary

- **Difficulty:** Hard  
- **Pattern:** Advanced Graphs  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/alien-dictionary/>  
- **NeetCode:** <https://neetcode.io/problems/foreign-dictionary>  
- **Video:** <https://www.youtube.com/watch?v=6kTZYvNNyps>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

The words are already sorted in an unknown alphabet order.  
So when you compare two **adjacent** words, the **first position where they differ** tells you a rule about letter order:

- If `w1[j] != w2[j]`, then `w1[j]` must come **before** `w2[j]` in the alien alphabet (`w1[j]` -> `w2[j]`).

All these rules form a **directed graph** (letters = nodes, “comes before” = directed edge).  
Now the problem becomes: **find a topological ordering** of this graph.

DFS helps in two ways:

- Build the ordering (postorder append).
- Detect cycles (if there’s a cycle, no valid alphabet exists).

Also, special invalid case:

- If `w1` is longer but `w2` is a prefix of `w1` (like `"abc"` before `"ab"`), that's impossible - return `""`.

```cpp
class Solution {
public:
    unordered_map<char, unordered_set<char>> adj;
    unordered_map<char, bool> visited;
    string result;

    string foreignDictionary(vector<string>& words) {
        for (const auto& word : words) {
            for (char ch : word) {
                adj[ch];
            }
        }

        for (size_t i = 0; i < words.size() - 1; ++i) {
            const string& w1 = words[i], & w2 = words[i + 1];
            size_t minLen = min(w1.length(), w2.length());
            if (w1.length() > w2.length() &&
                w1.substr(0, minLen) == w2.substr(0, minLen)) {
                return "";
            }
            for (size_t j = 0; j < minLen; ++j) {
                if (w1[j] != w2[j]) {
                    adj[w1[j]].insert(w2[j]);
                    break;
                }
            }
        }

        for (const auto& pair : adj) {
            if (dfs(pair.first)) {
                return "";
            }
        }

        reverse(result.begin(), result.end());
        return result;
    }

    bool dfs(char ch) {
        if (visited.find(ch) != visited.end()) {
            return visited[ch];
        }

        visited[ch] = true;
        for (char next : adj[ch]) {
            if (dfs(next)) {
                return true;
            }
        }
        visited[ch] = false;
        result.push_back(ch);
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(N + V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of unique characters, $E$ is the number of edges and $N$ is the sum of lengths of all the strings.

## 2. Topological Sort (Kahn's Algorithm)

From the sorted alien words, each pair of adjacent words gives you a **letter-order rule** at the first mismatching character:

- if `w1[j] != w2[j]`, then `w1[j]` -> `w2[j]` (meaning `w1[j]` comes before `w2[j]`).

These rules form a **directed graph**. The alien alphabet is just a **topological ordering** of this graph.

Kahn's algorithm (BFS topological sort) works by:

- Counting how many prerequisites each letter has (`indegree`).
- Always picking letters with `indegree = 0` (no unmet prerequisites) and "removing" them from the graph.

If there's a **cycle**, some letters will never reach `indegree` `0`, so we won't be able to output all letters.

Also invalid input case:

- If a longer word comes before its own prefix (e.g., `"abc"` before `"ab"`), ordering is impossible.

```cpp
class Solution {
public:
    string foreignDictionary(vector<string>& words) {
        unordered_map<char, unordered_set<char>> adj;
        unordered_map<char, int> indegree;
        for (string w : words) {
            for (char c : w) {
                adj[c] = unordered_set<char>();
                indegree[c] = 0;
            }
        }

        for (int i = 0; i < words.size() - 1; i++) {
            string w1 = words[i], w2 = words[i + 1];
            int minLen = min(w1.size(), w2.size());
            if (w1.size() > w2.size() &&
                w1.substr(0, minLen) == w2.substr(0, minLen)) {
                return "";
            }
            for (int j = 0; j < minLen; j++) {
                if (w1[j] != w2[j]) {
                    if (!adj[w1[j]].count(w2[j])) {
                        adj[w1[j]].insert(w2[j]);
                        indegree[w2[j]]++;
                    }
                    break;
                }
            }
        }

        queue<char> q;
        for (auto &[c, deg] : indegree) {
            if (deg == 0) {
                q.push(c);
            }
        }

        string res;
        while (!q.empty()) {
            char char_ = q.front();
            q.pop();
            res += char_;
            for (char neighbor : adj[char_]) {
                indegree[neighbor]--;
                if (indegree[neighbor] == 0) {
                    q.push(neighbor);
                }
            }
        }

        return res.size() == indegree.size() ? res : "";
    }
};
```

**Complexity**

- Time complexity: $O(N + V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of unique characters, $E$ is the number of edges and $N$ is the sum of lengths of all the strings.

## Standalone solution file (`cpp/0269-alien-dictionary.cpp` in the NeetCode repo)

```cpp
#include<iostream>
#include<map>
#include<vector>
#include<queue>
using namespace std;

class Solution {
public:
    string alienOrder(vector<string>& words) {
        map<char,int> degree;
        map<char, vector<char>> graph;
        int n = words.size();

        for (auto& word : words) {
            for (auto& ch : word) {
                degree[ch] = 0;
        }

        for (int i = 0; i < n - 1; i++) {
         int l = min((int)words[i].size(), (int)words[i + 1].size());
         for (int j = 0; j < l; j++) {
            char x = words[i][j];
            char y = words[i + 1][j];
            if (x != y) {
               graph[x].push_back(y);
               degree[y]++;
               break;
            }
         }
      }
      
      string ret = "";
      queue<char> q;
      map<char, int>::iterator it = degree.begin();
      while (it != degree.end()) {
         if (it->second == 0) {
            q.push(it->first);
         }
         it++;
      }

      while (!q.empty()) {
         char x = q.front();
         q.pop();
         ret += x;
         vector<char>::iterator sit = graph[x].begin();
         while (sit != graph[x].end()) {
            degree[*sit]--;
            if (degree[*sit] == 0) {
               q.push(*sit);
            }
            sit++;
         }
      }
      return ret.size() == degree.size() ? ret : "";
      }
    }
};
```
