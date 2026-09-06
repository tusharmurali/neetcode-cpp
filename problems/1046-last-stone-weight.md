# 1046. Last Stone Weight

- **Difficulty:** Easy  
- **Pattern:** Heap / Priority Queue  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/last-stone-weight/>  
- **NeetCode:** <https://neetcode.io/problems/last-stone-weight>  
- **Video:** <https://www.youtube.com/watch?v=B-QCq79-Vfw>  
- **Video approach:** 3. Heap  

[← Back to index](../INDEX.md)

## 1. Sorting

You always need to smash the **two heaviest stones** together.  
A simple way to ensure this is:

1. **Sort the list of stones** so the heaviest stones are at the end.
2. Remove the last two stones (the largest values).
3. Smash them:
    - If they are equal → both disappear.
    - If they are different → the difference becomes a new stone.
4. Insert the new stone (if any) back into the list.
5. Repeat until at most one stone remains.

Sorting each time is not the most efficient approach, but it is straightforward and easy to implement.

```cpp
class Solution {
public:
    int lastStoneWeight(vector<int>& stones) {
        while (stones.size() > 1) {
            sort(stones.begin(), stones.end());
            int cur = stones.back() - stones[stones.size() - 2];
            stones.pop_back();
            stones.pop_back();
            if (cur != 0) {
                stones.push_back(cur);
            }
        }
        return stones.empty() ? 0 : stones[0];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 2. Binary Search

We always smash the **two heaviest stones**.  
If we keep the stones in **sorted order**, the two heaviest are at the **end** of the array, so we can pick them easily.

After smashing:

- We remove the two heaviest stones.
- If they are different, their **difference** becomes a new stone.
- To keep the array sorted, we need to insert this new stone at the **correct position**.

Instead of scanning linearly to find the position, we use **binary search** to quickly find where this new stone should go in the sorted list, and then shift elements to insert it there. This keeps the list sorted for the next iteration.

```cpp
class Solution {
public:
    int lastStoneWeight(vector<int>& stones) {
        sort(stones.begin(), stones.end());
        int n = stones.size();

        while (n > 1) {
            int cur = stones[n - 1] - stones[n - 2];
            n -= 2;
            if (cur > 0) {
                int l = 0, r = n;
                while (l < r) {
                    int mid = (l + r) / 2;
                    if (stones[mid] < cur) {
                        l = mid + 1;
                    } else {
                        r = mid;
                    }
                }
                int pos = l;
                stones.push_back(0);
                for (int i = n + 1; i > pos; i--) {
                    stones[i] = stones[i - 1];
                }
                stones[pos] = cur;
                n++;
            }
        }
        return n > 0 ? stones[0] : 0;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 3. Heap ▶ video

We always need to repeatedly remove the **two heaviest stones**.  
A **max-heap** is perfect for this because it lets us efficiently extract the largest values.

Most languages provide **min-heaps**, so a common trick is to **store negative values**.  
This makes the smallest (most negative) value represent the _largest_ stone.

Process:

1. Convert all stones to negative and build a heap.
2. Repeatedly pop the two smallest (i.e., the two heaviest stones).
3. Smash them:
    - If equal → both are destroyed.
    - If different → push the negative of their difference back into the heap.
4. When one or zero stones remain, return the remaining weight or `0`.

```cpp
class Solution {
public:
    int lastStoneWeight(vector<int>& stones) {
        priority_queue<int> maxHeap;
        for (int s : stones) {
            maxHeap.push(s);
        }

        while (maxHeap.size() > 1) {
            int first = maxHeap.top();
            maxHeap.pop();
            int second = maxHeap.top();
            maxHeap.pop();
            if (second < first) {
                maxHeap.push(first - second);
            }
        }

        maxHeap.push(0);
        return maxHeap.top();
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 4. Bucket Sort

Since all stone values lie within a **limited numeric range**, we can avoid sorting or using a heap by using **bucket sort / frequency counting**.

Instead of tracking every stone individually, we store how many stones exist for each possible weight.

Key ideas:

- Let `bucket[w]` store how many stones of weight `w` we have.
- We repeatedly look for the **heaviest available stone**.
- When smashing stones of weights `a` and `b`:
    - If `a == b`, they cancel out.
    - If different, the leftover stone `a - b` gets added back into the bucket.
- We continue until only one non-zero weight remains.

This works because bucket operations (increment, decrement, scanning) are efficient when the weight range is manageable.

```cpp
class Solution {
public:
    int lastStoneWeight(vector<int>& stones) {
        int maxStone = 0;
        for (int stone : stones) {
            maxStone = max(maxStone, stone);
        }

        vector<int> bucket(maxStone + 1, 0);
        for (int stone : stones) {
            bucket[stone]++;
        }

        int first = maxStone, second = maxStone;
        while (first > 0) {
            if (bucket[first] % 2 == 0) {
                first--;
                continue;
            }

            int j = min(first - 1, second);
            while (j > 0 && bucket[j] == 0) {
                j--;
            }

            if (j == 0) {
                return first;
            }

            second = j;
            bucket[first]--;
            bucket[second]--;
            bucket[first - second]++;
            first = max(first - second, second);
        }

        return first;
    }
};
```

**Complexity**

- Time complexity: $O(n + w)$
- Space complexity: $O(w)$

> Where $n$ is the length of the $stones$ array and $w$ is the maximum value in the $stones$ array.

## Standalone solution file (`cpp/1046-last-stone-weight.cpp` in the NeetCode repo)

```cpp
/*
    Given array of stones to smash, return smallest possible weight of last stone
    If x == y both stones destroyed, if x != y stone x destroyed, stone y = y - x
    Ex. stones = [2,7,4,1,8,1] -> 1, [2,4,1,1,1], [2,1,1,1], [1,1,1], [1]

    Max heap, pop 2 biggest, push back difference until no more 2 elements left

    Time: O(n log n)
    Space: O(n)
*/

class Solution {
public:
    int lastStoneWeight(vector<int>& stones) {
        priority_queue<int> pq;
        for (int i = 0; i < stones.size(); i++) {
            pq.push(stones[i]);
        }
        
        while (pq.size() > 1) {
            int y = pq.top();
            pq.pop();
            int x = pq.top();
            pq.pop();
            if (y > x) {
                pq.push(y - x);
            }
        }
        
        if (pq.empty()) {
            return 0;
        }
        return pq.top();
    }
};
```
