# 2405. Optimal Partition of String

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/optimal-partition-of-string/>  
- **NeetCode:** <https://neetcode.io/problems/optimal-partition-of-string>  
- **Video:** <https://www.youtube.com/watch?v=CKZPdiXiQf0>  

[← Back to index](../INDEX.md)

## 1. Greedy (Hash Set)

To minimize the number of substrings, we want each substring to be as long as possible while containing only unique characters. A greedy approach works perfectly here: extend the current substring until we encounter a duplicate character, then start a new substring.

We use a hash set to track characters in the current substring. When we see a character already in the set, we've found a duplicate, so we increment our count and clear the set to start fresh.

```cpp
class Solution {
public:
    int partitionString(string s) {
        unordered_set<char> curSet;
        int res = 1;
        for (char c : s) {
            if (curSet.count(c)) {
                res++;
                curSet.clear();
            }
            curSet.insert(c);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

## 2. Greedy (Array)

Instead of using a set and clearing it on each partition, we can track the last index where each character appeared. A character causes a conflict only if its last occurrence is within the current partition (at or after the start index).

This approach avoids the overhead of clearing the set and uses constant extra space since we only need to track `26` lowercase letters.

```cpp
class Solution {
public:
    int partitionString(string s) {
        vector<int> lastIdx(26, -1);
        int res = 1, start = 0;
        for (int i = 0; i < s.size(); i++) {
            int j = s[i] - 'a';
            if (lastIdx[j] >= start) {
                start = i;
                res++;
            }
            lastIdx[j] = i;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

## 3. Greedy (Bit Mask)

Since we only have `26` lowercase letters, we can represent the set of characters in the current partition using a single integer as a bitmask. Each bit position corresponds to a letter (bit `0` for `'a'`, bit `1` for `'b'`, etc.).

This is the most space-efficient approach and uses fast bitwise operations to check membership and add characters.

```cpp
class Solution {
public:
    int partitionString(string s) {
        int res = 1, mask = 0;
        for (char c : s) {
            int i = c - 'a';
            if (mask & (1 << i)) {
                mask = 0;
                res++;
            }
            mask |= (1 << i);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/2405-optimal-partition-of-string.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int partitionString(string s) {
        vector<int> lastSeen(26, -1);
        int count = 1, substringStart = 0;

        for (int i = 0; i < s.length(); i++) {
            if (lastSeen[s[i] - 'a'] >= substringStart) {
                count++;
                substringStart = i;
            }
            lastSeen[s[i] - 'a'] = i;
        }

        return count;
    }
};


class Solution {
  public:
    int minPartitions(std::string s) {
        // Set to keep track of characters in the current substring
        std::unordered_set<char> currentChars;
        // Variable to count the number of partitions
        int partitionCount = 0;

        // Iterate over each character in the string
        for (char c : s) {
            // If the character is already in the set, it means we've encountered a duplicate
            if (currentChars.find(c) != currentChars.end()) {
                // Increment the partition count and start a new substring
                partitionCount++;
                currentChars.clear();
            }
            // Add the current character to the set
            currentChars.insert(c);
        }

        // There will be at least one partition at the end if currentChars is not empty
        if (!currentChars.empty()) {
            partitionCount++;
        }

        return partitionCount;
    }
};
```
