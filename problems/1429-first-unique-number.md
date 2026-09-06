# 1429. First Unique Number

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/first-unique-number/>  
- **NeetCode:** <https://neetcode.io/problems/first-unique-number>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The straightforward approach stores all numbers in a queue. When asked for the first unique number, we scan through the queue and count occurrences of each element. The first element with count `1` is our answer.

```cpp
class FirstUnique {
private:
    queue<int> q;

public:
    FirstUnique(vector<int>& nums) {
        for (int num : nums) {
            q.push(num);
        }
    }

    int showFirstUnique() {
        queue<int> temp = q;
        while (!temp.empty()) {
            int num = temp.front();
            temp.pop();

            int count = 0;
            queue<int> countTemp = q;
            while (!countTemp.empty()) {
                if (countTemp.front() == num) count++;
                countTemp.pop();
            }

            if (count == 1) {
                return num;
            }
        }
        return -1;
    }

    void add(int value) {
        q.push(value);
    }
};
```

**Complexity**

- Time complexity:
    - **constructor**: $O(K)$

    - **add()**: $O(1)$

    - **showFirstUnique()**: $O(N^2)$

- Space complexity: $O(N)$

> Where $K$ is the length of the initial array passed into the constructor and $N$ is the total number of items added into the queue so far (including those from the constructor).

## 2. Queue and HashMap of Unique-Status

We can speed up uniqueness checks by maintaining a hash map that tracks whether each number is unique. The queue preserves insertion order. When showing the first unique, we pop non-unique elements from the front of the queue until we find a unique one or the queue is empty.

```cpp
class FirstUnique {
private:
    queue<int> q;
    unordered_map<int, bool> isUnique;

public:
    FirstUnique(vector<int>& nums) {
        for (int num : nums) {
            this->add(num);
        }
    }

    int showFirstUnique() {
        while (!q.empty() && !isUnique[q.front()]) {
            q.pop();
        }

        if (!q.empty()) {
            return q.front();
        }

        return -1;
    }

    void add(int value) {
        if (isUnique.find(value) == isUnique.end()) {
            isUnique[value] = true;
            q.push(value);
        } else {
            isUnique[value] = false;
        }
    }
};
```

**Complexity**

- Time complexity:
    - **constructor**: $O(K)$

    - **add()**: $O(1)$

    - **showFirstUnique()**: $O(1)$ (amortized)

- Space complexity: $O(N)$

> Where $K$ is the length of the initial array passed into the constructor and $N$ is the total number of items added into the queue so far (including those from the constructor).

## 3. LinkedHashSet for Queue, and HashMap of Unique-Statuses

Instead of lazily removing non-unique elements during `showFirstUnique()`, we can eagerly remove them when they become non-unique. Using a LinkedHashSet (or OrderedDict) allows O(1) removal by value while preserving insertion order. This makes `showFirstUnique()` a true O(1) operation.

```cpp
class FirstUnique {
private:
    std::list<int> setQueue;
    std::unordered_map<int, std::list<int>::iterator> queuePosition;
    std::unordered_map<int, bool> isUnique;

public:
    FirstUnique(vector<int>& nums) {
        for (int num : nums) {
            this->add(num);
        }
    }

    int showFirstUnique() {
        // If the queue contains values, we need to get the first one from it.
        // We can do this by making an iterator, and getting its first item.
        if (!setQueue.empty()) {
            return setQueue.front();
        }
        return -1;
    }

    void add(int value) {
        // Case 1: This value is not yet in the data structure.
        // It should be ADDED.
        if (isUnique.find(value) == isUnique.end()) {
            isUnique[value] = true;
            setQueue.push_back(value);
            queuePosition[value] = std::prev(setQueue.end());
        // Case 2: This value has been seen once, so is now becoming
        // non-unique. It should be REMOVED.
        } else if (isUnique[value]) {
            isUnique[value] = false;
            setQueue.erase(queuePosition[value]);
            queuePosition.erase(value);
        }
    }
};
```

**Complexity**

- Time complexity:
    - **constructor**: $O(K)$

    - **add()**: $O(1)$

    - **showFirstUnique()**: $O(1)$

- Space complexity: $O(N)$

> Where $K$ is the length of the initial array passed into the constructor and $N$ is the total number of items added into the queue so far (including those from the constructor).
