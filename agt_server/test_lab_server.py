"""
test harness for running lab stencil solution agents against the server.

starts server, connects 2 solution agents, triggers tournament via SIGTSTP,
waits for completion. used for verifying end-to-end server connectivity.
"""

import subprocess
import signal
import time
import sys
import os
import threading

PYTHON = os.path.join(os.path.dirname(__file__), '..', '.venv', 'bin', 'python')
SERVER_SCRIPT = os.path.join(os.path.dirname(__file__), 'server', 'server.py')
BASE = os.path.dirname(__file__)

# map of lab -> (game_type, list of solution script paths)
LABS = {
    "lab01_chicken": {
        "game": "chicken",
        "agents": [
            os.path.join(BASE, "stencils", "lab01_stencil", "solutions", "competition_agent_solution.py"),
            os.path.join(BASE, "stencils", "lab01_stencil", "solutions", "competition_agent_solution.py"),
        ],
    },
    "lab02_bos": {
        "game": "bos",
        "agents": [
            os.path.join(BASE, "stencils", "lab02_stencil", "solutions", "BOSCompetitionExampleAgent.py"),
            os.path.join(BASE, "stencils", "lab02_stencil", "solutions", "BOSCompetitionExampleAgent.py"),
        ],
    },
    "lab02_bosii": {
        "game": "bosii",
        "agents": [
            os.path.join(BASE, "stencils", "lab02_stencil", "solutions", "bosii_competition_stencil.py"),
            os.path.join(BASE, "stencils", "lab02_stencil", "solutions", "bosii_competition_stencil.py"),
        ],
    },
    "lab03_chicken": {
        "game": "chicken",
        "agents": [
            os.path.join(BASE, "stencils", "lab03_stencil", "solutions", "my_agent.py"),
            os.path.join(BASE, "stencils", "lab03_stencil", "solutions", "my_agent.py"),
        ],
    },
    "lab07_auction": {
        "game": "auction",
        "agents": [
            os.path.join(BASE, "stencils", "lab07_stencil", "solutions", "competition_agent.py"),
            os.path.join(BASE, "stencils", "lab07_stencil", "solutions", "competition_agent.py"),
        ],
    },
}


def drain_pipe(proc, lines_list):
    """drain stdout from a subprocess into a list, preventing pipe buffer blocking."""
    try:
        for line in iter(proc.stdout.readline, b''):
            lines_list.append(line.decode().rstrip())
    except (ValueError, OSError):
        pass


def test_lab(lab_name, lab_config, port=8080):
    """test a single lab end-to-end."""
    game = lab_config["game"]
    agent_scripts = lab_config["agents"]

    print(f"\n{'='*60}")
    print(f"TESTING: {lab_name} (game={game})")
    print(f"{'='*60}")

    # start server
    print(f"  starting server for {game} on port {port}...")
    server_proc = subprocess.Popen(
        [PYTHON, SERVER_SCRIPT, "--game", game, "--port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=BASE,
    )
    # drain server stdout in background to prevent pipe blocking
    server_lines = []
    server_thread = threading.Thread(target=drain_pipe, args=(server_proc, server_lines), daemon=True)
    server_thread.start()

    time.sleep(3)

    if server_proc.poll() is not None:
        time.sleep(0.5)
        print(f"  SERVER FAILED TO START:")
        for line in server_lines[-20:]:
            print(f"    {line}")
        return False

    # start agent processes
    agent_procs = []
    agent_lines_list = []
    agent_threads = []
    for i, script in enumerate(agent_scripts):
        print(f"  starting agent {i+1}: {os.path.basename(script)}")
        proc = subprocess.Popen(
            [PYTHON, script],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=os.path.dirname(script),
        )
        agent_procs.append(proc)
        lines = []
        agent_lines_list.append(lines)
        t = threading.Thread(target=drain_pipe, args=(proc, lines), daemon=True)
        t.start()
        agent_threads.append(t)
        time.sleep(1)

    # check agents connected
    time.sleep(2)
    for i, proc in enumerate(agent_procs):
        if proc.poll() is not None:
            time.sleep(0.5)
            print(f"  AGENT {i+1} DIED EARLY:")
            for line in agent_lines_list[i][-20:]:
                print(f"    {line}")
            server_proc.kill()
            return False

    # trigger tournament via SIGTSTP
    print(f"  triggering tournament (SIGTSTP)...")
    os.kill(server_proc.pid, signal.SIGTSTP)

    # wait for tournament to complete (up to 60 seconds)
    print(f"  waiting for tournament...")
    try:
        for proc in agent_procs:
            proc.wait(timeout=60)
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT waiting for agents to finish")
        for proc in agent_procs:
            proc.kill()
        server_proc.kill()
        # show engine lines for debugging
        engine_lines = [l for l in server_lines if '[ENGINE]' in l]
        if engine_lines:
            print(f"  ENGINE progress ({len(engine_lines)} lines):")
            for line in engine_lines[-10:]:
                print(f"    {line}")
        return False

    # collect results
    success = True
    for i, proc in enumerate(agent_procs):
        rc = proc.returncode
        agent_out = "\n".join(agent_lines_list[i])
        if rc != 0:
            print(f"  AGENT {i+1} exited with code {rc}")
            for line in agent_lines_list[i][-15:]:
                print(f"    {line}")
            success = False
        else:
            if "TOURNAMENT RESULTS" in agent_out or "FINAL LEADERBOARD" in agent_out:
                print(f"  agent {i+1}: tournament completed successfully")
            else:
                print(f"  agent {i+1}: exited ok but no tournament results found")
                for line in agent_lines_list[i][-10:]:
                    print(f"    {line}")

    # cleanup server
    server_proc.kill()

    if success:
        print(f"  RESULT: PASS")
    else:
        print(f"  RESULT: FAIL")
        # show server errors
        error_lines = [l for l in server_lines if 'error' in l.lower() or 'Error' in l or 'Traceback' in l]
        if error_lines:
            print(f"  SERVER ERRORS:")
            for line in error_lines[-10:]:
                print(f"    {line}")

    return success


if __name__ == "__main__":
    # allow specifying a single lab to test
    if len(sys.argv) > 1:
        labs_to_test = {k: v for k, v in LABS.items() if sys.argv[1] in k}
    else:
        labs_to_test = LABS

    results = {}
    for lab_name, lab_config in labs_to_test.items():
        # kill any leftover processes on port 8080
        os.system("lsof -ti:8080 2>/dev/null | xargs kill -9 2>/dev/null")
        time.sleep(1)
        results[lab_name] = test_lab(lab_name, lab_config)

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for lab_name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  {lab_name}: {status}")
