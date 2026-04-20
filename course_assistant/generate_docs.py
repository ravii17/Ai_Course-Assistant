import os

docs = {
    "doc_001.txt": """Computer Networks Overview
Networks basically connect devices so they can share resources. The core concept here is the OSI model, which is just a conceptual framework that explains how networking actually works so different systems can talk to each other.

The 7 OSI layers are:
- Physical: hardware connections and raw bits.
- Data Link: node-to-node data and error checking.
- Network: routing packets (like IP addresses).
- Transport: reliable or unreliable data transfer (TCP/UDP).
- Session: handles application sessions.
- Presentation: data formatting, encryption, and compression.
- Application: actual network apps like HTTP or FTP.""",

    "doc_002.txt": """Database Management Systems (DBMS)
A DBMS is software we use to store, manage, and retrieve data efficiently.

Important stuff to remember:
- ACID Properties: for reliable transactions (Atomicity, Consistency, Isolation, Durability).
- Normalization: organizing data to avoid repetition (1NF, 2NF, 3NF).
- Concurrency Control: making sure simultaneous operations don't mess up the database.
- Models: Relational (tables) and ER (Entity-Relationship) models.

Basically, a DBMS separates the data from the application code.""",

    "doc_003.txt": """Software Engineering Principles
Software Engineering is just applying engineering principles to build software. We use it to design, develop, test, and maintain systems.

Main phases:
- Requirements: figuring out what the client actually wants.
- Design: planning the architecture.
- Implementation: the coding part.
- Testing: finding bugs so it actually works.
- Maintenance: updating it after release.

Most places use methodologies like Agile (flexible, iterative) or Waterfall (linear, step-by-step).""",

    "doc_004.txt": """Operating Systems (OS)
An Operating System is the core software that manages hardware and software resources.

What an OS does:
- Process Management: handles running processes and scheduling them on the CPU without deadlocks.
- Memory: tracks what memory is free or used, and allocates it to processes.
- File System: organizes files into folders and handles access permissions.
- Device: manages connected hardware using I/O controllers.
- Security: blocks unauthorized access.

Examples are Windows, Linux, and macOS.""",

    "doc_005.txt": """Data Structures
Data structures are ways to organize data so it's easy and fast to work with.

The main ones:
- Arrays: fixed size, accessed by index.
- Linked Lists: elements point to the next one. Size is dynamic but access is slower.
- Stacks: LIFO (last in, first out), like a stack of plates. Push and pop.
- Queues: FIFO (first in, first out), like a line at a store. Enqueue and dequeue.
- Trees: hierarchical with a root. Binary Search Trees (BST) are super common.
- Hash Tables: key-value pairs using a hash function for really fast lookups.
- Graphs: nodes connected by edges, used for networks.

Picking the right one is super important for performance.""",

    "doc_006.txt": """Object-Oriented Programming (OOP)
OOP revolves around "objects" that hold data (attributes) and code (methods).

The 4 main concepts:
- Encapsulation: bundling data and methods together in a class and restricting direct access.
- Abstraction: hiding the complicated internal stuff and only showing what's needed.
- Inheritance: classes can inherit properties from parent classes to reuse code.
- Polymorphism: different objects can respond differently to the same method.

Python, Java, and C++ are the big OOP languages.""",

    "doc_007.txt": """Computer Networks Formulas
Some important formulas for computer networks:

- Throughput is the actual data transfer rate (usually less than bandwidth).
  Transmission Delay = Packet Size / Bandwidth
  Propagation Delay = Distance / Propagation Speed
- RTT (Round Trip Time) = 2 * Propagation Delay
- Shannon Capacity tells you the max data rate for a noisy channel: C = B * log2(1 + S/N)

Make sure to memorize these for the exam.""",

    "doc_008.txt": """Software Development Life Cycle (SDLC)
SDLC is the standard process for designing and building software on time and within budget.

The phases depend on each other:
1. Requirement Analysis: what does the system need?
2. Design: planning the architecture and data structures.
3. Coding: writing the actual software.
4. Testing: checking if it meets requirements and fixing bugs.
5. Deployment: giving it to the users.
6. Maintenance: fixing issues and updating after release.

Getting the requirements and design right early on is critical.""",

    "doc_009.txt": """SQL Basics
SQL is used to work with relational databases.

The main command types:
- DDL (Data Definition): for schemas. CREATE, ALTER, and DROP tables or views.
- DML (Data Manipulation): for the data itself. INSERT, UPDATE, DELETE records.
- DQL (Data Query): just the SELECT command to fetch data.

Example query:
SELECT employee_name, salary FROM Employees WHERE salary > 50000;

It's declarative, meaning you just tell it what you want, not how to get it.""",

    "doc_010.txt": """Deadlock in OS
Deadlock happens in an OS when processes get stuck waiting for resources that other processes are holding, so nobody can move forward.

The 4 conditions that cause it (Coffman conditions):
1. Mutual Exclusion: resources can't be shared.
2. Hold and Wait: a process holds a resource but waits for another.
3. No Preemption: resources can't be forcefully taken away.
4. Circular Wait: processes are waiting on each other in a circle.

To handle deadlocks, we can either prevent them (by breaking one of those conditions), avoid them (like using banker's algorithm), or just detect them and kill a process to recover.""",

    "doc_011.txt": """IP Addressing
An IP address is a numeric label for devices on a network. IPv4 uses 32-bit addresses.

The main classes:
- Class A: First bit is 0 (huge networks).
- Class B: Starts with 10 (medium networks).
- Class C: Starts with 110 (small networks).

Subnetting splits a network into smaller pieces for better routing and security. The subnet mask hides the network part so you just see the host. DHCP is used to hand out these IPs automatically.""",

    "doc_012.txt": """Software Testing
Testing makes sure the code actually does what it's supposed to do, finds bugs, and saves money in the long run.

Different types:
- Unit Testing: testing small individual functions (usually done by devs).
- Integration Testing: testing how different parts work together.
- System Testing: testing the whole completed application.
- Acceptance Testing: users testing to make sure it meets their needs.

Black-box testing means you don't look at the code, white-box means you do. Regression testing is re-testing after making changes. Tools like pytest are used for automation.""",

    "doc_013.txt": """Entity-Relationship Model
The ER model helps visualize how a database is structured before building it.

The main parts:
- Entity: a thing like a Student or Course (drawn as a rectangle).
- Attribute: properties of an entity like Name or ID (drawn as an oval). Primary keys are underlined.
- Relationship: how entities are connected (drawn as a diamond).

Cardinality shows the numbers: 1:1, 1:N, N:1, or M:N.
Once you draw the ER diagram, it's pretty easy to convert it into actual database tables.""",

    "doc_014.txt": """CPU Scheduling Algorithms
CPU scheduling decides which process gets to use the CPU while another one waits (like for I/O).

Common algorithms:
- FCFS: First-Come, First-Served. Simple, but short processes can get stuck waiting for long ones.
- SJF: Shortest Job First. Best for reducing wait times, but it's hard to guess how long a job will actually take.
- Round Robin (RR): everyone gets a small time slice. Once time is up, the process goes to the back of the line. Great for responsiveness.
- Priority: highest priority goes first, but low priority jobs might starve.""",

    "doc_015.txt": """Memory Management
Memory management in the OS efficiently handles giving out RAM to active programs.

Important concepts:
- Paging: splits memory into standard-sized 'pages' (logical) and 'frames' (physical) so we don't need contiguous memory. A page table keeps track.
- Segmentation: splits memory into variable sizes based on the program's structure.
- Virtual Memory: makes it seem like we have more RAM than we actually do by swapping parts to the hard drive.
- Page Faults: when a program tries to access memory that isn't currently loaded, so the OS fetches it from the disk. Stuff like LRU determines which old page gets kicked out."""
}

os.makedirs("e:/Project/Ai-Project/course_assistant/docs", exist_ok=True)
for filename, content in docs.items():
    with open(f"e:/Project/Ai-Project/course_assistant/docs/{filename}", "w", encoding="utf-8") as f:
        f.write(content)

print("Created 15 docs in course_assistant/docs/")
