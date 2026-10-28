def glob_match(pattern: str, path: str) -> bool:
    pattern_segments = pattern.split("/")
    path_segments = path.split("/")
    
    memo = {}

    def solve(p_idx: int, s_idx: int) -> bool:
        state = (p_idx, s_idx)
        if state in memo:
            return memo[state]
        
        # Base case: reached end of pattern
        if p_idx == len(pattern_segments):
            # Match is successful only if we also reached end of path
            return s_idx == len(path_segments)
        
        res = False
        curr_p = pattern_segments[p_idx]
        
        if curr_p == "**":
            # ** can match zero or more segments
            # Option 1: Match zero segments (skip **)
            if solve(p_idx + 1, s_idx):
                res = True
            # Option 2: Match one or more segments (consume one and stay on **)
            elif s_idx < len(path_segments) and solve(p_idx, s_idx + 1):
                res = True
        elif s_idx < len(path_segments):
            curr_s = path_segments[s_idx]
            
            if curr_p == "*":
                # * matches any run of characters in a single segment
                # Since * is defined as "any run of characters other than /",
                # and we split by /, * matches the entire current segment.
                res = solve(p_idx + 1, s_idx + 1)
            elif "?" in curr_p:
                # Handle ? and literal characters within a segment
                # Note: The spec says "?" matches one character other than "/"
                # and "*" matches any run other than "/". 
                # This implies "?" and "*" are segment-level or character-level.
                # Re-reading: "?" matches one char, "*" matches any run.
                # These are applied to the segment string.
                
                if len(curr_p) == 1 and curr_p == "?":
                    if len(curr_s) == 1:
                        res = solve(p_idx + 1, s_idx + 1)
                else:
                    # If the segment contains wildcards, we must match the segment string
                    # However, the spec says "?" matches one char other than "/"
                    # and "*" matches any run other than "/".
                    # This suggests the pattern segment itself can be a mix.
                    # But the examples show pattern segments like "*.py" or "a?c".
                    # Let's implement segment-level matching for the segment string.
                    res = match_segment(curr_p, curr_s) and solve(p_idx + 1, s_idx + 1)
            else:
                # Literal segment match
                if curr_p == curr_s:
                    res = solve(p_idx + 1, s_idx + 1)
        
        memo[state] = res
        return res

    def match_segment(p_seg: str, s_seg: str) -> bool:
        # Standard glob matching for a single segment string
        # using ? and *
        p_len = len(p_seg)
        s_len = len(s_seg)
        
        # DP for segment matching
        dp = [[False] * (s_len + 1) for _ in range(p_len + 1)]
        dp[0][0] = True
        
        for i in range(1, p_len + 1):
            char = p_seg[i-1]
            if char == '*':
                # * matches zero or more characters
                dp[i][0] = dp[i-1][0]
                for j in range(1, s_len + 1):
                    dp[i][j] = dp[i-1][j] or dp[i][j-1]
            elif char == '?':
                # ? matches exactly one character
                for j in range(1, s_len + 1):
                    dp[i][j] = dp[i-1][j-1]
            else:
                # Literal match
                for j in range(1, s_len + 1):
                    if char == s_seg[j-1]:
                        dp[i][j] = dp[i-1][j-1]
        return dp[p_len][s_len]

    # The logic above for '*' in solve() was slightly redundant with match_segment.
    # Let's refine solve to use match_segment for all non-** segments.
    
    memo = {}
    def solve_refined(p_idx: int, s_idx: int) -> bool:
        state = (p_idx, s_idx)
        if state in memo: return memo[state]
        
        if p_idx == len(pattern_segments):
            return s_idx == len(path_segments)
        
        curr_p = pattern_segments[p_idx]
        
        if curr_p == "**":
            # Match zero segments
            if solve_refined(p_idx + 1, s_idx):
                memo[state] = True
                return True
            # Match one or more segments
            if s_idx < len(path_segments) and solve_refined(p_idx, s_idx + 1):
                memo[state] = True
                return True
            memo[state] = False
            return False
        else:
            # Match current segment using segment-level rules
            if s_idx < len(path_segments) and match_segment(curr_p, path_segments[s_idx]):
                if solve_refined(p_idx + 1, s_idx + 1):
                    memo[state] = True
                    return True
            memo[state] = False
            return False

    return solve_refined(0, 0)
