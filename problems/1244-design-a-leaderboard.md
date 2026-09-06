# 1244. Design A Leaderboard

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/design-a-leaderboard/>  
- **NeetCode:** <https://neetcode.io/problems/design-a-leaderboard>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest approach stores player scores in a hash map. Adding a score or resetting is straightforward with hash map operations. To find the sum of the top K scores, we extract all scores, sort them in descending order, and sum the first K values. While easy to implement, sorting all scores for every `top` query is inefficient when there are many players.

```cpp
class Leaderboard {
private:
    unordered_map<int, int> scores;

public:
    Leaderboard() {}

    void addScore(int playerId, int score) {
        scores[playerId] += score;
    }

    int top(int K) {
        vector<int> values;
        values.reserve(scores.size());
        
        for (const auto& pair : scores) {
            values.push_back(pair.second);
        }
        
        sort(values.begin(), values.end(), greater<int>());
        
        int total = 0;
        for (int i = 0; i < K; i++) {
            total += values[i];
        }
        return total;
    }

    void reset(int playerId) {
        scores[playerId] = 0;
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ for `addScore`
    - $O(1)$ for `reset`
    - $O(N \log N)$ for `top`

- Space complexity: $O(N)$

>  Where $N$ is the total number of players in the leaderboard.

## 2. Heap for top-K

Instead of sorting all `N` scores, we can use a min-heap of size `K` to find the top `K` scores more efficiently. As we iterate through all scores, we maintain a heap containing the `K` largest scores seen so far. When the heap exceeds size `K`, we remove the smallest element. After processing all scores, the heap contains exactly the top `K` scores, and we sum them up.

```cpp
class Leaderboard {
private:
    unordered_map<int, int> scores;
    
public:
    Leaderboard() {
        
    }
    
    void addScore(int playerId, int score) {
        if (scores.find(playerId) == scores.end()) {
            scores[playerId] = 0;
        }
        scores[playerId] += score;
    }
    
    int top(int K) {
        // By default, priority_queue is max-heap, so we use greater<int> for min-heap
        priority_queue<int, vector<int>, greater<int>> heap;
        
        for (const auto& entry : scores) {
            heap.push(entry.second);
            if (heap.size() > K) {
                heap.pop();
            }
        }
        
        int total = 0;
        while (!heap.empty()) {
            total += heap.top();
            heap.pop();
        }
        return total;
    }
    
    void reset(int playerId) {
        scores[playerId] = 0;
    }
};
```

**Complexity**

- Time complexity:
    - $O(1)$ for `addScore`
    - $O(1)$ for `reset`
    - $O(N \log K)$ for `top`

- Space complexity: $O(N + K)$

>  Where $N$ is the total number of players in the leaderboard, and $K$ is the number of top-scoring players.

## 3. Using a TreeMap / SortedMap

A `TreeMap` (or sorted dictionary) keeps scores in sorted order, allowing us to iterate from highest to lowest efficiently. The key insight is to track how many players share each score rather than storing individual player entries. When a score changes, we decrement the count for the old score and increment for the new one. For `top(K)`, we iterate through scores in descending order, accumulating until we reach `K` players.

```cpp
class Leaderboard {
public:
    unordered_map<int, int> scores;
    map<int, int, greater<int>> sortedScores;

    Leaderboard() {}

    void addScore(int playerId, int score) {
        if (scores.find(playerId) == scores.end()) {
            scores[playerId] = score;
            sortedScores[score]++;
        } else {
            int preScore = scores[playerId];
            sortedScores[preScore]--;
            if (sortedScores[preScore] == 0) {
                sortedScores.erase(preScore);
            }

            int newScore = preScore + score;
            scores[playerId] = newScore;
            sortedScores[newScore]++;
        }
    }

    int top(int K) {
        int count = 0, sum = 0;

        for (auto& [key, times] : sortedScores) {
            for (int i = 0; i < times; i++) {
                sum += key;
                count++;
                if (count == K) break;
            }
            if (count == K) break;
        }

        return sum;
    }

    void reset(int playerId) {
        int preScore = scores[playerId];
        sortedScores[preScore]--;
        if (sortedScores[preScore] == 0) {
            sortedScores.erase(preScore);
        }
        scores.erase(playerId);
    }
};
```

**Complexity**

- Time complexity:
    - $O(\log N)$ for `addScore`

    - $O(\log N)$ for `reset`.  Note that this complexity is in the case when every player always maintains a unique score.

    - $O(K)$ for `top`. Note that if the data structure doesn't provide a natural iterator, then we can simply get a list of all the key-value pairs and they will naturally be sorted due to the nature of this data structure. In that case, the complexity would be $O(N)$ since we would be forming a new list. 

- Space complexity: $O(N)$ used by the `scores` dictionary. Also, if you obtain all the key-value pairs in a new list in the `top` function, then an additional $O(N)$ would be used.


>  Where $N$ is the total number of players in the leaderboard, and $K$ is the number of top-scoring players.
