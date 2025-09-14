# GEMINI.md - Pigeonhole Streaming System

## Project Overview

The Pigeonhole Streaming System is a comprehensive solution for managing and optimizing Kodi on Fire TV devices. It provides automated deployment, fleet management, custom Kodi configurations, and a suite of tools for testing and validation. The system is designed for stability, performance, and a professional user experience, with a focus on the Fire TV Cube.

**Key Technologies:**

*   **Kodi:** The core media center application.
*   **Python:** Used for automation, testing, and the HTTP API controller.
*   **Batch Scripts:** For automating deployment and recovery processes.
*   **ADB (Android Debug Bridge):** For communicating with and managing Fire TV devices.
*   **YAML:** For configuration management of the device fleet.
*   **Ansible:** For automation of fleet management tasks.

**Architecture:**

The system is architected around a central management station (the `M:` drive) that communicates with a fleet of Fire TV devices over the network. The management station stores all the necessary files for deployment, configuration, and maintenance. The system uses a combination of batch scripts, Python scripts, and ADB commands to automate the entire process of setting up and managing Kodi on the Fire TV devices.

## Building and Running

**Building:**

There is no explicit build process for the project. The system is designed to be run directly from the `M:` drive.

**Running:**

To deploy the Pigeonhole Streaming System to a Fire TV device, run the following command:

```batch
M:\deploy_pigeonhole_stable_final.bat
```

**Testing:**

To run the test suite, execute the following commands:

```bash
python M:\test_kodi_http.py
python M:\test_streaming_functionality.py
python M:\addon_validation_system.py
```

## Development Conventions

*   **Configuration as Code:** The system relies heavily on configuration files (e.g., `fleet-config.yaml`, `advanced_cache_settings.xml`) to manage the behavior of the devices and applications.
*   **Automation:** The project emphasizes automation for deployment, recovery, and testing.
*   **Modularity:** The project is organized into modules for different functionalities (e.g., `DEPLOYMENT`, `VALIDATION`, `INTEGRATION`).
*   **HTTP API:** The system can be controlled and monitored via an HTTP API, which is implemented in the `kodi_http_controller.py` file.
