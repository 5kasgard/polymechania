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
            res = s_idx == len(path_segments)
            memo[state] = res
            return res

        p_seg = pattern_segments[p_idx]

        # Case 1: "**" matches zero or more entire segments
        if p_seg == "**":
            # Option A: "**" matches zero segments (move to next pattern segment)
            if solve(p_idx + 1, s_idx):
                memo[state] = True
                return True
            # Option B: "**" matches one or more segments (consume one path segment and stay on "**")
            if s_idx < len(path_segments):
                if solve(p_idx, s_idx + 1):
                    memo[state] = True
                    return True
            memo[state] = False
            return False

        # Case 2: Single segment matching
        # If we ran out of path segments but pattern still has non-"**" segments
        if s_idx == len(path_segments):
            # Only possible if remaining pattern segments are all "**"
            # But we handled "**" above. If we are here, p_seg is not "**".
            # However, a pattern like "a/**" vs "a" is handled by the "**" logic.
            # If p_seg is not "**", it must match something.
            memo[state] = False
            return False

        s_seg = path_segments[s_idx]

        # Sub-case: "?" matches exactly one character (not "/")
        if p_seg == "?":
            if len(s_seg) == 1:
                res = solve(p_idx + 1, s_idx + 1)
                memo[state] = res
                return res
            else:
                memo[state] = False
                return False

        # Sub-case: "*" matches zero or more characters (not "/")
        if p_seg == "*":
            # Try all possible split points in the current segment
            for i in range(len(s_seg) + 1):
                # The "*" matches s_seg[:i], then we move to next pattern segment
                # But wait, "*" is within a segment. The spec says "*" matches any run 
                # of characters other than "/". This means "*" is a segment-level 
                # wildcard for characters within a segment.
                # Actually, the spec says: "?" matches one char, "*" matches any run.
                # This implies "*" is part of a segment or is the segment.
                # Re-reading: "a?c" vs "a/c" is False. This means "?" is char-level.
                # "src/*.py" vs "src/x/a.py" is False. This means "*" is char-level.
                # "src/**/*.py" vs "src/x/y/a.py" is True. This means "**" is segment-level.
                pass

        # Correcting interpretation:
        # "**" is a special segment.
        # Other segments can contain "?" and "*".
        # Let's re-evaluate segment matching.
        
        # If p_seg is not "**", it must match s_seg exactly using "?" and "*"
        if match_segment(p_seg, s_seg):
            res = solve(p_idx + 1, s_idx + 1)
            memo[state] = res
            return res
        
        memo[state] = False
        return False

    def match_segment(p_seg: str, s_seg: str) -> bool:
        # Standard wildcard matching for a single segment (no "/" allowed)
        # p_seg can contain '?' and '*'
        m, n = len(p_seg), len(s_seg)
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True
        
        for i in range(1, m + 1):
            if p_seg[i-1] == '*':
                dp[i][0] = dp[i-1][0]
            else:
                dp[i][0] = False
                
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if p_seg[i-1] == '*':
                    dp[i][j] = dp[i-1][j] or dp[i][j-1]
                elif p_seg[i-1] == '?' or p_seg[i-1] == s_seg[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = False
        return dp[m][n]

    # The logic above for "**" is correct for segment-level.
    # But the segment-level matching for "*" and "?" needs to be integrated.
    # Let's refine the solve function.

    memo = {}

    def solve_refined(p_idx: int, s_idx: int) -> bool:
        state = (p_idx, s_idx)
        if state in memo: return memo[state]

        if p_idx == len(pattern_segments):
            return s_idx == len(path_segments)

        p_seg = pattern_segments[p_idx]

        if p_seg == "**":
            # Match zero segments
            if solve_refined(p_idx + 1, s_idx):
                memo[state] = True
                return True
            # Match one or more segments
            if s_idx < len(path_segments):
                if solve_refined(p_idx, s_idx + 1):
                    memo[state] = True
                    return True
            memo[state] = False
            return False
        else:
            # p_seg is a normal segment (may contain * or ?)
            # It must match exactly one segment s_seg
            if s_idx < len(path_segments):
                if match_segment(p_seg, path_segments[s_idx]):
                    if solve_refined(p_idx + 1, s_idx + 1):
                        memo[state] = True
                        return True
            
            memo[state] = False
            return False

    return solve_refined(0, 0)
