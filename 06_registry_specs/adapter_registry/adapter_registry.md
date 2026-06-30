**Adapter registry** 

**1\. Overview**

`adapter_registry` is a core runtime module in the LEDO Ontology-Centric Cyber-Physical System. Its role is to determine and manage which external control system adapter should receive an approved execution request, such as an `ApprovedAction` or `ExecutionRequest`.

This module does not directly execute commands that have passed the Safety Gate. Instead, it is responsible for the following:

1. Managing the list of registered external system adapters  
2. Validating adapter capability, protocol, target type, and site scope  
3. Selecting an adapter compatible with the approved action  
4. Checking adapter health status  
5. Validating version, permission, and safety boundaries  
6. Returning a safe adapter reference for the Execution Dispatcher

In other words, `adapter_registry` is not a simple dynamic address book in the execution layer. It is a **safe routing kernel that deterministically selects verified external control interfaces**.

---

## **2\. Position in the System**

`adapter_registry` is located in the following section of the overall LEDO architecture:

Approved Action / Safety Gate Layer

        ↓

Unified Cyber-Physical Core Layer

        ↓

Execution Request & External Control Integration Layer

        ↓

adapter\_registry

        ↓

Fleet Manager Adapter / Robot Middleware Adapter / PLC Adapter / SCADA Adapter / BIM Adapter / Site Platform Adapter

The Safety Gate answers the question:

Is this action safe to execute?

`adapter_registry` answers the question:

Through which external system adapter should this action be delivered?

---

## **3\. Core Purpose**

The purpose of `adapter_registry` is not simple Python dictionary management.

Its core purpose is the following:

ApprovedAction → ExecutionRequest → Compatible Adapter Resolution

In other words, it safely connects an approved action based on the following criteria:

| Criterion | Description |
| ----- | ----- |
| action\_type | STOP\_WORK, DISPATCH\_ROBOT, LOCK\_ZONE, REQUEST\_INSPECTION, etc. |
| target\_type | worker, robot, equipment, zone, sensor, fleet, plc, etc. |
| protocol | REST, gRPC, MQTT, OPC-UA, ROS2, Modbus, Kafka, etc. |
| capability | Functions the adapter can perform |
| site\_scope | Scope of applicable sites, zones, or equipment groups |
| risk\_level | routine, warning, high\_risk, emergency |
| health\_status | Whether the adapter is currently available |
| version | Compatible adapter contract version |
| authority | Whether the adapter is authorized to receive the action |

---

## **4\. Design Principles**

### **4.1 The LLM Must Not Directly Select the Adapter**

Adapter selection in `adapter_registry` must not be based on LLM judgment. It must be based on **explicit capability contracts and policy rules**.

The LLM may only participate up to the following stage:

Natural language situation interpretation → Action Candidate generation

However, actual adapter selection must be determined by the following:

Ontology Action Contract

Policy Rule

Capability Matrix

Adapter Metadata

Health Check

Safety Boundary

---

### **4.2 The Registry Is a Selector, Not an Executor**

`adapter_registry` does not send actual commands.

adapter\_registry.select\_adapter(request)

This returns only an adapter object or adapter reference.

Actual execution must be handled by a separate module.

ExecutionDispatcher.dispatch(adapter, execution\_request)

This separation makes execution responsibility, audit responsibility, and failure recovery responsibility clear.

---

### **4.3 Dynamic Registration Must Be Restricted**

In construction, industrial, and robotics safety systems, arbitrary adapters must not be registered at runtime without control.

Therefore, adapter registration must satisfy the following conditions:

1. Schema validation  
2. Capability contract validation  
3. Protocol whitelist validation  
4. Site authorization validation  
5. Version compatibility validation  
6. Security credential validation  
7. Administrator approval or deployment pipeline approval

Even when hot reload is required during operation, it is safer not to apply new adapters directly to the active state. The following structure is recommended:

candidate registry

        ↓ validation

shadow registry

        ↓ approval

active registry

---

## **5\. Core Responsibilities of adapter\_registry**

### **5.1 Adapter Registration**

External system adapters are registered in the registry.

Example adapters include:

RobotFleetAdapter

SCADAAdapter

PLCAdapter

MQTTEquipmentAdapter

ROS2RobotAdapter

BIMSyncAdapter

InspectionPlatformAdapter

NotificationAdapter

Each adapter should have the following metadata:

adapter\_id

adapter\_name

adapter\_type

supported\_action\_types

supported\_target\_types

supported\_protocols

capabilities

site\_scope

risk\_limit

contract\_version

health\_status

security\_profile

---

### **5.2 Adapter Lookup**

When an `ExecutionRequest` is received, the registry finds compatible adapter candidates.

Example:

ExecutionRequest:

    action\_type \= DISPATCH\_ROBOT

    target\_type \= robot

    protocol\_preference \= REST

    site\_id \= site\_A

    zone\_id \= zone\_12

The registry finds an adapter that satisfies the following conditions:

adapter.supports\_action(DISPATCH\_ROBOT)

adapter.supports\_target(robot)

adapter.site\_scope includes site\_A / zone\_12

adapter.health\_status \== HEALTHY

adapter.contract\_version compatible

adapter.risk\_limit \>= request.risk\_level

---

### **5.3 Capability Validation**

It is not enough for an adapter to simply exist.

For example, even if `RobotFleetAdapter` is registered, a command must not be sent to it unless it has the required capabilities.

Example required capabilities:

DISPATCH\_ROBOT

REPLAN\_ROUTE

PAUSE\_MISSION

RETURN\_TO\_BASE

EMERGENCY\_STOP

Therefore, the registry must validate action compatibility based on the adapter’s capability matrix.

---

### **5.4 Health Status Management**

`adapter_registry` must track the status of each adapter.

Example health statuses:

HEALTHY

DEGRADED

UNAVAILABLE

MAINTENANCE

DISABLED

UNKNOWN

Safety-critical actions should only be delivered to adapters whose status is `HEALTHY`.

However, for emergency actions, a fallback adapter may be used according to a separate emergency policy if the primary adapter fails.

---

### **5.5 Fallback Adapter Selection**

In industrial sites, adapter failure can directly lead to execution failure.

Therefore, the registry may have a fallback policy.

Example:

Primary: RobotFleetAdapter

Fallback 1: ROS2DirectAdapter

Fallback 2: ManualOperatorNotificationAdapter

Fallback 3: EmergencyStopRelayAdapter

However, fallback must not be automatically applied without control.

Especially in physical equipment control, a fallback adapter may have different safety properties. Therefore, policy and safety boundary validation must be performed again before using a fallback adapter.

---

## **6\. Core Data Models**

### **6.1 AdapterType**

from enum import Enum

class AdapterType(str, Enum):

    ROBOT\_FLEET \= "robot\_fleet"

    ROBOT\_MIDDLEWARE \= "robot\_middleware"

    PLC \= "plc"

    SCADA \= "scada"

    MQTT\_DEVICE \= "mqtt\_device"

    OPC\_UA \= "opc\_ua"

    BIM \= "bim"

    NOTIFICATION \= "notification"

    INSPECTION\_PLATFORM \= "inspection\_platform"

    SITE\_PLATFORM \= "site\_platform"

---

### **6.2 AdapterHealthStatus**

class AdapterHealthStatus(str, Enum):

    HEALTHY \= "healthy"

    DEGRADED \= "degraded"

    UNAVAILABLE \= "unavailable"

    MAINTENANCE \= "maintenance"

    DISABLED \= "disabled"

    UNKNOWN \= "unknown"

---

### **6.3 AdapterMetadata**

from pydantic import BaseModel, Field

from typing import Optional

class AdapterMetadata(BaseModel):

    adapter\_id: str

    adapter\_name: str

    adapter\_type: AdapterType

    supported\_action\_types: list\[str\] \= Field(default\_factory=list)

    supported\_target\_types: list\[str\] \= Field(default\_factory=list)

    supported\_protocols: list\[str\] \= Field(default\_factory=list)

    capabilities: list\[str\] \= Field(default\_factory=list)

    site\_scope: list\[str\] \= Field(default\_factory=list)

    zone\_scope: list\[str\] \= Field(default\_factory=list)

    max\_risk\_level: str \= "routine"

    contract\_version: str \= "1.0.0"

    health\_status: AdapterHealthStatus \= AdapterHealthStatus.UNKNOWN

    is\_enabled: bool \= True

    security\_profile: Optional\[str\] \= None

    description: Optional\[str\] \= None

---

### **6.4 AdapterRegistration**

class AdapterRegistration(BaseModel):

    metadata: AdapterMetadata

    adapter\_instance: object

In actual implementation, it is better to use an abstract interface instead of `object`.

class BaseAdapter(ABC):

    @abstractmethod

    async def health\_check(self) \-\> AdapterHealthStatus:

        pass

    @abstractmethod

    async def execute(self, request: ExecutionRequest) \-\> ExecutionResult:

        pass

---

## **7\. adapter\_registry Interface**

### **7.1 Basic Responsibilities**

class AdapterRegistry:

    def register(self, adapter: BaseAdapter, metadata: AdapterMetadata) \-\> None:

        ...

    def unregister(self, adapter\_id: str) \-\> None:

        ...

    def get(self, adapter\_id: str) \-\> BaseAdapter:

        ...

    def list\_adapters(self) \-\> list\[AdapterMetadata\]:

        ...

    def find\_candidates(self, request: ExecutionRequest) \-\> list\[BaseAdapter\]:

        ...

    def select\_adapter(self, request: ExecutionRequest) \-\> BaseAdapter:

        ...

    def update\_health(self, adapter\_id: str, status: AdapterHealthStatus) \-\> None:

        ...

---

### **7.2 Core Selection Flow**

ExecutionRequest input

        ↓

Check action\_type

        ↓

Check target\_type

        ↓

Check site\_scope / zone\_scope

        ↓

Check capability

        ↓

Check protocol compatibility

        ↓

Check contract\_version

        ↓

Check health\_status

        ↓

Check policy guard

        ↓

Select adapter

        ↓

Return to ExecutionDispatcher

---

## **8\. Selection Algorithm**

### **8.1 Basic Filtering**

def find\_candidates(self, request: ExecutionRequest) \-\> list\[AdapterRegistration\]:

    candidates \= \[\]

    for registration in self.\_adapters.values():

        metadata \= registration.metadata

        if not metadata.is\_enabled:

            continue

        if metadata.health\_status \!= AdapterHealthStatus.HEALTHY:

            continue

        if request.action\_type not in metadata.supported\_action\_types:

            continue

        if request.target\_type not in metadata.supported\_target\_types:

            continue

        if request.site\_id not in metadata.site\_scope:

            continue

        if request.required\_capability not in metadata.capabilities:

            continue

        candidates.append(registration)

    return candidates

---

### **8.2 Priority-Based Selection**

If multiple candidates exist, selection may be based on the following criteria:

1. Exact site match  
2. Exact zone match  
3. Protocol preference match  
4. Higher reliability score  
5. Lower latency  
6. Lower recent failure count  
7. Newer compatible version  
8. Explicit priority weight

Example:

def select\_adapter(self, request: ExecutionRequest) \-\> BaseAdapter:

    candidates \= self.find\_candidates(request)

    if not candidates:

        raise AdapterNotFoundError(

            f"No compatible adapter found for action={request.action\_type}, "

            f"target={request.target\_type}, site={request.site\_id}"

        )

    ranked \= sorted(

        candidates,

        key=lambda item: (

            item.metadata.health\_status \== AdapterHealthStatus.HEALTHY,

            request.preferred\_protocol in item.metadata.supported\_protocols,

            request.zone\_id in item.metadata.zone\_scope,

        ),

        reverse=True,

    )

    return ranked\[0\].adapter\_instance

---

## **9\. Relationship with the Safety Gate**

`adapter_registry` does not replace the Safety Gate.

The role of the Safety Gate is:

Is this action safe to execute?

The role of `adapter_registry` is:

To which verified external system should this action be delivered?

Therefore, the following structure must be maintained:

Action Candidate

        ↓

Policy Validation

        ↓

Safety Gate

        ↓

Approved Action

        ↓

Execution Request Builder

        ↓

adapter\_registry

        ↓

Execution Dispatcher

        ↓

External Adapter

The important principle is:

adapter\_registry must not be called for execution before the Safety Gate.

However, it may be used in read-only mode for capability planning or dry-run validation.

---

## **10\. Connection with the Ontology**

`adapter_registry` should be strongly connected to the ontology.

For example, the following relationships may be defined in the ontology:

RobotFleetAdapter

    hasCapability DispatchRobot

    hasCapability StopRobot

    supportsTarget Robot

    usesProtocol REST

    controlsSystem RobotFleetManager

The same structure may be represented as RDF triples:

ledo:RobotFleetAdapter\_A

    rdf:type ledo:RobotFleetAdapter ;

    ledo:hasCapability ledo:DispatchRobot ;

    ledo:hasCapability ledo:EmergencyStop ;

    ledo:supportsTarget ledo:Robot ;

    ledo:usesProtocol ledo:REST ;

    ledo:hasSiteScope ledo:Site\_A .

With this structure, `adapter_registry` becomes not merely a code configuration file, but a runtime projection of an ontology-defined execution interface.

---

## **11\. Configuration Example**

In the early stage, adapters may be managed through YAML or JSON configuration.

adapters:

  \- adapter\_id: robot\_fleet\_main

    adapter\_name: Main Robot Fleet Adapter

    adapter\_type: robot\_fleet

    supported\_action\_types:

      \- DISPATCH\_ROBOT

      \- REPLAN\_ROUTE

      \- PAUSE\_MISSION

      \- RETURN\_TO\_BASE

    supported\_target\_types:

      \- robot

      \- robot\_fleet

    supported\_protocols:

      \- REST

      \- gRPC

    capabilities:

      \- dispatch\_robot

      \- replan\_route

      \- pause\_mission

      \- return\_to\_base

    site\_scope:

      \- site\_A

    zone\_scope:

      \- zone\_01

      \- zone\_02

      \- zone\_03

    max\_risk\_level: high\_risk

    contract\_version: 1.0.0

    is\_enabled: true

    security\_profile: robot\_fleet\_service\_account

In the operation stage, this configuration may be integrated with the following storage systems:

PostgreSQL: adapter metadata, version, audit

Redis: live health status, runtime cache

Ontology Store: semantic capability definition

Vault: credentials, tokens, certificates

Audit Store: registration/change history

---

## **12\. Failure Scenarios**

### **12.1 Adapter Not Found**

An ApprovedAction exists, but no compatible adapter is available.

Response:

ExecutionRejected

Reason: ADAPTER\_NOT\_FOUND

Audit record

Supervisor notification

Fallback policy check

---

### **12.2 Adapter Unhealthy**

The adapter is registered, but health\_status \= UNAVAILABLE.

Response:

Exclude primary adapter

Search fallback adapter

Hold execution if no fallback exists

---

### **12.3 Capability Mismatch**

A DISPATCH\_ROBOT request is received, but the adapter only supports PAUSE\_MISSION.

Response:

Raise CapabilityMismatchError

Reject ExecutionRequest

Record ontology/registry configuration mismatch in audit log

---

### **12.4 Version Mismatch**

ExecutionRequest contract\_version \= 2.0

Adapter contract\_version \= 1.0

Response:

Raise VersionCompatibilityError

Check migration adapter or compatibility layer

---

### **12.5 Site Scope Violation**

A Site\_B command is sent to an adapter dedicated to Site\_A.

Response:

Raise ScopeViolationError

Record security audit event

This case must be treated not as a simple error, but as a security event.

---

## **13\. Audit Logging**

`adapter_registry` must record all important events in the audit log.

Events to record:

ADAPTER\_REGISTERED

ADAPTER\_UNREGISTERED

ADAPTER\_ENABLED

ADAPTER\_DISABLED

ADAPTER\_HEALTH\_CHANGED

ADAPTER\_SELECTED

ADAPTER\_SELECTION\_FAILED

ADAPTER\_CAPABILITY\_MISMATCH

ADAPTER\_SCOPE\_VIOLATION

ADAPTER\_VERSION\_MISMATCH

Example audit record:

{

  "event\_type": "ADAPTER\_SELECTED",

  "adapter\_id": "robot\_fleet\_main",

  "action\_type": "DISPATCH\_ROBOT",

  "target\_type": "robot",

  "site\_id": "site\_A",

  "zone\_id": "zone\_02",

  "execution\_request\_id": "exec\_req\_123",

  "timestamp": "2026-06-26T09:00:00Z"

}

---

## **14\. Security Design**

`adapter_registry` is security-critical because it manages connections to external systems.

Essential security principles:

1. Adapter registration must be allowed only by administrators or deployment pipelines.  
2. Arbitrary adapter injection at runtime must be prohibited.  
3. Credentials must not be stored directly in the registry. Only references to Vault or Secret Manager should be stored.  
4. Authority scope must be limited per adapter.  
5. Site, zone, and action scope validation must be mandatory.  
6. mTLS or signed requests should be used.  
7. Adapter selection failures must also be recorded in the audit log.  
8. Emergency actions must use a separate adapter whitelist.

---

## **15\. Recommended File Structure**

execution\_integration/

    adapters/

        base\_adapter.py

        robot\_fleet\_adapter.py

        ros2\_adapter.py

        plc\_adapter.py

        scada\_adapter.py

        notification\_adapter.py

    registry/

        adapter\_registry.py

        adapter\_metadata.py

        adapter\_selector.py

        adapter\_health.py

        adapter\_errors.py

    schemas/

        execution\_request.py

        execution\_result.py

        adapter\_contract.py

    policies/

        adapter\_policy.py

        fallback\_policy.py

    tests/

        test\_adapter\_registry.py

        test\_adapter\_selection.py

        test\_adapter\_scope.py

        test\_adapter\_health.py

---

## **16\. Minimal Implementation Example**

class AdapterRegistry:

    def \_\_init\_\_(self) \-\> None:

        self.\_adapters: dict\[str, AdapterRegistration\] \= {}

    def register(self, adapter: BaseAdapter, metadata: AdapterMetadata) \-\> None:

        if metadata.adapter\_id in self.\_adapters:

            raise AdapterAlreadyRegisteredError(metadata.adapter\_id)

        self.\_validate\_metadata(metadata)

        self.\_adapters\[metadata.adapter\_id\] \= AdapterRegistration(

            metadata=metadata,

            adapter\_instance=adapter,

        )

    def unregister(self, adapter\_id: str) \-\> None:

        if adapter\_id not in self.\_adapters:

            raise AdapterNotFoundError(adapter\_id)

        del self.\_adapters\[adapter\_id\]

    def get(self, adapter\_id: str) \-\> BaseAdapter:

        registration \= self.\_adapters.get(adapter\_id)

        if registration is None:

            raise AdapterNotFoundError(adapter\_id)

        return registration.adapter\_instance

    def find\_candidates(self, request: ExecutionRequest) \-\> list\[AdapterRegistration\]:

        candidates: list\[AdapterRegistration\] \= \[\]

        for registration in self.\_adapters.values():

            metadata \= registration.metadata

            if not self.\_is\_compatible(metadata, request):

                continue

            candidates.append(registration)

        return candidates

    def select\_adapter(self, request: ExecutionRequest) \-\> BaseAdapter:

        candidates \= self.find\_candidates(request)

        if not candidates:

            raise AdapterNotFoundError(

                f"No adapter found for action={request.action\_type}, "

                f"target={request.target\_type}, site={request.site\_id}"

            )

        selected \= self.\_rank\_candidates(candidates, request)\[0\]

        return selected.adapter\_instance

    def update\_health(

        self,

        adapter\_id: str,

        status: AdapterHealthStatus,

    ) \-\> None:

        registration \= self.\_adapters.get(adapter\_id)

        if registration is None:

            raise AdapterNotFoundError(adapter\_id)

        registration.metadata.health\_status \= status

    def \_is\_compatible(

        self,

        metadata: AdapterMetadata,

        request: ExecutionRequest,

    ) \-\> bool:

        if not metadata.is\_enabled:

            return False

        if metadata.health\_status \!= AdapterHealthStatus.HEALTHY:

            return False

        if request.action\_type not in metadata.supported\_action\_types:

            return False

        if request.target\_type not in metadata.supported\_target\_types:

            return False

        if request.site\_id not in metadata.site\_scope:

            return False

        if request.required\_capability not in metadata.capabilities:

            return False

        return True

    def \_rank\_candidates(

        self,

        candidates: list\[AdapterRegistration\],

        request: ExecutionRequest,

    ) \-\> list\[AdapterRegistration\]:

        return sorted(

            candidates,

            key=lambda registration: (

                request.preferred\_protocol in registration.metadata.supported\_protocols,

                request.zone\_id in registration.metadata.zone\_scope,

            ),

            reverse=True,

        )

    def \_validate\_metadata(self, metadata: AdapterMetadata) \-\> None:

        if not metadata.supported\_action\_types:

            raise InvalidAdapterMetadataError("supported\_action\_types is required")

        if not metadata.supported\_target\_types:

            raise InvalidAdapterMetadataError("supported\_target\_types is required")

        if not metadata.capabilities:

            raise InvalidAdapterMetadataError("capabilities is required")

---

## **17\. Test Scenarios**

The following tests are required.

### **17.1 Normal Selection**

Verify that RobotFleetAdapter is selected when a DISPATCH\_ROBOT request is received.

### **17.2 Excluding Disabled Adapters**

Verify that an adapter with is\_enabled \= false is excluded from candidates.

### **17.3 Excluding Unhealthy Adapters**

Verify that an adapter with health\_status \= UNAVAILABLE is not selected.

### **17.4 Capability Mismatch**

Verify that an adapter that does not support the requested capability is excluded.

### **17.5 Site Scope Mismatch**

Verify that an adapter for another site is not selected.

### **17.6 Fallback Selection**

Verify that a fallback adapter is selected when the primary adapter fails.

### **17.7 Audit Logging**

Verify that successful and failed adapter selection events are recorded in the audit log.

---

## **18\. Expansion Roadmap**

The initial version can start as an in-memory registry.

Phase 1: In-memory registry

Phase 2: YAML/JSON config loading

Phase 3: PostgreSQL metadata persistence

Phase 4: Redis health cache

Phase 5: Ontology capability sync

Phase 6: Shadow/Active registry version switching

Phase 7: Multi-site distributed adapter registry

---

## **19\. Conclusion**

`adapter_registry` is a highly important safety module in the LEDO execution layer.

This module is not simply code that stores adapter objects. It is an **execution routing registry that deterministically controls the final connection point between approved actions and external physical control systems**.

The core principles are as follows:

1\. Execution adapters are selected only after the Safety Gate.

2\. The LLM must not directly select adapters.

3\. Selection is based on capability contracts.

4\. Site, zone, and action scope must be validated.

5\. Selection is based on health status.

6\. Fallback is restricted by policy.

7\. All selections and failures must be recorded in the audit log.

8\. External system credentials must not be stored directly in the registry.

9\. Ontology-defined capabilities must be connected with registry runtime metadata.

10\. Execution is handled by the dispatcher; the registry only selects.

Therefore, `adapter_registry` plays the following role in the LEDO system:

Ontology-defined Action

        ↓

Safety-approved Execution Request

        ↓

Deterministic Adapter Resolution

        ↓

External Cyber-Physical System Integration

By maintaining this structure, LEDO can safely separate LLM-based intent generation from real physical control systems while still connecting various robots, equipment, sensors, SCADA systems, PLCs, and site platforms in an extensible way.

# 

# **adapter\_registry** 

# **1\. 개요**

`adapter_registry`는 LEDO Ontology-Centric Cyber-Physical System에서 **승인된 실행 요청(Approved Action / Execution Request)을 어떤 외부 제어 시스템 어댑터로 보낼지 결정하고 관리하는 핵심 런타임 모듈**이다.

이 모듈은 Safety Gate를 통과한 명령을 직접 실행하지 않는다. 대신 다음을 담당한다.

1. 등록된 외부 시스템 어댑터 목록 관리  
2. 어댑터의 capability, protocol, target type, site scope 검증  
3. Approved Action과 호환되는 adapter 선택  
4. adapter health 상태 확인  
5. version, permission, safety boundary 검증  
6. Execution Dispatcher가 사용할 수 있는 안전한 adapter reference 반환

즉, `adapter_registry`는 실행 계층의 “동적 주소록”이 아니라, **검증된 외부 제어 인터페이스를 결정론적으로 선택하는 안전한 라우팅 커널**이다.

---

## **2\. 시스템 내 위치**

`adapter_registry`는 전체 LEDO 아키텍처에서 다음 구간에 위치한다.

Approved Action / Safety Gate Layer  
        ↓  
Unified Cyber-Physical Core Layer  
        ↓  
Execution Request & External Control Integration Layer  
        ↓  
adapter\_registry  
        ↓  
Fleet Manager Adapter / Robot Middleware Adapter / PLC Adapter / SCADA Adapter / BIM Adapter / Site Platform Adapter

Safety Gate가 “이 Action은 실행해도 된다”를 판단한다면, `adapter_registry`는 “이 Action을 어떤 외부 시스템 어댑터를 통해 전달해야 하는가”를 판단한다.

---

## **3\. 핵심 목적**

`adapter_registry`의 목적은 단순한 Python dictionary 관리가 아니다.

핵심 목적은 다음과 같다.

ApprovedAction → ExecutionRequest → Compatible Adapter Resolution

즉, 승인된 액션을 다음 기준으로 안전하게 연결한다.

| 기준 | 설명 |
| ----- | ----- |
| action\_type | STOP\_WORK, DISPATCH\_ROBOT, LOCK\_ZONE, REQUEST\_INSPECTION 등 |
| target\_type | worker, robot, equipment, zone, sensor, fleet, plc 등 |
| protocol | REST, gRPC, MQTT, OPC-UA, ROS2, Modbus, Kafka 등 |
| capability | adapter가 수행 가능한 기능 |
| site\_scope | 특정 현장, 구역, 장비군에 대한 적용 범위 |
| risk\_level | routine, warning, high\_risk, emergency |
| health\_status | adapter가 현재 사용 가능한 상태인지 |
| version | 호환 가능한 adapter contract version |
| authority | 해당 adapter가 해당 action을 받을 권한이 있는지 |

---

## **4\. 설계 원칙**

### **4.1 LLM이 adapter를 직접 선택하지 않는다**

`adapter_registry`의 adapter 선택은 LLM 판단이 아니라, **명시적 capability contract와 policy rule 기반**이어야 한다.

LLM은 다음까지만 관여할 수 있다.

자연어 상황 해석 → Action Candidate 생성

하지만 실제 adapter 선택은 다음 기준으로 결정되어야 한다.

Ontology Action Contract  
Policy Rule  
Capability Matrix  
Adapter Metadata  
Health Check  
Safety Boundary

---

### **4.2 Registry는 실행자가 아니라 선택자다**

`adapter_registry`는 실제 명령을 보내지 않는다.

adapter\_registry.select\_adapter(request)

는 adapter 객체나 adapter reference를 반환할 뿐이다.

실제 실행은 별도 모듈이 담당한다.

ExecutionDispatcher.dispatch(adapter, execution\_request)

이렇게 분리해야 실행 책임, 감사 책임, 장애 복구 책임이 명확해진다.

---

### **4.3 동적 등록은 제한적으로 허용한다**

건설/산업/로봇 안전 시스템에서는 아무 adapter나 런타임에 등록되면 안 된다.

따라서 adapter 등록은 다음 조건을 만족해야 한다.

1. schema 검증 통과  
2. capability contract 검증  
3. protocol whitelist 통과  
4. site authorization 통과  
5. version compatibility 통과  
6. security credential 검증  
7. 관리자 승인 또는 배포 파이프라인 승인

운영 중 hot reload가 필요하더라도 즉시 active 상태로 반영하지 않고 다음 구조를 사용하는 것이 안전하다.

candidate registry  
        ↓ 검증  
shadow registry  
        ↓ 승인  
active registry

---

## **5\. adapter\_registry의 핵심 책임**

### **5.1 Adapter 등록**

외부 시스템 어댑터를 registry에 등록한다.

예시 adapter:

RobotFleetAdapter  
SCADAAdapter  
PLCAdapter  
MQTTEquipmentAdapter  
ROS2RobotAdapter  
BIMSyncAdapter  
InspectionPlatformAdapter  
NotificationAdapter

각 adapter는 다음 metadata를 가져야 한다.

adapter\_id  
adapter\_name  
adapter\_type  
supported\_action\_types  
supported\_target\_types  
supported\_protocols  
capabilities  
site\_scope  
risk\_limit  
contract\_version  
health\_status  
security\_profile

---

### **5.2 Adapter 조회**

Execution Request가 들어오면 registry는 호환 가능한 adapter 후보를 찾는다.

예시:

ExecutionRequest:  
    action\_type \= DISPATCH\_ROBOT  
    target\_type \= robot  
    protocol\_preference \= REST  
    site\_id \= site\_A  
    zone\_id \= zone\_12

Registry는 다음 조건을 만족하는 adapter를 찾는다.

adapter.supports\_action(DISPATCH\_ROBOT)  
adapter.supports\_target(robot)  
adapter.site\_scope includes site\_A / zone\_12  
adapter.health\_status \== HEALTHY  
adapter.contract\_version compatible  
adapter.risk\_limit \>= request.risk\_level

---

### **5.3 Capability 검증**

adapter가 단순히 존재하는 것만으로는 부족하다.

예를 들어 `RobotFleetAdapter`가 등록되어 있어도 다음 capability가 없으면 명령을 보내면 안 된다.

DISPATCH\_ROBOT  
REPLAN\_ROUTE  
PAUSE\_MISSION  
RETURN\_TO\_BASE  
EMERGENCY\_STOP

따라서 registry는 adapter의 capability matrix를 기준으로 action compatibility를 검증해야 한다.

---

### **5.4 Health 상태 관리**

adapter\_registry는 각 adapter의 상태를 추적해야 한다.

예시 health status:

HEALTHY  
DEGRADED  
UNAVAILABLE  
MAINTENANCE  
DISABLED  
UNKNOWN

Safety-critical action은 `HEALTHY` 상태의 adapter에만 전달되어야 한다.

단, emergency action은 별도 정책에 따라 primary adapter가 실패하면 fallback adapter를 사용할 수 있다.

---

### **5.5 Fallback Adapter 선택**

산업 현장에서는 adapter 장애가 곧 실행 실패로 이어질 수 있다.

따라서 registry는 fallback policy를 가질 수 있다.

예시:

Primary: RobotFleetAdapter  
Fallback 1: ROS2DirectAdapter  
Fallback 2: ManualOperatorNotificationAdapter  
Fallback 3: EmergencyStopRelayAdapter

하지만 fallback은 무조건 자동으로 하면 안 된다.

특히 물리 장비 제어는 fallback adapter가 다른 안전 특성을 가질 수 있기 때문에 반드시 policy와 safety boundary 검증을 다시 수행해야 한다.

---

## **6\. 핵심 데이터 모델**

### **6.1 AdapterType**

from enum import Enum

class AdapterType(str, Enum):  
    ROBOT\_FLEET \= "robot\_fleet"  
    ROBOT\_MIDDLEWARE \= "robot\_middleware"  
    PLC \= "plc"  
    SCADA \= "scada"  
    MQTT\_DEVICE \= "mqtt\_device"  
    OPC\_UA \= "opc\_ua"  
    BIM \= "bim"  
    NOTIFICATION \= "notification"  
    INSPECTION\_PLATFORM \= "inspection\_platform"  
    SITE\_PLATFORM \= "site\_platform"

---

### **6.2 AdapterHealthStatus**

class AdapterHealthStatus(str, Enum):  
    HEALTHY \= "healthy"  
    DEGRADED \= "degraded"  
    UNAVAILABLE \= "unavailable"  
    MAINTENANCE \= "maintenance"  
    DISABLED \= "disabled"  
    UNKNOWN \= "unknown"

---

### **6.3 AdapterMetadata**

from pydantic import BaseModel, Field  
from typing import Optional

class AdapterMetadata(BaseModel):  
    adapter\_id: str  
    adapter\_name: str  
    adapter\_type: AdapterType

    supported\_action\_types: list\[str\] \= Field(default\_factory=list)  
    supported\_target\_types: list\[str\] \= Field(default\_factory=list)  
    supported\_protocols: list\[str\] \= Field(default\_factory=list)  
    capabilities: list\[str\] \= Field(default\_factory=list)

    site\_scope: list\[str\] \= Field(default\_factory=list)  
    zone\_scope: list\[str\] \= Field(default\_factory=list)

    max\_risk\_level: str \= "routine"  
    contract\_version: str \= "1.0.0"

    health\_status: AdapterHealthStatus \= AdapterHealthStatus.UNKNOWN  
    is\_enabled: bool \= True

    security\_profile: Optional\[str\] \= None  
    description: Optional\[str\] \= None

---

### **6.4 AdapterRegistration**

class AdapterRegistration(BaseModel):  
    metadata: AdapterMetadata  
    adapter\_instance: object

실제 구현에서는 `object`보다 추상 인터페이스를 두는 것이 좋다.

class BaseAdapter(ABC):  
    @abstractmethod  
    async def health\_check(self) \-\> AdapterHealthStatus:  
        pass

    @abstractmethod  
    async def execute(self, request: ExecutionRequest) \-\> ExecutionResult:  
        pass

---

## **7\. adapter\_registry 인터페이스**

### **7.1 기본 책임**

class AdapterRegistry:  
    def register(self, adapter: BaseAdapter, metadata: AdapterMetadata) \-\> None:  
        ...

    def unregister(self, adapter\_id: str) \-\> None:  
        ...

    def get(self, adapter\_id: str) \-\> BaseAdapter:  
        ...

    def list\_adapters(self) \-\> list\[AdapterMetadata\]:  
        ...

    def find\_candidates(self, request: ExecutionRequest) \-\> list\[BaseAdapter\]:  
        ...

    def select\_adapter(self, request: ExecutionRequest) \-\> BaseAdapter:  
        ...

    def update\_health(self, adapter\_id: str, status: AdapterHealthStatus) \-\> None:  
        ...

---

### **7.2 핵심 선택 흐름**

ExecutionRequest 입력  
        ↓  
action\_type 확인  
        ↓  
target\_type 확인  
        ↓  
site\_scope / zone\_scope 확인  
        ↓  
capability 확인  
        ↓  
protocol compatibility 확인  
        ↓  
contract\_version 확인  
        ↓  
health\_status 확인  
        ↓  
policy guard 확인  
        ↓  
adapter 선택  
        ↓  
ExecutionDispatcher로 반환

---

## **8\. 선택 알고리즘**

### **8.1 기본 필터링**

def find\_candidates(self, request: ExecutionRequest) \-\> list\[AdapterRegistration\]:  
    candidates \= \[\]

    for registration in self.\_adapters.values():  
        metadata \= registration.metadata

        if not metadata.is\_enabled:  
            continue

        if metadata.health\_status \!= AdapterHealthStatus.HEALTHY:  
            continue

        if request.action\_type not in metadata.supported\_action\_types:  
            continue

        if request.target\_type not in metadata.supported\_target\_types:  
            continue

        if request.site\_id not in metadata.site\_scope:  
            continue

        if request.required\_capability not in metadata.capabilities:  
            continue

        candidates.append(registration)

    return candidates

---

### **8.2 우선순위 선택**

후보가 여러 개인 경우 다음 기준으로 선택할 수 있다.

1. exact site match  
2. exact zone match  
3. protocol preference match  
4. higher reliability score  
5. lower latency  
6. lower recent failure count  
7. newer compatible version  
8. explicit priority weight

예시:

def select\_adapter(self, request: ExecutionRequest) \-\> BaseAdapter:  
    candidates \= self.find\_candidates(request)

    if not candidates:  
        raise AdapterNotFoundError(  
            f"No compatible adapter found for action={request.action\_type}, "  
            f"target={request.target\_type}, site={request.site\_id}"  
        )

    ranked \= sorted(  
        candidates,  
        key=lambda item: (  
            item.metadata.health\_status \== AdapterHealthStatus.HEALTHY,  
            request.preferred\_protocol in item.metadata.supported\_protocols,  
            request.zone\_id in item.metadata.zone\_scope,  
        ),  
        reverse=True,  
    )

    return ranked\[0\].adapter\_instance

---

## **9\. Safety Gate와의 관계**

`adapter_registry`는 Safety Gate를 대체하지 않는다.

Safety Gate의 역할:

이 Action이 실행되어도 안전한가?

adapter\_registry의 역할:

이 Action을 어떤 검증된 외부 시스템으로 전달해야 하는가?

따라서 다음 구조를 유지해야 한다.

Action Candidate  
        ↓  
Policy Validation  
        ↓  
Safety Gate  
        ↓  
Approved Action  
        ↓  
Execution Request Builder  
        ↓  
adapter\_registry  
        ↓  
Execution Dispatcher  
        ↓  
External Adapter

중요한 원칙은 다음과 같다.

adapter\_registry는 Safety Gate 이전에 호출되면 안 된다.

단, 사전 capability planning이나 dry-run 검증에서는 읽기 전용으로 사용할 수 있다.

---

## **10\. Ontology와의 연결**

adapter\_registry는 ontology와 강하게 연결되어야 한다.

예를 들어 ontology에는 다음 관계가 정의될 수 있다.

RobotFleetAdapter  
    hasCapability DispatchRobot  
    hasCapability StopRobot  
    supportsTarget Robot  
    usesProtocol REST  
    controlsSystem RobotFleetManager

또는 RDF triple로 표현하면 다음과 같다.

ledo:RobotFleetAdapter\_A  
    rdf:type ledo:RobotFleetAdapter ;  
    ledo:hasCapability ledo:DispatchRobot ;  
    ledo:hasCapability ledo:EmergencyStop ;  
    ledo:supportsTarget ledo:Robot ;  
    ledo:usesProtocol ledo:REST ;  
    ledo:hasSiteScope ledo:Site\_A .

이렇게 하면 adapter\_registry는 단순 코드 설정 파일이 아니라, ontology-defined execution interface의 런타임 projection이 된다.

---

## **11\. Configuration 예시**

초기에는 YAML 또는 JSON 설정으로 adapter를 관리할 수 있다.

adapters:  
  \- adapter\_id: robot\_fleet\_main  
    adapter\_name: Main Robot Fleet Adapter  
    adapter\_type: robot\_fleet  
    supported\_action\_types:  
      \- DISPATCH\_ROBOT  
      \- REPLAN\_ROUTE  
      \- PAUSE\_MISSION  
      \- RETURN\_TO\_BASE  
    supported\_target\_types:  
      \- robot  
      \- robot\_fleet  
    supported\_protocols:  
      \- REST  
      \- gRPC  
    capabilities:  
      \- dispatch\_robot  
      \- replan\_route  
      \- pause\_mission  
      \- return\_to\_base  
    site\_scope:  
      \- site\_A  
    zone\_scope:  
      \- zone\_01  
      \- zone\_02  
      \- zone\_03  
    max\_risk\_level: high\_risk  
    contract\_version: 1.0.0  
    is\_enabled: true  
    security\_profile: robot\_fleet\_service\_account

운영 단계에서는 이 설정이 다음 저장소들과 연동될 수 있다.

PostgreSQL: adapter metadata, version, audit  
Redis: live health status, runtime cache  
Ontology Store: semantic capability definition  
Vault: credentials, tokens, certificates  
Audit Store: registration/change history

---

## **12\. 장애 시나리오**

### **12.1 Adapter 없음**

ApprovedAction은 존재하지만 호환 adapter가 없음

대응:

ExecutionRejected  
Reason: ADAPTER\_NOT\_FOUND  
Audit 기록  
Supervisor 알림  
Fallback policy 확인

---

### **12.2 Adapter 비정상**

Adapter는 등록되어 있지만 health\_status \= UNAVAILABLE

대응:

Primary adapter 제외  
Fallback adapter 탐색  
Fallback도 없으면 execution hold

---

### **12.3 Capability 불일치**

DISPATCH\_ROBOT 요청이 들어왔지만 adapter가 PAUSE\_MISSION만 지원

대응:

CapabilityMismatchError 발생  
ExecutionRequest rejected  
Ontology/Registry 설정 불일치 감사 기록

---

### **12.4 Version 불일치**

ExecutionRequest contract\_version \= 2.0  
Adapter contract\_version \= 1.0

대응:

VersionCompatibilityError 발생  
Migration adapter 또는 compatibility layer 확인

---

### **12.5 Site Scope 위반**

Site\_A 전용 adapter에 Site\_B 명령을 보내려 함

대응:

ScopeViolationError 발생  
Security audit 기록

이 케이스는 단순 오류가 아니라 보안 이벤트로 취급해야 한다.

---

## **13\. Audit Logging**

adapter\_registry는 모든 중요한 이벤트를 감사 로그로 남겨야 한다.

기록 대상:

ADAPTER\_REGISTERED  
ADAPTER\_UNREGISTERED  
ADAPTER\_ENABLED  
ADAPTER\_DISABLED  
ADAPTER\_HEALTH\_CHANGED  
ADAPTER\_SELECTED  
ADAPTER\_SELECTION\_FAILED  
ADAPTER\_CAPABILITY\_MISMATCH  
ADAPTER\_SCOPE\_VIOLATION  
ADAPTER\_VERSION\_MISMATCH

예시 audit record:

{  
  "event\_type": "ADAPTER\_SELECTED",  
  "adapter\_id": "robot\_fleet\_main",  
  "action\_type": "DISPATCH\_ROBOT",  
  "target\_type": "robot",  
  "site\_id": "site\_A",  
  "zone\_id": "zone\_02",  
  "execution\_request\_id": "exec\_req\_123",  
  "timestamp": "2026-06-26T09:00:00Z"  
}

---

## **14\. 보안 설계**

adapter\_registry는 외부 시스템 연결을 관리하기 때문에 보안상 매우 중요하다.

필수 보안 원칙:

1. adapter registration은 관리자 또는 배포 파이프라인만 가능  
2. runtime에서 임의 adapter injection 금지  
3. credentials는 registry에 직접 저장하지 않고 Vault/Secret Manager 참조만 저장  
4. adapter별 권한 범위 제한  
5. site/zone/action scope 검증 필수  
6. mTLS 또는 signed request 사용  
7. adapter 선택 실패도 audit log에 기록  
8. emergency action은 별도 adapter whitelist 적용

---

## **15\. 권장 파일 구조**

execution\_integration/  
    adapters/  
        base\_adapter.py  
        robot\_fleet\_adapter.py  
        ros2\_adapter.py  
        plc\_adapter.py  
        scada\_adapter.py  
        notification\_adapter.py

    registry/  
        adapter\_registry.py  
        adapter\_metadata.py  
        adapter\_selector.py  
        adapter\_health.py  
        adapter\_errors.py

    schemas/  
        execution\_request.py  
        execution\_result.py  
        adapter\_contract.py

    policies/  
        adapter\_policy.py  
        fallback\_policy.py

    tests/  
        test\_adapter\_registry.py  
        test\_adapter\_selection.py  
        test\_adapter\_scope.py  
        test\_adapter\_health.py

---

## **16\. 최소 구현 예시**

class AdapterRegistry:  
    def \_\_init\_\_(self) \-\> None:  
        self.\_adapters: dict\[str, AdapterRegistration\] \= {}

    def register(self, adapter: BaseAdapter, metadata: AdapterMetadata) \-\> None:  
        if metadata.adapter\_id in self.\_adapters:  
            raise AdapterAlreadyRegisteredError(metadata.adapter\_id)

        self.\_validate\_metadata(metadata)

        self.\_adapters\[metadata.adapter\_id\] \= AdapterRegistration(  
            metadata=metadata,  
            adapter\_instance=adapter,  
        )

    def unregister(self, adapter\_id: str) \-\> None:  
        if adapter\_id not in self.\_adapters:  
            raise AdapterNotFoundError(adapter\_id)

        del self.\_adapters\[adapter\_id\]

    def get(self, adapter\_id: str) \-\> BaseAdapter:  
        registration \= self.\_adapters.get(adapter\_id)

        if registration is None:  
            raise AdapterNotFoundError(adapter\_id)

        return registration.adapter\_instance

    def find\_candidates(self, request: ExecutionRequest) \-\> list\[AdapterRegistration\]:  
        candidates: list\[AdapterRegistration\] \= \[\]

        for registration in self.\_adapters.values():  
            metadata \= registration.metadata

            if not self.\_is\_compatible(metadata, request):  
                continue

            candidates.append(registration)

        return candidates

    def select\_adapter(self, request: ExecutionRequest) \-\> BaseAdapter:  
        candidates \= self.find\_candidates(request)

        if not candidates:  
            raise AdapterNotFoundError(  
                f"No adapter found for action={request.action\_type}, "  
                f"target={request.target\_type}, site={request.site\_id}"  
            )

        selected \= self.\_rank\_candidates(candidates, request)\[0\]  
        return selected.adapter\_instance

    def update\_health(  
        self,  
        adapter\_id: str,  
        status: AdapterHealthStatus,  
    ) \-\> None:  
        registration \= self.\_adapters.get(adapter\_id)

        if registration is None:  
            raise AdapterNotFoundError(adapter\_id)

        registration.metadata.health\_status \= status

    def \_is\_compatible(  
        self,  
        metadata: AdapterMetadata,  
        request: ExecutionRequest,  
    ) \-\> bool:  
        if not metadata.is\_enabled:  
            return False

        if metadata.health\_status \!= AdapterHealthStatus.HEALTHY:  
            return False

        if request.action\_type not in metadata.supported\_action\_types:  
            return False

        if request.target\_type not in metadata.supported\_target\_types:  
            return False

        if request.site\_id not in metadata.site\_scope:  
            return False

        if request.required\_capability not in metadata.capabilities:  
            return False

        return True

    def \_rank\_candidates(  
        self,  
        candidates: list\[AdapterRegistration\],  
        request: ExecutionRequest,  
    ) \-\> list\[AdapterRegistration\]:  
        return sorted(  
            candidates,  
            key=lambda registration: (  
                request.preferred\_protocol in registration.metadata.supported\_protocols,  
                request.zone\_id in registration.metadata.zone\_scope,  
            ),  
            reverse=True,  
        )

    def \_validate\_metadata(self, metadata: AdapterMetadata) \-\> None:  
        if not metadata.supported\_action\_types:  
            raise InvalidAdapterMetadataError("supported\_action\_types is required")

        if not metadata.supported\_target\_types:  
            raise InvalidAdapterMetadataError("supported\_target\_types is required")

        if not metadata.capabilities:  
            raise InvalidAdapterMetadataError("capabilities is required")

---

## **17\. 테스트 시나리오**

필수 테스트는 다음과 같다.

### **17.1 정상 선택**

DISPATCH\_ROBOT 요청이 들어왔을 때 RobotFleetAdapter가 선택되는지 검증

### **17.2 disabled adapter 제외**

is\_enabled \= false인 adapter는 후보에서 제외되는지 검증

### **17.3 unhealthy adapter 제외**

health\_status \= UNAVAILABLE인 adapter는 선택되지 않는지 검증

### **17.4 capability mismatch**

요청 capability를 지원하지 않는 adapter가 제외되는지 검증

### **17.5 site scope mismatch**

다른 site의 adapter가 선택되지 않는지 검증

### **17.6 fallback selection**

primary adapter 장애 시 fallback adapter가 선택되는지 검증

### **17.7 audit logging**

adapter 선택 성공/실패 이벤트가 audit log에 남는지 검증

---

## **18\. 확장 방향**

초기 버전에서는 in-memory registry로 시작할 수 있다.

Phase 1: In-memory registry  
Phase 2: YAML/JSON config loading  
Phase 3: PostgreSQL metadata persistence  
Phase 4: Redis health cache  
Phase 5: Ontology capability sync  
Phase 6: Shadow/Active registry version switching  
Phase 7: Multi-site distributed adapter registry

---

## **19\. 결론**

`adapter_registry`는 LEDO 실행 계층에서 매우 중요한 안전 모듈이다.

이 모듈은 단순히 adapter 객체를 저장하는 코드가 아니라, **승인된 Action과 외부 물리 제어 시스템 사이의 마지막 연결 지점을 결정론적으로 통제하는 실행 라우팅 레지스트리**이다.

핵심 원칙은 다음과 같다.

1\. Safety Gate 이후에만 실행용 adapter 선택  
2\. LLM이 adapter를 직접 선택하지 않음  
3\. capability contract 기반 선택  
4\. site/zone/action scope 검증  
5\. health 상태 기반 선택  
6\. fallback은 policy 기반으로 제한  
7\. 모든 선택과 실패는 audit log 기록  
8\. 외부 시스템 credentials는 registry에 직접 저장하지 않음  
9\. ontology-defined capability와 registry runtime metadata를 연결  
10\. 실행은 dispatcher가 담당하고 registry는 선택만 담당

따라서 `adapter_registry`는 LEDO 시스템에서 다음 역할을 한다.

Ontology-defined Action  
        ↓  
Safety-approved Execution Request  
        ↓  
Deterministic Adapter Resolution  
        ↓  
External Cyber-Physical System Integration

이 구조를 유지하면 LEDO는 LLM 기반 intent generation과 실제 물리 제어 시스템 사이를 안전하게 분리하면서도, 다양한 로봇·장비·센서·SCADA·PLC·현장 플랫폼을 확장 가능한 방식으로 연결할 수 있다.

