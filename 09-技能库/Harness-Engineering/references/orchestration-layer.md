# Harness Engineering - Orchestration Layer

## Core Function
Handles complex task decomposition, multi-Agent collaboration, and system state coordination.

## Key Components
1. Task Auto-Decomposition
2. Multi-Agent Mutual Review
3. Middleware State Coordination

## State Machine
START -> PLANNING -> EXECUTING -> VALIDATING -> DONE
            |           |            |
            v           v            v
         ERROR <- FEEDBACK <- RETRY

## 龙心OS Integration
Five Quadrants map to state machine states.
Zhi-Xing-He-Yi optimizes next decomposition.

*Harness v1.0 2026-04-03*
