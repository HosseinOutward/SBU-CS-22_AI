from os import environ
import traceback
import json
from time import sleep, time

from gimulator.client import DirectorClient
from gimulator.proto_pb2 import *

from env import Env

NUMBER_OF_PLAYERS = 1


def main():
    # client = DirectorClient(True, host="127.0.0.1:3333", token="396a4a80-22a4-4108-8ef6-c3e411395ce8")
    client = DirectorClient(True)
    config = json.load(open("./config.json", 'r'))

    while True:
        print("Getting users")
        users = list(client.GetActors())
        if all(map(lambda x: x.status == running or x.status == unknown, users)):
            if len(users) == NUMBER_OF_PLAYERS and all(map(lambda x: x.readiness, users)):
                # We have our agent
                break
        elif any(map(lambda x: x.status == failed or x.status == succeeded, users)):
            # Failed Agent(s)
            result = Result(id=environ['GIMULATOR_ROOM_ID'])
            result.status = Result.failed
            result.msg = 'Actor failed!'
            client.PutResult(result)
        sleep(1)

    results = []

    try:
        # Sending total runs
        client.Put(Message(key=Key(type="world", name="director-run", namespace="sbu-ai-2022"),
                           content=json.dumps({"total": len(config['runs'])})))

        for index, run in enumerate(config["runs"]):
            print(f"RUN {index + 1}")

            client.Put(Message(key=Key(type="world", name="director-run", namespace="sbu-ai-2022"), content=str(index)))

            # PHASE 1: INIT
            # print(run)
            world = Env(run['map'], run['agent_loc'])

            # if index == 0:
            # Broadcasting initial data to agent
            print("Broadcasting initial data")
            message = {
                "location": run['loc'],
            }
            sleep(.25)
            client.Put(Message(key=Key(type="world", name="director-init", namespace="sbu-ai-2022"),
                               content=json.dumps(message)))

            # Waiting for agent to receive init data and be ready
            for action in client.Watch(Key(type="world", name="actor-init", namespace="sbu-ai-2022")):
                if action.content == "ready":
                    # agent = world.add_agent(Agent, tuple(run['loc']))
                    break
            # else:
            #     agent = world.add_agent(Agent, tuple(run['loc']))

            print("[Director] Init done")
            # END OF PHASE 1: INIT

            # PHASE 2: MAIN
            # Firing first response
            message = world.perceive()
            message['status'] = "success"
            sleep(.25)
            client.Put(
                Message(key=Key(type="action", name="director", namespace="sbu-ai-2022"), content=json.dumps(message)))
            print("Sent kickstart")
            # gui = cli_ui()

            startTime = time()

            for action in client.Watch(Key(type="action", name="actor", namespace="sbu-ai-2022")):
                now = time()
                # if now - startTime > 600:
                #     # Agent had exception
                #     print("Agent reached the timeout")
                #     client.Put(Message(key=Key(type="action", name="director", namespace="sbu-ai-2022"), content=json.dumps({"status": "timed_out"})))

                #     result = Result(id=environ['GIMULATOR_ROOM_ID'])
                #     result.status = Result.failed
                #     result.msg = f'Agent reached the timeout (600s).\nThe maximum duration for agent execution is 10 minutes per map.'
                #     client.PutResult(result)

                response = json.loads(action.content)
                print(response)

                if response['action'] == "fail":
                    # Agent had exception
                    print("Agent had an exception")
                    client.Put(Message(key=Key(type="action", name="director", namespace="sbu-ai-2022"),
                                       content=json.dumps({"status": "failed"})))

                    result = Result(id=environ['GIMULATOR_ROOM_ID'])
                    result.status = Result.failed
                    result.msg = f'Actor failed! (EXCEPTION)\nmessage: {response["message"]}'
                    print("sending result")
                    client.PutResult(result)

                status = world.evolve(response['action'])
                newState = world.perceive()
                # gui.display(world.state)

                if world.goal_test():
                    # Agent solved the problem
                    client.Put(Message(key=Key(type="action", name="director", namespace="sbu-ai-2022"),
                                       content=json.dumps({"status": "victory"})))
                    results.append({
                        "index": index,
                        # "run": run,
                        "score": newState['score'],
                        "cost": newState['cost']
                    })
                    break

                message = world.perceive()
                message['status'] = status
                client.Put(Message(key=Key(type="action", name="director", namespace="sbu-ai-2022"),
                                   content=json.dumps(message)))
            print(f"RUN {index + 1} FINISHED")
    except Exception as e:
        # Evaluator had exception
        tb = traceback.format_exc()
        print("Evaluator faced an exception")
        print(tb, e)
        client.Put(Message(key=Key(type="action", name="director", namespace="sbu-ai-2022"),
                           content=json.dumps({"status": "exception", "traceback": tb, "exception": str(e)})))

        result = Result(id=environ['GIMULATOR_ROOM_ID'])
        result.status = Result.failed
        result.msg = f'Evaluator faced an exception.'
        client.PutResult(result)

    sleep(.5)

    print("Results:", results)
    totalCost_Agent = sum(result['cost'] for result in results)
    totalCost_Opt = sum(run['cost'] for run in config['runs'])
    totalPoints = round(totalCost_Opt * 100 / totalCost_Agent, 3)
    print(f"Final Score: {totalPoints}")

    # Packaging into gimulator result object
    gResult = Result(id=environ['GIMULATOR_ROOM_ID'])
    gResult.status = Result.success
    gResult.scores.extend([Result.Score(name=users[0].name, score=str(totalPoints))])
    client.PutResult(gResult)
    exit(0)


if __name__ == '__main__':
    main()
