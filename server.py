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
            
            @app.get("/")
            async def root():
                return {"message": "Email Triage Environment is running!", "endpoints": ["/reset", "/step", "/health", "/metadata", "/schema", "/state", "/mcp"]}
            
            @app.get("/health")
            async def health():
                return {"status": "healthy"}
            
            @app.get("/metadata")
            async def metadata():
                return {
                    "name": "email-triage-env",
                    "description": "Email triage environment for AI agents",
                    "version": "1.0.0"
                }
            
            @app.get("/schema")
            async def schema():
                return {
                    "action": {
                        "type": "object",
                        "properties": {
                            "email_id": {"type": "integer"},
                            "action": {"type": "string", "enum": ["urgent", "normal", "spam"]}
                        }
                    },
                    "observation": {
                        "type": "object",
                        "properties": {
                            "current_email": {"type": "object"},
                            "remaining_count": {"type": "integer"}
                        }
                    },
                    "state": {
                        "type": "object"
                    }
                }
            
            @app.get("/reset")
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
                action_obj = EmailAction(email_id=action["email_id"], action=action["action"])
                observation, reward, done, info = env.step(action_obj)
                return {"observation": observation.dict(), "reward": reward, "done": done, "info": info}
            
            @app.get("/state")
            async def get_state():
                global env
                if env is None:
                    return {"error": "Environment not initialized"}
                return env.state()
            
            @app.post("/mcp")
            async def mcp(request: dict = None):
                if request is None:
                    request = {}
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id", 1),
                    "result": {"status": "ok"}
                }
            
            @app.get("/openapi.json")
            async def get_openapi():
                return app.openapi()
            
            def main():
                """Entry point for openenv-server command"""
                import uvicorn
                parser = argparse.ArgumentParser()
                parser.add_argument("--port", type=int, default=7860)
                args = parser.parse_args()
                uvicorn.run(app, host="0.0.0.0", port=args.port)
            
            if __name__ == "__main__":
                main()

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