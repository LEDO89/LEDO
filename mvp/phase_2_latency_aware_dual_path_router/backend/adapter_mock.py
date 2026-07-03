from .schemas import AdapterResult, ExecutionRequest, PhysicalCommandStatus, new_id


class AdapterMock:
    def dispatch(self, request: ExecutionRequest) -> AdapterResult:
        return AdapterResult(
            id=new_id("adapter_result"),
            trace_id=request.trace_id,
            execution_request_id=request.id,
            adapter_id="adapter.mock.external-boundary",
            accepted=True,
            status="SIMULATED_ACCEPTED",
            physical_command_status=PhysicalCommandStatus.NEVER_CREATED,
            reason="Mock adapter accepted bounded request and did not create a PhysicalCommand.",
        )

