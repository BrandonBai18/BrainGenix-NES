//=================================================================//
// This file is part of the BrainGenix-NES Neuron Emulation System //
//=================================================================//

/*
    Description: This file is responsible for implementing the model multithreading feature.
    Documentation Status: Complete
    Additonal Notes: None
    Date Created: 2021-12-03
*/ 

#pragma once

// Standard Libraries (BG convention: use <> instead of "")
#include <vector>
#include <iostream>
#include <thread>
#include <mutex>
#include <chrono>

// Third-Party Libraries (BG convention: use <> instead of "")

// Internal Libraries (BG convention: use <> instead of "")
#include <LoggingSystem.h>


class NES_CLASS_ThreadingEngine {

    private:

        LoggerClass *Logger_; /**<Logger Instance Pointer*/
        std::vector<std::thread> ThreadList_; /**<Vector containing worker threads.*/
        std::mutex CanPrint;

    public:

        /**
         * @brief Construct a new nes class threadingengine object
         * 
         */
        NES_CLASS_ThreadingEngine(LoggerClass *Logger);


        /**
         * @brief Destroy the nes class threadingengine object
         * 
         */
        ~NES_CLASS_ThreadingEngine();

        //void Test(const char* Msg, int i, int *counter);

};