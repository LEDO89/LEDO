package ledo.mvp

default allow := false

allow if {
  input.action_type == "E_STOP"
  input.event_urgency == "CRITICAL_REALTIME"
  not input.forbidden
}

allow if {
  input.action_type == "REPLAN_WORK"
  input.approval_status == "APPROVED"
  not input.forbidden
}

approval_status := "NOT_REQUIRED" if {
  input.action_type == "E_STOP"
  input.event_urgency == "CRITICAL_REALTIME"
}

approval_status := "PENDING" if {
  input.action_type == "REPLAN_WORK"
}

