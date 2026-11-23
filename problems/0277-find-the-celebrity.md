# 277. Find the Celebrity

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-the-celebrity/>  
- **NeetCode:** <https://neetcode.io/problems/find-the-celebrity>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A celebrity is someone who is known by everyone but knows nobody. For each person, we can check if they satisfy both conditions: they don't know anyone else, and everyone else knows them. If both conditions hold, that person is the celebrity.

```cpp
/* The knows API is defined for you.
      bool knows(int a, int b); */

class Solution {
private:
    int numberOfPeople;

    bool isCelebrity(int i) {
        for (int j = 0; j < numberOfPeople; j++) {
            if (i == j) continue; // Don't ask if they know themselves.
            if (knows(i, j) || !knows(j, i)) {
                return false;
            }
        }
        return true;
    }

public:
    int findCelebrity(int n) {
        numberOfPeople = n;
        for (int i = 0; i < n; i++) {
            if (isCelebrity(i)) {
                return i;
            }
        }
        return -1;
    }
};
```

**Complexity**

We don't know what time and space the `knows(...)` API uses. Because it's not our concern, we'll assume it's `O(1)` for the purpose of analysing our algorithm.

- Time complexity: $O(n^2)$
- Space complexity: $O(1)$

>  Where $n$ is the number of nodes in the graph.

## 2. Logical Deduction

Each `knows(a, b)` call eliminates one person from being a celebrity. If `a` knows `b`, then `a` cannot be the celebrity (celebrities know nobody). If `a` doesn't know `b`, then `b` cannot be the celebrity (everyone must know the celebrity). By iterating through all people once, we can narrow down to a single candidate. We then verify this candidate with a second pass.

```cpp
class Solution {
private:
    int n;

    bool is_celebrity(int i) {
        for (int j = 0; j < n; j++) {
            if (i == j) continue;
            if (knows(i, j) || !knows(j, i)) {
                return false;
            }
        }
        return true;
    }

public:
    int findCelebrity(int n) {
        this->n = n;
        int celebrity_candidate = 0;

        for (int i = 1; i < n; i++) {
            if (knows(celebrity_candidate, i)) {
                celebrity_candidate = i;
            }
        }

        if (is_celebrity(celebrity_candidate)) {
            return celebrity_candidate;
        }
        return -1;
    }
};
```

**Complexity**

We don't know what time and space the `knows(...)` API uses. Because it's not our concern, we'll assume it's `O(1)` for the purpose of analysing our algorithm.

- Time complexity: $O(n)$
- Space complexity: $O(1)$

>  Where $n$ is the number of nodes in the graph.

## 3. Logical Deduction with Caching

The logical deduction approach may call `knows(a, b)` multiple times with the same arguments during the verification phase. By caching the results of each call, we can avoid redundant API calls. This is particularly useful when the `knows` function is expensive to evaluate.

```cpp
/* The knows API is defined for you.
      bool knows(int a, int b); */

class Solution {
private:
    int numberOfPeople;
    unordered_map<long long, bool> cache;

    bool cachedKnows(int a, int b) {
        long long key = (long long)a * numberOfPeople + b;
        auto it = cache.find(key);
        if (it == cache.end()) {
            it = cache.emplace(key, knows(a, b)).first;
        }
        return it->second;
    }

    bool isCelebrity(int i) {
        for (int j = 0; j < numberOfPeople; j++) {
            if (i == j) continue; // Don't ask if they know themselves.
            if (cachedKnows(i, j) || !cachedKnows(j, i)) {
                return false;
            }
        }
        return true;
    }

public:
    int findCelebrity(int n) {
        numberOfPeople = n;
        int celebrityCandidate = 0;
        for (int i = 0; i < n; i++) {
            if (cachedKnows(celebrityCandidate, i)) {
                celebrityCandidate = i;
            }
        }
        if (isCelebrity(celebrityCandidate)) {
            return celebrityCandidate;
        }
        return -1;
    }
};
```

**Complexity**

We don't know what time and space the `knows(...)` API uses. Because it's not our concern, we'll assume it's `O(1)` for the purpose of analysing our algorithm.

- Time complexity: $O(n)$
- Space complexity: $O(n)$

>  Where $n$ is the number of nodes in the graph.
