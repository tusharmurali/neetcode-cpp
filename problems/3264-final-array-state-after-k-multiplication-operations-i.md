# 3264. Final Array State After K Multiplication Operations I

- **Difficulty:** Easy  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/final-array-state-after-k-multiplication-operations-i/>  
- **NeetCode:** <https://neetcode.io/problems/final-array-state-after-k-multiplication-operations-i>  
- **Video:** <https://www.youtube.com/watch?v=AaoytRXBXGs>  

[← Back to index](../INDEX.md)

## 1. Simulation

The problem asks us to repeatedly find the minimum element and multiply it by a given multiplier. A straightforward approach is to simulate exactly what the problem describes: for each of the `k` operations, scan through the array to find the smallest element (choosing the first occurrence if there are ties), then multiply that element by the multiplier.

```cpp
class Solution {
public:
    vector<int> getFinalState(vector<int>& nums, int k, int multiplier) {
        int n = nums.size();
        for (int _ = 0; _ < k; _++) {
            int minIdx = 0;
            for (int i = 1; i < n; i++) {
                if (nums[i] < nums[minIdx]) {
                    minIdx = i;
                }
            }
            nums[minIdx] *= multiplier;
        }
        return nums;
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(1)$ extra space.

> Where $n$ is the size of the input array, and $k$ is the number of operations.

## 2. Min-Heap

Instead of scanning the entire array each time to find the minimum, we can use a min-heap (priority queue) to efficiently retrieve the smallest element. The heap keeps elements sorted by their value, and when values are equal, by their index. After extracting the minimum, we multiply it, update the result array, and push the updated value back into the heap.

```cpp
class Solution {
public:
    vector<int> getFinalState(vector<int>& nums, int k, int multiplier) {
        int n = nums.size();
        vector<int> res = nums;

        auto cmp = [&](int a, int b) {
            if (res[a] != res[b]) return res[a] > res[b];
            return a > b;
        };
        priority_queue<int, vector<int>, decltype(cmp)> minHeap(cmp);

        for (int i = 0; i < n; i++) {
            minHeap.push(i);
        }

        for (int _ = 0; _ < k; _++) {
            int i = minHeap.top();
            minHeap.pop();
            res[i] *= multiplier;
            minHeap.push(i);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity:
    - $O(n + k \log n)$ in Python.
    - $O(n \log n + k \log n)$ in other languages.

* Space complexity: $O(n)$

> Where $n$ is the size of the input array, and $k$ is the number of operations.
