from __future__ import annotations

from .api_gateway import service

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import StreamingResponse

    LOCAL_MVP_FRONTEND_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ]

    app = FastAPI(title="LEDO MVP Phase 2 Latency-Aware Dual Path Router")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=LOCAL_MVP_FRONTEND_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/state")
    def get_state():
        return service.current_state()

    @app.post("/api/scenario/critical-collision")
    def critical_collision():
        return service.run_critical_collision()

    @app.post("/api/scenario/async-replan")
    def async_replan():
        return service.run_async_replan()

    @app.post("/api/approval/approve")
    def approve():
        return service.approve_pending()

    @app.post("/api/approval/reject")
    def reject():
        return service.reject_pending()

    @app.post("/api/reset")
    def reset():
        return service.reset()

    @app.get("/api/graph")
    def graph():
        state = service.current_state()
        return {"nodes": state.graph_nodes, "edges": state.graph_edges}

    @app.get("/api/audit")
    def audit():
        return service.current_state().audit_trace

    @app.get("/api/execution-status")
    def execution_status():
        state = service.current_state()
        return {
            "execution_request": state.execution_request,
            "adapter_result": state.adapter_result,
            "physical_command_status": state.physical_command_status,
        }

    @app.get("/api/rule-trace")
    def rule_trace():
        return service.current_state().rule_decision_trace

    @app.get("/api/events/stream")
    def stream():
        async def events():
            yield f"data: {service.current_state().model_dump_json()}\\n\\n"

        return StreamingResponse(events(), media_type="text/event-stream")

except Exception:
    app = None
