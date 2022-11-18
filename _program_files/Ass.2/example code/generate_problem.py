def is_goal(state):
    for i,a in enumerate(state[:-1]):
        if ((state[i+1]-a)!=0).astype(int).sum()>0: return False
    return True


def BFS_SAMPLE_CODE():
    q = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                q.append([[i,j,k]])
    np.random.shuffle(q)

    while q:
        node = q.pop()

        action_list=[]
        for i in range(3):
            for j in [[1], [0,2], [1]][node[-1][i]]:
                new_tail = list(node[-1])
                new_tail[i]=j
                if new_tail in node: continue
                action_list.append(new_tail)
        np.random.shuffle(action_list)

        for action in action_list:
            child_state = [list(a) for a in node]+[action]

            # add children to queue
            q.append(child_state)

            # return if goal test is true
            if len(child_state)==27:
                yield child_state
# results=[]
res=BFS_SAMPLE_CODE()
a=next(res)
# results.append(a)