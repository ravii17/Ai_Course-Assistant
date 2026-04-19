import datetime

def current_datetime() -> str:
    """Returns the current system date and time."""
    try:
        now = datetime.datetime.now()
        return f"Current date and time is: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    except Exception as e:
        return f"Tool Error: Could not get datetime: {str(e)}"

def calculator(expression: str) -> str:
    """Evaluates a simple mathematical expression."""
    try:
        # Extremely basic safety check (in production use abstract syntax trees or safer libs)
        allowed_chars = "0123456789+-*/(). "
        if not all(c in allowed_chars for c in expression):
            return "Tool Error: Invalid characters in expression."
        
        # safely evaluate standard math expression
        result = eval(expression, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"Tool Error: Could not calculate {expression}: {str(e)}"

def syllabus_topics() -> str:
    """Returns the provided syllabus topics."""
    return (
        "The B.Tech syllabus topics covered include:\n"
        "1. Computer Networks (OSI, TCP/UDP, IP processing, routing)\n"
        "2. Database Management Systems (SQL basics, Normalization, ER models)\n"
        "3. Software Engineering (SDLC, Testing metrics)\n"
        "4. Operating Systems (Deadlocks, Scheduling algorithms, Memory management)\n"
        "5. Data Structures (Graphs, Trees, Hash maps)\n"
        "6. Object-Oriented Programming (Abstraction, Inheritance, Polymorphism)"
    )

def fallback_web_info_placeholder() -> str:
    """Provides a fallback message when external info is requested."""
    return "Tool Information: Browsing the live web is restricted. Please refer to course notes or ask generic programming questions instead."
