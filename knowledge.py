"""Verified DStarix Techno context used by the chatbot.

The project keeps this as a simple static knowledge base for a Week 2
Prompt Templates + LangChain assignment. It is not RAG and does not scrape
websites at runtime.
"""

OFFICIAL_LINKS = {
    "website": "https://www.dstarix.in/",
    "about": "https://www.dstarix.in/about",
    "services": "https://www.dstarix.in/services",
    "pricing": "https://www.dstarix.in/pricing",
    "contact": "https://www.dstarix.in/contact",
    "careers": "https://www.dstarix.in/careers",
    "linkedin": "https://www.linkedin.com/company/dstarix-techno/",
    "linkedin_jobs": "https://www.linkedin.com/company/dstarix-techno/jobs/",
}

CURRENT_OPENINGS_LAST_VERIFIED = "2026-07-19"

CURRENT_OPENINGS = [
    {
        "role": "Senior AI Engineer",
        "team": "Engineering",
        "location": "Remote / Bengaluru",
        "type": "Full-time",
        "source_url": "https://www.dstarix.in/careers#open-roles",
    },
    {
        "role": "ML Research Engineer",
        "team": "Research",
        "location": "Remote",
        "type": "Full-time",
        "source_url": "https://www.dstarix.in/careers#open-roles",
    },
    {
        "role": "Forward-Deployed Engineer",
        "team": "Delivery",
        "location": "Hybrid / Bengaluru",
        "type": "Full-time",
        "source_url": "https://www.dstarix.in/careers#open-roles",
    },
    {
        "role": "Senior Product Designer",
        "team": "Design",
        "location": "Remote",
        "type": "Full-time",
        "source_url": "https://www.dstarix.in/careers#open-roles",
    },
    {
        "role": "AI Solutions Architect",
        "team": "Solutions",
        "location": "Remote / EU",
        "type": "Full-time",
        "source_url": "https://www.dstarix.in/careers#open-roles",
    },
    {
        "role": "Developer Relations Engineer",
        "team": "Growth",
        "location": "Remote",
        "type": "Full-time",
        "source_url": "https://www.dstarix.in/careers#open-roles",
    },
]

SOURCE_REFERENCES = {
    "Company Overview": [
        OFFICIAL_LINKS["website"],
        OFFICIAL_LINKS["about"],
        "User-provided company description",
    ],
    "Services": [
        "https://www.dstarix.in/services",
        "https://www.dstarix.in/ai-solutions",
        "https://www.dstarix.in/generative-ai",
        "https://www.dstarix.in/agentic-ai",
        "https://www.dstarix.in/rag-solutions",
        "https://www.dstarix.in/custom-llm-development",
        "https://www.dstarix.in/workflow-automation",
        "https://www.dstarix.in/voice-ai",
        "https://www.dstarix.in/ai-chatbots",
    ],
    "Industries": ["https://www.dstarix.in/industries"],
    "Pricing": [OFFICIAL_LINKS["pricing"]],
    "Careers": [OFFICIAL_LINKS["careers"], OFFICIAL_LINKS["linkedin_jobs"]],
    "Contact": [OFFICIAL_LINKS["contact"]],
    "FAQ": ["https://www.dstarix.in/faq"],
}

COMPANY_CONTEXT = """
DStarix Techno verified company context

Important boundaries:
- Do not invent services, contact details, job openings, internship openings, salaries, clients, statistics, policies, or guarantees.
- Do not claim to browse the web, check LinkedIn, or read live job posts.
- If a detail is not present in this context, say that it is not available in the verified knowledge base.

Company Overview:
- DStarix Techno is an AI and software technology company focused on building enterprise AI systems, automation tools, enterprise software, and Agentic AI solutions.
- Tagline: "Building Intelligent Solutions for the AI-Driven Future."
- Industry: Software Development.
- Founded: 2026, confirmed by the user.
- Headquarters information provided by the user: Bangalore, Karnataka.
- The official website describes DStarix Techno as a company that builds enterprise AI systems that deliver measurable business value, including generative and agentic products and private, production-grade deployments.
- The broader goal is to combine artificial intelligence with modern software engineering to build useful digital products and solve real business problems.

Mission / Purpose:
- DStarix Techno focuses on dependable AI in business operations.
- The company emphasizes production-ready systems, evaluation, guardrails, observability, security, scalability, and measurable business outcomes.

AI Services:
- Generative AI applications.
- Agentic AI and autonomous AI systems.
- RAG solutions over private business knowledge.
- Custom LLM development.
- Enterprise AI platforms.
- Workflow automation.
- Voice AI.
- AI chatbots and virtual assistants.
- AI consulting, AI development, and AI automation.
- Document AI, knowledge management, predictive AI, computer vision, private AI, MLOps, and cloud AI are listed on the services page as related capabilities.

Generative AI:
- DStarix builds generative AI systems for content, code, imagery, and structured data.
- The official site emphasizes brand grounding, policy guardrails, structured outputs, PII redaction, human-in-the-loop review, model routing, caching, distillation, and evaluation for factuality, tone, and safety.

Agentic AI:
- DStarix builds multi-agent systems that can plan, use tools, and complete multi-step workflows.
- The official site emphasizes guardrailed autonomy, typed tool contracts, approvals for high-impact actions, observability, audit trails, retries, escalation, and human handoff when confidence is low.

RAG Solutions:
- DStarix builds retrieval-augmented generation systems that answer from a company's documents, tickets, and databases.
- The official site emphasizes hybrid retrieval, reranking, grounding checks, citations, permission-aware access, freshness sync, and evaluation.
- Typical RAG use cases include enterprise knowledge assistants, customer support deflection, policy and compliance Q&A, technical documentation search, contract and document retrieval, federated search, and access-controlled retrieval.

Custom LLM Development:
- DStarix provides fine-tuning, distillation, and alignment for models that need to fit a specific domain, strict output format, cost target, or latency target.
- The official site mentions data curation, synthetic data augmentation, LoRA/QLoRA, full fine-tuning when warranted, distillation, and preference alignment.

Enterprise AI:
- DStarix helps organizations move from scattered AI pilots to governed AI platforms.
- Enterprise AI work may include reference architectures, shared services, model gateways, governance, policy controls, SSO, RBAC, multi-tenant isolation, cost controls, observability, reusable components, and platform engineering.

Workflow Automation and AI Automation:
- DStarix automates multi-step, cross-system processes using AI to read context, classify information, extract from unstructured inputs, make judgment calls, and complete work across systems.
- The official site emphasizes process mapping, integrations, SLA monitoring, alerting, human approval gates, confidence thresholds, and exception handling.

Voice AI:
- DStarix builds real-time voice agents for support, scheduling, and telephony.
- The official site mentions streaming speech recognition, speech synthesis, natural turn-taking, barge-in, SIP telephony integration, grounded answers, and real actions.

AI Chatbots:
- DStarix builds chat assistants for customer support, lead qualification, onboarding, order/account actions, appointment booking, IT/HR helpdesk, proactive outreach, feedback collection, and multilingual coverage.
- The official site emphasizes knowledge grounding, citations, human handoff, omnichannel deployment, analytics, safety guardrails, tone control, and PII handling.

Technologies / AI Ecosystem:
- Models listed on the official site include Claude, GPT-4 class models, Llama, Mistral, Gemini, and fine-tuned open models.
- Orchestration and runtime tools listed include LangGraph, LlamaIndex, custom agent runtimes, Temporal, and Model Context Protocol.
- Data and retrieval tools listed include pgvector, Pinecone, Weaviate, Elasticsearch, and hybrid search.
- Infrastructure listed includes AWS, GCP, Azure, Kubernetes, vLLM, and Ray.
- Evaluation and observability tools listed include Braintrust, Ragas, custom evaluation harnesses, LLM-as-judge, human review, OpenTelemetry, Langfuse, Datadog, Prometheus, and Grafana.

Industries Served:
- Financial Services: risk, fraud, advisory copilots, underwriting copilots, regulatory reporting, and client advisory.
- Healthcare & Life Sciences: clinical documentation, research acceleration, clinical scribing, prior authorization, literature review, and patient triage.
- Manufacturing: vision inspection, predictive maintenance, defect detection, supply planning, and digital twins.
- Retail & E-commerce: personalization, merchandising, support automation, product discovery, demand forecasting, and content generation.
- Legal & Compliance: contract intelligence, eDiscovery, policy Q&A, and due diligence.
- Logistics & Supply Chain: routing, forecasting, ETA prediction, exception triage, and document AI.
- Technology & SaaS: AI features, in-product copilots, code assistance, support deflection, and analytics.
- Energy & Utilities: grid optimization, predictive asset intelligence, load forecasting, asset monitoring, field copilots, and safety vision.

How DStarix Works With Clients:
- The official website describes a five-stage delivery model: Discover, Design, Build, Deploy, and Scale.
- Discover: map high-value use cases, quantify ROI, and pressure-test feasibility.
- Design: create reference architecture, data flows, guardrails, and an evaluation strategy.
- Build: use rapid, evaluation-driven iteration and show working software regularly.
- Deploy: ship to the customer's cloud or on-prem environment with monitoring, canary rollouts, and rollback.
- Scale: optimize cost and latency, expand workflows, and enable the client's team to own the system.

Frequently Asked Questions:
- Production timelines: the FAQ says most pilots reach a production-ready prototype in 6 to 9 weeks, while full builds typically run 3 to 5 months depending on integrations and compliance requirements.
- Data privacy: the FAQ says DStarix can deploy to a customer's VPC or on-prem environment with open models when required, with zero data egress and auditability.
- Model choice: DStarix says it is model-agnostic and selects or combines frontier and open models based on accuracy, latency, cost, and data-residency needs.
- Hallucination reduction: the site emphasizes grounding answers in approved sources, citations, guardrails, evaluation harnesses, and instructing assistants to say when they do not know.
- Ongoing operations: the site mentions monitoring, MLOps, rollback, support, and either ongoing operations or handoff depending on the engagement.

Pricing Guidance:
- The pricing page lists engagement models, not fixed prices for every project.
- Pilot: fixed-scope pilot listed at $25k, intended to prove one high-value use case with a production-ready prototype.
- Build: custom pricing per engagement for end-to-end production AI system delivery.
- Enterprise: annual partnership discussed with sales, including dedicated delivery pod, platform and governance, private/on-prem deployment, roadmap, and support.
- For exact project pricing, users should contact DStarix through the pricing or contact page.

Careers and Internships:
- DStarix has an official careers page and an official LinkedIn Jobs page.
- Current openings last verified from the official DStarix Careers page on 2026-07-19:
  1. Senior AI Engineer, Engineering, Remote / Bengaluru, Full-time.
  2. ML Research Engineer, Research, Remote, Full-time.
  3. Forward-Deployed Engineer, Delivery, Hybrid / Bengaluru, Full-time.
  4. Senior Product Designer, Design, Remote, Full-time.
  5. AI Solutions Architect, Solutions, Remote / EU, Full-time.
  6. Developer Relations Engineer, Growth, Remote, Full-time.
- The verified careers page did not list a Data Analyst, DA, fresher, or internship opening at the time above.
- For current jobs and internships, users should still verify the official Careers page and LinkedIn Jobs page because openings may change after the last verification date.

Contact / Getting Started:
- Official website: https://www.dstarix.in/
- Contact page: https://www.dstarix.in/contact
- Official email listed on the contact page: contact@dstarix.in
- Contact form fields include full name, work email, company, project type, and project details.
- The contact page says enquiries are answered within one business day.
- Delivery pods listed on the contact page: Bengaluru, Belagavi, and Hyderabad.
- HQ listed on the contact page: Bengaluru, India, Bengaluru 560104.

Official Links:
- Website: https://www.dstarix.in/
- About: https://www.dstarix.in/about
- Services: https://www.dstarix.in/services
- Pricing: https://www.dstarix.in/pricing
- Contact: https://www.dstarix.in/contact
- Careers: https://www.dstarix.in/careers
- Official LinkedIn: https://www.linkedin.com/company/dstarix-techno/
- Official LinkedIn Jobs: https://www.linkedin.com/company/dstarix-techno/jobs/
"""


def get_company_context() -> str:
    """Return the static verified company context for the prompt."""
    return COMPANY_CONTEXT.strip()


def get_current_openings() -> list[dict[str, str]]:
    """Return current openings captured from the official Careers page."""
    return CURRENT_OPENINGS
