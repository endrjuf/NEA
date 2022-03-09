
x = "Result: Hello, it's Me. I Was Wondering If After All These Years You'd Like To Me To Go Over Heard Everything They Say? That Time Supposed To Heal You. Hello? Can You Hear Me? I'm In California? Dreaming About Who We Used To Be when We Were Young Girls And Free? I Forgot and How We Felt Before The Me To Talk About Myself. Did You Ever Make It Out Of That Town? When The Twist Secret? Let The Boots Are Running? I'm."
lim=200

for s in x.split("\n"):
    if s == "": print
    w=0
    l = []
    for d in s.split():
        if w + len(d) + 1 <= lim:
            l.append(d)
            w += len(d) + 1
        else:
            print(" ".join(l))
            l = [d]
            w = len(d)
    if (len(l)): print(" ".join(l))