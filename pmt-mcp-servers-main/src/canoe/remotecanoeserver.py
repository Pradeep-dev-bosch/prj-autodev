"""
Remote FastAPI Server for CANoe Operations
This server provides HTTP endpoints for CANoe automation on a Windows machine.
It wraps the CANoeClient COM automation functionality.
"""

import argparse
import asyncio
import glob
import logging
import os
import shutil
import subprocess
import time
from typing import Any, List, Optional

import pythoncom
import uvicorn
import win32com.client as win32
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(title="CANoe Remote Server", version="1.0.0")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("canoe_remote_server.log"), logging.StreamHandler()],
)


class CANoeClient:
    init_count = 0

    def __init__(self):
        if CANoeClient.init_count == 0:
            self._clear_cache()
            CANoeClient.init_count += 1
        self._initialize_canoe()

    def _initialize_canoe(self):
        """Initializes CANoe application."""
        pythoncom.CoInitialize()
        self.CANoe = win32.Dispatch("CANoe.Application")
        logging.info(f"Loaded CANoe version --> {self.CANoe.Version.FullName}")

    def _clear_cache(self):
        """Clears CANoe cache."""
        try:
            cache_dir = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Temp", "gen_py")
            if os.path.isdir(cache_dir):
                try:
                    shutil.rmtree(cache_dir)
                    logging.info("CanOE local python cache cleared.")
                except Exception as e:
                    logging.warning(f"Failed to clear CanOE local python cache: {e}. Skipping.")
            else:
                logging.info("Canoe local python cache already cleared.")
        except Exception as e:
            logging.warning(f"Unexpected error while clearing cache: {e}. Skipping.")

    def startMeasurement(self) -> str:
        """
        Starts a measurement in CANoe.

        Returns:
            str: Status message.
        """
        measurement = self.CANoe.Measurement

        if measurement.Running is False:
            logging.info("Starting CanOE measurement..")
            measurement.Start()
            time.sleep(3)
            timeout_sec = 20
            while not measurement.Running and (timeout_sec > 0):
                time.sleep(1)
                timeout_sec -= 1
                pythoncom.PumpWaitingMessages()

            if timeout_sec <= 0:
                logging.error("The measurement start operation timed out(20sec)")
                return "The measurement start operation timed out. Please check CANoe write window for errors"
            time.sleep(1)
            return "Canoe Measurement Started Successfully"
        else:
            logging.warning("Measurement already running!!!")
            return "Measurement already running!"

    def stopMeasurement(self) -> str:
        """Stops a measurement in CANoe.

        Returns:
            str: Status message.
        """

        measurement = self.CANoe.Measurement

        if measurement.Running is True:
            measurement.StopEx()
            timeout_sec = 10

            while measurement.Running and timeout_sec > 0:
                timeout_sec -= 1
                time.sleep(1)
                pythoncom.PumpWaitingMessages()
            logging.info("CanOE measurement stopped")

            if timeout_sec <= 0:
                logging.error("The measurement stop operation timed out")
            time.sleep(0.5)
            return "Canoe Measurement Stopped Successfully."
        else:
            logging.warning("Measurement already Stopped!!!")
            return "Measurement already stopped!!!"

    def openConfiguration(self, configurationFilePath: str) -> str:
        """
        Switches the loaded configuration in CANoe.

        Args:
            configurationFilePath (str): Path to Project .cfg file

        Returns:
            str: Status message with configuration path.
        """
        configurationFilePath = os.path.abspath(configurationFilePath)
        if not os.path.exists(configurationFilePath):
            logging.error(f"Configuration file does not exist: {configurationFilePath}")
            raise FileNotFoundError(f"Configuration file does not exist: {configurationFilePath}")

        self.CANoe.Open(configurationFilePath)
        timeout_sec = 40
        while self.CANoe.Configuration.OpenConfigurationResult.result == 1 and timeout_sec > 0:
            time.sleep(1)
            pythoncom.PumpWaitingMessages()
            timeout_sec -= 1

        checkConfigResult = self.CANoe.Configuration.OpenConfigurationResult.result

        if checkConfigResult != 0:
            logging.error("The configuration could not be opened due to an error")
            raise Exception("The configuration could not be opened due to an error. Please check CANoe write window")

        logging.info(f"Loaded CANoe configuration --> {self.CANoe.Configuration.Name}")
        return f"Loaded CANoe configuration --> {self.CANoe.Configuration.Path}\\{self.CANoe.Configuration.Name}.cfg"

    def addXCPConfiguration(self, xcpConfigurationFilePath: str) -> str:
        """
        Adds XCP configuration files to CANoe.

        Args:
            xcpConfigurationFilePath (str): XCP configuration file path to load

        Returns:
            str: Status message.
        """
        xcpConfigurationFilePath = os.path.abspath(xcpConfigurationFilePath)
        if not os.path.exists(xcpConfigurationFilePath):
            raise FileNotFoundError(f"XCP configuration file does not exist: {xcpConfigurationFilePath}")

        self.CANoe.Configuration.GeneralSetup.XCPSetup.ECUs.AddConfiguration(xcpConfigurationFilePath)
        if self.CANoe.Configuration.GeneralSetup.XCPSetup.ECUs.Count == 0:
            raise Exception("The XCP configuration could not be loaded")

        logging.info(f"XCP configuration {xcpConfigurationFilePath} loaded")
        return f"XCP configuration {xcpConfigurationFilePath} loaded"

    def removeAllXCPDevices(self) -> str:
        """Remove all XCP devices (ECUs) from the loaded CANoe configuration.

        Returns:
            str: Status message.
        """

        ecus = self.CANoe.Configuration.GeneralSetup.XCPSetup.ECUs
        while ecus.Count > 0:
            ecus.Remove(1)
        logging.info("All XCP devices removed from CANoe configuration")
        return "All XCP devices removed from CANoe configuration"

    def getSysVarValue(self, namespace: str, name: str) -> str:
        """
        Gets the value of a system variable.

        Args:
            namespace (str): Namespace of the variable
            name (str): Name of the variable

        Returns:
            str: System variable value formatted as string.
        """
        namespaces = self.CANoe.System.Namespaces
        target_namespace = namespaces(namespace)
        target_variable = target_namespace.variables(name)
        return f"Value of @{namespace}::{name}: {target_variable.Value}"

    def setSysVarValue(self, namespace: str, name: str, value: int | float | str) -> str:
        """
        Sets the value of a system variable.

        Args:
            namespace (str): Namespace of the variable
            name (str): Name of the variable
            value (int | float | str): Value to be set

        Returns:
            str: Status message.
        """
        namespaces = self.CANoe.System.Namespaces
        target_namespace = namespaces(namespace)
        target_variable = target_namespace.variables(name)
        target_variable.Value = value
        return f"Set @{namespace}::{name} to value: {value}"

    def getTestConfigurationsInfo(self) -> dict:
        """
        Retrieves detailed information about all test configurations in the loaded CANoe configuration.

        Returns:
            dict: A dictionary containing information about each test configuration, including:
                  - Name, ID, Enabled status, Report path
                  - Variant Profiles: A list of available variant profiles for the test configuration.
        """
        result = {}
        test_configs = self.CANoe.Configuration.TestConfigurations
        for i in range(1, test_configs.Count + 1):
            test_config = win32.CastTo(test_configs.Item(i), "ITestConfiguration8")

            variant_profiles = []
            profiles = test_config.ListAllVariantProfiles()
            for j in range(1, profiles.Count + 1):
                variant_profiles.append(profiles.Item(j))

            report_info = "Report path could not be retrieved check if report is configured"
            try:
                test_config_report = test_config.Report
                if test_config_report is not None:
                    report_info = {"FullPath": test_config_report.FullPath}
            except Exception:
                report_info = "Error retrieving report info: check vteststudio license."

            test_units_info = {}
            test_units = test_config.TestUnits
            for k in range(1, test_units.Count + 1):
                test_unit = test_units.Item(k)

                test_unit_report_info = "Report path could not be retrieved check if report is configured"
                try:
                    test_unit_report = test_unit.Report
                    if test_unit_report is not None:
                        test_unit_report_info = {
                            "Enabled": test_unit_report.Enabled,
                            "FullPath": test_unit_report.FullPath,
                        }
                except Exception:
                    test_unit_report_info = "Error retrieving report info: check vteststudio license."
                try:
                    test_units_info[f"Test Unit {k}"] = {
                        "Name": test_unit.Name,
                        "FullPath": test_unit.FullName,
                        "Caption": test_unit.Caption,
                        "Enabled": test_unit.Enabled,
                        "Report": test_unit_report_info,
                        "Verdict": test_unit.Verdict,
                    }
                except Exception:
                    test_units_info[f"Test Unit {k}"] = (
                        f"Error retrieving test unit info for {test_unit.Name}, check vteststudio license"
                    )

            result[f"Test Configuration {i}"] = {
                "Name": test_config.Name,
                "ID": i,
                "Enabled": test_config.Enabled,
                "Report": report_info,
                "Variant Profiles": variant_profiles,
            }
        return result

    def createTestConfiguration(self, test_config_name: str = None) -> dict:
        """
        Creates a new test configuration in CANoe.

        Args:
            test_config_name (str, optional): Optional name for the new test configuration.

        Returns:
            dict: Status message with test configuration ID.
        """
        test_config = self.CANoe.Configuration.TestConfigurations.Add()
        if test_config_name:
            test_config.Name = test_config_name
        result = {
            "Test Configuration Create Status": f"Created new test configuration: {test_config.Name}",
            "test_config_item_id": test_config.Id,
        }
        logging.info(f"Created new test configuration: {test_config.Name}")
        return result

    def addTestUnitToTestConfig(self, test_unit_path: str, test_config_item_id: int = None) -> str:
        """
        Adds one or more test units (.vtuexe) to a specified test configuration in CANoe.

        Args:
            test_unit_path (str): Path to a .vtuexe file or a folder containing .vtuexe files.
            test_config_item_id (int, optional): Optional ID of the test configuration to add the unit(s) to (1-based index).
                                                  If None, a new test config will be created.

        Returns:
            str: Status message with count of added test units.
        """

        # Determine if path is a file or directory
        test_unit_path = os.path.abspath(test_unit_path)
        vtuexe_files = []

        if os.path.isfile(test_unit_path) and test_unit_path.lower().endswith(".vtuexe"):
            vtuexe_files = [test_unit_path]
        elif os.path.isdir(test_unit_path):
            vtuexe_files = glob.glob(os.path.join(test_unit_path, "*.vtuexe"))
        else:
            logging.error(f"Provided path is neither a .vtuexe file nor a directory: {test_unit_path}")
            raise FileNotFoundError(f"Provided path is neither a .vtuexe file nor a directory: {test_unit_path}")

        if not vtuexe_files:
            logging.error(f"No .vtuexe files found at: {test_unit_path}")
            raise FileNotFoundError(f"No .vtuexe files found at: {test_unit_path}")

        if test_config_item_id is not None:
            test_configs = self.CANoe.Configuration.TestConfigurations
            if test_config_item_id < 1 or test_config_item_id > test_configs.Count:
                raise ValueError(f"Invalid test configuration ID: {test_config_item_id}")
            test_config = win32.CastTo(test_configs.Item(test_config_item_id), "ITestConfiguration8")
        else:
            test_config = self.CANoe.Configuration.TestConfigurations.Add()

        for vtuexe_file in vtuexe_files:
            test_config.TestUnits.Add(vtuexe_file)
            logging.info(f"Added test unit from {vtuexe_file} to test configuration {test_config.Name}")

        return f"Added {len(vtuexe_files)} test unit(s) to test configuration {test_config.Name}"

    def executeTestConfiguration(self, test_suite: str, sw_variant: str = None) -> dict:
        """
        Execute test configuration(s) in vTESTstudio.

        Args:
            test_suite (str): Comma-separated test configuration names
            sw_variant (str, optional): Optional variant profile to apply

        Returns:
            dict: {
                "test_suite": str,
                "variant": str,
                "enabled_count": int,
                "passed_count": int,
                "failed_count": int,
                "other_count": int,
                "failed_tests": [list of failed test names],
                "report_path": str or None
            }
        """
        result = {
            "test_suite": test_suite,
            "variant": sw_variant,
            "enabled_count": 0,
            "passed_count": 0,
            "failed_count": 0,
            "other_count": 0,
            "failed_tests": [],
            "report_path": None,
        }

        tests = [t.strip() for t in test_suite.split(",")]
        test_units = self.CANoe.Configuration.TestConfigurations.Count

        for test_unit_idx in range(1, test_units + 1):
            testConfig = self.CANoe.Configuration.TestConfigurations.Item(test_unit_idx)

            if testConfig.Name not in tests:
                continue

            testConfig = win32.CastTo(testConfig, "ITestConfiguration8")

            # Apply variant if specified
            if sw_variant:
                variant_profiles = testConfig.ListAllVariantProfiles()
                available = [variant_profiles.Item(i) for i in range(1, variant_profiles.Count + 1)]

                if sw_variant in available:
                    testConfig.SetVariantProfileAsync(sw_variant)
                    time.sleep(2)  # Wait for variant to apply
                    logging.info(f"Applied variant {sw_variant} to {testConfig.Name}")

            # Start test configuration
            testConfig.Start()

            # Wait for start (max 100 seconds)
            wait_cycles = 0
            while not testConfig.Running and wait_cycles < 1000:
                time.sleep(0.1)
                pythoncom.PumpWaitingMessages()
                wait_cycles += 1

            if wait_cycles >= 1000:
                raise TimeoutError(f"Test configuration {testConfig.Name} failed to start")

            logging.info(f"Test configuration {testConfig.Name} started")

            # Wait for completion (max ~2 hours)
            wait_cycles = 0
            while testConfig.Running and wait_cycles < 8000:
                time.sleep(1)
                pythoncom.PumpWaitingMessages()
                wait_cycles += 1

            if wait_cycles >= 8000:
                raise TimeoutError(f"Test configuration {testConfig.Name} execution timed out")

            logging.info(f"Test configuration {testConfig.Name} completed")

            # Collect results
            self._collect_vtest_results(testConfig, result)

            # Get report path if available
            try:
                if testConfig.Report and testConfig.Report.Enabled:
                    result["report_path"] = testConfig.Report.FullName
            except Exception:
                pass

        return result

    def _collect_vtest_results(self, testConfig, result: dict) -> None:
        """Helper to collect vTESTstudio test results.

        Args:
            testConfig: Test configuration COM object
            result (dict): Result dictionary to update with test verdicts
        """
        verdict_map = {
            0: "NotAvailable",
            1: "Passed",
            2: "Failed",
            3: "None",
            4: "Inconclusive",
            5: "ErrorInTestSystem",
        }

        for element in testConfig.Elements:
            for sub_tree in element.Elements:
                for test in sub_tree.Elements:
                    # Check if test has sub-tests
                    if test.Elements.Count != 0:
                        for sub_test in test.Elements:
                            if not sub_test.Enabled:
                                continue

                            result["enabled_count"] += 1
                            test_path = f"{element.Caption}/{sub_tree.Caption}/{test.Caption}/{sub_test.Caption}"

                            if sub_test.Verdict == 1:
                                result["passed_count"] += 1
                            elif sub_test.Verdict == 2:
                                result["failed_count"] += 1
                                result["failed_tests"].append(test_path)
                            else:
                                result["other_count"] += 1
                                result["failed_tests"].append(
                                    f"{test_path} ({verdict_map.get(sub_test.Verdict, 'Unknown')})"
                                )
                    else:
                        if not test.Enabled:
                            continue

                        result["enabled_count"] += 1
                        test_path = f"{element.Caption}/{sub_tree.Caption}/{test.Caption}"

                        if test.Verdict == 1:
                            result["passed_count"] += 1
                        elif test.Verdict == 2:
                            result["failed_count"] += 1
                            result["failed_tests"].append(test_path)
                        else:
                            result["other_count"] += 1
                            result["failed_tests"].append(f"{test_path} ({verdict_map.get(test.Verdict, 'Unknown')})")

    def getTestEnvironmentsInfo(self) -> dict:
        """
        Retrieves detailed information about all test environments in the loaded CANoe configuration.

        Returns:
            dict: A dictionary containing information about each test environment, including:
                  - Name, FullName, ID, Enabled status, and Path of the test environment.
                  - Test Modules: A dictionary of test modules within each environment, with details such as
                    Name, FullName, ID, Enabled status, Path, Report info, and Verdict.
                  - Test Modules Count: The number of test modules in the environment.

        Note:
            Logs a warning and returns a message if no test environments are found.
        """
        result = {}
        testenvs = self.CANoe.Configuration.TestSetup.TestEnvironments
        if testenvs.Count == 0:
            logging.warning("No test environments found in the loaded CANoe configuration")
            return {"Test Environments": "No test environments found in the loaded CANoe configuration"}
        for i in range(1, testenvs.Count + 1):
            testenv = win32.CastTo(testenvs.Item(i), "ITestEnvironment2")

            test_modules_info = {}
            for j in range(1, testenv.TestModules.Count + 1):
                test_module = testenv.TestModules.Item(j)
                test_module_report = test_module.Report
                tm_report_info = {}
                if test_module_report is not None:
                    tm_report_info = {
                        "Enabled": test_module_report.Enabled,
                        "Name": test_module_report.Name,
                        "FullName": test_module_report.FullName,
                        "Path": test_module_report.Path,
                    }
                test_modules_info[f"Test Module {j}"] = {
                    "Name": test_module.Name,
                    "FullName": test_module.FullName,
                    "ID": j,
                    "Enabled": test_module.Enabled,
                    "Path": test_module.Path,
                    "Report": tm_report_info,
                    "Verdict": test_module.Verdict,
                }

            result[f"Test Environment {i}"] = {
                "Name": testenv.Name,
                "FullName": testenv.FullName,
                "ID": i,
                "Enabled": testenv.Enabled,
                "Path": testenv.Path,
                "Test Modules": test_modules_info,
                "Test Modules Count": testenv.TestModules.Count,
            }
        return result

    def addTestEnvironment(self, test_environment_file_path: str) -> str:
        """
        Adds a CAPL/XML test environment to the CANoe configuration.

        Args:
            test_environment_file_path (str): Path to the test environment file (.tse)

        Returns:
            str: Status message.
        """
        test_environment_file_path = os.path.abspath(test_environment_file_path)
        if not os.path.exists(test_environment_file_path):
            logging.error(f"Test environment file does not exist: {test_environment_file_path}")
            raise FileNotFoundError(f"Test environment file does not exist: {test_environment_file_path}")

        # check if this test env is already added in canoe config
        for testenv in self.CANoe.Configuration.TestSetup.TestEnvironments:
            if os.path.abspath(testenv.FullName).lower() == test_environment_file_path.lower():
                logging.warning(f"Test environment already added: {test_environment_file_path}")
                return f"Test environment already added: {test_environment_file_path}"

        self.CANoe.Configuration.TestSetup.TestEnvironments.Add(test_environment_file_path)
        logging.info(f"Added test environment from {test_environment_file_path}")
        return f"Added test environment from {test_environment_file_path}"

    def createTestEnvironment(self, test_environment_file_name: str) -> str:
        """
        Creates a CAPL/XML test environment in the CANoe configuration.

        Args:
            test_environment_file_name (str): Name of the test environment to be created

        Returns:
            str: Status message.
        """
        # check if this test env is already added in canoe config
        for testenv in self.CANoe.Configuration.TestSetup.TestEnvironments:
            if os.path.abspath(testenv.Name).lower() == test_environment_file_name.lower():
                logging.warning(f"Test environment already added: {test_environment_file_name}")
                return f"Test environment already added: {test_environment_file_name}"

        self.CANoe.Configuration.TestSetup.TestEnvironments.Add(test_environment_file_name)
        logging.info(f"Created test environment from {test_environment_file_name}")
        return f"Created test environment from {test_environment_file_name}"

    def addXMLTestModuleToTestEnvironment(
        self, test_module_path: str, test_environment_name: str, test_module_components_list: list
    ) -> dict:
        """
        Adds XML test modules (.vxt) to a specified test environment in CANoe.

        Args:
            test_module_path (str): Path to a .vxt file.
            test_environment_name (str): Name of the test environment to add the module(s) to.
            test_module_components_list (list): List of specific test module file paths components to add.

        Returns:
            dict: Status message with test module component count and report path.
        """
        test_module_path = os.path.abspath(test_module_path)
        if not os.path.exists(test_module_path):
            logging.error(f"Test module file does not exist: {test_module_path}")
            raise FileNotFoundError(f"Test module file does not exist: {test_module_path}")

        # Find the specified test environment
        testenvs = self.CANoe.Configuration.TestSetup.TestEnvironments
        target_env = None
        for i in range(1, testenvs.Count + 1):
            env = win32.CastTo(testenvs.Item(i), "ITestEnvironment2")
            if env.Name == test_environment_name:
                target_env = env
                break

        if target_env is None:
            logging.error(f"Test environment not found: {test_environment_name}")
            raise ValueError(f"Test environment not found: {test_environment_name}")

        test_module = target_env.TestModules.Add(test_module_path)

        # If specific components are provided, enable only those
        test_module_components = test_module.Modules
        for test_component_file in test_module_components_list:
            if not os.path.exists(test_component_file):
                logging.error(f"Test module component file does not exist: {test_component_file}")
                raise FileNotFoundError(f"Test module component file does not exist: {test_component_file}")
            else:
                test_module_components.Add(test_component_file)

        logging.info(f"Added test module from {test_module_path} to test environment {test_environment_name}")

        result = {
            "Test Module Add Status": f"Added test module from {test_module_path} to test environment {test_environment_name}",
            "Test Module Components Added Count": test_module_components.Count,
            "Test Module Report Path": test_module.Report.FullName if test_module.Report else "No report configured",
        }

        return result

    def addCAPLTestModuleToTestEnvironment(self, test_module_path: str, test_environment_name: str) -> dict:
        """
        Adds CAPL test modules (.can) to a specified test environment in CANoe.

        Args:
            test_module_path (str): Path to a .can file (CAPL file).
            test_environment_name (str): Name of the test environment to add the module(s) to.

        Returns:
            dict: Status message with test module report path.
        """
        test_module_path = os.path.abspath(test_module_path)
        if not os.path.exists(test_module_path):
            logging.error(f"Test module file does not exist: {test_module_path}")
            raise FileNotFoundError(f"Test module file does not exist: {test_module_path}")

        # Find the specified test environment
        testenvs = self.CANoe.Configuration.TestSetup.TestEnvironments
        target_env = None
        for i in range(1, testenvs.Count + 1):
            env = win32.CastTo(testenvs.Item(i), "ITestEnvironment2")
            if env.Name == test_environment_name:
                target_env = env
                break

        if target_env is None:
            logging.error(f"Test environment not found: {test_environment_name}")
            raise ValueError(f"Test environment not found: {test_environment_name}")

        test_module = target_env.TestModules.Add(test_module_path)

        logging.info(f"Added CAPL test module from {test_module_path} to test environment {test_environment_name}")

        result = {
            "Test Module Add Status": f"Added CAPL test module from {test_module_path} to test environment {test_environment_name}",
            "Test Module Report Path": test_module.Report.FullName if test_module.Report else "No report configured",
        }

        return result

    def executeTestEnvironment(self, test_environments: str) -> dict:
        """
        Execute CAPL/XML test environment(s).

        Args:
            test_environments (str): Comma-separated test environment names

        Returns:
            dict: {
                "test_environments": str,
                "enabled_count": int,
                "passed_count": int,
                "failed_count": int,
                "other_count": int,
                "failed_tests": {test_name: verdict},
                "report_paths": [list of report paths]
            }
        """
        result = {
            "test_environments": test_environments,
            "enabled_count": 0,
            "passed_count": 0,
            "failed_count": 0,
            "other_count": 0,
            "failed_tests": {},
            "report_paths": [],
        }

        verdict_map = {
            0: "NotAvailable",
            1: "Passed",
            2: "Failed",
            3: "None",
            4: "Inconclusive",
            5: "ErrorInTestSystem",
        }

        env_list = [env.strip() for env in test_environments.split(",")]

        for testenv in self.CANoe.Configuration.TestSetup.TestEnvironments:
            testenv = win32.CastTo(testenv, "ITestEnvironment2")

            if testenv.Name not in env_list:
                continue

            # Get all test modules in environment
            test_modules = []
            self._traverse_test_items(testenv, lambda tm: test_modules.append(tm))

            for test_module in test_modules:
                if not test_module.Enabled:
                    continue

                result["enabled_count"] += 1
                logging.info(f"Executing {testenv.Name} -> {test_module.Name}")

                # Execute test module
                module_event = win32.WithEvents(test_module, ModuleEventHandler)
                test_module.Start()

                # Wait for start (max 100 seconds)
                wait_cycles = 0
                while not module_event.testModuleStarted and wait_cycles < 1000:
                    time.sleep(0.1)
                    pythoncom.PumpWaitingMessages()
                    wait_cycles += 1

                if wait_cycles >= 1000:
                    raise TimeoutError(f"Test module {test_module.Name} failed to start")

                # Wait for completion (default 500 seconds, endurance tests 2 hours)
                max_wait = 72000 if "_endurance" in test_module.Name.lower() else 5000
                wait_cycles = 0

                while not module_event.testModuleStopped and wait_cycles < max_wait:
                    time.sleep(1)
                    pythoncom.PumpWaitingMessages()
                    wait_cycles += 1

                if wait_cycles >= max_wait:
                    raise TimeoutError(f"Test module {test_module.Name} execution timed out")

                # Collect verdict
                verdict = verdict_map[test_module.Verdict]
                test_path = f"{testenv.Name}/{test_module.Name}"

                logging.info(f"{test_path} -> {verdict}")

                if verdict == "Passed":
                    result["passed_count"] += 1
                elif verdict == "Failed":
                    result["failed_count"] += 1
                    result["failed_tests"][test_path] = verdict
                else:
                    result["other_count"] += 1
                    result["failed_tests"][test_path] = verdict
                time.sleep(0.5)

            # Generate report if enabled
            try:
                time.sleep(1)
                for tm in test_modules:
                    if tm.Enabled and tm.Report and tm.Report.Enabled:
                        result["report_paths"].append(tm.Report.FullName)
            except Exception as e:
                logging.warning(f"Could not generate report for {testenv.Name}: {e}")

        return result

    def executeTestModules(self, test_module_names: str) -> dict:
        """
        Execute specific test module(s) by name.

        Args:
            test_module_names (str): Comma-separated test module names

        Returns:
            dict: {
                "test_modules": str,
                "executed_count": int,
                "passed_count": int,
                "failed_count": int,
                "other_count": int,
                "results": {module_name: verdict}
            }
        """
        result = {
            "test_modules": test_module_names,
            "executed_count": 0,
            "passed_count": 0,
            "failed_count": 0,
            "other_count": 0,
            "reports_paths": [],
            "results": {},
        }

        verdict_map = {
            0: "NotAvailable",
            1: "Passed",
            2: "Failed",
            3: "None",
            4: "Inconclusive",
            5: "ErrorInTestSystem",
        }

        module_list = [m.strip() for m in test_module_names.split(",")]

        for testenv in self.CANoe.Configuration.TestSetup.TestEnvironments:
            testenv = win32.CastTo(testenv, "ITestEnvironment2")

            # Get all test modules
            test_modules = []
            self._traverse_test_items(testenv, lambda tm: test_modules.append(tm))

            for test_module in test_modules:
                if test_module.Name not in module_list:
                    continue

                result["executed_count"] += 1
                logging.info(f"Executing {test_module.Name}")

                # Execute test module
                module_event = win32.WithEvents(test_module, ModuleEventHandler)
                test_module.Start()

                # Wait for start (max 100 seconds)
                wait_cycles = 0
                while not module_event.testModuleStarted and wait_cycles < 1000:
                    time.sleep(0.1)
                    pythoncom.PumpWaitingMessages()
                    wait_cycles += 1

                if wait_cycles >= 1000:
                    raise TimeoutError(f"Test module {test_module.Name} failed to start")

                # Wait for completion
                max_wait = 72000 if "_endurance" in test_module.Name.lower() else 5000
                wait_cycles = 0

                while not module_event.testModuleStopped and wait_cycles < max_wait:
                    time.sleep(1)
                    pythoncom.PumpWaitingMessages()
                    wait_cycles += 1

                if wait_cycles >= max_wait:
                    raise TimeoutError(f"Test module {test_module.Name} execution timed out")

                # Collect verdict
                verdict = verdict_map[test_module.Verdict]
                test_path = f"{testenv.Name}/{test_module.Name}"

                logging.info(f"{test_path} -> {verdict}")
                result["results"][test_path] = verdict

                if verdict == "Passed":
                    result["passed_count"] += 1
                elif verdict == "Failed":
                    result["failed_count"] += 1
                else:
                    result["other_count"] += 1

                # Add report path if available
                try:
                    time.sleep(0.5)
                    if test_module.Report:
                        result["reports_paths"].append(test_module.Report.FullName)
                except Exception as e:
                    logging.warning(f"Could not get report for {test_module.Name}: {e}")

        return result

    def _traverse_test_items(self, parent, callback) -> None:
        """Helper to recursively traverse test modules in folders.

        Args:
            parent: Parent test environment or folder COM object
            callback: Callback function to execute for each test module
        """
        for test in parent.TestModules:
            callback(test)
        for folder in parent.Folders:
            self._traverse_test_items(folder, callback)

    def enableDisableMeasurementSetupBlock(self, block_name: str, active: bool) -> str:
        """
        Activate/deactivate a block in measurement setup.

        Args:
            block_name (str): Name of the block.
            active (bool): True to activate, False to deactivate.

        Returns:
            str: Status message.
        """
        try:
            measurement_setup = self.CANoe.Configuration.OnlineSetup
            measurement_setup.ActivateEndBlock(block_name, active)
            return f"{block_name} --> {'Activated' if active else 'Deactivated'} successfully"
        except Exception as e:
            raise Exception(f"Unable to activate {block_name} in measurement_setup --> {e}")

    def getLoggingBlockList(self) -> dict:
        """Returns list of logging block names in measurement setup.

        Returns:
            dict: Dictionary with "Logging Blocks" key containing list of block names.
        """
        try:
            logging_collection = self.CANoe.Configuration.OnlineSetup.LoggingCollection
            logging_block_list = [logging_collection.Item(i).FullName for i in range(1, logging_collection.Count + 1)]
            return {"Logging Blocks": f"{logging_block_list}"}
        except Exception as e:
            raise Exception(f"Unable to get logging block list --> {e}")

    def getSimulationSetupInfo(self) -> dict:
        """Get information about the simulation setup.

        Returns:
            dict: A dictionary containing information about each bus in the simulation setup, including:
                  - Name, Active status, BusType
                  - Databases: List of database file paths
                  - Nodes: Dictionary of nodes with their Active status, FullName, and AttachedBuses
        """
        simulation_setup_info = {}
        bus_type_enum = {0: "Invalid", 1: "CAN", 11: "Ethernet"}
        try:
            simulation_setup = self.CANoe.Configuration.SimulationSetup
            buses = [simulation_setup.Buses.Item(i) for i in range(1, simulation_setup.Buses.Count + 1)]
            for bus in buses:
                bus_info = {}
                bus_info["Name"] = bus.Name
                bus_info["Active"] = bus.Active
                bus_info["BusType"] = bus.Channels.Item(1).BusType if bus.Channels.Count > 0 else "N/A"
                if bus_info["BusType"] in bus_type_enum:
                    bus_info["BusType"] = bus_type_enum[bus_info["BusType"]]
                bus_info["Databases"] = [bus.Databases.Item(i).FullName for i in range(1, bus.Databases.Count + 1)]
                nodes = [bus.Nodes.Item(i) for i in range(1, bus.Nodes.Count + 1)]
                node_info = {}
                for node in nodes:
                    node_info[node.Name] = {
                        "Active": node.Active,
                        "FullName": node.FullName,
                        "AttachedBuses": [
                            node.AttachedBuses.Item(i).Name for i in range(1, node.AttachedBuses.Count + 1)
                        ],
                    }
                bus_info["Nodes"] = node_info
                simulation_setup_info[bus.Name] = bus_info

            logging.info("Simulation setup info retrieved successfully")
            return simulation_setup_info
        except Exception as e:
            import traceback

            print(traceback.format_exc())
            logging.error(f"Error getting simulation setup info: {str(e)}")
            raise Exception(f"Error getting simulation setup info: {str(e)}")


class SystemVariablesHandler:
    """Handler for CANoe var events"""

    def __init__(self):
        self.Changed = False

    def OnChange(self, value):
        """
        triggers when a event occurs and set changed to True

        Args:
          value: event type


        """
        self.Changed = True


class TestConfigurationEventHandler:
    """
    A handler for events that come from a test configuration
    """

    def __init__(self):
        self.testConfigStarted = False

    def OnStart(self):
        """
        Called when a test configuration is
        started.

        """
        self.testConfigStarted = True


class MeasurementEventHandler:
    """
    A handler for events that come from a
    measurement
    """

    def __init__(self):
        self.measurementStarted = False
        self.measurementStopped = False

    def OnStart(self):
        """
        Called when a measurement is
        started.
        """
        self.measurementStarted = True

    def OnStop(self):
        """
        Called when a measurement is
        stopped.
        """
        self.measurementStopped = True


class ModuleEventHandler:
    """handler for test modules start and stop"""

    def __init__(self):
        self.testModuleStarted = False
        self.testModuleStopped = False

    def OnStop(self, reason):
        """
        on stop event actions

        Args:
          reason: reason for stop

        """
        self.testModuleStopped = True
        return

    def OnStart(self):
        """handler for test module start"""
        self.testModuleStarted = True
        return


class ReportEventHandler:
    """test report handler"""

    def __init__(self):
        self.statusReportGenerated = False

    def OnReportGenerated(self, success, sourceFullName, generatedFullName):
        """
        called when test report is generated

        Args:
          success:
          sourceFullName (str):
          generatedFullName (str):

        Returns:

        """
        print(
            "TestModule - Report Generated ["
            + str(success)
            + "]: "
            + str(sourceFullName)
            + " -> "
            + str(generatedFullName)
        )
        self.statusReportGenerated = True
        return


# Request/Response Models
class ConfigPathRequest(BaseModel):
    config_path: str


class XCPConfigRequest(BaseModel):
    xcp_configuration_file_path: str


class SysVarGetRequest(BaseModel):
    namespace: str
    name: str


class SysVarSetRequest(BaseModel):
    namespace: str
    name: str
    value: Any


class TestConfigNameRequest(BaseModel):
    test_config_name: Optional[str] = None


class TestConfigExecuteRequest(BaseModel):
    test_suite: str
    sw_variant: Optional[str] = None


class TestUnitAddRequest(BaseModel):
    test_unit_path: str
    test_config_item_id: Optional[int] = None


class TestEnvironmentAddRequest(BaseModel):
    test_environment_file_path: str


class TestEnvironmentCreateRequest(BaseModel):
    test_environment_name: str


class XMLTestModuleAddRequest(BaseModel):
    test_module_path: str
    test_environment_name: str
    test_module_components_list: List[str]


class CAPLTestModuleAddRequest(BaseModel):
    test_module_path: str
    test_environment_name: str


class TestEnvironmentExecuteRequest(BaseModel):
    test_environments: str


class TestModulesExecuteRequest(BaseModel):
    test_module_names: str


class MeasurementBlockRequest(BaseModel):
    block_name: str
    active: bool


# Initialize app state for CANoe client (replaces global variable)
app.state.canoe_client = None


def _is_canoe_process_running() -> bool:
    """Check if CANoe64.exe process is currently running.

    Returns:
        bool: True if CANoe64.exe is found in the process list.
    """
    try:
        output = subprocess.check_output('tasklist /FI "IMAGENAME eq CANoe64.exe"', shell=True).decode()
        return "CANoe64.exe" in output
    except Exception as e:
        logging.warning(f"Could not check CANoe process status: {e}")
        return False


async def get_canoe_client() -> CANoeClient:
    """Return the shared CANoeClient if CANoe is running, else raise HTTPException."""
    if app.state.canoe_client is None:
        if _is_canoe_process_running():
            logging.info("CANoe64.exe process detected. Connecting to existing CANoe instance...")
            try:
                app.state.canoe_client = CANoeClient()
                logging.info("Successfully connected to existing CANoe instance.")
            except Exception as e:
                logging.error(f"Failed to connect to running CANoe instance: {e}")
                raise HTTPException(
                    status_code=503,
                    detail=f"CANoe64.exe is running but could not connect: {e}",
                )
        else:
            logging.warning("No CANoe instance running and client not initialized.")
            raise HTTPException(
                status_code=503,
                detail="No CANoe configuration is opened. Please either open a CANoe configuration manually "
                "or use the /launch_canoe endpoint with a config_path to launch CANoe.",
            )
    return app.state.canoe_client


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    canoe_client = app.state.canoe_client
    return {
        "status": "healthy",
        "canoe_initialized": canoe_client is not None,
        "canoe_version": canoe_client.CANoe.Version.FullName if canoe_client else None,
    }


@app.get("/launch_canoe")
async def launch_canoe(config_path: str = ""):
    """
    Launch CANoe application and optionally load a configuration.

    Args:
        config_path (str, optional): Path to CANoe config file.

    Returns:
        dict: Launch status with version information.
    """
    try:
        if app.state.canoe_client is not None:
            logging.warning("CANoe application already initialized. Reinitializing...")

        await asyncio.sleep(0.5)  # Small delay for initialization
        app.state.canoe_client = CANoeClient()

        result = {
            "Canoe Launch Status": f"CANoe application launched with version: {app.state.canoe_client.CANoe.Version.FullName}"
        }

        if config_path:
            await asyncio.sleep(1)
            load_result = app.state.canoe_client.openConfiguration(config_path)
            result["Configuration Load Status"] = load_result

        logging.info(f"CANoe launched successfully: {result}")
        return result

    except Exception as e:
        logging.error(f"Error launching CANoe: {str(e)}")
        return {"status": "error", "message": f"Error launching CANoe: {str(e)}"}


@app.post("/load_configuration")
async def load_configuration(request: ConfigPathRequest, canoe: CANoeClient = Depends(get_canoe_client)):
    """
    Load a CANoe configuration file.

    Args:
        request: Configuration file path

    Returns:
        dict: Configuration load status.
    """
    try:
        result = canoe.openConfiguration(request.config_path)
        logging.info(f"Configuration loaded: {result}")
        return {"Configuration Load Status": result}
    except Exception as e:
        logging.error(f"Error loading configuration: {str(e)}")
        return {"status": "error", "message": f"Error loading configuration: {str(e)}"}


@app.get("/start_measurement")
async def start_measurement(canoe: CANoeClient = Depends(get_canoe_client)):
    """
    Start CANoe measurement.

    Returns:
        dict: Measurement start status.
    """
    try:
        result = canoe.startMeasurement()
        logging.info(f"Measurement started: {result}")
        return {"Measurement Start Status": result}
    except Exception as e:
        logging.error(f"Error starting measurement: {str(e)}")
        return {"status": "error", "message": f"Error starting measurement: {str(e)}"}


@app.get("/stop_measurement")
async def stop_measurement(canoe: CANoeClient = Depends(get_canoe_client)):
    """
    Stop CANoe measurement.

    Returns:
        dict: Measurement stop status.
    """
    try:
        result = canoe.stopMeasurement()
        logging.info(f"Measurement stopped: {result}")
        return {"Measurement Stop Status": result}
    except Exception as e:
        logging.error(f"Error stopping measurement: {str(e)}")
        return {"status": "error", "message": f"Error stopping measurement: {str(e)}"}


@app.post("/add_xcp_configuration")
async def add_xcp_configuration(request: XCPConfigRequest, canoe: CANoeClient = Depends(get_canoe_client)):
    """
    Add XCP configuration to CANoe.

    Args:
        request: XCP configuration file path

    Returns:
        dict: XCP configuration load status.
    """
    try:
        result = canoe.addXCPConfiguration(request.xcp_configuration_file_path)
        logging.info(f"XCP configuration added: {result}")
        return {"XCP Configuration Load Status": result}
    except Exception as e:
        logging.error(f"Error adding XCP configuration: {str(e)}")
        return {"status": "error", "message": f"Error adding XCP configuration: {str(e)}"}


@app.get("/remove_all_xcp_devices")
async def remove_all_xcp_devices(canoe: CANoeClient = Depends(get_canoe_client)):
    """
    Remove all XCP devices from CANoe configuration.

    Returns:
        dict: XCP devices removal status.
    """
    try:
        result = canoe.removeAllXCPDevices()
        logging.info(f"XCP devices removed: {result}")
        return {"XCP Devices Removal Status": result}
    except Exception as e:
        logging.error(f"Error removing XCP devices: {str(e)}")
        return {"status": "error", "message": f"Error removing XCP devices: {str(e)}"}


@app.get("/get_sysvar_value")
async def get_sysvar_value(namespace: str, name: str, canoe: CANoeClient = Depends(get_canoe_client)):
    """
    Get CANoe system variable value.

    Args:
        namespace: System variable namespace
        name: System variable name

    Returns:
        dict: System variable value.
    """
    try:
        result = canoe.getSysVarValue(namespace, name)
        logging.info(f"SysVar value retrieved: {result}")
        return {"SysVar Value": result}
    except Exception as e:
        logging.error(f"Error getting SysVar value: {str(e)}")
        return {"status": "error", "message": f"Error getting SysVar value: {str(e)}"}


@app.post("/set_sysvar_value")
async def set_sysvar_value(request: SysVarSetRequest, canoe: CANoeClient = Depends(get_canoe_client)):
    """
    Set CANoe system variable value.

    Args:
        request: System variable namespace, name, and value

    Returns:
        dict: System variable set status.
    """
    try:
        result = canoe.setSysVarValue(request.namespace, request.name, request.value)
        logging.info(f"SysVar value set: {result}")
        return {"SysVar Set Status": result}
    except Exception as e:
        logging.error(f"Error setting SysVar value: {str(e)}")
        return {"status": "error", "message": f"Error setting SysVar value: {str(e)}"}


@app.get("/get_test_configurations_info")
async def get_test_configurations_info(canoe: CANoeClient = Depends(get_canoe_client)):
    """
    Get information about all test configurations.

    Returns:
        dict: Test configurations information.
    """
    try:
        result = canoe.getTestConfigurationsInfo()
        logging.info("Test configurations info retrieved")
        return result
    except Exception as e:
        logging.error(f"Error getting test configurations info: {str(e)}")
        return {"status": "error", "message": f"Error getting test configurations info: {str(e)}"}


@app.post("/create_test_configuration")
async def create_test_configuration(request: TestConfigNameRequest, canoe: CANoeClient = Depends(get_canoe_client)):
    """
    Create a new test configuration.

    Args:
        request: Optional test configuration name

    Returns:
        dict: Test configuration creation status.
    """
    try:
        result = canoe.createTestConfiguration(request.test_config_name)
        logging.info(f"Test configuration created: {result}")
        return result
    except Exception as e:
        logging.error(f"Error creating test configuration: {str(e)}")
        return {"status": "error", "message": f"Error creating test configuration: {str(e)}"}


@app.post("/execute_test_configuration")
async def execute_test_configuration(request: TestConfigExecuteRequest, canoe: CANoeClient = Depends(get_canoe_client)):
    """
    Execute test configuration(s).

    Args:
        request: Test suite names and optional variant

    Returns:
        dict: Test execution results.
    """
    try:
        result = canoe.executeTestConfiguration(request.test_suite, request.sw_variant)
        logging.info(f"Test configuration executed: {result}")
        return result
    except Exception as e:
        logging.error(f"Error executing test configuration: {str(e)}")
        return {"status": "error", "message": f"Error executing test configuration: {str(e)}"}


@app.post("/add_test_unit_to_test_config")
async def add_test_unit_to_test_config(request: TestUnitAddRequest, canoe: CANoeClient = Depends(get_canoe_client)):
    """
    Add test unit(s) to a test configuration.

    Args:
        request: Test unit path and optional config ID

    Returns:
        dict: Test unit add status.
    """
    try:
        result = canoe.addTestUnitToTestConfig(request.test_unit_path, request.test_config_item_id)
        logging.info(f"Test unit added: {result}")
        return {"Test Unit Add Status": result}
    except Exception as e:
        logging.error(f"Error adding test unit: {str(e)}")
        return {"status": "error", "message": f"Error adding test unit: {str(e)}"}


@app.get("/get_test_environments_info")
async def get_test_environments_info(canoe: CANoeClient = Depends(get_canoe_client)):
    """
    Get information about all test environments.

    Returns:
        dict: Test environments information.
    """
    try:
        result = canoe.getTestEnvironmentsInfo()
        logging.info("Test environments info retrieved")
        return result
    except Exception as e:
        logging.error(f"Error getting test environments info: {str(e)}")
        return {"status": "error", "message": f"Error getting test environments info: {str(e)}"}


@app.post("/add_test_environment")
async def add_test_environment(request: TestEnvironmentAddRequest, canoe: CANoeClient = Depends(get_canoe_client)):
    """
    Add a test environment to CANoe configuration.

    Args:
        request: Test environment file path

    Returns:
        dict: Test environment add status.
    """
    try:
        result = canoe.addTestEnvironment(request.test_environment_file_path)
        logging.info(f"Test environment added: {result}")
        return {"Test Environment Add Status": result}
    except Exception as e:
        logging.error(f"Error adding test environment: {str(e)}")
        return {"status": "error", "message": f"Error adding test environment: {str(e)}"}


@app.post("/create_test_environment")
async def create_test_environment(
    request: TestEnvironmentCreateRequest, canoe: CANoeClient = Depends(get_canoe_client)
):
    """
    Create a test environment in CANoe.

    Args:
        request: Test environment name

    Returns:
        dict: Test environment creation status.
    """
    try:
        result = canoe.createTestEnvironment(request.test_environment_name)
        logging.info(f"Test environment created: {result}")
        return {"Test Environment Create Status": result}
    except Exception as e:
        logging.error(f"Error creating test environment: {str(e)}")
        return {"status": "error", "message": f"Error creating test environment: {str(e)}"}


@app.post("/add_xml_test_module_to_test_environment")
async def add_xml_test_module_to_test_environment(
    request: XMLTestModuleAddRequest, canoe: CANoeClient = Depends(get_canoe_client)
):
    """
    Add XML test module to a test environment.

    Args:
        request: Test module path, environment name, and components list

    Returns:
        dict: Test module add status.
    """
    try:
        result = canoe.addXMLTestModuleToTestEnvironment(
            request.test_module_path, request.test_environment_name, request.test_module_components_list
        )
        logging.info(f"XML test module added: {result}")
        return result
    except Exception as e:
        logging.error(f"Error adding XML test module: {str(e)}")
        return {"status": "error", "message": f"Error adding XML test module: {str(e)}"}


@app.post("/add_capl_test_module_to_test_environment")
async def add_capl_test_module_to_test_environment(
    request: CAPLTestModuleAddRequest, canoe: CANoeClient = Depends(get_canoe_client)
):
    """
    Add CAPL test module to a test environment.

    Args:
        request: Test module path and environment name

    Returns:
        dict: Test module add status.
    """
    try:
        result = canoe.addCAPLTestModuleToTestEnvironment(request.test_module_path, request.test_environment_name)
        logging.info(f"CAPL test module added: {result}")
        return result
    except Exception as e:
        logging.error(f"Error adding CAPL test module: {str(e)}")
        return {"status": "error", "message": f"Error adding CAPL test module: {str(e)}"}


@app.post("/execute_test_environment")
async def execute_test_environment(
    request: TestEnvironmentExecuteRequest, canoe: CANoeClient = Depends(get_canoe_client)
):
    """
    Execute test environment(s).

    Args:
        request: Test environment names

    Returns:
        dict: Test execution results.
    """
    try:
        result = canoe.executeTestEnvironment(request.test_environments)
        logging.info(f"Test environment executed: {result}")
        return result
    except Exception as e:
        logging.error(f"Error executing test environment: {str(e)}")
        return {"status": "error", "message": f"Error executing test environment: {str(e)}"}


@app.post("/execute_test_modules")
async def execute_test_modules(request: TestModulesExecuteRequest, canoe: CANoeClient = Depends(get_canoe_client)):
    """
    Execute test module(s).

    Args:
        request: Test module names

    Returns:
        dict: Test execution results.
    """
    try:
        result = canoe.executeTestModules(request.test_module_names)
        logging.info(f"Test modules executed: {result}")
        return result
    except Exception as e:
        logging.error(f"Error executing test modules: {str(e)}")
        return {"status": "error", "message": f"Error executing test modules: {str(e)}"}


@app.post("/enable_disable_measurement_setup_block")
async def enable_disable_measurement_setup_block(
    request: MeasurementBlockRequest, canoe: CANoeClient = Depends(get_canoe_client)
):
    """
    Enable or disable a measurement setup block.

    Args:
        request: Block name and active status

    Returns:
        dict: Block status update result.
    """
    try:
        result = canoe.enableDisableMeasurementSetupBlock(request.block_name, request.active)
        logging.info(f"Measurement block updated: {result}")
        return {"Measurement Setup Block Status": result}
    except Exception as e:
        logging.error(f"Error updating measurement block: {str(e)}")
        return {"status": "error", "message": f"Error updating measurement block: {str(e)}"}


@app.get("/get_logging_block_list")
async def get_logging_block_list(canoe: CANoeClient = Depends(get_canoe_client)):
    """
    Get list of logging blocks in measurement setup.

    Returns:
        dict: List of logging blocks.
    """
    try:
        result = canoe.getLoggingBlockList()
        logging.info("Logging block list retrieved")
        return result
    except Exception as e:
        logging.error(f"Error getting logging block list: {str(e)}")
        return {"status": "error", "message": f"Error getting logging block list: {str(e)}"}


@app.get("/quit_canoe")
async def quit_canoe(save_cfg: bool = False):
    """
    Quit CANoe application.

    Args:
        save_cfg (bool, optional): Save configuration changes before quitting. Default is False.

    Returns:
        dict: Quit status.
    """
    canoe_client = app.state.canoe_client

    if canoe_client is None:
        return {"message": "CANoe application is not running"}

    try:
        measurement = canoe_client.CANoe.Measurement

        # Stop measurement if running with retries
        wait_sec = 5
        while measurement.Running and wait_sec > 0:
            try:
                canoe_client.stopMeasurement()
                await asyncio.sleep(1)
            except Exception as e:
                logging.warning(f"Measurement couldn't be stopped, waiting -> {wait_sec}s remaining. Error: {e}")

            pythoncom.PumpWaitingMessages()
            wait_sec -= 1

        if measurement.Running:
            logging.warning("Tried multiple times but couldn't stop measurement, force quitting CANoe")
        else:
            logging.info("CANoe measurement stopped successfully")

        await asyncio.sleep(2)

        # Save or discard configuration changes
        if save_cfg:
            canoe_client.CANoe.Configuration.Modified = True
            logging.info("Saving configuration changes")
        else:
            canoe_client.CANoe.Configuration.Modified = False
            logging.info("Discarding configuration changes")

        # Quit CANoe application
        try:
            canoe_client.CANoe.Quit()
            logging.info("CANoe application quit command sent")
        except Exception as e:
            logging.warning(f"Unable to quit CANoe application gracefully: {e}")

        app.state.canoe_client = None
        await asyncio.sleep(3)

        # Force kill if processes are still running
        try:
            output = subprocess.check_output("tasklist", shell=True).decode()

            killed_processes = []
            if "CANoe64.exe" in output:
                logging.info("Forcing CANoe64.exe termination")
                os.system("taskkill /im CANoe64.exe /f 2>nul >nul")
                killed_processes.append("CANoe64.exe")

            if "CANoeTBE.exe" in output:
                logging.info("Forcing CANoeTBE.exe termination")
                os.system("taskkill /im CANoeTBE.exe /f 2>nul >nul")
                killed_processes.append("CANoeTBE.exe")

            if killed_processes:
                return {
                    "message": "CANoe application quit successfully (force killed)",
                    "killed_processes": killed_processes,
                }
            else:
                return {"message": "CANoe application quit successfully"}

        except Exception as e:
            logging.warning(f"Error checking/killing CANoe processes: {e}")
            return {"message": "CANoe application quit (process cleanup skipped)"}

    except Exception as e:
        logging.error(f"Error quitting CANoe: {str(e)}")
        app.state.canoe_client = None
        return {"status": "error", "message": f"Error quitting CANoe: {str(e)}"}


@app.get("/get_simulation_setup_info")
async def get_simulation_setup_info(canoe: CANoeClient = Depends(get_canoe_client)):
    """Get information about the simulation setup.

    Returns:
        dict: Simulation setup information.
    """
    try:
        result = canoe.getSimulationSetupInfo()
        logging.info("Simulation setup info retrieved")
        return result
    except Exception as e:
        logging.error(f"Error getting simulation setup info: {str(e)}")
        return {"status": "error", "message": f"Error getting simulation setup info: {str(e)}"}


@app.get("/get_canoe_configuration_info")
async def get_canoe_configuration_info(canoe: CANoeClient = Depends(get_canoe_client)) -> dict:
    """Helper function to get basic configuration info."""
    try:
        config = canoe.CANoe.Configuration
        config_info = {"Canoe Workspace Path": config.Path, "Name": config.Name + r".cfg"}
        logging.info("Configuration info retrieved successfully")
        return config_info
    except Exception as e:
        logging.error(f"Error getting configuration info: {str(e)}")
        return {"status": "error", "message": f"Error getting configuration info: {str(e)}"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CANoe Remote Server")
    parser.add_argument("--port", type=int, default=None, help="Port to run the server on")
    args = parser.parse_args()

    port = args.port if args.port is not None else int(os.getenv("CANOE_REMOTE_PORT", "8037"))
    host = "0.0.0.0"

    logging.info(f"Starting CANoe Remote Server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
