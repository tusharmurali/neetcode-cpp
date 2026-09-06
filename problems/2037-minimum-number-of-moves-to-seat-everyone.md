# 2037. Minimum Number of Moves to Seat Everyone

- **Difficulty:** Easy  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-number-of-moves-to-seat-everyone/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-number-of-moves-to-seat-everyone>  
- **Video:** <https://www.youtube.com/watch?v=wS7Ag33hf8E>  

[← Back to index](../INDEX.md)

## 1. Greedy + Sorting

To minimize total movement, pair the closest seats with the closest students. Sorting both arrays puts them in order, allowing us to match the `i`-th smallest student with the `i`-th smallest seat. This greedy pairing ensures we never have crossing assignments, which would increase total distance.

Why does this work? If we had two students at positions `a < b` and two seats at positions `x < y`, pairing `(a, y)` and `(b, x)` would create crossing paths. Simple algebra shows `|a - x| + |b - y|` is always less than or equal to `|a - y| + |b - x|` when `a < b` and `x < y`.

```cpp
class Solution {
public:
    int minMovesToSeat(vector<int>& seats, vector<int>& students) {
        sort(seats.begin(), seats.end());
        sort(students.begin(), students.end());

        int res = 0;
        for (int i = 0; i < seats.size(); i++) {
            res += abs(seats[i] - students[i]);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 2. Counting Sort

When the range of positions is bounded, counting sort can be faster than comparison-based sorting. We create frequency arrays for both seats and students, then simulate the sorted pairing by walking through positions from smallest to largest.

Two pointers traverse the count arrays, finding the next available seat and next waiting student. Each match contributes its distance to the `res`.

```cpp
class Solution {
public:
    int minMovesToSeat(vector<int>& seats, vector<int>& students) {
        int max_index = 0;
        for (int s : seats) max_index = max(max_index, s);
        for (int s : students) max_index = max(max_index, s);
        max_index++;

        vector<int> count_seats(max_index, 0);
        vector<int> count_students(max_index, 0);

        for (int seat : seats) count_seats[seat]++;
        for (int student : students) count_students[student]++;

        int i = 0, j = 0, res = 0, remain = seats.size();
        while (remain > 0) {
            if (count_seats[i] == 0) {
                i++;
                continue;
            }
            if (count_students[j] == 0) {
                j++;
                continue;
            }
            res += abs(i - j);
            count_seats[i]--;
            count_students[j]--;
            remain--;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m1 + m2)$
- Space complexity: $O(m1 + m2)$

> Where $n$ is the size of the input arrays, $m1$ is the maximum value in the array $seats$, and $m2$ is the maximum value in the array $students$.

## 3. Counting Sort (Optimal)

When multiple students are at the same position or multiple seats are at the same position, we can batch process them. Instead of matching one pair at a time, we match `min(count_seats[i], count_students[j])` pairs at once, multiplying the distance by the batch `size`.

This optimization reduces iterations when there are many duplicates, though the asymptotic complexity remains the same.

```cpp
class Solution {
public:
    int minMovesToSeat(vector<int>& seats, vector<int>& students) {
        int maxSeat = *max_element(seats.begin(), seats.end());
        int maxStudent = *max_element(students.begin(), students.end());

        vector<int> count_seats(maxSeat + 1, 0);
        vector<int> count_students(maxStudent + 1, 0);

        for (int s : seats) count_seats[s]++;
        for (int s : students) count_students[s]++;

        int remain = seats.size(), i = 0, j = 0, res = 0;
        while (remain > 0) {
            if (count_seats[i] == 0) {
                i++;
                continue;
            }
            if (count_students[j] == 0) {
                j++;
                continue;
            }
            int tmp = min(count_seats[i], count_students[j]);
            res += abs(i - j) * tmp;
            count_seats[i] -= tmp;
            count_students[j] -= tmp;
            remain -= tmp;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m1 + m2)$
- Space complexity: $O(m1 + m2)$

> Where $n$ is the size of the input arrays, $m1$ is the maximum value in the array $seats$, and $m2$ is the maximum value in the array $students$.
