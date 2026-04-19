import os

docs = {
    "doc_001.txt": """Topic: Computer Networks Overview
Computer Networks connect multiple devices to share resources and information. Central to networking is the OSI (Open Systems Interconnection) model, a conceptual framework used to describe the functions of a networking system. The OSI model characterizes computing functions into a universal set of rules and requirements in order to support interoperability between different products and software.

The OSI model consists of seven layers:
1. Physical Layer: Handles the physical connection between devices and the transmission of raw bit streams.
2. Data Link Layer: Node-to-node data transfer and error handling.
3. Network Layer: Handles routing and forwarding of data packets across different networks (e.g., IP).
4. Transport Layer: Provides reliable or unreliable data transfer services (TCP/UDP).
5. Session Layer: Manages sessions and dialogues between applications.
6. Presentation Layer: Data translation, encryption, and compression.
7. Application Layer: Network applications like HTTP, FTP, SMTP.

Understanding these layers helps network engineers isolate and troubleshoot problems efficiently.""",

    "doc_002.txt": """Topic: Database Management Systems (DBMS)
A Database Management System (DBMS) is software designed to store, retrieve, define, and manage data in a database. The primary goal of a DBMS is to provide an environment that is both convenient and efficient to use in retrieving and storing database information.

Key concepts in DBMS:
1. ACID Properties: Ensures reliable processing of transactions. Atomicity, Consistency, Isolation, and Durability.
2. Normalization: The process of organizing data to minimize redundancy. The stages include 1NF (eliminating repeating groups), 2NF (eliminating redundant data), and 3NF (eliminating columns not dependent on key).
3. Concurrency Control: Managing simultaneous operations on the database without conflicting with one another.
4. Data Models: Relational Model (tables and relations), Entity-Relationship (ER) Model.

DBMS provides data independence, separating the data structure from the application programming.""",

    "doc_003.txt": """Topic: Software Engineering Principles
Software Engineering is the systematic application of engineering approaches to the development of software. A software engineer applies principles of computer science and mathematical analysis to the design, development, testing, and evaluation of the software and systems.

Important Software Engineering concepts include:
1. Requirements gathering: Understanding what the client actually needs.
2. Architecture & Design: Translating requirements into a software architecture.
3. Implementation: The actual coding phase.
4. Testing: Ensuring the software works as intended and is free of bugs.
5. Maintenance: Updating and improving software after it has been deployed.

Popular methodologies include Agile, Scrum, and Waterfall, each with specific advantages and use cases. Agile focuses on iterative development and flexibility, while Waterfall is linear and sequential.""",

    "doc_004.txt": """Topic: Operating Systems (OS)
An Operating System is system software that manages computer hardware, software resources, and provides common services for computer programs.

Core responsibilities of an OS:
1. Process Management: Handles the creation, scheduling, and termination of processes. An OS must ensure that multiple processes share the CPU fairly without deadlock.
2. Memory Management: Keeps track of primary memory, i.e., what part of it is in use by whom, what part is not in use. It allocates the memory when a process requests it and deallocates it when it's freed.
3. File System Management: Organizes files into directories for easy navigation and usage. Handles file permissions and storage.
4. Device Management: Keeps track of all devices using I/O controllers.
5. Security and Access Control: Prevents unauthorized access to programs and data.

Linux, Windows, and macOS are popular OS examples.""",

    "doc_005.txt": """Topic: Data Structures
Data structures are ways to organize and store data so that they can be accessed and worked with efficiently. They define the relationship between the data, and the operations that can be performed on the data.

Common Data Structures:
1. Arrays: A collection of elements identified by index or key. Fixed size.
2. Linked Lists: Elements point to the next element. Dynamic size but slower access time.
3. Stacks: LIFO (Last In, First Out) structure. Operations include push and pop.
4. Queues: FIFO (First In, First Out) structure. Operations include enqueue and dequeue.
5. Trees: Hierarchical structure with a root and children. Popular trees include Binary Search Trees (BST).
6. Hash Tables: Implements an associative array, mapping keys to values using a hash function for constant time lookups.
7. Graphs: A set of nodes connected by edges, used to model networks.

Choosing the right data structure is crucial for algorithm optimization.""",

    "doc_006.txt": """Topic: Object-Oriented Programming (OOP)
Object-Oriented Programming is a programming paradigm based on the concept of "objects", which can contain data and code. The data is in the form of fields (often known as attributes or properties), and the code is in the form of procedures (often known as methods).

The four pillars of OOP:
1. Encapsulation: Bundling the data and the methods that act on that data into a single unit (class). It restricts direct access to some of the object's components.
2. Abstraction: Hiding internal complex details and showing only the essential features of the object.
3. Inheritance: A mechanism where one class inherits properties and behaviors from a parent class, promoting code reusability.
4. Polymorphism: The ability of different objects to respond in a unique way to the same method call.

Java, C++, and Python are widely used OOP languages.""",

    "doc_007.txt": """Topic: Computer Networks Formulas
In Computer Networks, several formulas and metrics determine performance. 

1. Throughput is the actual rate of data transfer over the network, usually lower than bandwidth.
   Formulas:
   - Transmission Delay = Packet Size (L) / Bandwidth (B)
   - Propagation Delay = Distance (d) / Propagation Speed (v)
   
2. Round Trip Time (RTT): The time required for a signal to go from the sender to the receiver and back again.
   - RTT = 2 * Propagation Delay

3. TCP Error Control (Checksum/Sliding Window): The maximum window size for Stop and Wait is 1. For Go-Back-N, it's 2^m - 1 where m is the sequence number bits.

4. Shannon Capacity: Defines the maximum data rate of a noisy channel.
   - C = B * log2(1 + S/N)
   where B is bandwidth, S is signal power, and N is noise power.

These calculations are heavily tested in academic exams.""",

    "doc_008.txt": """Topic: Software Development Life Cycle (SDLC)
SDLC is a process used by the software industry to design, develop, and test high-quality software. The SDLC aims to produce a high-quality software that meets or exceeds customer expectations, reaches completion within times and cost estimates.

Phases:
1. Requirement Analysis: Defining what the system should do.
2. System Design: Defining the hardware/software architecture, components, modules, interfaces, and data.
3. Implementation (Coding): Translating the design into code.
4. Testing: Evaluating the system or its component(s) with the intent to find whether it satisfies the specified requirements or not.
5. Deployment: Releasing the software to the customer.
6. Maintenance: Modifying the software after delivery to correct faults, improve performance, or adapt to a changed environment.

The success of SDLC depends heavily on phase 1 and 2, which set the foundation.""",

    "doc_009.txt": """Topic: SQL Basics
Structured Query Language (SQL) is the standard language for dealing with Relational Databases. It can be used to insert, search, update, and delete database records.

Core commands are divided into categories:
1. DDL (Data Definition Language): Deals with database schemas and descriptions.
   - CREATE: Creates a new table, a view of a table, or other object.
   - ALTER: Modifies an existing database object.
   - DROP: Deletes an entire table, a view, or other object.
   
2. DML (Data Manipulation Language): Deals with data manipulation.
   - INSERT: Creates a record.
   - UPDATE: Modifies records.
   - DELETE: Deletes records.
   
3. DQL (Data Query Language): Contains exactly one command, SELECT, to retrieve data.

Example query:
SELECT employee_name, salary FROM Employees WHERE salary > 50000;
This simple query demonstrates SQL's declarative nature, focusing on what data to retrieve rather than how to retrieve it.""",

    "doc_010.txt": """Topic: Deadlock in OS
A deadlock is a situation where a set of processes are blocked because each process is holding a resource and waiting for another resource acquired by some other process. 

Four necessary conditions for Deadlock (Coffman conditions):
1. Mutual Exclusion: At least one resource must be held in a non-shareable mode.
2. Hold and Wait: A process must be holding at least one resource and waiting to acquire additional resources held by other processes.
3. No Preemption: Resources cannot be preempted; a resource can be released only voluntarily by the process holding it.
4. Circular Wait: A set of processes are waiting for each other in a circular chain.

Deadlock Handling Strategies:
- Deadlock Prevention: Negating one of the four Coffman conditions.
- Deadlock Avoidance: Using algorithms like Banker's Algorithm to dynamically analyze resource-allocation states.
- Deadlock Detection and Recovery: Allowing deadlocks to occur, detecting them, and then preempting resources or killing processes to recover.""",

    "doc_011.txt": """Topic: IP Addressing
An IP (Internet Protocol) address is a numerical label assigned to each device connected to a computer network that uses the IP for communication. 

IPv4 involves a 32-bit address space, usually formatted in dotted-decimal notation (e.g., 192.168.1.1). 
Classes in IPv4:
- Class A: First bit is 0. Used for massive networks. (0.0.0.0 - 127.255.255.255)
- Class B: First two bits are 10. Medium networks. (128.0.0.0 - 191.255.255.255)
- Class C: First three bits are 110. Small networks. (192.0.0.0 - 223.255.255.255)

Subnetting is the practice of dividing a network into two or smaller networks. It increases routing efficiency and enhances security of the network. A subnet mask like 255.255.255.0 hides the network part of the IP address, leaving the host part. Local networks heavily rely on DHCP to automatically distribute these IP addresses to computers as they connect.""",

    "doc_012.txt": """Topic: Software Testing
Software testing is the process of evaluating and verifying that a software product or application does what it is supposed to do. Testing helps prevent bugs, reduces development costs, and improves performance.

Types of Testing:
1. Unit Testing: Testing individual units or components of the software. Usually done by developers.
2. Integration Testing: Testing combined parts of an application to determine if they function together correctly.
3. System Testing: Testing the complete and integrated software.
4. Acceptance Testing: Done by the end-user to determine if the system meets the business requirements.

Testing methods include Black-Box testing (tester doesn't know internal code), White-Box testing (tester knows internal code structure), and Regression testing (re-running tests after code changes). Automation scripts using tools like Selenium or Pytest are critical in modern CI/CD pipelines.""",

    "doc_013.txt": """Topic: Entity-Relationship Model
The Entity-Relationship (ER) model is a high-level conceptual data model. It enables database designers to visualize how database entities relate to each other.

Components of an ER Diagram:
1. Entity: A real-world object (e.g., Student, Teacher, Course). Represented by a rectangle.
2. Attribute: Properties of an entity (e.g., Student Roll No, Name). Represented by an oval.
   - Primary Key: An attribute that uniquely identifies an entity (underlined oval).
   - Multivalued Attribute: Represented by a double oval.
3. Relationship: Describes how two or more entities are associated (e.g., 'Enrolls in'). Represented by a diamond.

Cardinality defines the numerical attributes of the relationship:
- One-to-One (1:1)
- One-to-Many (1:N)
- Many-to-One (N:1)
- Many-to-Many (M:N)

By converting ER models to relational tables, a structured database can be easily deployed.""",

    "doc_014.txt": """Topic: CPU Scheduling Algorithms
CPU scheduling is a process that allows one process to use the CPU while the execution of another process is on hold (in waiting state) due to unavailability of any resource like I/O.

Important Algorithms:
1. First-Come, First-Served (FCFS): The process that requests the CPU first is allocated the CPU first. It is non-preemptive and can lead to the 'convoy effect' where short processes wait for a long one.
2. Shortest Job Next (SJN/SJF): Associates with each process the length of its next CPU burst. Best approach for minimizing average waiting time, but predicting burst time is hard.
3. Round Robin (RR): Each process gets a small unit of CPU time (time quantum), usually 10-100 milliseconds. After this time has elapsed, the process is preempted and added to the end of the ready queue. Ideal for time-sharing systems.
4. Priority Scheduling: A priority is associated with each process, and the CPU is allocated to the process with the highest priority. Can cause starvation.""",

    "doc_015.txt": """Topic: Memory Management
Memory management in operating systems securely and efficiently distributes computer memory to active applications.

Key Concepts:
1. Paging: A memory management scheme that eliminates the need for contiguous allocation of physical memory. Logical memory is divided into blocks of the same size called 'pages', and physical memory into 'frames'. The Page Table translates logical addresses to physical addresses.
2. Segmentation: Divides memory into variable-size segments reflecting the logical structure of a program (e.g., main function, stack, symbol table).
3. Virtual Memory: An abstraction that gives the illusion of a very large memory. It allows execution of processes that are not completely in memory.
4. Page Faults: Occurs when a program attempts to access a block of memory that is not stored in the physical memory. The OS must then fetch it from disk (swap space).
Page replacement algorithms like LRU (Least Recently Used) or FIFO decide which page to evict when memory is full."""
}

os.makedirs("e:/Project/Ai-Project/course_assistant/docs", exist_ok=True)
for filename, content in docs.items():
    with open(f"e:/Project/Ai-Project/course_assistant/docs/{filename}", "w", encoding="utf-8") as f:
        f.write(content)

print("Created 15 docs in course_assistant/docs/")
