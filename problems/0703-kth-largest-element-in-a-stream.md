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

A **min-heap of size at most `k`** is perfect for this:

- A min-heap always keeps the **smallest value at the top**.
- If the heap contains the `k` largest elements,
  then the **smallest among them** is exactly the **k-th largest overall**.
- Whenever a new number arrives:
    - If we add it and the heap grows beyond `k`,
      we remove the smallest element - because it cannot be in the top `k` anymore.

After trimming, the heap holds at most `k` elements. Once at least `k` values have arrived, it holds exactly the **top `k` elements**, and retrieving the k-th largest takes `O(1)`.

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

- Time complexity:
    - Python: $O(n + (n-k) \log n + m \log(k + 1))$ when $n > k$, or $O(n + m \log(k + 1))$ otherwise. Heapifying takes $O(n)$, followed by $n-k$ heap removals when $n > k$.
    - Java, C++, C#, Swift, Rust: $O((n + m) \log(k + 1))$. Trimming after each initial insertion keeps the heap at most $k+1$ elements during insertion and at most $k$ afterward.
    - JavaScript, Go, Kotlin: $O(n \log(n + 1) + m \log(k + 1))$. These versions insert all $n$ initial values before trimming the heap, so initialization takes $O(n \log(n + 1))$.
- Space complexity (peak heap storage):
    - Java, C++, C#, Swift, Rust: $O(k)$, since the heap is trimmed after each initial insertion.
    - Python, JavaScript, Go, Kotlin: $O(n + k)$, equivalently $O(\max(n, k))$, since the heap initially holds all $n$ values and can later grow to $k+1$ during an insertion. Python reuses the input list, so its peak heap storage includes that existing list rather than a separate $n$-element heap.

Each $add()$ call takes $O(\log(k + 1))$ amortized time, accounting for occasional backing-array resizing. Using $\log(k + 1)$ also covers $k = 1$.

> Where $n$ is the initial array length, $m$ is the number of calls made to $add()$, and $k$ is the rank being tracked.

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
