"""
server.py - OpenEnv server for Email Triage Environment
This exposes your environment via HTTP for Hugging Face Spaces
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from openenv import OpenEnvServer
from environment import EmailTriageEnvironment
from models import EmailObservation, EmailAction, EmailReward

# Create and configure the server
server = OpenEnvServer(
    env_class=EmailTriageEnvironment,
    observation_model=EmailObservation,
    action_model=EmailAction,
    reward_model=EmailReward,
)

# Run the server
if __name__ == "__main__":
    server.run()