# AI Assistant Working Notes for `raspberry_pi_pico`

Concise, project-specific guidance for automated coding agents. Stay concrete; mirror existing patterns.

## 1. Project Purpose & Shape
Collection of MicroPython example scripts for Raspberry Pi Pico / Pico W: sensors (BME680, internal temp), displays (SSD1306 / SH1106), networking (Wi-Fi, simple HTTP fetch, MQTT), RTC (PCF8563), GPIO inputs (buttons, PIR), and small UX demos (LEDs, potentiometer). Library drivers live in `lib/`. Root scripts are standalone runnable entrypoints—no central package/import graph besides shared helpers (`connect_to_wlan.py`, `umqtt_simple.py`, sensor/display drivers under `lib/`).

## 2. Runtime Environment
- Target: MicroPython firmware on Pico / Pico W.
- Assume constrained RAM/flash: avoid heavy standard library usage; keep allocations low inside loops.
- Country code explicitly set via `rp2.country("DE")` in Wi-Fi scripts.
- Sensitive credentials isolated in separate (ignored) config modules (`wlan_config.py`, `mqtt_config.py`)—never hardcode secrets in examples.

## 3. Common Patterns
| Concern | Pattern in Repo | Notes |
| ------- | --------------- | ----- |
| Wi-Fi connect | `connect_to_wlan()` (see `connect_to_wlan.py`) returns global `wlan`; retry loop with max_wait countdown; raises on failure | Reuse this helper; don't duplicate inline logic unless tweaking behavior. |
| Sensor over I2C | Create `I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)`; optional bus scan; instantiate driver (`BME680_I2C`, `SSD1306_I2C`) | Keep pin/freq consistent unless documenting change. |
| Internal temperature | ADC(4) reading → voltage → formula `27 - (v - 0.706)/0.001721` | Use same formula for consistency. |
| MQTT publish loop | Connect, publish one payload, disconnect each cycle; catch `OSError` | Maintain short-lived connections; keep topic as `bytes`. |
| Display update loop | `display.fill(0)` then multiple `display.text(...)` then `display.show()` | Clear screen each iteration; keep 1s sleep typical. |
| Interrupt (PIR) | Configure pin with `irq(trigger=Pin.IRQ_RISING, handler=...)` plus brief debounce `sleep_ms(100)` | Follow same structure for new motion/edge handlers. |
| Timing | Use `time.sleep(1)` (or ms) inside infinite loop; minimal asynchronous patterns yet | If adding async, isolate to new example; note TODO list mentions async experimentation. |

## 4. Library Drivers
- `lib/bme680.py` is an adapted Adafruit driver; don't broaden API without reason. Provide wrapper utilities in new files instead of editing driver unless fixing a bug.
- Other drivers: `pcf8563.py` (RTC), `sh1106.py` (display). Prefer adding new hardware drivers under `lib/` with self-contained classes mirroring this naming style.

## 5. File / Naming Conventions
- Example scripts prefixed with `example_` + hardware/feature description.
- One script = one demonstrable feature; minimal cross-imports (avoid complex coupling).
- Support / helper modules have imperative names: `connect_to_wlan.py`, `umqtt_simple.py`.
- Legacy or experimental code kept under `Old_Code/`; do not depend on it for new examples.

## 6. Adding New Examples (Checklist)
1. Place file at repo root named `example_<feature>.py`.
2. Import shared helpers instead of re-implementing (e.g., Wi-Fi, MQTT, display init if factored).
3. Guard endless loops only if needed for tests; otherwise follow existing infinite loop style with consistent sleep intervals.
4. Keep output prints concise (German messages appear—maintain language consistency if modifying those sections; English fine for new hardware notes).
5. Document pin assignments near top with clear variable names.

## 7. Error Handling & Resource Use
- Simple raise on network failure; otherwise fail fast.
- MQTT errors caught as `OSError` and reported, then loop continues after sleep.
- Close network resources where supported (e.g., `response.close()` after HTTP GET).
- Avoid large string concatenations inside tight loops; reuse formatted f-strings pattern as seen in display updates.

## 8. Secrets & Configuration
- Expect `wlan_config.py` with `ssid`, `psk`; `mqtt_config.py` with `user`, `password` (not committed). If generating code needing these, reference attributes, do not inline values.
- If absent, instruct user (comments) to create minimal config file with those variables.

## 9. Potential Extensions (Respect Existing Style)
- Async versions: create parallel `example_<feature>_async.py` rather than modifying synchronous originals.
- Data logging: replicate `example_internal_temperature_data_logging.py` style (if extending, stream to MQTT or file with lightweight buffering).

## 10. When Unsure
Prefer small, isolated example script over refactor of shared code. Ask before restructuring drivers or centralizing logic beyond existing helper patterns.

## 11. Quick References
- Wi-Fi helper: `connect_to_wlan.connect_to_wlan()`
- Internal temp formula: `27 - (spannung - 0.706) / 0.001721`
- BME680 usage: see `example_bme680_ssd1306.py` (bus scan + display render) 
- MQTT cycle: see `example_pico2w_mqtt.py` (connect → publish → disconnect per loop)

---
Provide changes aligned with these patterns. If proposing architecture shifts (e.g., async event loop), flag clearly as experimental.
