from .schemas import AdapterResult, FeedbackEvent, PhysicalCommandStatus, new_id


def create_feedback(adapter_result: AdapterResult) -> FeedbackEvent:
    return FeedbackEvent(
        id=new_id("feedback"),
        trace_id=adapter_result.trace_id,
        execution_request_id=adapter_result.execution_request_id,
        adapter_result_id=adapter_result.id,
        status="SIMULATED_FEEDBACK_RECEIVED",
        physical_command_status=PhysicalCommandStatus.NEVER_CREATED,
        reason="Simulated feedback closes the mock external boundary loop.",
    )

