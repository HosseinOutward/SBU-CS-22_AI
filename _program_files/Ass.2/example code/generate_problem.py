import gui, ai, sim, json
import numpy as np
import sys

def is_goal(state):
    for i,a in enumerate(state[:-1]):
        if ((state[i+1]-a)!=0).astype(int).sum()>0: return False
    return True


def generate_cube():
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


def generate_problem_from_cube(yyy):
    with open(r"complete_rubic.txt", 'r') as fp:
        res=eval(fp.read())
    ok=True
    while ok:
        ok=False
        al=[]
        env=sim.Simulator(res[yyy], [[i+1,i+2] for i in range(26) if np.random.random()<0.3])
        interf=sim.Interface()
        agent = ai.Agent()
        a=interf.valid_actions(env, [])
        for _ in range(3):
            al.append(a[np.random.randint(0, len(a))])
            interf.evolve(env, al[-1])
            if not interf.valid_state(env):
                ok=True
                break
        if interf.goal_test(env): ok=True
        agent.act(interf.perceive(env))
        if len(agent.predicted_actions)>=1: ok=True

    with open(r"problem_set.txt", 'a') as fp:
        fp.write(interf.perceive(env))
        fp.write(",\n")


generate_problem_from_cube(int(sys.argv[1]))
