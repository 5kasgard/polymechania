import re

def glob_match(pattern: str, path: str) -> bool:
    """
    Matches a pattern against a path using glob rules.
    '?' matches one char (not '/'), '*' matches any run (not '/'), 
    '**' matches zero or more segments.
    """
    pattern_segments = pattern.split('/')
    path_segments = path.split('/')

    memo = {}

    def match_segment(p_seg: str, s_seg: str) -> bool:
        """Matches a single pattern segment against a single path segment."""
        if p_seg == '*':
            # '*' matches any run of characters (possibly empty)
            # In a single segment, this is equivalent to matching anything.
            return True
        if p_seg == '?':
            # '?' matches exactly one character
            return len(s_seg) == 1
        
        # For other patterns, we convert the glob segment to a regex.
        # We escape special regex characters but keep our glob logic.
        # Since we are matching a single segment, we don't need to worry about '/'
        # because the split already handled it.
        regex_pattern = ""
        i = 0
        while i < len(p_seg):
            if p_seg[i] == '*':
                # Handle multiple '*' in a segment as a single '*'
                regex_pattern += '.*'
                while i + 1 < len(p_seg) and p_seg[i+1] == '*':
                    i += 1
            elif p_seg[i] == '?':
                regex_pattern += '.'
            else:
                regex_pattern += re.escape(p_seg[i])
            i += 1
        
        return re.fullmatch(regex_pattern, s_seg) is not None

    def solve(p_idx: int, s_idx: int) -> bool:
        state = (p_idx, s_idx)
        if state in memo:
            return memo[state]

        # Base case: reached end of pattern
        if p_idx == len(pattern_segments):
            # Match is successful only if we also reached end of path
            return s_idx == len(path_segments)

        p_seg = pattern_segments[p_idx]

        if p_seg == '**':
            # Case 1: '**' matches zero segments
            if solve(p_idx + 1, s_idx):
                memo[state] = True
                return True
            
            # Case 2: '**' matches one or more segments
            # We try matching the rest of the pattern against the path starting from s_idx, s_idx+1, etc.
            for next_s in range(s_idx + 1, len(path_segments) + 1):
                if solve(p_idx + 1, next_s):
                    memo[state] = True
                    return True
            
            # Case 3: '**' consumes one segment and stays as '**' to potentially consume more
            # This is covered by the loop above, but for clarity:
            # We can think of '**' as (zero segments) OR (one segment AND '**')
            # However, the loop above is more direct for the "zero or more" logic.
            
            # Actually, a simpler way for '**':
            # It can match zero segments: solve(p_idx + 1, s_idx)
            # Or it can match one segment and we stay at p_idx: solve(p_idx, s_idx + 1)
            # But we must ensure we don't loop infinitely if s_idx reaches end.
            # Let's use the loop approach.
            
            memo[state] = False
            return False
        else:
            # Standard segment matching
            if s_idx < len(path_segments) and match_segment(p_seg, path_segments[s_idx]):
                res = solve(p_idx + 1, s_idx + 1)
                memo[state] = res
                return res
            else:
                memo[state] = False
                return False

    # Special handling for the '**' logic to avoid recursion depth issues 
    # and ensure it matches the "zero or more segments" correctly.
    # The loop in the 'if p_seg == "**"' block handles the "zero or more" correctly.
    
    # Re-implementing the solve logic slightly more robustly for '**'
    def solve_robust(p_idx: int, s_idx: int) -> bool:
        state = (p_idx, s_idx)
        if state in memo: return memo[state]

        if p_idx == len(pattern_segments):
            return s_idx == len(path_segments)

        p_seg = pattern_segments[p_idx]

        if p_seg == '**':
            # Try matching zero segments
            if solve_robust(p_idx + 1, s_idx):
                memo[state] = True
                return True
            # Try matching one or more segments
            for i in range(s_idx, len(path_segments)):
                if solve_robust(p_idx + 1, i + 1):
                    memo[state] = True
                    return True
            memo[state] = False
            return False
        else:
            if s_idx < len(path_segments) and match_segment(p_seg, path_segments[s_idx]):
                res = solve_robust(p_idx + 1, s_idx + 1)
                memo[state] = res
                return res
            memo[state] = False
            return False

    return solve_robust(0, 0)
