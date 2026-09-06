# 422. Valid Word Square

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/valid-word-square/>  
- **NeetCode:** <https://neetcode.io/problems/valid-word-square>  

[← Back to index](../INDEX.md)

## 1. Storing New Words

A word square has a special property: the k-th row reads the same as the k-th column. To verify this, we can construct new words by reading each column vertically and then compare them to the original row words. If every row word matches its corresponding column word, we have a valid word square. We first check basic constraints: the number of rows must equal the maximum word length, and the first row must be the longest.

```cpp
class Solution {
public:
    bool validWordSquare(vector<string>& words) {
        int cols = 0;
        int rows = words.size();
        vector<string> newWords;

        for (auto& word : words) {
            cols = max(cols, (int)word.size());
        }

        // If the first row doesn't have maximum number of characters, or
        // the number of rows is not equal to columns it can't form a square.
        if (cols != words[0].size() || rows != cols) {
            return false;
        }

        for (int col = 0; col < cols; ++col) {
            string newWord;
            // Iterate on each character of column 'col'.
            for (int row = 0; row < rows; ++row) {
                // If the current row's word's size is less than the column number it means this column is empty,
                // or, if there is a character present then use it to make the new word.
                if (col < words[row].size()) {
                    newWord += words[row][col];
                }
            }
            // Push the new word of column 'col' in the list.
            newWords.push_back(newWord);
        }

        // Check if all row's words match with the respective column's words.
        return words == newWords;
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot m)$
- Space complexity: $O(n \cdot m)$

> Where $n$ is the number of strings in the `words` array and $m$ is the maximum length of a string

## 2. Iterate on the Matrix

Instead of building new words and comparing lists, we can directly verify the word square property: for every position `(row, col)`, the character must equal the character at position `(col, row)`. This is essentially checking that the matrix is symmetric along its main diagonal. We iterate through each character and verify this symmetry, handling cases where one position might be out of bounds.

```cpp
class Solution {
public:
    bool validWordSquare(vector<string>& words) {
        for (int wordNum = 0; wordNum < words.size(); ++wordNum) {
            for (int charPos = 0; charPos < words[wordNum].size(); ++charPos) {
                // charPos (curr 'row' word) is bigger than column word, or
                // wordNum (curr 'column' word) is bigger than row word, or
                // characters at index (wordNum,charPos) and (charPos,wordNum) are not equal.
                if (charPos >= words.size() ||
                    wordNum >= words[charPos].size() ||
                    words[wordNum][charPos] != words[charPos][wordNum]){
                    return false;
                }
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot m)$
- Space complexity: $O(1)$ constant space

> Where $n$ is the number of strings in the `words` array and $m$ is the maximum length of a string
