# 2709. Greatest Common Divisor Traversal

- **Difficulty:** Hard  
- **Pattern:** Advanced Graphs  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/greatest-common-divisor-traversal/>  
- **NeetCode:** <https://neetcode.io/problems/greatest-common-divisor-traversal>  
- **Video:** <https://www.youtube.com/watch?v=jZ-RVp5CVYY>  
- **Video approach:** 2. Disjoint Set Union  

[← Back to index](../INDEX.md)

## 1. Brute Force (DFS)

Two indices can be connected if their corresponding values share a common factor greater than `1`. We can model this as a graph where each index is a node, and edges connect pairs with GCD > 1. The problem reduces to checking if all nodes belong to a single connected component.

```cpp
class Solution {
public:
    bool canTraverseAllPairs(vector<int>& nums) {
        int n = nums.size();
        vector<bool> visit(n, false);
        vector<vector<int>> adj(n);
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (__gcd(nums[i], nums[j]) > 1) {
                    adj[i].push_back(j);
                    adj[j].push_back(i);
                }
            }
        }

        dfs(0, adj, visit);
        for (bool node : visit) {
            if (!node) {
                return false;
            }
        }
        return true;
    }

private:
    void dfs(int node, vector<vector<int>>& adj, vector<bool>& visit) {
        visit[node] = true;
        for (int& nei : adj[node]) {
            if (!visit[nei]) {
                dfs(nei, adj, visit);
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 \log n)$
- Space complexity: $O(n ^ 2)$

## 2. Disjoint Set Union ▶ video

Instead of building explicit edges between indices, we can connect indices through their prime factors. Two numbers sharing a prime factor should be in the same component. Using Union-Find, we union each index with the first occurrence of each of its prime factors. This avoids O(n^2) pairwise comparisons.

```cpp
class UnionFind {
private:
    int n;
    vector<int> Parent;
    vector<int> Size;

public:
    UnionFind(int n) : n(n), Parent(n + 1), Size(n + 1, 1) {
        for (int i = 0; i <= n; i++) {
            Parent[i] = i;
        }
    }

    int find(int node) {
        if (Parent[node] != node) {
            Parent[node] = find(Parent[node]);
        }
        return Parent[node];
    }

    bool unionNodes(int u, int v) {
        int pu = find(u);
        int pv = find(v);
        if (pu == pv) return false;
        n--;
        if (Size[pu] < Size[pv]) swap(pu, pv);
        Size[pu] += Size[pv];
        Parent[pv] = pu;
        return true;
    }

    bool isConnected() {
        return n == 1;
    }
};

class Solution {
public:
    bool canTraverseAllPairs(vector<int>& nums) {
        int n = nums.size();
        UnionFind uf(n);

        unordered_map<int, int> factor_index;

        for (int i = 0; i < n; i++) {
            int num = nums[i];
            int f = 2;
            while (f * f <= num) {
                if (num % f == 0) {
                    if (factor_index.count(f)) {
                        uf.unionNodes(i, factor_index[f]);
                    } else {
                        factor_index[f] = i;
                    }
                    while (num % f == 0) {
                        num /= f;
                    }
                }
                f++;
            }
            if (num > 1) {
                if (factor_index.count(num)) {
                    uf.unionNodes(i, factor_index[num]);
                } else {
                    factor_index[num] = i;
                }
            }
        }

        return uf.isConnected();
    }
};
```

**Complexity**

- Time complexity: $O(m + n\sqrt {m})$
- Space complexity: $O(n \log m)$

> Where $n$ is the size of the array $nums$ and $m$ is the maximum value in the array.

## 3. Sieve of Eratosthenes + DSU

We can speed up factorization by precomputing the smallest prime factor (SPF) for each number using the Sieve of Eratosthenes. With SPF, we can factorize any number in O(log m) time. We then use Union-Find to connect each index directly to virtual nodes representing primes.

```cpp
class UnionFind {
private:
    vector<int> Parent, Size;

public:
    UnionFind(int n) {
        Parent.resize(n + 1);
        Size.resize(n + 1, 1);
        for (int i = 0; i <= n; i++) {
            Parent[i] = i;
        }
    }

    int find(int node) {
        if (Parent[node] != node) {
            Parent[node] = find(Parent[node]);
        }
        return Parent[node];
    }

    bool unionSet(int u, int v) {
        int pu = find(u);
        int pv = find(v);
        if (pu == pv) {
            return false;
        }
        if (Size[pu] < Size[pv]) {
            swap(pu, pv);
        }
        Size[pu] += Size[pv];
        Parent[pv] = pu;
        return true;
    }
};

class Solution {
public:
    bool canTraverseAllPairs(vector<int>& nums) {
        int N = nums.size();
        if (N == 1) {
            return true;
        }
        for (int num : nums) {
            if (num == 1) {
                return false;
            }
        }

        int MAX = *max_element(nums.begin(), nums.end());
        vector<int> sieve(MAX + 1, 0);
        for (int p = 2; p * p <= MAX; p++) {
            if (sieve[p] == 0) {
                for (int composite = p * p; composite <= MAX; composite += p) {
                    sieve[composite] = p;
                }
            }
        }

        UnionFind uf(N + MAX + 1);
        for (int i = 0; i < N; i++) {
            int num = nums[i];
            if (sieve[num] == 0) { // num is prime
                uf.unionSet(i, N + num);
                continue;
            }

            while (num > 1) {
                int prime = sieve[num] != 0 ? sieve[num] : num;
                uf.unionSet(i, N + prime);
                while (num % prime == 0) {
                    num /= prime;
                }
            }
        }

        int root = uf.find(0);
        for (int i = 1; i < N; i++) {
            if (uf.find(i) != root) {
                return false;
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(m + n \log m)$
- Space complexity: $O(n + m)$

> Where $n$ is the size of the array $nums$ and $m$ is the maximum value in the array.

## 4. Sieve of Eratosthenes + DFS

Rather than Union-Find, we can build an explicit graph connecting indices to virtual prime nodes and use DFS for connectivity. Each index connects to nodes representing its prime factors, and primes connect back to indices. A single DFS from index `0` should reach all indices if they form one component.

```cpp
class Solution {
public:
    bool canTraverseAllPairs(vector<int>& nums) {
        int N = nums.size();
        if (N == 1) return true;
        if (find(nums.begin(), nums.end(), 1) != nums.end()) return false;

        int MAX = *max_element(nums.begin(), nums.end());
        vector<int> sieve(MAX + 1, 0);
        for (int p = 2; p * p <= MAX; p++) {
            if (sieve[p] == 0) {
                for (int composite = p * p; composite <= MAX; composite += p) {
                    sieve[composite] = p;
                }
            }
        }

        unordered_map<int, vector<int>> adj;
        for (int i = 0; i < N; i++) {
            int num = nums[i];
            if (!adj.count(i)) adj[i] = {};

            if (sieve[num] == 0) {
                adj[N + num].push_back(i);
                adj[i].push_back(N + num);
                continue;
            }

            while (num > 1) {
                int prime = (sieve[num] == 0) ? num : sieve[num];
                adj[N + prime].push_back(i);
                adj[i].push_back(N + prime);
                while (num % prime == 0) num /= prime;
            }
        }

        unordered_set<int> visited;
        dfs(0, adj, visited);
        for (int i = 0; i < N; i++) {
            if (visited.find(i) == visited.end()) return false;
        }
        return true;
    }

private:
    void dfs(int node, unordered_map<int, vector<int>>& adj, unordered_set<int>& visited) {
        visited.insert(node);
        for (int& neighbor : adj[node]) {
            if (visited.find(neighbor) == visited.end()) {
                dfs(neighbor, adj, visited);
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(m + n \log m)$
- Space complexity: $O(n + m)$

> Where $n$ is the size of the array $nums$ and $m$ is the maximum value in the array.

## 5. Sieve of Eratosthenes + BFS

BFS provides an iterative alternative to DFS for checking graph connectivity. We build the same graph structure connecting indices to prime nodes, then use a queue to explore all reachable nodes starting from index `0`.

```cpp
class Solution {
public:
    bool canTraverseAllPairs(vector<int>& nums) {
        int N = nums.size();
        if (N == 1) return true;
        if (find(nums.begin(), nums.end(), 1) != nums.end()) return false;

        int MAX = *max_element(nums.begin(), nums.end());
        vector<int> sieve(MAX + 1, 0);
        int p = 2;
        while (p * p <= MAX) {
            if (sieve[p] == 0) {
                for (int composite = p * p; composite <= MAX; composite += p) {
                    sieve[composite] = p;
                }
            }
            p++;
        }

        unordered_map<int, vector<int>> adj;
        for (int i = 0; i < N; i++) {
            int num = nums[i];
            if (sieve[num] == 0) { // num is prime
                adj[i].push_back(N + num);
                adj[N + num].push_back(i);
                continue;
            }

            while (num > 1) {
                int prime = (sieve[num] != 0) ? sieve[num] : num;
                adj[i].push_back(N + prime);
                adj[N + prime].push_back(i);
                while (num % prime == 0) {
                    num /= prime;
                }
            }
        }

        unordered_set<int> visited;
        queue<int> q;
        q.push(0);
        visited.insert(0);

        while (!q.empty()) {
            int node = q.front();
            q.pop();
            for (int& nei : adj[node]) {
                if (visited.find(nei) == visited.end()) {
                    visited.insert(nei);
                    q.push(nei);
                }
            }
        }

        for (int i = 0; i < N; i++) {
            if (visited.find(i) == visited.end()) {
                return false;
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(m + n \log m)$
- Space complexity: $O(n + m)$

> Where $n$ is the size of the array $nums$ and $m$ is the maximum value in the array.
