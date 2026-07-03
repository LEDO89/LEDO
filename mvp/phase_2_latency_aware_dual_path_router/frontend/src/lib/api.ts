import type { WarRoomState } from "./types";

export const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://127.0.0.1:8765";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path}`;
  try {
    const response = await fetch(url, {
      ...init,
      headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
      cache: "no-store"
    });
    if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
    return response.json();
  } catch (error) {
    const detail = error instanceof Error ? error.message : "request failed";
    throw new Error(`API request failed for ${url}: ${detail}`);
  }
}

export const api = {
  state: () => request<WarRoomState>("/api/state"),
  critical: () => request<WarRoomState>("/api/scenario/critical-collision", { method: "POST" }),
  asyncReplan: () => request<WarRoomState>("/api/scenario/async-replan", { method: "POST" }),
  approve: () => request<WarRoomState>("/api/approval/approve", { method: "POST" }),
  reject: () => request<WarRoomState>("/api/approval/reject", { method: "POST" }),
  reset: () => request<WarRoomState>("/api/reset", { method: "POST" })
};
