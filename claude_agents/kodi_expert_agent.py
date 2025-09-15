#!/usr/bin/env python3
"""
Kodi Expert Agent - Complete Kodi v22 Development & Troubleshooting System
Integrated with kodi.wiki knowledge and Fire TV Cube specialization
"""
import requests
import json
import base64
import subprocess
import time
import os
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse

class KodiExpertAgent:
    def __init__(self, fire_tv_ip="192.168.1.130", http_port=8080):
        self.fire_tv_ip = fire_tv_ip
        self.http_port = http_port
        self.username = "kodi"
        self.password = "0000"
        self.base_url = f"http://{fire_tv_ip}:{http_port}/jsonrpc"
        self.adb_path = "M:\\adb\\adb.exe"

        # Auth header for Kodi API
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_credentials}"
        }

        # Kodi.wiki knowledge base
        self.wiki_base = "https://kodi.wiki"
        self.knowledge_cache = {}

        # Fire TV Cube specific configurations
        self.fire_tv_specs = {
            "cpu": "ARM Cortex-A73",
            "ram": "2GB",
            "storage": "16GB",
            "gpu": "Mali-G52 MP2",
            "optimal_cache": 209715200,  # 200MB
            "max_buffer": 4.0,
            "android_version": "7.1",
            "kodi_version": "22.x"
        }

        # Expert knowledge domains
        self.expertise = {
            "addon_development": self._addon_development_expert,
            "skin_development": self._skin_development_expert,
            "api_integration": self._api_integration_expert,
            "performance_optimization": self._performance_optimization_expert,
            "troubleshooting": self._troubleshooting_expert,
            "fire_tv_specialization": self._fire_tv_specialization_expert,
            "streaming_setup": self._streaming_setup_expert,
            "repository_management": self._repository_management_expert
        }

    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [KODI-EXPERT] [{level}] {message}")

    def fetch_kodi_wiki_knowledge(self, topic):
        """Fetch and cache knowledge from kodi.wiki"""
        if topic in self.knowledge_cache:
            return self.knowledge_cache[topic]

        wiki_urls = {
            "addon_development": f"{self.wiki_base}/view/Add-on_development",
            "addon_structure": f"{self.wiki_base}/view/Add-on_structure",
            "json_rpc": f"{self.wiki_base}/view/JSON-RPC_API/v12",
            "skin_development": f"{self.wiki_base}/view/Skin_development",
            "addon_xml": f"{self.wiki_base}/view/Addon.xml",
            "dependencies": f"{self.wiki_base}/view/Add-on_dependencies",
            "repository": f"{self.wiki_base}/view/HOW-TO:Create_add-on_repositories",
            "debugging": f"{self.wiki_base}/view/Log_file",
            "settings": f"{self.wiki_base}/view/Settings.xml",
            "advanced_settings": f"{self.wiki_base}/view/Advancedsettings.xml",
            "fire_tv": f"{self.wiki_base}/view/Amazon_Fire_TV",
            "android": f"{self.wiki_base}/view/Android"
        }

        if topic in wiki_urls:
            try:
                self.log(f"Fetching {topic} knowledge from kodi.wiki...")
                response = requests.get(wiki_urls[topic], timeout=10)
                if response.status_code == 200:
                    # Extract key information (simplified - in production would use proper parsing)
                    content = response.text
                    self.knowledge_cache[topic] = content
                    return content
            except Exception as e:
                self.log(f"Failed to fetch {topic}: {e}", "ERROR")

        return None

    def kodi_api(self, method, params=None, timeout=15):
        """Execute Kodi JSON-RPC API call with expert error handling"""
        try:
            payload = {"jsonrpc": "2.0", "method": method, "id": 1}
            if params:
                payload["params"] = params

            response = requests.post(self.base_url, json=payload, headers=self.headers, timeout=timeout)

            if response.status_code == 200:
                result = response.json()
                if "error" in result:
                    self.log(f"Kodi API Error: {result['error']}", "ERROR")
                    return None
                return result.get("result", result)
            else:
                self.log(f"HTTP Error {response.status_code}: {response.text}", "ERROR")
                return None

        except requests.exceptions.ConnectionError:
            self.log("Kodi not responding - checking connection...", "ERROR")
            return None
        except Exception as e:
            self.log(f"API call failed: {e}", "ERROR")
            return None

    def adb_cmd(self, command, timeout=30):
        """Execute ADB command with expert error handling"""
        try:
            full_cmd = f'"{self.adb_path}" -s {self.fire_tv_ip}:5555 {command}'
            result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=timeout)

            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                error_msg = result.stderr.strip() if result.stderr else result.stdout.strip()
                self.log(f"ADB Error: {error_msg}", "ERROR")
                return False, error_msg

        except subprocess.TimeoutExpired:
            self.log(f"ADB command timeout: {command}", "ERROR")
            return False, "Command timeout"
        except Exception as e:
            self.log(f"ADB execution failed: {e}", "ERROR")
            return False, str(e)

    def _addon_development_expert(self, issue_description):
        """Expert addon development knowledge and solutions"""
        self.log("Applying addon development expertise...")

        # Fetch latest addon development knowledge
        addon_knowledge = self.fetch_kodi_wiki_knowledge("addon_development")
        structure_knowledge = self.fetch_kodi_wiki_knowledge("addon_structure")

        # Analyze current addon state
        addons = self.kodi_api("Addons.GetAddons", {
            "properties": ["name", "enabled", "broken", "dependencies", "version"]
        })

        solutions = []

        if addons and "addons" in addons:
            # Check for common addon issues
            for addon in addons["addons"]:
                if addon.get("broken", False):
                    solutions.append({
                        "issue": f"Broken addon: {addon['name']}",
                        "addon_id": addon["addonid"],
                        "solution": self._fix_broken_addon(addon),
                        "priority": "HIGH"
                    })

                if not addon.get("enabled", True):
                    solutions.append({
                        "issue": f"Disabled addon: {addon['name']}",
                        "addon_id": addon["addonid"],
                        "solution": self._enable_addon_with_dependencies(addon),
                        "priority": "MEDIUM"
                    })

        return {
            "expertise_domain": "addon_development",
            "analysis": "Complete addon system analysis performed",
            "solutions": solutions,
            "recommendations": self._generate_addon_recommendations()
        }

    def _skin_development_expert(self, issue_description):
        """Expert skin development and troubleshooting"""
        self.log("Applying skin development expertise...")

        # Fetch skin development knowledge
        skin_knowledge = self.fetch_kodi_wiki_knowledge("skin_development")

        # Get current skin info
        skin_info = self.kodi_api("System.GetInfoLabels", {
            "labels": ["Skin.CurrentSkin", "Skin.Name", "System.BuildVersion"]
        })

        # Check available skins
        skins = self.kodi_api("Addons.GetAddons", {
            "type": "xbmc.gui.skin",
            "properties": ["name", "enabled", "broken"]
        })

        solutions = []

        if skins and "addons" in skins:
            for skin in skins["addons"]:
                if skin["addonid"] == "skin.arctic.zephyr.pigeonhole":
                    if skin.get("broken", False):
                        solutions.append({
                            "issue": "Pigeonhole skin marked as broken",
                            "solution": self._repair_pigeonhole_skin(),
                            "priority": "CRITICAL"
                        })
                    elif not skin.get("enabled", True):
                        solutions.append({
                            "issue": "Pigeonhole skin disabled",
                            "solution": self._enable_pigeonhole_skin(),
                            "priority": "HIGH"
                        })

        return {
            "expertise_domain": "skin_development",
            "current_skin": skin_info,
            "available_skins": skins,
            "solutions": solutions,
            "recommendations": self._generate_skin_recommendations()
        }

    def _fire_tv_specialization_expert(self, issue_description):
        """Fire TV Cube specific optimization and troubleshooting"""
        self.log("Applying Fire TV Cube specialization...")

        # Fire TV specific checks
        device_info = self._get_fire_tv_device_info()
        performance_metrics = self._analyze_fire_tv_performance()

        solutions = []

        # Check cache optimization
        current_cache = self._get_current_cache_settings()
        if current_cache < self.fire_tv_specs["optimal_cache"]:
            solutions.append({
                "issue": "Sub-optimal cache configuration for Fire TV Cube",
                "solution": self._optimize_fire_tv_cache(),
                "priority": "HIGH"
            })

        # Check for Amazon bloatware interference
        bloatware_check = self._check_amazon_bloatware()
        if bloatware_check["found"]:
            solutions.append({
                "issue": f"Amazon bloatware detected: {len(bloatware_check['packages'])} packages",
                "solution": self._remove_amazon_bloatware_safe(),
                "priority": "MEDIUM"
            })

        return {
            "expertise_domain": "fire_tv_specialization",
            "device_info": device_info,
            "performance_metrics": performance_metrics,
            "solutions": solutions,
            "fire_tv_optimizations": self._generate_fire_tv_optimizations()
        }

    def _streaming_setup_expert(self, issue_description):
        """Expert streaming configuration and troubleshooting"""
        self.log("Applying streaming setup expertise...")

        # Check streaming addon configuration
        streaming_addons = ["plugin.video.thecrew", "plugin.video.fen.lite", "script.module.resolveurl"]
        addon_status = {}

        for addon_id in streaming_addons:
            addon_info = self.kodi_api("Addons.GetAddonDetails", {
                "addonid": addon_id,
                "properties": ["enabled", "broken", "installed"]
            })
            addon_status[addon_id] = addon_info

        # Check ResolveURL configuration
        resolveurl_config = self._check_resolveurl_configuration()

        solutions = []

        # Analyze streaming readiness
        if not addon_status.get("script.module.resolveurl"):
            solutions.append({
                "issue": "ResolveURL missing - required for streaming",
                "solution": self._install_resolveurl(),
                "priority": "CRITICAL"
            })

        if not resolveurl_config["properly_configured"]:
            solutions.append({
                "issue": "ResolveURL not properly configured",
                "solution": self._configure_resolveurl_for_streaming(),
                "priority": "HIGH"
            })

        return {
            "expertise_domain": "streaming_setup",
            "addon_status": addon_status,
            "resolveurl_config": resolveurl_config,
            "solutions": solutions,
            "streaming_recommendations": self._generate_streaming_recommendations()
        }

    def _troubleshooting_expert(self, issue_description):
        """Advanced troubleshooting with kodi.wiki knowledge"""
        self.log("Applying advanced troubleshooting expertise...")

        # Comprehensive system analysis
        system_info = self.kodi_api("System.GetInfoBooleans", {
            "booleans": [
                "System.HasNetwork",
                "System.InternetState",
                "System.HasHDD",
                "System.HasMediaDVD"
            ]
        })

        # Get log file location and analyze
        log_analysis = self._analyze_kodi_logs()

        # Performance analysis
        performance_analysis = self._analyze_system_performance()

        return {
            "expertise_domain": "troubleshooting",
            "system_info": system_info,
            "log_analysis": log_analysis,
            "performance_analysis": performance_analysis,
            "solutions": self._generate_troubleshooting_solutions(issue_description)
        }

    def _fix_broken_addon(self, addon):
        """Fix broken addon using expert knowledge"""
        addon_id = addon["addonid"]
        self.log(f"Fixing broken addon: {addon_id}")

        # Check dependencies first
        if "dependencies" in addon:
            for dep in addon["dependencies"]:
                dep_id = dep.get("addonid")
                if dep_id:
                    self.kodi_api("Addons.SetAddonEnabled", {
                        "addonid": dep_id,
                        "enabled": True
                    })

        # Try to re-enable
        result = self.kodi_api("Addons.SetAddonEnabled", {
            "addonid": addon_id,
            "enabled": False
        })
        time.sleep(1)
        result = self.kodi_api("Addons.SetAddonEnabled", {
            "addonid": addon_id,
            "enabled": True
        })

        return f"Attempted to fix {addon_id} by disabling/re-enabling and checking dependencies"

    def _repair_pigeonhole_skin(self):
        """Expert Pigeonhole skin repair"""
        self.log("Repairing Pigeonhole skin...")

        # Check if skin files exist on device
        success, output = self.adb_cmd('shell "test -d /sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons/skin.arctic.zephyr.pigeonhole"')

        if not success:
            return "Pigeonhole skin files missing - need to reinstall from repository"

        # Check addon.xml integrity
        success, output = self.adb_cmd('shell "test -f /sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons/skin.arctic.zephyr.pigeonhole/addon.xml"')

        if not success:
            return "Pigeonhole skin addon.xml missing - need to reinstall"

        # Try to fix permissions
        self.adb_cmd('shell "chmod -R 755 /sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons/skin.arctic.zephyr.pigeonhole"')

        # Enable skin
        result = self.kodi_api("Addons.SetAddonEnabled", {
            "addonid": "skin.arctic.zephyr.pigeonhole",
            "enabled": True
        })

        return f"Pigeonhole skin repair attempted - enable result: {result}"

    def diagnose_and_solve(self, issue_description):
        """Main expert diagnosis and solution method"""
        self.log("="*60)
        self.log("KODI EXPERT AGENT - COMPREHENSIVE ANALYSIS")
        self.log("="*60)

        # Determine expertise domains needed
        domains_needed = self._analyze_issue_domains(issue_description)

        expert_analysis = {}
        all_solutions = []

        # Apply relevant expertise
        for domain in domains_needed:
            if domain in self.expertise:
                self.log(f"Applying {domain} expertise...")
                analysis = self.expertise[domain](issue_description)
                expert_analysis[domain] = analysis
                all_solutions.extend(analysis.get("solutions", []))

        # Prioritize solutions
        prioritized_solutions = self._prioritize_solutions(all_solutions)

        # Generate expert recommendations
        expert_recommendations = self._generate_expert_recommendations(expert_analysis)

        return {
            "issue_analyzed": issue_description,
            "domains_applied": domains_needed,
            "expert_analysis": expert_analysis,
            "prioritized_solutions": prioritized_solutions,
            "expert_recommendations": expert_recommendations,
            "next_steps": self._generate_next_steps(prioritized_solutions)
        }

    def _analyze_issue_domains(self, issue_description):
        """Determine which expertise domains are needed"""
        domains = []

        issue_lower = issue_description.lower()

        # Addon-related issues
        if any(word in issue_lower for word in ["addon", "plugin", "script", "missing", "broken"]):
            domains.append("addon_development")

        # Skin-related issues
        if any(word in issue_lower for word in ["skin", "interface", "theme", "pigeonhole"]):
            domains.append("skin_development")

        # Streaming-related issues
        if any(word in issue_lower for word in ["stream", "play", "video", "resolveurl", "crew", "fen"]):
            domains.append("streaming_setup")

        # Fire TV specific
        if any(word in issue_lower for word in ["fire tv", "performance", "cache", "amazon"]):
            domains.append("fire_tv_specialization")

        # Always include troubleshooting for comprehensive analysis
        domains.append("troubleshooting")

        return list(set(domains))  # Remove duplicates

    def _prioritize_solutions(self, solutions):
        """Expert solution prioritization"""
        priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}

        return sorted(solutions, key=lambda x: priority_order.get(x.get("priority", "LOW"), 3))

    def _generate_expert_recommendations(self, analysis):
        """Generate expert recommendations based on analysis"""
        recommendations = []

        # Analyze patterns across domains
        if "addon_development" in analysis and "streaming_setup" in analysis:
            recommendations.append({
                "type": "INTEGRATION",
                "recommendation": "Focus on ResolveURL configuration as it affects both addon functionality and streaming capability"
            })

        if "skin_development" in analysis and "fire_tv_specialization" in analysis:
            recommendations.append({
                "type": "OPTIMIZATION",
                "recommendation": "Ensure Pigeonhole skin is optimized for Fire TV Cube hardware specifications"
            })

        return recommendations

    def execute_expert_solutions(self, analysis_result):
        """Execute the prioritized solutions"""
        self.log("Executing expert solutions...")

        executed_solutions = []

        for solution in analysis_result["prioritized_solutions"]:
            self.log(f"Executing: {solution['issue']}")

            try:
                if "solution" in solution and callable(solution["solution"]):
                    result = solution["solution"]()
                else:
                    result = "Solution method not executable"

                executed_solutions.append({
                    "issue": solution["issue"],
                    "result": result,
                    "success": "error" not in str(result).lower()
                })

            except Exception as e:
                executed_solutions.append({
                    "issue": solution["issue"],
                    "result": f"Execution failed: {e}",
                    "success": False
                })

        return executed_solutions

    # Helper methods for expert analysis
    def _get_fire_tv_device_info(self):
        """Get Fire TV device information"""
        success, model = self.adb_cmd('shell "getprop ro.product.model"')
        success2, version = self.adb_cmd('shell "getprop ro.build.version.release"')

        return {
            "model": model if success else "Unknown",
            "android_version": version if success2 else "Unknown",
            "specs": self.fire_tv_specs
        }

    def _analyze_fire_tv_performance(self):
        """Analyze Fire TV performance metrics"""
        # Get memory info
        success, memory = self.adb_cmd('shell "cat /proc/meminfo | head -5"')

        # Get CPU info
        success2, cpu = self.adb_cmd('shell "top -n 1 | head -5"')

        return {
            "memory_info": memory if success else "Unable to retrieve",
            "cpu_info": cpu if success2 else "Unable to retrieve"
        }

    def _check_resolveurl_configuration(self):
        """Check ResolveURL configuration status"""
        # Check if ResolveURL settings exist
        success, output = self.adb_cmd('shell "test -f /sdcard/Android/data/org.xbmc.kodi/files/.kodi/userdata/addon_data/script.module.resolveurl/settings.xml"')

        return {
            "properly_configured": success,
            "settings_file_exists": success,
            "configuration_details": "Settings file check completed"
        }

    def _generate_next_steps(self, solutions):
        """Generate next steps based on solutions"""
        if not solutions:
            return ["No critical issues found - system appears healthy"]

        steps = []

        critical_solutions = [s for s in solutions if s.get("priority") == "CRITICAL"]
        if critical_solutions:
            steps.append(f"Address {len(critical_solutions)} critical issues immediately")

        high_solutions = [s for s in solutions if s.get("priority") == "HIGH"]
        if high_solutions:
            steps.append(f"Resolve {len(high_solutions)} high priority issues")

        steps.append("Monitor system stability after changes")
        steps.append("Test streaming functionality")

        return steps

if __name__ == "__main__":
    # Example usage
    expert = KodiExpertAgent()

    issue = "Pigeonhole addons missing, skin not available, streaming not working"

    analysis = expert.diagnose_and_solve(issue)

    print(json.dumps(analysis, indent=2, default=str))