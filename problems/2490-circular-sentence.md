# 2490. Circular Sentence

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/circular-sentence/>  
- **NeetCode:** <https://neetcode.io/problems/circular-sentence>  
- **Video:** <https://www.youtube.com/watch?v=9Ty_eRjoDNM>  

[← Back to index](../INDEX.md)

## 1. Splitting the String

A sentence is circular if the last character of each word matches the first character of the next word, and the last word connects back to the first. By splitting the sentence into individual words, we can check each consecutive pair. Using modular indexing, we naturally handle the wrap-around from the last word to the first word in a single loop.

```cpp
class Solution {
public:
    bool isCircularSentence(string sentence) {
        vector<string> w;
        stringstream ss(sentence);
        string word;

        while (ss >> word) {
            w.push_back(word);
        }

        for (int i = 0; i < w.size(); i++) {
            char start = w[i][0];
            char end = w[(i - 1 + w.size()) % w.size()].back();
            if (start != end) {
                return false;
            }
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Iteration (Space Optimized)

Instead of splitting the string and storing all words, we can iterate through the sentence and check only the characters around each space. When we find a space, the character before it is the last character of the previous word, and the character after it is the first character of the next word. We also need to check that the first and last characters of the entire sentence match for the circular connection.

```cpp
class Solution {
public:
    bool isCircularSentence(string sentence) {
        for (int i = 0; i < sentence.size(); i++) {
            if (sentence[i] == ' ' && sentence[i - 1] != sentence[i + 1]) {
                return false;
            }
        }
        return sentence.front() == sentence.back();
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
