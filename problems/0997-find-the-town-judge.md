# 997. Find the Town Judge

- **Difficulty:** Easy  
- **Pattern:** Graphs  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/find-the-town-judge/>  
- **NeetCode:** <https://neetcode.io/problems/find-the-town-judge>  
- **Video:** <https://www.youtube.com/watch?v=QiGaxdUINJ8>  

[← Back to index](../INDEX.md)

## 1. Indegree & Outdegree

The town judge is trusted by everyone else but trusts nobody. In graph terms, if we model trust relationships as directed edges, the judge has an indegree of `n - 1` (everyone trusts them) and an outdegree of 0 (they trust nobody). We simply count incoming and outgoing edges for each person and find the one matching these criteria.

```cpp
class Solution {
public:
    int findJudge(int n, vector<vector<int>>& trust) {
        vector<int> incoming(n + 1, 0), outgoing(n + 1, 0);

        for (auto& t : trust) {
            outgoing[t[0]]++;
            incoming[t[1]]++;
        }

        for (int i = 1; i <= n; i++) {
            if (outgoing[i] == 0 && incoming[i] == n - 1)
                return i;
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 2. Indegree & Outdegree (Optimal)

We can combine the two arrays into one by using the difference: `delta[i] = incoming[i] - outgoing[i]`. The judge has `n - 1` people trusting them and trusts 0 people, so their delta equals `(n - 1) - 0 = n - 1`. Anyone who trusts at least one person will have a delta less than `n - 1`.

```cpp
class Solution {
public:
    int findJudge(int n, vector<vector<int>>& trust) {
        vector<int> delta(n + 1, 0);

        for (auto& t : trust) {
            delta[t[0]]--;
            delta[t[1]]++;
        }

        for (int i = 1; i <= n; i++) {
            if (delta[i] == n - 1) {
                return i;
            }
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V)$

> Where $V$ is the number of vertices and $E$ is the number of edges.
