# 729. My Calendar I

- **Difficulty:** Medium  
- **Pattern:** Intervals  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/my-calendar-i/>  
- **NeetCode:** <https://neetcode.io/problems/my-calendar-i>  
- **Video:** <https://www.youtube.com/watch?v=fIxck3tlId4>  

[← Back to index](../INDEX.md)

## 1. Iteration

Two events overlap if one starts before the other ends and vice versa. For each new booking request, we need to check whether it conflicts with any existing event. We can store all booked events in a list and iterate through them to detect overlaps. If no conflict is found, we add the new event to the list.

```cpp
class MyCalendar {
private:
    vector<pair<int, int>> events;

public:
    MyCalendar() {}

    bool book(int startTime, int endTime) {
        for (const auto& event : events) {
            if (startTime < event.second && event.first < endTime) {
                return false;
            }
        }
        events.push_back({startTime, endTime});
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$ for each $book()$ function call.
- Space complexity: $O(n)$

## 2. Binary Search Tree

We can organize events in a binary search tree where each node represents a booked interval. The tree is ordered by start times: intervals that end before a node's start time go to the left subtree, and intervals that start after a node's end time go to the right subtree. When inserting a new interval, we traverse the tree to find where it fits without overlapping any existing node. If it overlaps with a node during traversal, we reject it.

```cpp
class MyCalendar {
private:
    struct TreeNode {
        int start, end;
        TreeNode *left, *right;

        TreeNode(int start, int end) : start(start), end(end), left(nullptr), right(nullptr) {}
    };
    TreeNode *root;

    bool insert(TreeNode *node, int start, int end) {
        if (end <= node->start) {
            if (!node->left) {
                node->left = new TreeNode(start, end);
                return true;
            }
            return insert(node->left, start, end);
        } else if (start >= node->end) {
            if (!node->right) {
                node->right = new TreeNode(start, end);
                return true;
            }
            return insert(node->right, start, end);
        }
        return false;
    }

public:
    MyCalendar() : root(nullptr) {}

    bool book(int startTime, int endTime) {
        if (!root) {
            root = new TreeNode(startTime, endTime);
            return true;
        }
        return insert(root, startTime, endTime);
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$ in average case, $O(n)$ in worst case for each $book()$ function call.
- Space complexity: $O(n)$

## 3. Binary Search + Ordered Set

By keeping events sorted by start time, we can use binary search to quickly find where a new event would be inserted. We only need to check the immediate neighbors (the event just before and just after the insertion point) for potential overlaps. If the previous event ends after our start time, or the next event starts before our end time, we have a conflict. This gives us logarithmic search time per booking.

```cpp
class MyCalendar {
private:
    set<pair<int, int>> events;

public:
    MyCalendar() {}

    bool book(int startTime, int endTime) {
        if (startTime >= endTime) {
            return false;
        }

        auto next = events.lower_bound({startTime, startTime});
        if (next != events.end() && next->first < endTime) {
            return false;
        }
        if (next != events.begin()) {
            auto prev = std::prev(next);
            if (prev->second > startTime) {
                return false;
            }
        }

        events.insert({startTime, endTime});
        return true;
    }
};
```

**Complexity**

- Time complexity per $book()$ function call:
    - $O(\log n)$ for Python's `SortedList` and the ordered-set implementations in Java and C++.
    - $O(n)$ for the array/list-backed implementations (JavaScript, C#, Go, Kotlin, Swift, and Rust), since inserting at an arbitrary index can require shifting $O(n)$ elements.
- Space complexity: $O(n)$
