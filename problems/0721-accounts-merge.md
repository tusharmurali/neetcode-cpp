# 721. Accounts Merge

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/accounts-merge/>  
- **NeetCode:** <https://neetcode.io/problems/accounts-merge>  
- **Video:** <https://www.youtube.com/watch?v=6st4IxEF-90>  
- **Video approach:** 3. Disjoint Set Union  

[← Back to index](../INDEX.md)

## 1. Depth First Search

This is a graph connectivity problem in disguise. If two accounts share an email, they belong to the same person and should be merged. We can model this as a graph where emails are nodes, and emails within the same account are connected by edges. Finding all emails belonging to one person becomes finding all nodes in a connected component. `dfs` naturally explores an entire component, collecting all connected emails.

```cpp
class Solution {
    unordered_map<string, int> emailIdx; // email -> id
    vector<string> emails; // set of emails of all accounts
    unordered_map<int, int> emailToAcc; // email_index -> account_Id
    vector<vector<int>> adj;
    unordered_map<int, vector<string>> emailGroup; // index of acc -> list of emails
    vector<bool> visited;

public:
    vector<vector<string>> accountsMerge(vector<vector<string>>& accounts) {
        int n = accounts.size();
        int m = 0;

        // Build email index and mappings
        for (int accId = 0; accId < n; accId++) {
            vector<string>& account = accounts[accId];
            for (int i = 1; i < account.size(); i++) {
                string& email = account[i];
                if (emailIdx.find(email) == emailIdx.end()) {
                    emails.push_back(email);
                    emailIdx[email] = m;
                    emailToAcc[m] = accId;
                    m++;
                }
            }
        }

        // Build adjacency list
        adj.resize(m);
        for (auto& account : accounts) {
            for (int i = 2; i < account.size(); i++) {
                int id1 = emailIdx[account[i]];
                int id2 = emailIdx[account[i - 1]];
                adj[id1].push_back(id2);
                adj[id2].push_back(id1);
            }
        }

        visited.resize(m, false);
        // DFS traversal
        for (int i = 0; i < m; i++) {
            if (!visited[i]) {
                int accId = emailToAcc[i];
                dfs(i, accId);
            }
        }

        // Build result
        vector<vector<string>> res;
        for (auto& [accId, group] : emailGroup) {
            sort(group.begin(), group.end());
            vector<string> merged;
            merged.push_back(accounts[accId][0]);
            merged.insert(merged.end(), group.begin(), group.end());
            res.push_back(merged);
        }

        return res;
    }

private:
    void dfs(int node, int& accId) {
        visited[node] = true;
        emailGroup[accId].push_back(emails[node]);
        for (int& neighbor : adj[node]) {
            if (!visited[neighbor]) {
                dfs(neighbor, accId);
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O((n * m)\log (n * m))$
- Space complexity: $O(n * m)$

> Where $n$ is the number of accounts and $m$ is the number of emails.

## 2. Breadth First Search

`bfs` provides an alternative way to explore connected components. Starting from any unvisited email, we use a queue to visit all reachable emails level by level. Each email we dequeue gets added to the current component, and its unvisited neighbors are enqueued. The result is the same as `dfs`, but `bfs` uses iteration with a queue instead of recursion.

```cpp
class Solution {
    unordered_map<string, int> emailIdx; // email -> id
    vector<string> emails; // set of emails of all accounts
    unordered_map<int, int> emailToAcc; // email_index -> account_Id
    vector<vector<int>> adj;
    unordered_map<int, vector<string>> emailGroup; // index of acc -> list of emails
    vector<bool> visited;

public:
    vector<vector<string>> accountsMerge(vector<vector<string>>& accounts) {
        int n = accounts.size();
        int m = 0;

        // Build email index and mappings
        for (int accId = 0; accId < n; accId++) {
            vector<string>& account = accounts[accId];
            for (int i = 1; i < account.size(); i++) {
                string& email = account[i];
                if (emailIdx.find(email) == emailIdx.end()) {
                    emails.push_back(email);
                    emailIdx[email] = m;
                    emailToAcc[m] = accId;
                    m++;
                }
            }
        }

        // Build adjacency list
        adj.resize(m);
        for (auto& account : accounts) {
            for (int i = 2; i < account.size(); i++) {
                int id1 = emailIdx[account[i]];
                int id2 = emailIdx[account[i - 1]];
                adj[id1].push_back(id2);
                adj[id2].push_back(id1);
            }
        }

        visited.resize(m, false);
        // BFS traversal
        for (int i = 0; i < m; i++) {
            if (!visited[i]) {
                int accId = emailToAcc[i];
                bfs(i, accId);
            }
        }

        // Build result
        vector<vector<string>> res;
        for (auto& [accId, group] : emailGroup) {
            sort(group.begin(), group.end());
            vector<string> merged;
            merged.push_back(accounts[accId][0]);
            merged.insert(merged.end(), group.begin(), group.end());
            res.push_back(merged);
        }

        return res;
    }

private:
    void bfs(int start, int accId) {
        queue<int> q;
        q.push(start);
        visited[start] = true;

        while (!q.empty()) {
            int node = q.front();
            q.pop();
            emailGroup[accId].push_back(emails[node]);
            for (int& neighbor : adj[node]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    q.push(neighbor);
                }
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O((n * m)\log (n * m))$
- Space complexity: $O(n * m)$

> Where $n$ is the number of accounts and $m$ is the number of emails.

## 3. Disjoint Set Union ▶ video

Union-Find (Disjoint Set Union) is designed for exactly this type of problem: grouping elements into disjoint sets and merging sets efficiently. Instead of building a graph and traversing it, we assign each account an ID and union accounts that share an email. When we see an email for the first time, we record which account it belongs to. If we see it again, we union the current account with the one that first owned it. After processing all accounts, we group emails by their account's root representative.

```cpp
class UnionFind {
    vector<int> parent;
    vector<int> rank;

public:
    UnionFind(int n) {
        parent.resize(n);
        rank.resize(n, 1);
        for (int i = 0; i < n; i++) {
            parent[i] = i;
        }
    }

    int find(int x) {
        if (x != parent[x]) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }

    bool unionSets(int x1, int x2) {
        int p1 = find(x1);
        int p2 = find(x2);
        if (p1 == p2) {
            return false;
        }
        if (rank[p1] > rank[p2]) {
            parent[p2] = p1;
            rank[p1] += rank[p2];
        } else {
            parent[p1] = p2;
            rank[p2] += rank[p1];
        }
        return true;
    }
};

class Solution {
public:
    vector<vector<string>> accountsMerge(vector<vector<string>>& accounts) {
        int n = accounts.size();
        UnionFind uf(n);
        unordered_map<string, int> emailToAcc; // email -> index of acc

        // Build union-find structure
        for (int i = 0; i < n; i++) {
            for (int j = 1; j < accounts[i].size(); j++) {
                const string& email = accounts[i][j];
                if (emailToAcc.count(email)) {
                    uf.unionSets(i, emailToAcc[email]);
                } else {
                    emailToAcc[email] = i;
                }
            }
        }

        // Group emails by leader account
        map<int, vector<string>> emailGroup; // index of acc -> list of emails
        for (const auto& [email, accId] : emailToAcc) {
            int leader = uf.find(accId);
            emailGroup[leader].push_back(email);
        }

        // Build result
        vector<vector<string>> res;
        for (auto& [accId, emails] : emailGroup) {
            sort(emails.begin(), emails.end());
            vector<string> merged;
            merged.push_back(accounts[accId][0]);
            merged.insert(merged.end(), emails.begin(), emails.end());
            res.push_back(merged);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O((n * m)\log (n * m))$
- Space complexity: $O(n * m)$

> Where $n$ is the number of accounts and $m$ is the number of emails.
