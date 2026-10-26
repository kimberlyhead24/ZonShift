```mermaid
classDiagram
  class Controller
  class Rules
  class SensorPort
  class ActuatorPort
  class Simulator
  class SimulatedZone
  class Clock
  Controller --> Rules
  Controller --> SensorPort
  Controller --> ActuatorPort
  Simulator ..|> SensorPort
  Simulator ..|> ActuatorPort
  Simulator --> SimulatedZone
  Simulator --> Clock
```
