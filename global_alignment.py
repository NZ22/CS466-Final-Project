# Needleman–Wunsch algorithm

def global_alignment(v, w, match, mismatch, gap):
    n = len(v)
    m = len(w)

    dp = [[0 for j in range(m + 1)] for i in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = dp[i - 1][0] + gap
    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] + gap

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if v[i - 1] == w[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + match
            else:
                dp[i][j] = max(max(dp[i - 1][j] + gap, dp[i][j - 1] + gap), dp[i - 1][j - 1] + mismatch)

    return dp

def fitting_alignment(v, w, match, mismatch, gap):
    n = len(v)
    m = len(w)

    dp = [[0 for j in range(m + 1)] for i in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = dp[i - 1][0] + gap

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if v[i - 1] == w[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + match
            else:
                dp[i][j] = max(max(dp[i - 1][j] + gap, dp[i][j - 1] + gap), dp[i - 1][j - 1] + mismatch)

    return dp

def local_alignment(v, w, match, mismatch, gap):
    n = len(v)
    m = len(w)

    dp = [[0 for j in range(m + 1)] for i in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if v[i - 1] == w[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + match
            else:
                dp[i][j] = max(max(dp[i - 1][j] + gap, dp[i][j - 1] + gap), dp[i - 1][j - 1] + mismatch)
            dp[i][j] = max(dp[i][j], 0)

    return dp

def backtrace(v, w, dp, i, j, trace1, trace2, l, mode):
    if (mode == 1 and i == 0 and j == 0) or (mode == 2 and i == 0) or (mode == 3 and dp[i][j] == 0):
        l.append([trace2, trace1])
    elif i == 0:
        backtrace(v, w, dp, i, j - 1, "_" + trace1, w[j - 1] + trace2, l, mode)
    elif j == 0:
        backtrace(v, w, dp, i - 1, j, v[i - 1] + trace1, "_" + trace2, l, mode)
    else:
        if v[i - 1] == w[j - 1] or dp[i - 1][j - 1] + mismatch == dp[i][j]:
            backtrace(v, w, dp, i - 1, j - 1, v[i - 1] + trace1, w[j - 1] + trace2, l, mode)
        if dp[i - 1][j] + gap == dp[i][j]:
            backtrace(v, w, dp, i - 1, j, v[i - 1] + trace1, "_" + trace2, l, mode)
        if dp[i][j - 1] + gap == dp[i][j]:
            backtrace(v, w, dp, i, j - 1, "_" + trace1, w[j - 1] + trace2, l, mode)


if __name__ == 'main':
    w = input("Sequence w: ")
    v = input("Sequence v: ")

    match = float(input("\nmatch [default=1]: ") or 1)
    mismatch = float(input("mismatch [default=-1]: ") or -1)
    gap = float(input("gap [default=-1]: ") or -1)

    assert gap <= 0, "gap must not be positive"

    n = len(v)
    m = len(w)

    while True:
        mode = int(input("\nmode [1:global alignment, 2: fitting alignment, 3: local alignment]\
            [default=global alignment]: ") or 1)

        l = []
        score = None

        if mode == 1:
            dp = global_alignment(v, w, match, mismatch, gap)
            backtrace(v, w, dp, n, m, "", "", l, mode)
            score = dp[-1][-1]

        elif mode == 2:
            dp = fitting_alignment(v, w, match, mismatch, gap)

            score = dp[-1][-1]

            for x in dp:
                print (x)

            for j in range(m + 1):
                score = max(score, dp[n][j])
            for j in range(m + 1):
                if dp[n][j] == score:
                    backtrace(v, w, dp, n, j, "", "", l, mode) # TODO: fix

        elif mode == 3:
            dp = local_alignment(v, w, match, mismatch, gap)
            score = dp[-1][-1]
            for i in range(n + 1):
                for j in range(m + 1):
                    score = max(score, dp[i][j])
            for i in range(n + 1):
                for j in range(m + 1):
                    if dp[i][j] == score:
                        backtrace(v, w, dp, i, j, "", "", l, mode) # TODO:fix


        print ("\n\nSCORE: ", score)
        print (l[0])

        if len(l) > 1:
            print ()
            x = input("found at least {} sequences with score {} found, display all?[y/n]".format(len(l), score))

            if x == "y":
                for seq in l:
                    print (seq)