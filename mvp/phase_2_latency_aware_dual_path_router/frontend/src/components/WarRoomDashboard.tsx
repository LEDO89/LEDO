"use client";

import { useEffect, useState } from "react";
import { API_BASE, api } from "../lib/api";
import type { WarRoomState } from "../lib/types";
import { ApprovalPanel } from "./ApprovalPanel";
import { AuditTracePanel } from "./AuditTracePanel";
import { DecisionRouterPanel } from "./DecisionRouterPanel";
import { ExternalSystemStatusPanel } from "./ExternalSystemStatusPanel";
import { OntologyGraphPanel } from "./OntologyGraphPanel";
import { SituationPanel } from "./SituationPanel";

export function WarRoomDashboard() {
  const [state, setState] = useState<WarRoomState | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [requestStatus, setRequestStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);

  const run = async (fn: () => Promise<WarRoomState>) => {
    setRequestStatus("loading");
    try {
      setError(null);
      const nextState = await fn();
      setState(nextState);
      setLastUpdated(new Date().toISOString());
      setRequestStatus("success");
    } catch (err) {
      const message = err instanceof Error ? err.message : "request failed";
      console.error(message);
      setError(message);
      setRequestStatus("error");
    }
  };

  useEffect(() => {
    run(api.state);
  }, []);

  return (
    <main>
      <header className="topbar">
        <div>
          <h1>LEDO War Room</h1>
          <p>Latency-aware dual-path decision router</p>
          <dl className="statusGrid">
            <dt>API</dt><dd>{API_BASE}</dd>
            <dt>Status</dt><dd>{requestStatus}</dd>
            <dt>Trace ID</dt><dd>{state?.trace_id ?? "not_started"}</dd>
            <dt>Last Updated</dt><dd>{lastUpdated ?? "never"}</dd>
          </dl>
        </div>
        <div className="actions">
          <button onClick={() => run(api.critical)} disabled={requestStatus === "loading"}>Simulate Critical Collision</button>
          <button onClick={() => run(api.asyncReplan)} disabled={requestStatus === "loading"}>Simulate Async Replan</button>
          <button onClick={() => run(api.state)} disabled={requestStatus === "loading"}>Refresh Graph</button>
          <button onClick={() => run(api.state)} disabled={requestStatus === "loading"}>Refresh Audit</button>
          <button onClick={() => run(api.state)} disabled={requestStatus === "loading"}>Refresh Rule Trace</button>
          <button onClick={() => run(api.reset)} disabled={requestStatus === "loading"}>Reset Scenario</button>
        </div>
      </header>
      {error && <div className="error" role="alert">Request error: {error}</div>}
      <div className="dashboard">
        <SituationPanel state={state} />
        <DecisionRouterPanel state={state} />
        <ApprovalPanel
          state={state}
          loading={requestStatus === "loading"}
          onApprove={() => run(api.approve)}
          onReject={() => run(api.reject)}
        />
        <ExternalSystemStatusPanel state={state} />
        <OntologyGraphPanel state={state} />
        <AuditTracePanel state={state} />
      </div>
    </main>
  );
}
