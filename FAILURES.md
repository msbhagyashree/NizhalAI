# Failures we found and fixed

## Starter-kit compatibility and Windows video recording (2 Nov 2026)

- **What broke:** The starter kit could not read BOM-formatted JSON files, `cases show` crashed on NizhalAI test cases without temperature fields, and video recording crashed when Chromium emitted non-UTF-8 output.
- **How we found it:** Running `python -m ship_kit cases check`, `python -m ship_kit cases show`, and `python -m ship_kit video --spec video.json`.
- **What we changed:** Updated JSON reading to use `utf-8-sig`, adapted the case display to support NizhalAI cases, and enabled replacement of invalid characters in video subprocess output.
- **After:** Python syntax checks passed, all five NizhalAI cases displayed correctly, and the demo video was generated successfully at 34.6 seconds.

**Note:** These were starter-kit compatibility fixes, not measured improvements in the AI agent's answer quality. The agent evaluation gate is still pending.
