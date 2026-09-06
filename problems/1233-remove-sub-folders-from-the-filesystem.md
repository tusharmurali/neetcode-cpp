# 1233. Remove Sub-Folders from the Filesystem

- **Difficulty:** Medium  
- **Pattern:** Tries  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/remove-sub-folders-from-the-filesystem/>  
- **NeetCode:** <https://neetcode.io/problems/remove-sub-folders-from-the-filesystem>  
- **Video:** <https://www.youtube.com/watch?v=WDDLp2l9TrM>  

[← Back to index](../INDEX.md)

## 1. Hash Set

A folder is a subfolder if any of its ancestor paths exist in the input. We can check this efficiently by storing all folder paths in a hash set. For each folder, we examine every prefix ending at a `/` character. If any such prefix exists in the set, the current folder is a subfolder and should be excluded. In code, we use `i` to iterate through the path and check if `f[:i]` exists in the folder set.

```cpp
class Solution {
public:
    vector<string> removeSubfolders(vector<string>& folder) {
        vector<string> res;
        unordered_set<string> folder_set(folder.begin(), folder.end());

        for (string& f : folder) {
            res.push_back(f);
            for (int i = 0; i < f.size(); i++) {
                if (f[i] == '/' && folder_set.count(f.substr(0, i))) {
                    res.pop_back();
                    break;
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m ^ 2)$
- Space complexity: $O(n * m)$

> Where $n$ is the size of the string array $folder$ and $m$ is the length of each string.

## 2. Sorting

When folder paths are sorted lexicographically, parent folders always appear before their subfolders. This means if we iterate through the sorted list, a folder is a subfolder only if it starts with the most recently added result folder followed by `/`. We only need to compare against the last folder in `res`, not all of them.

```cpp
class Solution {
public:
    vector<string> removeSubfolders(vector<string>& folder) {
        sort(folder.begin(), folder.end());
        vector<string> res;
        res.push_back(folder[0]);

        for (int i = 1; i < folder.size(); i++) {
            if (folder[i].find(res.back() + "/") != 0) {
                res.push_back(folder[i]);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m ^ 2)$
- Space complexity: $O(n * m)$

> Where $n$ is the size of the string array $folder$ and $m$ is the length of each string.

## 3. Trie

A trie naturally represents hierarchical folder structures. Each node corresponds to a folder name segment, and we mark nodes that represent complete folder paths. When checking if a folder is a subfolder, we traverse the trie along its path. If we encounter a marked node before reaching the end, a parent folder exists, meaning this is a subfolder.

```cpp
class Trie {
public:
    Trie* children[128] = {};
    bool end_of_folder = false;

    void add(const string& path) {
        Trie* cur = this;
        string part;
        for (int i = 0; i < path.size(); i++) {
            if (path[i] == '/') {
                if (!part.empty()) {
                    for (char c : part) {
                        if (!cur->children[(int)c]) cur->children[(int)c] = new Trie();
                        cur = cur->children[(int)c];
                    }
                    if (!cur->children[(int)'/']) cur->children[(int)'/'] = new Trie();
                    cur = cur->children[(int)'/'];
                    part.clear();
                }
            } else {
                part += path[i];
            }
        }
        if (!part.empty()) {
            for (char c : part) {
                if (!cur->children[(int)c]) cur->children[(int)c] = new Trie();
                cur = cur->children[(int)c];
            }
            if (!cur->children[(int)'/']) cur->children[(int)'/'] = new Trie();
            cur = cur->children[(int)'/'];
        }
        cur->end_of_folder = true;
    }

    bool prefixSearch(const string& path) {
        Trie* cur = this;
        string part;
        for (int i = 0; i < (int)path.size(); i++) {
            if (path[i] == '/') {
                if (!part.empty()) {
                    for (char c : part) cur = cur->children[(int)c];
                    cur = cur->children[(int)'/'];
                    if (cur->end_of_folder) return true;
                    part.clear();
                }
            } else {
                part += path[i];
            }
        }
        return false;
    }
};

class Solution {
public:
    vector<string> removeSubfolders(vector<string>& folder) {
        Trie trie;
        for (auto& f : folder) trie.add(f);
        vector<string> res;
        for (auto& f : folder) {
            if (!trie.prefixSearch(f)) res.push_back(f);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n * m)$

> Where $n$ is the size of the string array $folder$ and $m$ is the length of each string.
