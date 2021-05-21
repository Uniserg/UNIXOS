import re
def split_cmd(cmd):
    # def strip():
    #     nonlocal to
    #     while to < len(cmd) and cmd[to] == ' ':
    #         to += 1
    #
    # exe, msg, params = ([0, 0] for _ in range(3))
    sp = []
    fr = 0
    to = 0
    t = ''
    while to < len(cmd):
        if cmd[to] == ' ':
            sp.append(cmd[fr:to])
            fr = to + 1
            to += 1
        to += 1

    sp.append(cmd[fr:to])
    return sp


s = "\"(.*?)\"|([^\\s]+)"
print(*filter(None, re.split(s, "ls")))
