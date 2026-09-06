# 846. Hand of Straights

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/hand-of-straights/>  
- **NeetCode:** <https://neetcode.io/problems/hand-of-straights>  
- **Video:** <https://www.youtube.com/watch?v=amnrMCVd2YI>  

[← Back to index](../INDEX.md)

## 1. Sorting

We are given a hand of cards and a group size. The goal is to check whether we can divide all cards into groups of size `groupSize` such that:

- each group consists of **consecutive numbers**
- every card is used **exactly once**

A simple and intuitive way to approach this is:

- always try to form groups starting from the **smallest available card**
- once we start a group at a number `x`, we must also have `x + 1`, `x + 2`, ..., `x + groupSize - 1`

Sorting the hand helps because it ensures we always process cards in increasing order, which naturally enforces the consecutive requirement.

A frequency map `count` helps us track how many times each card is still available.

```cpp
class Solution {
public:
    bool isNStraightHand(vector<int>& hand, int groupSize) {
        if (hand.size() % groupSize != 0) return false;

        unordered_map<int, int> count;
        for (int num : hand) count[num]++;

        sort(hand.begin(), hand.end());
        for (int num : hand) {
            if (count[num] > 0) {
                for (int i = num; i < num + groupSize; i++) {
                    if (count[i] == 0) return false;
                    count[i]--;
                }
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 2. Heap

We need to split the cards into groups of size `groupSize`, where each group is made of **consecutive numbers**, and every card is used exactly once.

A good strategy is to always start building a group from the **smallest card value that is still available**.  
If we can always extend that smallest value into a full consecutive group, then the hand is valid.

To do this efficiently:

- we store frequencies of each card in a map `count`
- we keep a **min-heap** of the available card values so we can always get the current smallest value quickly

When we start a group from `first` (the smallest value in the heap), we must use:
`first`, `first+1`, ..., `first+groupSize-1`

If at any point a required value is missing, grouping is impossible.

The heap also helps ensure we remove values in the correct order when their count reaches zero.

```cpp
class Solution {
public:
    bool isNStraightHand(vector<int>& hand, int groupSize) {
        if (hand.size() % groupSize != 0)
            return false;

        unordered_map<int, int> count;
        for (int n : hand)
            count[n] = 1 + count[n];

        priority_queue<int, vector<int>, greater<int>> minH;
        for (auto& pair : count)
            minH.push(pair.first);

        while (!minH.empty()) {
            int first = minH.top();
            for (int i = first; i < first + groupSize; i++) {
                if (count.find(i) == count.end())
                    return false;
                count[i] -= 1;
                if (count[i] == 0) {
                    if (i != minH.top())
                        return false;
                    minH.pop();
                }
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Ordered Map

We want to check if the cards can be divided into groups of size `groupSize`, where **each group consists of consecutive numbers** and **every card is used exactly once**.

Instead of explicitly forming each group, we can think in terms of **how many groups are currently “open”** and waiting to be extended.

As we process card values in increasing order:

- some groups may already be open and **expect the current number next**
- the current number can either:
    - extend existing open groups
    - or start new groups

The key idea is:

- if there are `open_groups` waiting for the current number, we must have **at least that many cards** of the current value
- any extra cards beyond extending existing groups will start **new groups**
- each group must close exactly after `groupSize` consecutive numbers

A queue is used to remember **how many new groups were started at each step**, so we can close them after `groupSize` steps.

```cpp
class Solution {
public:
    bool isNStraightHand(vector<int>& hand, int groupSize) {
        if (hand.size() % groupSize != 0) return false;

        map<int, int> count;
        for (int num : hand) count[num]++;

        queue<int> q;
        int lastNum = -1, openGroups = 0;

        for (auto& entry : count) {
            int num = entry.first;
            if ((openGroups > 0 && num > lastNum + 1) ||
                 openGroups > count[num]) {
                return false;
            }

            q.push(count[num] - openGroups);
            lastNum = num;
            openGroups = count[num];

            if (q.size() == groupSize) {
                openGroups -= q.front();
                q.pop();
            }
        }
        return openGroups == 0;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 4. Hash Map

We need to split the hand into groups of size `groupSize`, where each group is made of **consecutive numbers** and every card is used exactly once.

This approach uses only a frequency map and a simple rule:

- Any valid group must start at the **beginning of a consecutive run**
- So for a given number `num`, we first walk left to find the earliest possible start of its run
  (we keep moving left while `start - 1` still exists in the hand)
- Once we know a possible start, we try to repeatedly form consecutive groups starting from that start:
    - while there are still cards at `start`, we build a group:
      `start`, `start+1`, ..., `start+groupSize-1`
    - decrement counts as we use cards

By always forming groups from the earliest start in a run, we avoid skipping needed smaller cards and ensure groups remain consecutive.

```cpp
class Solution {
public:
    bool isNStraightHand(vector<int>& hand, int groupSize) {
        if (hand.size() % groupSize != 0) return false;

        unordered_map<int, int> count;
        for (int num : hand) count[num]++;

        for (int num : hand) {
            int start = num;
            while (count[start - 1] > 0) start--;
            while (start <= num) {
                while (count[start] > 0) {
                    for (int i = start; i < start + groupSize; i++) {
                        if (count[i] == 0) return false;
                        count[i]--;
                    }
                }
                start++;
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0846-hand-of-straights.cpp` in the NeetCode repo)

```cpp
/*
    Given int array, return true if can rearrange cards into groupSize consecutive
    Ex. hand = [1,2,3,6,2,3,4,7,8], groupSize = 3 -> true, [1,2,3],[2,3,4],[6,7,8]

    Loop thru ordered map, for a value, check groupSize consecutive & remove

    Time: O(n log n)
    Space: O(n)
*/

class Solution {
public:
    bool isNStraightHand(vector<int>& hand, int groupSize) {
        int n = hand.size();
        
        if (n % groupSize != 0) {
            return false;
        }
        
        // map {card value -> count}
        map<int, int> m;
        for (int i = 0; i < n; i++) {
            m[hand[i]]++;
        }
        
        while (!m.empty()) {
            int curr = m.begin()->first;
            for (int i = 0; i < groupSize; i++) {
                if (m[curr + i] == 0) {
                    return false;
                }
                m[curr + i]--;
                if (m[curr + i] < 1) {
                    m.erase(curr + i);
                }
            }
        }
        
        return true;
    }
};
```
