# Development Environment Setup Notes

## Your System
- **Primary Machine:** Windows 11 PC
- **Secondary Machine:** CachyOS PC (available if needed)
- **Docker:** Docker Desktop on Windows 11
- **Python:** 3.11+ (installed)
- **Node.js:** Optional (not needed for basic Flask app)

## AI Tools Available
- **Agent Zero:** Primary development orchestrator
- **OpenRouter:** LLM backend ($20 credits)
- **Perplexity Pro:** Research and documentation lookups
- **ChatGPT Plus:** Code review and debugging
- **Gemini Advanced:** Architecture and safety reviews

## Project Location
- **Repository:** swiftarm-pro-controller/
- **Backend Code:** swiftarm-pro-controller/backend/
- **Frontend Code:** swiftarm-pro-controller/frontend/
- **Docker Config:** swiftarm-pro-controller/docker/
- **Documentation:** swiftarm-pro-controller/docs/

## Key Ports
- Flask Development Server: http://localhost:5000
- Agent Zero Interface: http://localhost:50001
- Docker Compose Services: 5000 (Flask), 50001 (Agent Zero)

## USB Serial Device
- **Windows 11:** COM3, COM4, or similar (check Device Manager)
- **Docker:** Needs --device mapping (docker-compose.yml handles this)
- **Baud Rate:** 115200
- **Protocol:** Gcode with proprietary extensions

## Getting Help
- **For SwiftArm Pro specs:** Use Perplexity Pro
- **For code debugging:** Use ChatGPT Plus
- **For architecture decisions:** Use Gemini Advanced
- **For primary development:** Use Agent Zero
- **For quick fixes:** Use OpenRouter via Agent Zero
