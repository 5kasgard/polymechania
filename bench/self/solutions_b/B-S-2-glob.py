def glob_match(pattern: str, path: str) -> bool:
    """
    Matches a pattern against a path using '/' as a separator.
    '?' matches one character (not '/').
    '*' matches any run of characters (not '/').
    '**' matches zero or more entire segments.
    """
    # Split into segments. Note: "a//b" results in ["a", "", "b"]
    # Empty path "" results in []
    pattern_segments = pattern.split('/')
    path_segments = path.split('/') if path != "" else []

    # Memoization for the recursive matcher
    memo = {}

    def match(p_idx: int, s_idx: int) -> bool:
        state = (p_idx, s_idx)
        if state in memo:
            return memo[state]

        # Base case: reached end of pattern
        if p_idx == len(pattern_segments):
            # Match is successful if we also reached end of path
            res = s_idx == len(path_segments)
            memo[state] = res
            return res

        p_seg = pattern_segments[p_idx]

        # Case 1: "**" matches zero or more segments
        if p_seg == "**":
            # Option A: "**" matches zero segments (skip "**" in pattern)
            if match(p_idx + 1, s_idx):
                memo[state] = True
                return True
            
            # Option B: "**" matches one or more segments (consume one segment and stay on "**")
            if s_idx < len(path_segments):
                if match(p_idx, s_idx + 1):
                    memo[state] = True
                    return True
            
            memo[state] = False
            return False

        # Case 2: Single segment matching
        # If we ran out of path segments but pattern still has non-"**" segments
        if s_idx == len(path_segments):
            # Only possible if remaining pattern segments are all "**"
            # But we handled "**" above, so if we are here, it's a mismatch
            memo[state] = False
            return False

        s_seg = path_segments[s_idx]

        # If pattern segment is "*", it matches any run of chars in the current segment
        if p_seg == "*":
            # "*" matches the whole segment (including empty) and moves to next segment
            res = match(p_idx + 1, s_idx + 1)
            memo[state] = res
            return res

        # If pattern segment is "?", it matches exactly one char (not '/')
        if p_seg == "?":
            # "?" matches exactly one character. Since segments are split by '/',
            # a single char segment is the only thing that can match "?"
            # unless the segment is empty, but "?" must match one char.
            # However, the spec says "?" matches one character other than "/".
            # In a segment-based split, "?" matches a segment of length 1.
            if len(s_seg) == 1:
                res = match(p_idx + 1, s_idx + 1)
                memo[state] = res
                return res
            else:
                memo[state] = False
                return False

        # Case 3: Literal match or mixed pattern (e.g., "a*.py")
        # The spec says: "?" matches one char, "*" matches any run, "**" matches segments.
        # It doesn't explicitly say "*" can be part of a segment like "a*.py", 
        # but "src/**/*.py" implies segments can contain literals and wildcards.
        
        # We need a sub-matcher for the segment itself
        if match_segment(p_seg, s_seg):
            res = match(p_idx + 1, s_idx + 1)
            memo[state] = res
            return res
        
        memo[state] = False
        return False

    def match_segment(p_seg: str, s_seg: str) -> bool:
        # Sub-matcher for a single segment using '*' and '?'
        # This is a standard glob segment match
        p_len = len(p_seg)
        s_len = len(s_seg)
        
        # DP for segment matching
        dp = [[False] * (s_len + 1) for _ in range(p_len + 1)]
        dp[0][0] = True
        
        for i in range(1, p_len + 1):
            char = p_seg[i-1]
            if char == '*':
                # '*' matches zero or more characters
                dp[i][0] = dp[i-1][0]
                for j in range(1, s_len + 1):
                    dp[i][j] = dp[i-1][j] or dp[i][j-1]
            elif char == '?':
                # '?' matches exactly one character
                for j in range(1, s_len + 1):
                    dp[i][j] = dp[i-1][j-1]
            else:
                # Literal match
                for j in range(1, s_len + 1):
                    if char == s_seg[j-1]:
                        dp[i][j] = dp[i-1][j-1]
        
        return dp[p_len][s_len]

    return match(0, 0)
