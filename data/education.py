"""Educational modules and prompt engineering guides."""

from typing import List, Dict, Any

EDUCATIONAL_TOPICS: List[Dict[str, Any]] = [
    {
        "id": "role_prompting",
        "title": "Role Prompting (Persona Definition)",
        "badge": "Foundational",
        "concept": "Assigning an explicit persona or domain identity primes the model's latent representation, shaping vocabulary, technical depth, and viewpoint.",
        "why_it_matters": "Without a role, models default to an average, generalized conversational tone. An assigned role ('Senior Cloud Security Architect', 'K-12 Pedagogical Specialist') grounds the response in field-specific terminology and perspective.",
        "poor_example": "Explain how databases handle transactions.",
        "good_example": "Act as a Database Engine Core Developer specializing in PostgreSQL WAL and MVCC. Explain how ACID transactions are guaranteed during a sudden power loss.",
        "best_practices": [
            "Specify the level of seniority or specialization (e.g., 'Staff Distributed Systems Engineer' vs. 'programmer').",
            "Pair the role with the target audience (e.g., 'Explain to a junior developer' or 'Present to the CFO').",
            "Avoid theatrical roleplay unless writing creative fiction; focus on professional capability and perspective."
        ]
    },
    {
        "id": "context",
        "title": "Context Provision",
        "badge": "Contextual Grounding",
        "concept": "Supplying background situation, existing artifacts, audience familiarity, and domain assumptions.",
        "why_it_matters": "LLMs cannot guess unstated environmental constraints. Providing relevant context eliminates guesswork and prevents generic, unfocused replies.",
        "poor_example": "Review this code and tell me if it looks good.",
        "good_example": "We are migrating an e-commerce checkout service from Python 3.8 synchronous requests to Python 3.12 asyncio. The service handles ~12,000 requests per minute with a strict 250ms p99 SLA. Review this snippet specifically for connection pool exhaustion and memory leaks.",
        "best_practices": [
            "State the 'Why': What is the overarching business or technical goal?",
            "State the 'Where': Technical stack, runtime environment, version numbers, or organizational context.",
            "Include prior attempts or known limitations to avoid receiving obvious suggestions you have already dismissed."
        ]
    },
    {
        "id": "specificity",
        "title": "Specificity & Precision",
        "badge": "Signal-to-Noise",
        "concept": "Replacing vague terminology ('better', 'fast', 'short') with concrete scopes, numerical metrics, and definitive targets.",
        "why_it_matters": "Ambiguous language produces broad, superficial overviews. Specific instructions force the model to dedicate its generation budget to exact details.",
        "poor_example": "Give me some tips to improve our customer retention.",
        "good_example": "Provide 5 tactical retention strategies for a B2B enterprise SaaS product with a 14-day free trial. Focus specifically on day 3 through day 7 onboarding activation, where 40% of signups currently drop off.",
        "best_practices": [
            "Use exact quantifiers (e.g., 'Provide 3 trade-offs', 'Limit to top 4 failure modes').",
            "Define terms of art explicitly if your organization uses non-standard nomenclature.",
            "Eliminate fuzzy adjectives like 'comprehensive', 'actionable', or 'high-quality'—define what constitutes quality instead."
        ]
    },
    {
        "id": "constraints",
        "title": "Constraints & Guardrails",
        "badge": "Boundary Setting",
        "concept": "Setting explicit positive boundaries ('do this') and negative constraints ('do not do this') to prune unwanted outputs.",
        "why_it_matters": "Left unconstrained, models often over-explain, introduce unsolicited boilerplate, or propose tools outside your approved stack.",
        "poor_example": "Write a script to backup a database.",
        "good_example": "Write a Bash script to backup a MySQL 8 database to AWS S3. Constraints: Use only standard GNU coreutils and AWS CLI v2; do not install third-party Python packages; redact database credentials from stdout logs; include non-zero exit codes on any failed sub-step.",
        "best_practices": [
            "State negative constraints clearly ('Do NOT use external dependencies', 'Do NOT include conversational filler like \"Certainly! Here is...\"').",
            "Set strict ceiling limits (e.g., 'Maximum 200 words', 'No more than 5 bullet points').",
            "Specify edge-case behaviors (e.g., 'If the input is ambiguous, ask 2 clarifying questions before proceeding')."
        ]
    },
    {
        "id": "output_formatting",
        "title": "Output Formatting & Schema Control",
        "badge": "Structure & Integration",
        "concept": "Defining the exact visual or semantic structure of the output (JSON, Markdown tables, YAML, executive summary headers).",
        "why_it_matters": "Unstructured text requires human parsing or fragile regex. Structured formatting makes outputs immediately consumable by humans or downstream automated workflows.",
        "poor_example": "Compare Kubernetes and Docker Swarm.",
        "good_example": "Compare Kubernetes and Docker Swarm for a team of 4 engineers managing 15 microservices. Present your analysis as a Markdown comparison table with columns: 'Capability', 'Kubernetes', 'Docker Swarm', and 'Decision Factor'. Follow the table with a 3-sentence verdict.",
        "best_practices": [
            "Specify schemas or provide a template skeleton directly in the prompt.",
            "Designate specific Markdown headers (e.g., '## Executive Summary', '## Technical Trade-offs', '## Action Items').",
            "For programmatic ingestion, specify JSON schemas or use Gemini's structured output mode."
        ]
    },
    {
        "id": "few_shot",
        "title": "Few-Shot Prompting (In-Context Exemplars)",
        "badge": "Pattern Priming",
        "concept": "Providing 2-3 input-output exemplar pairs within the prompt to demonstrate the desired transformation, tone, and schema.",
        "why_it_matters": "Demonstrations communicate subtle stylistic patterns, edge-case handlings, and shorthand formats much faster and more reliably than lengthy prose instructions.",
        "poor_example": "Classify these customer support tickets.",
        "good_example": "Classify the sentiment and root problem of customer messages. Follow this exact format:\n\nInput: 'The login page keeps saying error 500 when I click submit.'\nCategory: Technical Bug | Severity: High | Sentiment: Frustrated\n\nInput: 'Is there a student discount for annual plans?'\nCategory: Billing Inquiry | Severity: Low | Sentiment: Neutral\n\nInput: 'Your new dashboard is so confusing, I cannot find my export button!'\nCategory: UI/UX Feedback | Severity: Medium | Sentiment: Negative\n\nInput: '{ticket_text}'\nCategory:",
        "best_practices": [
            "Ensure exemplars represent realistic diversity, including tricky edge cases.",
            "Keep formatting strictly uniform across all shots.",
            "2 to 4 high-quality exemplars are usually sufficient for modern Gemini models."
        ]
    },
    {
        "id": "chain_of_thought",
        "title": "Chain-of-Thought (Reasoning Guidance)",
        "badge": "Cognitive Decomposition",
        "concept": "Instructing the model to break down complex multi-step problems into sequential analytical stages before generating a final conclusion.",
        "why_it_matters": "Direct answering forces the model to predict the final token before computing intermediate steps, frequently leading to calculation errors and logic leaps. Decomposing the problem vastly enhances accuracy.",
        "poor_example": "Is it cheaper to run an EC2 m5.large on-demand for 1 year or buy an upfront 1-year reserved instance?",
        "good_example": "Calculate the total cost comparison between an on-demand m5.large EC2 instance versus a 1-year Standard All-Upfront Reserved Instance. Break your response into: Step 1: List published hourly rates and upfront costs. Step 2: Calculate total annual cost for 8,760 hours on-demand. Step 3: Compute the dollar savings and percentage difference. Step 4: Final recommendation based on workload predictability.",
        "best_practices": [
            "Request concise reasoning summaries or key intermediate steps rather than unstructured stream-of-consciousness or private internal reasoning.",
            "Ask for step-by-step verification (e.g., 'First verify prerequisites, then evaluate boundary conditions, then output conclusion').",
            "Encourage the model to explicitly state its assumptions before delivering the final answer."
        ]
    }
]
