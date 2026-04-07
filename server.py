"""
server.py - OpenEnv server for Email Triage Environment
"""

import sys
import os
import argparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from openenv import OpenEnvServer
from environment import EmailTriageEnvironment
from models import EmailObservation, EmailAction, EmailReward

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=7860)
    args = parser.parse_args()
    
    server = OpenEnvServer(
        env_class=EmailTriageEnvironment,
        observation_model=EmailObservation,
        action_model=EmailAction,
        reward_model=EmailReward,
    )
    
    server.run(host="0.0.0.0", port=args.port)