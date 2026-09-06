# 1647. Minimum Deletions to Make Character Frequencies Unique

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-deletions-to-make-character-frequencies-unique/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-deletions-to-make-character-frequencies-unique>  
- **Video:** <https://www.youtube.com/watch?v=h8AZEN49gTc>  

[← Back to index](../INDEX.md)

## 1. Hash Set

For frequencies to be unique, no two characters can have the same count. When we encounter a frequency that already exists, we must delete characters until we reach an unused frequency (or zero). A hash set tracks which frequencies are already taken. For each character's frequency, we decrement it until we find an available slot, counting each decrement as a deletion.

```cpp
class Solution {
public:
    int minDeletions(string s) {
        vector<int> count(26, 0);
        for (char& c : s) {
            count[c - 'a']++;
        }

        unordered_set<int> usedFreq;
        int res = 0;

        for (int& freq : count) {
            while (freq > 0 && usedFreq.count(freq)) {
                freq--;
                res++;
            }
            usedFreq.insert(freq);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m ^ 2)$
- Space complexity: $O(m)$

> Where $n$ is the length of the string $s$ and $m$ is the total number of unique frequncies possible.

## 2. Max-Heap

Using a max-heap, we process frequencies from largest to smallest. When the top two frequencies are equal, we have a conflict. We resolve it by decrementing one of them and pushing the reduced value back (if still positive). This greedy approach ensures we minimize deletions by keeping larger frequencies intact when possible.

```cpp
class Solution {
public:
    int minDeletions(string s) {
        unordered_map<char, int> freq;
        for (char& c : s) {
            freq[c]++;
        }

        priority_queue<int> maxHeap;
        for (auto& f : freq) {
            maxHeap.push(f.second);
        }

        int res = 0;
        while (maxHeap.size() > 1) {
            int top = maxHeap.top();
            maxHeap.pop();
            if (top == maxHeap.top()) {
                if (top - 1 > 0) {
                    maxHeap.push(top - 1);
                }
                res++;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m ^ 2 \log m)$
- Space complexity: $O(m)$

> Where $n$ is the length of the string $s$ and $m$ is the total number of unique frequncies possible.

## 3. Sorting

By sorting frequencies in descending order, we process them from highest to lowest. We track the maximum allowed frequency for the next character. If a frequency exceeds this limit, we delete down to the limit. After each character, the next allowed frequency decreases by one (minimum `0`). This ensures all final frequencies are distinct.

```cpp
class Solution {
public:
    int minDeletions(string s) {
        vector<int> count(26, 0);
        for (char& c : s) {
            count[c - 'a']++;
        }

        sort(count.begin(), count.end(), greater<int>());
        int res = 0;
        int maxAllowedFreq = count[0];

        for (int& freq : count) {
            if (freq > maxAllowedFreq) {
                res += freq - maxAllowedFreq;
                freq = maxAllowedFreq;
            }
            maxAllowedFreq = max(0, freq - 1);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m \log m)$
- Space complexity: $O(m)$

> Where $n$ is the length of the string $s$ and $m$ is the total number of unique frequncies possible.
