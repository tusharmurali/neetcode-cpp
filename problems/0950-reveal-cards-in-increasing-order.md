# 950. Reveal Cards In Increasing Order

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/reveal-cards-in-increasing-order/>  
- **NeetCode:** <https://neetcode.io/problems/reveal-cards-in-increasing-order>  
- **Video:** <https://www.youtube.com/watch?v=i2QrUdwWlak>  

[← Back to index](../INDEX.md)

## 1. Simulation Using Queue - I

The reveal process takes the top card, then moves the next card to the bottom. To arrange cards so they reveal in increasing order, we simulate this process in reverse by tracking positions. We use a queue of indices representing available positions. As we assign sorted values in order, each assignment follows the reveal pattern: take the front index, then rotate the next index to the back.

```cpp
class Solution {
public:
    vector<int> deckRevealedIncreasing(vector<int>& deck) {
        sort(deck.begin(), deck.end());
        int n = deck.size();
        vector<int> res(n);
        queue<int> q;

        for (int i = 0; i < n; i++) {
            q.push(i);
        }

        for (int num : deck) {
            int i = q.front();
            q.pop();
            res[i] = num;
            if (!q.empty()) {
                q.push(q.front());
                q.pop();
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 2. Simulation Using Queue - II

Another approach processes the sorted deck from largest to smallest. We build the final arrangement by simulating the reverse of the reveal process: before placing each card, we rotate the bottom card to the top (undoing the move that would have happened during reveal). This builds the deck configuration backward.

```cpp
class Solution {
public:
    vector<int> deckRevealedIncreasing(vector<int>& deck) {
        sort(deck.begin(), deck.end());
        queue<int> q;

        for (int i = deck.size() - 1; i >= 0; i--) {
            if (!q.empty()) {
                q.push(q.front());
                q.pop();
            }
            q.push(deck[i]);
        }

        vector<int> res(deck.size());
        for (int i = deck.size() - 1; i >= 0; i--) {
            res[i] = q.front();
            q.pop();
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Simulation Using Deque

A deque supports efficient operations at both ends, making it ideal for simulating the reverse reveal process. Starting with the largest card, we repeatedly move the back element to the front (reversing the bottom-to-top move), then insert the current card at the front. This directly constructs the deck arrangement.

```cpp
class Solution {
public:
    vector<int> deckRevealedIncreasing(vector<int>& deck) {
        sort(deck.begin(), deck.end());
        deque<int> dq;
        dq.push_back(deck.back());

        for (int i = deck.size() - 2; i >= 0; i--) {
            dq.push_front(dq.back());
            dq.pop_back();
            dq.push_front(deck[i]);
        }

        return vector<int>(dq.begin(), dq.end());
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 4. Simulation Using Two Pointers

Instead of using a queue or deque, we can simulate the assignment directly on the result array. We track which positions are still empty and use a skip flag to alternate between placing a card and skipping a position (mirroring the reveal process). This approach uses constant extra space beyond the result array.

```cpp
class Solution {
public:
    vector<int> deckRevealedIncreasing(vector<int>& deck) {
        int n = deck.size();
        vector<int> res(n, 0);
        bool skip = false;
        int deckIndex = 0, i = 0;

        sort(deck.begin(), deck.end());

        while (deckIndex < n) {
            if (res[i] == 0) {
                if (!skip) {
                    res[i] = deck[deckIndex++];
                }
                skip = !skip;
            }
            i = (i + 1) % n;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity:
    - $O(1)$ or $O(n)$ space depending on the sorting algorithm.
    - $O(n)$ space for the output array.
