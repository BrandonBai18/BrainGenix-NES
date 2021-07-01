[![Codacy Badge](https://app.codacy.com/project/badge/Grade/64207ebc26b34f24b1ad39ad43df315d)](https://www.codacy.com/gh/carboncopies/BrainGenix-NES/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=carboncopies/BrainGenix-NES&amp;utm_campaign=Badge_Grade)

What's BrainGenix-NES?

BrainGenix-NES or NES is the Neuron Emulation System division of the BrainGenix department. NES is a distributed biological neuron simulator designed for the emulation of human minds. The simulator uses Apache Zookeeper and other production-grade systems to ensure that it's both stable and fault-tolerant. It's designed with scalability in mind to run with one neuron or a hundred billion.

Key Features
 - NES runs with as many neurons as your simulation has, be it one or a billion.
 - Performance is also an issue with simulations, so NES supports almost every model. It's based on the popular Brian simulator, so any model that can be written as a differential equation is supported.
 - Based on Apache Zookeeper, NES uses the leader-follower system. Based on this system, even a fault with the leader node won't cause the system to crash.
 - NES has an extensive Simulation API that allows any other system to interact with the simulation that NES runs.
 - Management of the entire BrainGenix software suite can be acomplished via BrainGenix's unified CLI or GUI.
 - NES also interfaces with ERS and STS, the other parts of BrainGenix.
 
Documentation
Currently the best source of information about NES can be found within our Technical specifications document down below:
https://docs.google.com/document/d/1tVIB7KQcSRKNU_df8oPVR3wyBHagjv2xvqaMy-oDg18/edit#

