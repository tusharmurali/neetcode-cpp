# 68. Text Justification

- **Difficulty:** Hard  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/text-justification/>  
- **NeetCode:** <https://neetcode.io/problems/text-justification>  
- **Video:** <https://www.youtube.com/watch?v=TzMl4Z7pVh8>  

[← Back to index](../INDEX.md)

## 1. Iteration

Text justification requires packing words into lines of fixed width, distributing extra spaces as evenly as possible between words. The challenge is handling three distinct cases: regular lines with multiple words (distribute spaces evenly, with extra spaces going to the left gaps), single-word lines (pad with trailing spaces), and the last line (left-justified with trailing spaces).

The key is to greedily fit as many words as possible on each line, then calculate how to distribute the remaining space among the gaps between words.

```cpp
class Solution {
public:
    vector<string> fullJustify(vector<string>& words, int maxWidth) {
        vector<string> res;
        vector<string> line;
        int length = 0, i = 0;

        while (i < words.size()) {
            if (length + words[i].size() + line.size() <= maxWidth) {
                line.push_back(words[i]);
                length += words[i].size();
                i++;
            } else {
                // Line complete
                int extra_space = maxWidth - length;
                int remainder = extra_space % max(1, (int)(line.size() - 1));
                int space = extra_space / max(1, (int)(line.size() - 1));

                for (int j = 0; j < max(1, (int)line.size() - 1); j++) {
                    line[j] += string(space, ' ');
                    if (remainder > 0) {
                        line[j] += " ";
                        remainder--;
                    }
                }

                string justified_line = accumulate(line.begin(), line.end(), string());
                res.push_back(justified_line);
                line.clear();
                length = 0;
            }
        }

        // Handling last line
        string last_line = accumulate(line.begin(), line.end(), string(),
                                      [](string a, string b) {
                                            return a.empty() ? b : a + " " + b;
                                        });
        int trail_space = maxWidth - last_line.size();
        last_line += string(trail_space, ' ');
        res.push_back(last_line);

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n * m)$

> Where $n$ is the number of words and $m$ is the average length of the words.
