# 1086. High Five

- **Difficulty:** Easy  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/high-five/>  
- **NeetCode:** <https://neetcode.io/problems/high-five>  

[← Back to index](../INDEX.md)

## 1. Using Sorting

We need to find each student's average of their top `5` scores.
If we sort all items by student ID (ascending) and by score (descending), then for each student, their first `5` entries will be their highest scores.
We can then group by student, sum their top `5` scores, and compute the average.

```cpp
class Solution {
private:
    int K;

public:
    vector<vector<int>> highFive(vector<vector<int>>& items) {
        this->K = 5;
        // sort items using the custom comparator
        sort(items.begin(), items.end(),
            [](const vector<int> &a, const vector<int> &b) {
                if (a[0] != b[0])
                // item with lower id goes first
                return a[0] < b[0];
                // in case of tie for ids, item with higher score goes first
                return a[1] > b[1];
            });
        vector<vector<int>> solution;
        int n = items.size();
        int i = 0;
        while (i < n) {
            int id = items[i][0];
            int sum = 0;
            // obtain total using the top 5 scores
            for (int k = i; k < i + this->K; ++k)
                sum += items[k][1];
            // ignore all the other scores for the same id
            while (i < n && items[i][0] == id)
                i++;
            solution.push_back({id, sum / this->K});
        }
        return solution;
    }
};
```

**Complexity**

- Time complexity: $O(N \log N)$
- Space complexity: $O(N)$

> Where $N$ is the total number of items.

## 2. Using Map and Max Heap

Instead of sorting all items, we can use a map to group scores by student ID and a max heap for each student.
The max heap naturally keeps the largest scores at the top, so extracting the top `5` is straightforward.
Using a TreeMap (or sorted map) ensures students are processed in ID order.

```cpp
class Solution {
private:
    int K;

public:
    vector<vector<int>> highFive(vector<vector<int>>& items) {
        this->K = 5;
        map<int, priority_queue<int>> allScores;
        for (const auto &item: items) {
            int id = item[0];
            int score = item[1];
            // Add score to the max heap
            allScores[id].push(score);
        }
        vector<vector<int>> solution;
        for (auto &[id, scores] : allScores) {
            int sum = 0;
            // obtain the top k scores (k = 5)
            for (int i = 0; i < this->K; ++i) {
                sum += scores.top();
                scores.pop();
            }
            solution.push_back({id, sum / this->K});
        }
        return solution;
    }
};
```

**Complexity**

- Time complexity: $O(N \log N)$
- Space complexity: $O(N)$

> Where $N$ is the total number of items.

## 3. Using Map and Min Heap

A min heap of size `5` is more space efficient than storing all scores.
As we process each score, we add it to the heap. If the heap size exceeds `5`, we remove the smallest score.
This ensures the heap always contains the top `5` scores for each student.
At the end, we simply sum all elements in the heap to get the total of the top `5` scores.

```cpp
class Solution {
private:
    int K;

public:
    vector<vector<int>> highFive(vector<vector<int>>& items) {
        this->K = 5;
        map<int, priority_queue<int, vector<int>, greater<int>>> allScores;
        for (const auto &item: items) {
            int id = item[0];
            int score = item[1];
            // insert the score in the min heap
            allScores[id].push(score);
            // remove the minimum element from the min heap in case the size of the min heap exceeds 5
            if (allScores[id].size() > this->K)
                allScores[id].pop();
        }
        vector<vector<int>> solution;
        for (auto &[id, top_scores]: allScores) {
            int total = 0;
            // min heap contains the top 5 scores
            for (int i = 0; i < this->K; ++i) {
                total += top_scores.top();
                top_scores.pop();
            }
            solution.push_back({id, total / this->K});
        }
        return solution;
    }
};
```

**Complexity**

- Time complexity: $O(N \log N)$
- Space complexity: $O(N)$

> Where $N$ is the total number of items.
