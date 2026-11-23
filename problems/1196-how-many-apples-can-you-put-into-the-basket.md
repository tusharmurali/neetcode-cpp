# 1196. How Many Apples Can You Put into the Basket

- **Difficulty:** Easy  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/how-many-apples-can-you-put-into-the-basket/>  
- **NeetCode:** <https://neetcode.io/problems/how-many-apples-can-you-put-into-the-basket>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming

```cpp
class Solution {
public:
    int maxNumberOfApples(vector<int>& weight) {
        int n = weight.size();
        vector<int> dp(n + 1, INT_MAX);
        dp[0] = 0;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j >= 1; j--) {
                dp[j] = min(dp[j], dp[j - 1] + weight[i]);
            }
        }

        int res = 0;
        for (int j = 0; j <= n; j++) {
            if (dp[j] <= 5000) {
                res = j;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

> Where $n$ is the number of apples.

## 2. Sorting

```cpp
class Solution {
public:
    int maxNumberOfApples(vector<int>& weight) {
        sort(weight.begin(), weight.end());
        int apples = 0, units = 0;
        for (int w : weight) {
            if (units + w > 5000) {
                break;
            }
            units += w;
            apples++;
        }
        return apples;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

> Where $n$ is the number of apples.

## 3. Min-Heap

```cpp
class Solution {
public:
    int maxNumberOfApples(vector<int>& weight) {
        priority_queue<int, vector<int>, greater<int>> minHeap(weight.begin(), weight.end());
        int apples = 0, units = 0;
        while (!minHeap.empty() && units + minHeap.top() <= 5000) {
            units += minHeap.top();
            minHeap.pop();
            apples++;
        }
        return apples;
    }
};
```

**Complexity**

- Time complexity: $O(n + k \log n)$
- Space complexity: $O(n)$

> Where $n$ is the number of apples and $k$ is the number of apples put into the basket.

## 4. Counting Sort

```cpp
class Solution {
public:
    int maxNumberOfApples(vector<int>& weight) {
        vector<int> count(1001, 0);
        for (int w : weight) {
            count[w]++;
        }

        int apples = 0, units = 0;
        for (int w = 1; w <= 1000; w++) {
            if (count[w] == 0) {
                continue;
            }
            int take = min(count[w], (5000 - units) / w);
            if (take == 0) {
                break;
            }
            apples += take;
            units += take * w;
        }
        return apples;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(m)$

> Where $n$ is the number of apples and $m$ is the maximum weight of an apple ($m = 1000$).
