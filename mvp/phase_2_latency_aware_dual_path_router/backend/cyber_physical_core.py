from .adapter_mock import AdapterMock
from .execution_request import create_execution_request
from .feedback import create_feedback
from .schemas import AdapterResult, ApprovedAction, ExecutionRequest, FeedbackEvent, SafetyGatePass


class CyberPhysicalCore:
    def __init__(self, adapter=None) -> None:
        self.adapter = adapter or AdapterMock()

    def execute(self, approved_action: ApprovedAction, safety_pass: SafetyGatePass) -> tuple[ExecutionRequest, AdapterResult, FeedbackEvent]:
        request = create_execution_request(approved_action, safety_pass)
        adapter_result = self.adapter.dispatch(request)
        feedback = create_feedback(adapter_result)
        return request, adapter_result, feedback
