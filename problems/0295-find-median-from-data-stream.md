# 295. Find Median From Data Stream

- **Difficulty:** Hard  
- **Pattern:** Heap / Priority Queue  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/find-median-from-data-stream/>  
- **NeetCode:** <https://neetcode.io/problems/find-median-in-a-data-stream>  
- **Video:** <https://www.youtube.com/watch?v=itmhHWaHupI>  

[← Back to index](../INDEX.md)

## 1. Sorting

The simplest way to find the median is to keep all numbers in a list and
sort them whenever we need the median. After sorting, the numbers are in
increasing order, making it easy to pick the "middle" value(s).

- If we have an **odd** number of elements, the median is the **middle** element.
- If we have an **even** number of elements, the median is the **average**
  of the two middle elements.

This approach is slow because sorting happens every time we query the median,
but it is the easiest to understand and implement.

```cpp
class MedianFinder {
    vector<int> data;

public:
    MedianFinder() {}

    void addNum(int num) {
        data.push_back(num);
    }

    double findMedian() {
        sort(data.begin(), data.end());
        int n = data.size();
        if (n & 1) {
            return data[n / 2];
        } else {
            return (data[n / 2] + data[n / 2 - 1]) / 2.0;
        }
    }
};
```

**Complexity**

- Time complexity: $O(m)$ for $addNum()$, $O(m * n \log n)$ for $findMedian()$.
- Space complexity: $O(n)$

> Where $m$ is the number of function calls and $n$ is the length of the array.

## 2. Heap

To efficiently find the median while numbers keep coming, we split the
stream into two halves:

- A **max-heap** (`small`) that stores the _smaller half_ of the numbers.
    - The largest number of this half is on top.
- A **min-heap** (`large`) that stores the _larger half_ of the numbers.
    - The smallest number of this half is on top.

The goal:

- Ensure both heaps are balanced in size (difference at most 1).
- Ensure all numbers in `small` are ≤ all numbers in `large`.

This setup allows:

- Median = top of the bigger heap (if odd count)
- Median = average of both tops (if even count)

This gives **O(log n)** insert and **O(1)** median lookup.

```cpp
class MedianFinder {
    priority_queue<int, vector<int>, less<int>> smallHeap;
    priority_queue<int, vector<int>, greater<int>> largeHeap;

public:
    MedianFinder() {}

    void addNum(int num) {
        smallHeap.push(num);
        if (!largeHeap.empty() && smallHeap.top() > largeHeap.top()) {
            largeHeap.push(smallHeap.top());
            smallHeap.pop();
        }
        if (smallHeap.size() > largeHeap.size() + 1) {
            largeHeap.push(smallHeap.top());
            smallHeap.pop();
        }
        if (largeHeap.size() > smallHeap.size() + 1) {
            smallHeap.push(largeHeap.top());
            largeHeap.pop();
        }
    }

    double findMedian() {
        if (smallHeap.size() == largeHeap.size()) {
            return (largeHeap.top() + smallHeap.top()) / 2.0;
        } else if (smallHeap.size() > largeHeap.size()) {
            return smallHeap.top();
        } else {
            return largeHeap.top();
        }
    }
};
```

**Complexity**

- Time complexity: $O(m * \log n)$ for $addNum()$, $O(m)$ for $findMedian()$.
- Space complexity: $O(n)$

> Where $m$ is the number of function calls and $n$ is the length of the array.

## Standalone solution file (`cpp/0295-find-median-from-data-stream.cpp` in the NeetCode repo)

```cpp
/*
    Implement data structure that gets the median from a data stream

    Max heap of lower values & min heap of higher values, access to mids

    Time: O(log n) + O(1)
    Space: O(n)
*/

class MedianFinder {
public:
    MedianFinder() {
        
    }
    
    void addNum(int num) {
        if (lower.empty()) {
            lower.push(num);
            return;
        }
        
        if (lower.size() > higher.size()) {
            if (lower.top() > num) {
                higher.push(lower.top());
                lower.pop();
                lower.push(num);
            } else {
                higher.push(num);
            }
        } else {
            if (num > higher.top()) {
                lower.push(higher.top());
                higher.pop();
                higher.push(num);
            } else {
                lower.push(num);
            }
        }
    }
    
    double findMedian() {
        double result = 0.0;
        
        if (lower.size() == higher.size()) {
            result = lower.top() + (higher.top() - lower.top()) / 2.0;
        } else {
            if (lower.size() > higher.size()) {
                result = lower.top();
            } else {
                result = higher.top();
            }
        }
        
        return result;
    }
private:
    priority_queue<int> lower;
    priority_queue<int, vector<int>, greater<int>> higher;
};

/**
 * Your MedianFinder object will be instantiated and called as such:
 * MedianFinder* obj = new MedianFinder();
 * obj->addNum(num);
 * double param_2 = obj->findMedian();
 */
```
