# 332. Reconstruct Itinerary

- **Difficulty:** Hard  
- **Pattern:** Advanced Graphs  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/reconstruct-itinerary/>  
- **NeetCode:** <https://neetcode.io/problems/reconstruct-flight-path>  
- **Video:** <https://www.youtube.com/watch?v=ZyB_gQ8vqGA>  
- **Video approach:** 2. Hierholzer's Algorithm (Recursion)  

[← Back to index](../INDEX.md)

## 1. Depth First Search

We must build an itinerary that:

- starts from `"JFK"`
- uses **every ticket exactly once**
- is **lexicographically smallest** among all valid itineraries.

This DFS solution tries destinations in sorted order.
At each airport `src`, we **choose one outgoing ticket**, remove it (so it can't be reused), and continue DFS.
If we reach a dead end before using all tickets, we **backtrack**: undo the choice and try the next destination.

Sorting tickets ensures the first complete valid path we find is the smallest lexicographically.

```cpp
class Solution {
public:
    vector<string> findItinerary(vector<vector<string>>& tickets) {
        unordered_map<string, vector<string>> adj;
        for (auto& ticket : tickets) {
            adj[ticket[0]];
        }

        sort(tickets.begin(), tickets.end());
        for (auto& ticket : tickets) {
            adj[ticket[0]].push_back(ticket[1]);
        }

        vector<string> res = {"JFK"};
        dfs("JFK", res, adj, tickets.size() + 1);
        return res;
    }

private:
    bool dfs(const string& src, vector<string>& res,
             unordered_map<string, vector<string>>& adj, int targetLen) {
        if (res.size() == targetLen) {
            return true;
        }

        if (adj.find(src) == adj.end()) {
            return false;
        }

        vector<string> temp = adj[src];
        for (int i = 0; i < temp.size(); ++i) {
            string v = temp[i];
            adj[src].erase(adj[src].begin() + i);
            res.push_back(v);
            if (dfs(v, res, adj, targetLen)) return true;
            adj[src].insert(adj[src].begin() + i, v);
            res.pop_back();
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(E * V)$
- Space complexity: $O(E * V)$

> Where $E$ is the number of tickets (edges) and $V$ is the number of airports (vertices).

## 2. Hierholzer's Algorithm (Recursion) ▶ video

This problem is an **Eulerian Path** problem:  
we must use **every ticket exactly once** and form a valid path starting from `"JFK"`.

**Hierholzer's Algorithm** builds such a path by:

- always taking an available edge,
- going as deep as possible,
- and adding airports to the answer **only when no outgoing edges remain**.

To ensure the **lexicographically smallest** itinerary:

- we sort tickets,
- and always pick the smallest destination first.

The key idea:

> **Build the path in reverse while backtracking.**

```cpp
class Solution {
public:
    vector<string> findItinerary(vector<vector<string>>& tickets) {
        unordered_map<string, deque<string>> adj;
        for (auto& ticket : tickets) {
            adj[ticket[0]].push_back(ticket[1]);
        }
        for (auto& [src, dests] : adj) {
            sort(dests.rbegin(), dests.rend());
        }

        vector<string> res;
        dfs("JFK", adj, res);
        reverse(res.begin(), res.end());
        return res;
    }

private:
    void dfs(const string& src, unordered_map<string,
             deque<string>>& adj, vector<string>& res) {
        while (!adj[src].empty()) {
            string dst = adj[src].back();
            adj[src].pop_back();
            dfs(dst, adj, res);
        }
        res.push_back(src);
    }
};
```

**Complexity**

- Time complexity: $O(E\log E)$
- Space complexity: $O(E)$

> Where $E$ is the number of tickets (edges) and $V$ is the number of airports (vertices).

## 3. Hierholzer's Algorithm (Iteration)

This is the **iterative version of Hierholzer’s Algorithm** for finding an **Eulerian Path**.

We must:

- use **every ticket exactly once**,
- start from `"JFK"`,
- and return the **lexicographically smallest** valid itinerary.

Instead of recursion, we simulate the DFS using a **stack**:

- Keep moving forward while tickets exist.
- When stuck (no outgoing flights), **backtrack** and record the airport.

Key idea:

> **Airports are added to the answer only when they have no remaining outgoing edges.**

```cpp
class Solution {
public:
    vector<string> findItinerary(vector<vector<string>>& tickets) {
        unordered_map<string, vector<string>> adj;
        for (const auto& ticket : tickets) {
            adj[ticket[0]].push_back(ticket[1]);
        }
        for (auto& [src, destinations] : adj) {
            sort(destinations.rbegin(), destinations.rend());
        }

        vector<string> res;
        stack<string> stk;
        stk.push("JFK");

        while (!stk.empty()) {
            string curr = stk.top();
            if (adj[curr].empty()) {
                res.push_back(curr);
                stk.pop();
            } else {
                string next = adj[curr].back();
                adj[curr].pop_back();
                stk.push(next);
            }
        }

        reverse(res.begin(), res.end());
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(E\log E)$
- Space complexity: $O(E)$

> Where $E$ is the number of tickets (edges) and $V$ is the number of airports (vertices).

## Standalone solution file (`cpp/0332-reconstruct-itinerary.cpp` in the NeetCode repo)

```cpp
/*
    Given airline tickets, find valid itinerary (use all tickets once)
    Ex. tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
        output = ["JFK","MUC","LHR","SFO","SJC"]

    Greedy DFS, build route backwards when retreating, merge cycles into main path

    Time: O(E log (E / V)) -> E = # of flights, V = # of airports, sorting
    Space: O(V + E) -> store # of airports & # of flights in hash map
*/

class Solution {
public:
    vector<string> findItinerary(vector<vector<string>>& tickets) {
        unordered_map<string, multiset<string>> m;
        for (int i = 0; i < tickets.size(); i++) {
            m[tickets[i][0]].insert(tickets[i][1]);
        }
        
        vector<string> result;
        dfs(m, "JFK", result);
        reverse(result.begin(), result.end());
        return result;
    }
private:
    void dfs(unordered_map<string, multiset<string>>& m,
        string airport, vector<string>& result) {
        
        while (!m[airport].empty()) {
            string next = *m[airport].begin();
            m[airport].erase(m[airport].begin());
            dfs(m, next, result);
        }
        
        result.push_back(airport);
    }
};
```
