# 1087. Brace Expansion

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/brace-expansion/>  
- **NeetCode:** <https://neetcode.io/problems/brace-expansion>  

[← Back to index](../INDEX.md)

## 1. Recursion

The string consists of segments that are either single characters or groups of options inside braces. We process the string from left to right, extracting the options for each position. For the first position, we get all possible characters (sorted if from braces), then recursively generate all words from the remaining string. Each option at the current position is combined with each word from the recursive result.

```cpp
class Solution {
public:
    int storeFirstOptions(string& s, int startPos, vector<char>& firstOptions) {
        // If the first character is not '{', it means a single character
        if (s[startPos] != '{') {
            firstOptions.push_back(s[startPos]);
        } else {
            // Store all the characters between '{' and '}'
            while (s[startPos] != '}') {
                 if (s[startPos] >= 'a' && s[startPos] <= 'z') {
                     firstOptions.push_back(s[startPos]);
                 }
                startPos++;
            }

            // Sort the list
            sort(firstOptions.begin(), firstOptions.end());
        }

        // Increment it to point to the next character to be considered
        return startPos + 1;
    }

    vector<string> findAllWords(string& s, int startPos) {
        // Return empty string list if the string is empty
        if (startPos == s.size()) {
            return {""};
        }

        vector<char> firstOptions;

        // Store the characters for the first index as string in firstOptions
        int remStringStartPos = storeFirstOptions(s, startPos, firstOptions);
        vector<string> wordsWithRemString = findAllWords(s, remStringStartPos);

        vector<string> expandedWords;

        // Create new words by adding the character at the beginning
        for (char c : firstOptions) {
            for (string word : wordsWithRemString) {
                expandedWords.push_back(c + word);
            }
        }

        return expandedWords;
    }

    vector<string> expand(string s) {
        return findAllWords(s, 0);
    }
};
```

**Complexity**

- Time complexity: $O(N \cdot 3^{N/7})$

- Space complexity: $O(N \cdot 3^{N/7})$

> Where $N$ is the length of the given string.

## 2. Iteration

Instead of using recursion, we can build the words iteratively. Starting with an empty string, we process each segment of the input. For each segment, we take all current words and extend each one with every option from that segment. This is similar to a Cartesian product, building up the result position by position.

```cpp
class Solution {
public:
    int storeFirstOptions(string& s, int startPos, vector<string>& firstOptions) {
        // If the first character is not '{', it means a single character
        if (s[startPos] != '{') {
            firstOptions.push_back(string(1, s[startPos]));
        } else {
            // Store all the characters between '{' and '}'
            while (s[startPos] != '}') {
                 if (s[startPos] >= 'a' && s[startPos] <= 'z') {
                     firstOptions.push_back(string(1, s[startPos]));
                 }
                startPos++;
            }

            // Sort the list
            sort(firstOptions.begin(), firstOptions.end());
        }

        // Increment it to point to the next character to be considered
        return startPos + 1;
    }

    vector<string> expand(string s) {
        vector<string> expandedWords = {""};

        int startPos = 0;
        while (startPos < s.size()) {
            vector<string> firstOptions;
            // Store the characters for the first index as string in firstOptions
            int remStringStartPos = storeFirstOptions(s, startPos, firstOptions);

            vector<string> currWords;
            // Append the string in the list firstOptions to string in expandedWords
            for (string word : expandedWords) {
                for (string c : firstOptions) {
                    currWords.push_back(word + c);
                }
            }

            // Update the list expandedWords to have all the words
            expandedWords = currWords;
            // Pointing to the next character to be considered
            startPos = remStringStartPos;
        }
        return expandedWords;
    }
};
```

**Complexity**

- Time complexity: $O(N \cdot 3^{N/7})$

- Space complexity: $O(N \cdot 3^{N/7})$

> Where $N$ is the length of the given string.

## 3. Backtracking

Backtracking is a natural fit for generating all combinations. First, we parse the input string to extract all options for each position. Then we build words character by character: at each position, we try each available option, add it to the current word, recurse to the next position, and then remove it (backtrack) to try the next option.

```cpp
class Solution {
public:
    vector<vector<char>> allOptions;

    void storeAllOptions(string& s) {
        for (int pos = 0; pos < s.size(); pos++) {
            vector<char> currOptions;

            // If the first character is not '{', it means a single character
            if (s[pos] != '{') {
                currOptions.push_back(s[pos]);
            } else {
                // Store all the characters between '{' and '}'
                while (s[pos] != '}') {
                    if (s[pos] >= 'a' && s[pos] <= 'z') {
                        currOptions.push_back(s[pos]);
                    }
                    pos++;
                }
                // Sort the list
                sort(currOptions.begin(), currOptions.end());
            }
            allOptions.push_back(currOptions);
        }
    }

    void generateWords(string currString, vector<string>& expandedWords) {
        // If the currString is complete, we can store and return
        if (currString.size() == allOptions.size()) {
            expandedWords.push_back(currString);
            return;
        }

        // Fetch the options for the current index
        vector<char> currOptions = allOptions[currString.size()];

        // Add the character and go into recursion
        for (char c : currOptions) {
            currString += c;
            generateWords(currString, expandedWords);
            // Backtrack to previous state
            currString.pop_back();
        }
    }

    vector<string> expand(string s) {
        // Store the character options for different indices
        storeAllOptions(s);

        vector<string> expandedWords;
        generateWords("", expandedWords);
        return expandedWords;
    }
};
```

**Complexity**

- Time complexity: $O(N \cdot 3^{N/7})$

- Space complexity: $O(N)$

> Where $N$ is the length of the given string.
