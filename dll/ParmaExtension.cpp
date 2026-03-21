// ParmaExtension.cpp - ArmA Extension for Python Integration
#include <windows.h>
#include <string>
#include <sstream>
#include <Python.h>

// Global Python interpreter state
PyObject* g_mainModule = nullptr;
PyObject* g_globals = nullptr;

// Initialize Python interpreter
void InitializePython() {
    if (!Py_IsInitialized()) {
        Py_Initialize();
        PyRun_SimpleString("import sys");
        PyRun_SimpleString("sys.path.append('.')");

        g_mainModule = PyImport_AddModule("__main__");
        g_globals = PyModule_GetDict(g_mainModule);
    }
}

// Cleanup Python interpreter
void CleanupPython() {
    if (Py_IsInitialized()) {
        Py_Finalize();
    }
}

// Execute Python code and return result
std::string ExecutePythonCode(const std::string& code) {
    if (!Py_IsInitialized()) {
        InitializePython();
    }

    PyObject* result = PyRun_String(code.c_str(), Py_file_input, g_globals, g_globals);

    if (result) {
        PyObject* repr = PyObject_Repr(result);
        if (repr) {
            const char* str = PyUnicode_AsUTF8(repr);
            std::string output = str ? str : "Error converting result";
            Py_DECREF(repr);
            Py_DECREF(result);
            return output;
        }
        Py_DECREF(result);
    } else {
        PyErr_Print();
        return "Python execution error";
    }

    return "Unknown error";
}

// ArmA extension function - called by callExtension
extern "C" __declspec(dllexport) void __stdcall RVExtension(char* output, int outputSize, const char* input) {
    try {
        std::string command(input);

        // Parse command
        if (command == "INIT") {
            InitializePython();
            strcpy_s(output, outputSize, "Python initialized");
        }
        else if (command == "CLEANUP") {
            CleanupPython();
            strcpy_s(output, outputSize, "Python cleaned up");
        }
        else if (command.substr(0, 4) == "EXEC") {
            // Execute Python code: EXEC <python_code>
            std::string pythonCode = command.substr(5);
            std::string result = ExecutePythonCode(pythonCode);
            strcpy_s(output, outputSize, result.c_str());
        }
        else if (command.substr(0, 4) == "EVAL") {
            // Evaluate Python expression: EVAL <python_expression>
            std::string pythonExpr = command.substr(5);
            std::string result = ExecutePythonCode("print(" + pythonExpr + ")");
            strcpy_s(output, outputSize, result.c_str());
        }
        else {
            strcpy_s(output, outputSize, "Unknown command. Use: INIT, EXEC <code>, EVAL <expr>, CLEANUP");
        }
    }
    catch (const std::exception& e) {
        std::string error = "Error: ";
        error += e.what();
        strcpy_s(output, outputSize, error.c_str());
    }
}

// DLL entry point
BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH:
        // Initialize on load
        break;
    case DLL_PROCESS_DETACH:
        // Cleanup on unload
        CleanupPython();
        break;
    }
    return TRUE;
}