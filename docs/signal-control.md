# Adaptive Signal Control & Safety Validator

## Mandatory Safety Validator Rules
1. **Conflict Matrix**: Conflicting approaches (North/South vs East/West) can NEVER have green simultaneously.
2. **Phase Bounds**: Minimum green 10s, Maximum green 65s.
3. **Clearance Intervals**: Yellow interval 3s, All-Red clearance 2s.
4. **Starvation Prevention**: Every approach is guaranteed green within 3 signal cycles.
5. **Emergency Preemption**: Immediate clearance of conflicting phases to open a 30s green corridor for ambulances and fire trucks.
