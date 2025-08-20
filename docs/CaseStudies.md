# 📚 Case Studies

Illustrative scenarios to demonstrate how ManTion can be applied. These are examples to help guide evaluation.

## Automotive Assembly Line
- Goal: Reduce unintended line stops caused by accidental presses.
- Approach: Fist gesture mapped to emergency stop with 400ms debounce; presence detection around hazardous zones.
- Outcome: Fewer false stops in dry-runs; operators retain hands-free control during gloved operations.

## Food Processing Facility
- Goal: Minimize surface contamination on start/stop buttons.
- Approach: Replace physical buttons with palm-up gesture; add audible + visual feedback.
- Outcome: Reduced touchpoints; simplified sanitation workflow during audits.

## R&D Lab / Pilot Cell
- Goal: Prototype PLC integration without rewiring.
- Approach: Use `line_control.py` and Modbus/OPC-UA adapters; implement webhook to MES for event logs.
- Outcome: Faster prototyping cycles and clearer traceability of stop/start events.
