# 763. Partition Labels

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/partition-labels/>  
- **NeetCode:** <https://neetcode.io/problems/partition-labels>  
- **Video:** <https://www.youtube.com/watch?v=B7m8UmZE-vw>  

[← Back to index](../INDEX.md)

## 1. Two Pointers (Greedy)

We want to split the string into as many parts as possible such that **each letter appears in at most one part**.

The key observation is:

- for any character, we must include **all occurrences** of that character in the same partition
- so if a character appears later in the string, the current partition must extend at least up to that last occurrence

By knowing the **last index** of every character, we can greedily decide where to end each partition.

As we scan the string:

- we keep extending the current partition to the farthest last occurrence of any character seen so far
- once we reach that farthest point, the partition can safely end

```cpp
class Solution {
public:
    vector<int> partitionLabels(string s) {
        unordered_map<char, int> lastIndex;
        for (int i = 0; i < s.size(); i++) {
            lastIndex[s[i]] = i;
        }

        vector<int> res;
        int size = 0, end = 0;
        for (int i = 0; i < s.size(); i++) {
            size++;
            end = max(end, lastIndex[s[i]]);

            if (i == end) {
                res.push_back(size);
                size = 0;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
    - The last-index map contains at most $26$ entries because `s` consists only of lowercase English letters. More generally, this is $O(m)$, where $m$ is the alphabet size.

> Where $n$ is the length of the string $s$.

## Standalone solution file (`cpp/0763-partition-labels.cpp` in the NeetCode repo)

```cpp
/*
    Partition string so each letter appears in at most 1 part, return sizes
    Ex. s = "ababcbacadefegdehijhklij" -> [9,7,8]

    Greedy: determine last occurrence of each char, then loop thru & get sizes

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    vector<int> partitionLabels(string s) {
        int n = s.size();
        // {char -> last index in s}
        vector<int> lastIndex(26);
        for (int i = 0; i < n; i++) {
            lastIndex[s[i] - 'a'] = i;
        }
        
        int size = 0;
        int end = 0;
        
        vector<int> result;
        
        for (int i = 0; i < n; i++) {
            size++;
            // constantly checking for further indices if possible
            end = max(end, lastIndex[s[i] - 'a']);
            if (i == end) {
                result.push_back(size);
                size = 0;
            }
        }
        
        return result;
    }
};
```
