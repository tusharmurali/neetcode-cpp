# 616. Add Bold Tag in String

- **Difficulty:** Medium  
- **Pattern:** Intervals  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/add-bold-tag-in-string/>  
- **NeetCode:** <https://neetcode.io/problems/add-bold-tag-in-string>  

[← Back to index](../INDEX.md)

## 1. Mark Bold Characters

The key insight is that we need to track which characters should be bold, not which substrings. If we find all occurrences of each word in the string and mark every character position that falls within any match, we can then merge overlapping or adjacent bold regions naturally.

We use a boolean array where each index corresponds to a character in the string. For every word, we find all its occurrences and mark the corresponding positions as bold. When building the result, we only insert `<b>` at the start of a bold region and `</b>` at the end, which handles merging automatically.

```cpp
class Solution {
public:
    string addBoldTag(string s, vector<string>& words) {
        int n = s.size();
        vector<bool> bold(n);
        
        for (string word: words) {
            int start = s.find(word);
            while (start != -1) {
                for (int i = start; i < start + word.size(); i++) {
                    bold[i] = true;
                }
                
                start = s.find(word, start + 1);
            }
        }
        
        string openTag = "<b>";
        string closeTag = "</b>";
        string ans = "";
        
        for (int i = 0; i < n; i++) {
            if (bold[i] && (i == 0 || !bold[i - 1])) {
                ans += openTag;
            }
            
            ans += s[i];
            
            if (bold[i] && (i == n - 1 || !bold[i + 1])) {
                ans += closeTag;
            }
        }
        
        return ans;
    }
};
```

**Complexity**

The time complexity may differ between languages. It is dependent on how the built-in method is implemented.
For this analysis, we will assume that we are using Java.

- Time complexity: $O(m \cdot (n^2 \cdot k - n \cdot k^2))$
- Space complexity: $O(n)$

>  Where $n$ is `s.length`, $m$ is `words.length`, and $k$ is the average length of the words.
