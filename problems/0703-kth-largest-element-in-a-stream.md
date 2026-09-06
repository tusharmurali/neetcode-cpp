# 703. Kth Largest Element In a Stream

- **Difficulty:** Easy  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/kth-largest-element-in-a-stream/>  
- **NeetCode:** <https://neetcode.io/problems/kth-largest-integer-in-a-stream>  
- **Video:** <https://www.youtube.com/watch?v=hOjcdrqMoQ8>  
- **Video approach:** 2. Min-Heap  

[← Back to index](../INDEX.md)

## 1. Sorting

We want the **k-th largest number** in a stream of values.
The simplest approach:
Every time a new value comes in, **insert it**, sort the list, and then pick the element at position `len(arr) - k`.

Sorting keeps the numbers in increasing order, so the k-th largest element will always sit at the same index.  
This method is easy to understand but slow because sorting happens every time `add()` is called.

```cpp
class KthLargest {
public:
    vector<int> arr;
    int k;
    KthLargest(int k, vector<int>& nums) {
        this->arr = nums;
        this->k = k;
    }

    int add(int val) {
        arr.push_back(val);
        sort(arr.begin(), arr.end());
        return arr[arr.size() - k];
    }
};
```

**Complexity**

- Time complexity: $O(m * n\log n)$
- Space complexity:
    - $O(m)$ extra space.
    - $O(1)$ or $O(n)$ space depending on the sorting algorithm.

> Where $m$ is the number of calls made to $add()$ and $n$ is the current size of the array.

## 2. Min-Heap ▶ video

To maintain the **k-th largest element** in a stream of numbers, we do **not** need to store all values.  
Instead, we only need to keep track of the **k largest elements seen so far**.

A **min-heap of size `k`** is perfect for this:

- A min-heap always keeps the **smallest value at the top**.
- If the heap contains the `k` largest elements,
  then the **smallest among them** is exactly the **k-th largest overall**.
- Whenever a new number arrives:
    - If we add it and the heap grows beyond `k`,
      we remove the smallest element - because it cannot be in the top `k` anymore.

This way, the heap always holds exactly the **top `k` elements**, and retrieving the k-th largest is `O(1)`.

```cpp
class KthLargest {
private:
    priority_queue<int, vector<int>, greater<int>> minHeap;
    int k;

public:
    KthLargest(int k, vector<int>& nums) {
        this->k = k;
        for (int num : nums) {
            minHeap.push(num);
            if (minHeap.size() > k) {
                minHeap.pop();
            }
        }
    }

    int add(int val) {
        minHeap.push(val);
        if (minHeap.size() > k) {
            minHeap.pop();
        }
        return minHeap.top();
    }
};
```

**Complexity**

- Time complexity: $O(m * \log k)$
- Space complexity: $O(k)$

> Where $m$ is the number of calls made to $add()$.

## Standalone solution file (`cpp/0703-kth-largest-element-in-a-stream.cpp` in the NeetCode repo)

```cpp
/*
    Design a class to find the kth largest element in a stream

    Min heap & maintain only k elements, top will always be kth largest
    Ex. nums = [6,2,3,1,7], k = 3 -> [1,2,3,6,7] -> [3,6,7]

    Time: O(n log n + m log k) -> n = length of nums, m = add calls
    Space: O(n)
*/

class KthLargest {
public:
    KthLargest(int k, vector<int>& nums) {
        this->k = k;
        for (int i = 0; i < nums.size(); i++) {
            pq.push(nums[i]);
        }
        while (pq.size() > this->k) {
            pq.pop();
        }
    }
    
    int add(int val) {
        pq.push(val);
        if (pq.size() > k) {
            pq.pop();
        }
        return pq.top();
    }
private:
    int k;
    priority_queue<int, vector<int>, greater<int>> pq;
};

/**
 * Your KthLargest object will be instantiated and called as such:
 * KthLargest* obj = new KthLargest(k, nums);
 * int param_1 = obj->add(val);
 */
```
