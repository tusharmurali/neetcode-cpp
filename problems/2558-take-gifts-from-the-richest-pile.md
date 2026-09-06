# 2558. Take Gifts From the Richest Pile

- **Difficulty:** Easy  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/take-gifts-from-the-richest-pile/>  
- **NeetCode:** <https://neetcode.io/problems/take-gifts-from-the-richest-pile>  
- **Video:** <https://www.youtube.com/watch?v=bHEQ4D_XcyY>  

[← Back to index](../INDEX.md)

## 1. Simulation

The most straightforward approach simulates the process exactly as described. Each second, we find the pile with the most gifts, take gifts from it, and leave behind the floor of its square root. After `k` seconds, we sum up all remaining gifts. Finding the maximum each time requires scanning all piles.

```cpp
class Solution {
public:
    long long pickGifts(vector<int>& gifts, int k) {
        for (int t = 0; t < k; t++) {
            int maxIdx = 0;
            for (int i = 1; i < gifts.size(); i++) {
                if (gifts[i] > gifts[maxIdx]) {
                    maxIdx = i;
                }
            }
            gifts[maxIdx] = floor(sqrt(gifts[maxIdx]));
        }

        long long sum = 0;
        for (int g : gifts) sum += g;
        return sum;
    }
};
```

**Complexity**

* Time complexity: $O(n * k)$
* Space complexity: $O(1)$ extra space.

> Where $n$ is the size of input array, $k$ is the number of seconds.

## 2. Max-Heap

Finding the maximum element repeatedly is expensive with a linear scan. A max-heap keeps the largest element at the top, allowing O(log `n`) extraction and insertion. Each second, we pop the maximum, compute its square root, and push the result back. This is much faster when `k` is large relative to `n`.

```cpp
class Solution {
public:
    long long pickGifts(vector<int>& gifts, int k) {
        priority_queue<int> pq(gifts.begin(), gifts.end());

        for (int t = 0; t < k; t++) {
            int n = pq.top(); pq.pop();
            pq.push((int)floor(sqrt(n)));
        }

        long long sum = 0;
        while (!pq.empty()) {
            sum += pq.top(); pq.pop();
        }
        return sum;
    }
};
```

**Complexity**

* Time complexity:
    - $O(n + k \log n)$ in Python.
    - $O(n \log n + k \log n)$ in other languages.
* Space complexity: $O(n)$

> Where $n$ is the size of input array, $k$ is the number of seconds.
