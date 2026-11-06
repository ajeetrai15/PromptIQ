"""Curated prompt templates across key categories for learning and experimentation."""

from typing import List, Dict, Any

TEMPLATES: List[Dict[str, Any]] = [
    # 1. Learning
    {
        "id": "learn_quantum",
        "category": "Learning",
        "title": "Quantum Computing Fundamentals",
        "description": "Learn complex quantum physics concepts tailored for a software developer.",
        "prompt": "Explain quantum computing and how qubits work.",
        "notes": "Lacks learner background, desired analogies, depth, and output structure."
    },
    {
        "id": "learn_history",
        "category": "Learning",
        "title": "Historical Perspective Analysis",
        "description": "Understand the socio-economic causes of the Industrial Revolution.",
        "prompt": "Tell me why the industrial revolution happened.",
        "notes": "Lacks perspective balance, geographical scope, and structured takeaways."
    },

    # 2. Coding
    {
        "id": "code_refactor",
        "category": "Coding",
        "title": "Async Python Refactor & Error Handling",
        "description": "Transform synchronous I/O operations to robust asyncio with retry logic.",
        "prompt": "Write a Python script to scrape product prices from an e-commerce page.",
        "notes": "Missing library constraints, rate limiting, error handling, typing, and schema specifications."
    },
    {
        "id": "code_sql_opt",
        "category": "Coding",
        "title": "PostgreSQL Query Optimization",
        "description": "Diagnose slow analytical queries and optimize indexing strategy.",
        "prompt": "How can I speed up my slow PostgreSQL join query?",
        "notes": "Missing execution plan (EXPLAIN ANALYZE), schema definition, table sizes, and database version."
    },

    # 3. Research
    {
        "id": "research_battery",
        "category": "Research",
        "title": "Solid-State Battery Breakthroughs",
        "description": "Synthesize recent advances, commercial hurdles, and key market players.",
        "prompt": "Summarize recent research on solid state batteries.",
        "notes": "Lacks timeframe constraints, focus areas (materials, manufacturing, cost), and academic rigor."
    },
    {
        "id": "research_comp_ai",
        "category": "Research",
        "title": "Competitive Architecture Benchmark",
        "description": "Compare Mixture of Experts (MoE) vs. Dense Transformer architectures.",
        "prompt": "Compare MoE models with dense models in LLMs.",
        "notes": "Lacks explicit comparison dimensions (training cost, inference latency, memory footprint, routing instability)."
    },

    # 4. Content Writing
    {
        "id": "content_saas_launch",
        "category": "Content writing",
        "title": "Developer-Focused Product Launch Announcement",
        "description": "Draft an engaging launch post highlighting technical architecture and utility.",
        "prompt": "Write a blog post announcing our new developer API gateway.",
        "notes": "Lacks audience persona, unique value proposition, tone of voice, call to action, and format constraints."
    },
    {
        "id": "content_newsletter",
        "category": "Content writing",
        "title": "Executive AI Newsletter Summary",
        "description": "Summarize weekly generative AI updates for Fortune 500 tech leaders.",
        "prompt": "Write a weekly newsletter section about recent AI developments.",
        "notes": "Missing word count constraints, executive tone, actionable business impact sections, and formatting style."
    },

    # 5. Data Analysis
    {
        "id": "data_churn",
        "category": "Data analysis",
        "title": "SaaS Churn Cohort Diagnostic",
        "description": "Identify root causes of customer drop-off using cohort retention analysis.",
        "prompt": "How do I analyze customer churn for my subscription app?",
        "notes": "Lacks dataset description, statistical methodology, metric definitions (LTV, CAC, MRR), and output format."
    },
    {
        "id": "data_ab_test",
        "category": "Data analysis",
        "title": "A/B Test Significance & Decision Framework",
        "description": "Evaluate conversion lift while guarding against sample ratio mismatch and p-hacking.",
        "prompt": "Help me interpret my A/B test results where variant B got 3.4% and control got 3.1%.",
        "notes": "Missing sample size, baseline conversion, statistical power, test duration, and confidence interval requirements."
    },

    # 6. Interview Preparation
    {
        "id": "interview_sys_design",
        "category": "Interview preparation",
        "title": "Staff System Design Mock Interview",
        "description": "Simulate an interactive FAANG-level system design interview for a distributed rate limiter.",
        "prompt": "Prepare me for a system design interview about designing a rate limiter.",
        "notes": "Lacks interviewer persona, iterative questioning flow, scale numbers (RPS), and latency SLA constraints."
    },
    {
        "id": "interview_behavioral",
        "category": "Interview preparation",
        "title": "Executive Leadership STAR Framework",
        "description": "Polish behavioral responses demonstrating conflict resolution and strategic tradeoff.",
        "prompt": "How do I answer 'Tell me about a time you had a conflict with a stakeholder'?",
        "notes": "Missing candidate level, industry context, STAR structure breakdown, and follow-up probing questions."
    }
]


def get_categories() -> List[str]:
    """Retrieve distinct template categories."""
    seen = []
    for t in TEMPLATES:
        if t["category"] not in seen:
            seen.append(t["category"])
    return seen


def get_templates_by_category(category: str) -> List[Dict[str, Any]]:
    """Filter templates by category."""
    if not category or category == "All":
        return TEMPLATES
    return [t for t in TEMPLATES if t["category"].lower() == category.lower()]
