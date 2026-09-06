# 1700. Number of Students Unable to Eat Lunch

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-students-unable-to-eat-lunch/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-students-unable-to-eat-lunch>  
- **Video:** <https://www.youtube.com/watch?v=d_cvtFwnOZg>  

[← Back to index](../INDEX.md)

## 1. Queue

We simulate the lunch process exactly as described. Students form a queue and take the top sandwich only if it matches their preference; otherwise, they go to the back of the queue. The process stops when the top sandwich cannot be taken by anyone remaining in the queue. A queue data structure naturally models students rotating until a match is found.

```cpp
class Solution {
public:
    int countStudents(vector<int>& students, vector<int>& sandwiches) {
        int n = students.size();
        queue<int> q;

        for (int student : students) {
            q.push(student);
        }

        int res = n;
        for (int sandwich : sandwiches) {
            int cnt = 0;
            while (cnt < n && q.front() != sandwich) {
                q.push(q.front());
                q.pop();
                cnt++;
            }
            if (q.front() == sandwich) {
                q.pop();
                res--;
            } else {
                break;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Iteration

Instead of using a separate queue, we can simulate the rotation using a circular index on the original students array. When a student takes a sandwich, we mark their position as served (using `-1`). This avoids the overhead of queue operations while achieving the same behavior.

```cpp
class Solution {
public:
    int countStudents(vector<int>& students, vector<int>& sandwiches) {
        int n = students.size();
        int idx = 0;

        int res = n;
        for (int sandwich : sandwiches) {
            int cnt = 0;
            while (cnt < n && students[idx] != sandwich) {
                idx++;
                idx %= n;
                cnt++;
            }
            if (students[idx] == sandwich) {
                students[idx] = -1;
                res--;
            } else {
                break;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 3. Frequency Count

The key insight is that student order does not matter. Since students can rotate indefinitely, what matters is whether there exists any student who wants the current top sandwich. If we track how many students want each type (`0` or `1`), we can quickly check availability without simulating the queue.

```cpp
class Solution {
public:
    int countStudents(vector<int>& students, vector<int>& sandwiches) {
        int res = students.size();
        vector<int> cnt(2);
        for (int& student : students) {
            cnt[student]++;
        }

        for (int& s : sandwiches) {
            if (cnt[s] > 0) {
                cnt[s]--;
                res--;
            } else {
                break;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/1700-number-of-students-unable-to-eat-lunch.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int countStudents(vector<int>& students, vector<int>& sandwiches) {
        queue<int> q1;
        for(int i = 0; i < students.size(); i++) {
            q1.push(students[i]);
        }

        int sandwichPos = 0;
        int curr = 0;
        while(!q1.empty() && curr <= q1.size()) {
            if(q1.front() == sandwiches[sandwichPos]) {
                q1.pop();
                sandwichPos++;
                curr = 0;
            } else {
                q1.push(q1.front());
                q1.pop();
            }
            curr++;
        }
        return q1.size();
    }
};
```
