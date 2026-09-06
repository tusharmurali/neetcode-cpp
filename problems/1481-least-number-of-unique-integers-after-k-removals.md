# 1481. Least Number of Unique Integers after K Removal

- **Difficulty:** Medium  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/least-number-of-unique-integers-after-k-removals/>  
- **NeetCode:** <https://neetcode.io/problems/least-number-of-unique-integers-after-k-removals>  
- **Video:** <https://www.youtube.com/watch?v=Nsp_ta7SlEk>  

[← Back to index](../INDEX.md)

## 1. Sorting

To minimize the number of unique integers after removing `k` elements, we should prioritize removing integers that appear least frequently. By eliminating all occurrences of the rarest integers first, we reduce the unique count most efficiently. Sorting frequencies in ascending order lets us greedily remove elements starting from the smallest frequency.

```cpp
class Solution {
public:
    int findLeastNumOfUniqueInts(vector<int>& arr, int k) {
        unordered_map<int, int> freqMap;
        for (int num : arr) {
            freqMap[num]++;
        }

        vector<int> freq;
        for (auto& [_, count] : freqMap) {
            freq.push_back(count);
        }

        sort(freq.begin(), freq.end());

        int n = freq.size();
        for (int i = 0; i < n; i++) {
            if (k >= freq[i]) {
                k -= freq[i];
            } else {
                return n - i;
            }
        }
        return 0;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 2. Min-Heap

A min-heap naturally gives us access to the smallest frequency first. Instead of sorting all frequencies upfront, we can repeatedly extract the minimum frequency and try to remove that integer. This approach works similarly to sorting but uses a heap data structure for extraction.

```cpp
class Solution {
public:
    int findLeastNumOfUniqueInts(vector<int>& arr, int k) {
        unordered_map<int, int> freqMap;
        for (int num : arr) {
            freqMap[num]++;
        }

        priority_queue<int, vector<int>, greater<int>> minHeap;
        for (auto& [_, count] : freqMap) {
            minHeap.push(count);
        }

        int res = minHeap.size();
        while (k > 0 && !minHeap.empty()) {
            int f = minHeap.top();
            minHeap.pop();
            if (k >= f) {
                k -= f;
                res--;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Bucket Sort

Since frequencies are bounded by the array length, we can use bucket sort to avoid comparison-based sorting. We create buckets where bucket `f` contains the count of integers with frequency `f`. Then we iterate through buckets from frequency `1` upward, removing as many complete integers as possible at each frequency level.

```cpp
class Solution {
public:
    int findLeastNumOfUniqueInts(vector<int>& arr, int k) {
        unordered_map<int, int> freqMap;
        for (int num : arr) {
            freqMap[num]++;
        }

        vector<int> freqList(arr.size() + 1, 0);
        for (auto& [_, f] : freqMap) {
            freqList[f]++;
        }

        int res = freqMap.size();
        for (int f = 1; f < freqList.size(); f++) {
            int remove = freqList[f];
            if (k >= f * remove) {
                k -= f * remove;
                res -= remove;
            } else {
                remove = k / f;
                res -= remove;
                break;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
