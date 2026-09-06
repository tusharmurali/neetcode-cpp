# 346. Moving Average from Data Stream

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/moving-average-from-data-stream/>  
- **NeetCode:** <https://neetcode.io/problems/moving-average-from-data-stream>  

[← Back to index](../INDEX.md)

## 1. Array or List

The most straightforward way to compute a moving average is to store all incoming values in a list and calculate the average of the last `size` elements each time. When a new value arrives, we append it to the list, then sum the most recent values up to the window size. This approach is simple to implement but recalculates the sum from scratch on every call.

```cpp
class MovingAverage {
private:
    int size;
    vector<int> queue;

public:
    /** Initialize your data structure here. */
    MovingAverage(int size) { this->size = size; }

    double next(int val) {
        queue.push_back(val);
        // calculate the sum of the moving window
        int windowSum = 0;
        for (int i = max(0, (int)queue.size() - size); i < queue.size(); ++i)
            windowSum += queue[i];

        return windowSum * 1.0 / min((int)queue.size(), size);
    }
};
```

**Complexity**

- Time complexity: $O(N \cdot M)$
- Space complexity: $O(M)$

> Where $N$ is the size of the moving window and $M$ is the number of calls made to `next`.

## 2. Double-ended Queue

Instead of recalculating the sum each time, we can maintain a running sum and a queue that holds only the elements within the current window. When the window is full and a new element arrives, we remove the oldest element from both the queue and the running sum, then add the new element. This way, each `next()` call runs in constant time.

```cpp
class MovingAverage {
private:
    int size, windowSum = 0, count = 0;
    std::deque<int> queue;

public:
    MovingAverage(int size) { this->size = size; }

    double next(int val) {
        ++count;
        // calculate the new sum by shifting the window
        queue.push_back(val);
        int tail = count > size ? queue.front() : 0;
        if (count > size) queue.pop_front();

        windowSum = windowSum - tail + val;

        return static_cast<double>(windowSum) / std::min(size, count);
    }
};
```

**Complexity**

- Time complexity: $O(M)$
    - Time complexity per `next()` call is $O(1)$. Therefore, the total time complexity for $M$ calls is $O(M)$
- Space complexity: $O(N)$

> Where $N$ is the size of the moving window and $M$ is the number of calls made to `next`.

## 3. Circular Queue with Array

A circular queue (ring buffer) avoids the overhead of shifting elements when removing from the front. We use a fixed-size array where the head pointer wraps around when it reaches the end. The element being overwritten is the one leaving the window, so we subtract it from the running sum before adding the new value. This achieves constant time per operation with minimal memory overhead.

```cpp
class MovingAverage {
private:
    int size;
    int head = 0;
    int windowSum = 0;
    int count = 0;
    vector<int> queue;

public:
    MovingAverage(int size) {
        this->size = size;
        queue = vector<int>(size);
    }

    double next(int val) {
        ++count;

        // calculate the new sum by shifting the window
        int tail = (head + 1) % size;
        windowSum = windowSum - queue[tail] + val;

        // move on to the next head
        head = (head + 1) % size;
        queue[head] = val;
        return windowSum * 1.0 / min(size, count);
    }
};
```

**Complexity**

- Time complexity: $O(M)$
    - Time complexity per `next()` call is $O(1)$. Therefore, the total time complexity for $M$ calls is $O(M)$
- Space complexity: $O(N)$

> Where $N$ is the size of the moving window and $M$ is the number of calls made to `next`.
