# 1055. Shortest Way to Form String

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/shortest-way-to-form-string/>  
- **NeetCode:** <https://neetcode.io/problems/shortest-way-to-form-string>  

[← Back to index](../INDEX.md)

## 1. Concatenate until Subsequence

The most straightforward approach is to literally concatenate copies of `source` until `target` becomes a subsequence of the concatenated string. We first check if all characters in `target` exist in `source`; if not, it is impossible. Then we keep appending `source` to itself and check after each concatenation whether `target` is now a subsequence. The number of concatenations gives us our answer.

```cpp
class Solution {
public:
    int shortestWay(string source, string target) {

        // Boolean array to mark all characters of the source
        bool sourceChars[26] = {false};
        for (char c : source) {
            sourceChars[c - 'a'] = true;
        }

        // Check if all characters of the target are present in the source
        // If any character is not present, return -1
        for (char c : target) {
            if (!sourceChars[c - 'a']) {
                return -1;
            }
        }

        // Concatenate source until the target is a subsequence of the concatenated string
        string concatenatedSource = source;
        int count = 1;
        while (!isSubsequence(target, concatenatedSource)) {
            concatenatedSource += source;
            count++;
        }

        // Number of concatenations done
        return count;
    }

    // To check if toCheck is a subsequence of inString
    bool isSubsequence(string toCheck, string inString) {
        int i = 0, j = 0;
        while (i < toCheck.length() && j < inString.length()) {
            if (toCheck[i] == inString[j]) {
                i++;
            }
            j++;
        }

        return i == toCheck.length();
    }
};
```

**Complexity**

- Time complexity: $O(T^2 \cdot S)$
- Space complexity: $O(TS)$

> where $S$ is the length of `source` and $T$ is the length of `target`

## 2. Two Pointers

Instead of building a huge concatenated string, we can simulate the process more efficiently. We iterate through `target` character by character, and for each character, we scan through `source` to find it. When we reach the end of `source` without fully matching `target`, we wrap around to the beginning of `source` and increment our count. Using modulo arithmetic, we can treat `source` as circular without actually concatenating it.

```cpp
class Solution {
public:
    int shortestWay(string source, string target) {

        // Boolean array to mark all characters of source
        bool sourceChars[26] = {false};
        for (char c : source) {
            sourceChars[c - 'a'] = true;
        }

        // Check if all characters of target are present in source
        // If any character is not present, return -1
        for (char c : target) {
            if (!sourceChars[c - 'a']) {
                return -1;
            }
        }

        // Length of source to loop back to start of source using mod
        int m = source.length();

        // Pointer for source
        int sourceIterator = 0;

        // Number of times source is traversed. It will be incremented when
        // while finding occurrence of a character in target, sourceIterator
        // reaches the start of source again.
        int count = 0;

        // Find all characters of target in source
        for (char c : target) {

            // If while finding, iterator reaches start of source again,
            // increment count
            if (sourceIterator == 0) {
                count++;
            }

            // Find the first occurrence of c in source
            while (source[sourceIterator] != c) {

                // Formula for incrementing while looping back to start.
                sourceIterator = (sourceIterator + 1) % m;

                // If while finding, iterator reaches start of source again,
                // increment count
                if (sourceIterator == 0) {
                    count++;
                }
            }

            // Loop will break when c is found in source. Thus, increment.
            // Don't increment count until it is not clear that target has
            // remaining characters.
            sourceIterator = (sourceIterator + 1) % m;
        }

        // Return count
        return count;
    }
};
```

**Complexity**

- Time complexity: $O(S \cdot T)$
- Space complexity: $O(1)$ constant space used

> where $S$ is the length of `source` and $T$ is the length of `target`

## 3. Inverted Index and Binary Search

The two-pointer approach scans through `source` linearly for each character in `target`, which can be slow. We can speed this up by precomputing the positions of each character in `source`. For any character we need to find, we use binary search to quickly locate the next occurrence at or after our current position. If no such occurrence exists, we wrap to the beginning of `source` and start a new subsequence.

```cpp
class Solution {
public:
    int shortestWay(string source, string target) {

        // Array to store the vector of charToIndices of each character in source
        vector < int > charToIndices[26];
        for (int i = 0; i < source.size(); i++) {
            charToIndices[source[i] - 'a'].push_back(i);
        }

        // The current index in source
        int sourceIterator = 0;

        // Number of times we have to iterate through source to get target
        int count = 1;

        // Find all characters of target in source
        for (int i = 0; i < target.size(); i++) {

            // If the character is not present in source, return -1
            if (charToIndices[target[i] - 'a'].size() == 0) {
                return -1;
            }

            // Binary search to find the index of the character in source next to the source iterator
            vector < int > indices = charToIndices[target[i] - 'a'];
            int index = lower_bound(indices.begin(), indices.end(), sourceIterator) - indices.begin();

            // If we have reached the end of the list, we need to iterate
            // through source again, hence first index of character in source.
            if (index == indices.size()) {
                count++;
                sourceIterator = indices[0] + 1;
            } else {
                sourceIterator = indices[index] + 1;
            }
        }

        return count;
    }
};
```

**Complexity**

- Time complexity: $O(S + T \log(S))$
- Space complexity: $O(S)$

> where $S$ is the length of `source` and $T$ is the length of `target`

## 4. 2D Array

We can achieve constant-time lookups by precomputing a 2D array where `nextOccurrence[i][c]` gives the index of the next occurrence of character `c` at or after position `i` in `source`. We build this array from right to left using dynamic programming: at each position, we copy the values from the next position and then update the current character's entry. This allows `O(1)` character lookups during the matching phase.

```cpp
class Solution {
public:
    int shortestWay(string source, string target) {

        // Next Occurrence of Character after Index
        int nextOccurrence[source.length()][26];

        // Base Case
        for (int c = 0; c < 26; c++) {
            nextOccurrence[source.length() - 1][c] = -1;
        }
        nextOccurrence[source.length() - 1][source[source.length() - 1] - 'a'] = source.length() - 1;

        // Fill using recurrence relation
        for (int idx = source.length() - 2; idx >= 0; idx--) {
            for (int c = 0; c < 26; c++) {
                nextOccurrence[idx][c] = nextOccurrence[idx + 1][c];
            }
            nextOccurrence[idx][source[idx] - 'a'] = idx;
        }

        // Pointer to the current index in source
        int sourceIterator = 0;

        // Number of times we need to iterate through source
        int count = 1;

        // Find all characters of target in source
        for (char c : target) {

            // If the character is not present in source
            if (nextOccurrence[0][c - 'a'] == -1) {
                return -1;
            }

            // If we have reached the end of source, or the character is not in
            // source after source_iterator, loop back to beginning
            if (sourceIterator == source.length() || nextOccurrence[sourceIterator][c - 'a'] == -1) {
                count++;
                sourceIterator = 0;
            }

            // Next occurrence of character in source after source_iterator
            sourceIterator = nextOccurrence[sourceIterator][c - 'a'] + 1;
        }

        // Return the number of times we need to iterate through source
        return count;
    }
};
```

**Complexity**

- Time complexity: $O(S + T)$
- Space complexity: $O(S)$

> where $S$ is the length of `source` and $T$ is the length of `target`
