# 1165. Single-Row Keyboard

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/single-row-keyboard/>  
- **NeetCode:** <https://neetcode.io/problems/single-row-keyboard>  

[← Back to index](../INDEX.md)

## 1. Storing indexes for all letters

To type a word efficiently, we need to know where each key is located on the keyboard. By precomputing the position of every letter, we can quickly look up the distance between consecutive characters. The total time is the sum of all these distances as we move from one key to the next.

```cpp
class Solution {
public:
    int calculateTime(string keyboard, string word) {
        vector<int> keyIndices(26, -1);

        // Get the index for each key.
        for (int i = 0; i < keyboard.length(); i++)
            keyIndices[keyboard[i] - 'a'] = i;

        // Initialize previous index as starting index = 0.
        int prev = 0;
        int result = 0;

        // Calculate the total time.
        for (char &c : word) {
            // Add the distance from previous index
            // to current letter's index to the result.
            result += abs(prev - keyIndices[c - 'a']);

            // Update the previous index to current index for next iteration.
            prev = keyIndices[c - 'a'];
        }
        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ constant space

>  Where $n$ is the length of `word`.
