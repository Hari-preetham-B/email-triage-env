"""
server.py - OpenEnv server for Email Triage Environment
"""

import sys
import os
import argparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try different import options
try:
    from openenv.server import OpenEnvServer
except ImportError:
    try:
        from openenv.core import OpenEnvServer
    except ImportError:
        try:
            from openenv import OpenEnvServer
        except ImportError:
            # Fallback: Create a simple FastAPI server
            from fastapi import FastAPI
            from environment import EmailTriageEnvironment
            from models import EmailObservation, EmailAction, EmailReward
            
            app = FastAPI()
            env = None
            
            @app.post("/reset")
            async def reset():
                global env
                env = EmailTriageEnvironment()
                obs = env.reset()
                return {"status": "ok", "observation": obs.dict()}
            
            @app.post("/step")
            async def step(action: dict):
                global env
                if env is None:
                    return {"error": "Environment not initialized"}
                # Process action
                return {"status": "ok"}
            
            if __name__ == "__main__":
                import uvicorn
                uvicorn.run(app, host="0.0.0.0", port=7860)
            exit(0)

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