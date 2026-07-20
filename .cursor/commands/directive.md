Submit a Sovereign directive to the AOS Orchestrator:

Directive: $ARGUMENTS

Steps:
1. Call `submit_directive` with the directive text and appropriate priority
2. Call `get_orchestrator_status` to confirm queuing
3. If MOTOR directive, also call `process_motor_queue`
