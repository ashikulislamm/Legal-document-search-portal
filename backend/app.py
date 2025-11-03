from __future__ import annotations
import re
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


def _resolve_docs_dir() -> Path:
    """Resolve the documents directory.
    Prefers a sibling `docs/` next to this file, but will fall back to
    an older layout where docs lived under `venv/docs/`.
    """
    base_dir = Path(__file__).parent
    primary = base_dir / "docs"
    legacy = base_dir / "venv" / "docs"
    if primary.exists():
        return primary
    if legacy.exists():
        return legacy
    return primary  # default location even if it doesn't exist yet


DOCS_DIR = _resolve_docs_dir()
MIN_SUMMARY_SENTENCES = 2
MAX_SNIPPETS_PER_DOC = 3

app = FastAPI(title="Legal Search Mock API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Validate that documents are loaded on startup."""
    if not DOCS:
        raise RuntimeError(
            "No documents loaded. Please ensure .txt files exist in the docs directory."
        )
    print(f"API ready with {len(DOCS)} document(s) loaded.")


class GenerateRequest(BaseModel):
    query: str


class SearchResult(BaseModel):
    doc_id: str
    title: str
    score: float
    snippets: List[str]


class GenerateResponse(BaseModel):
    query: str
    results: List[SearchResult]
    summary: str
    meta: Dict[str, Any]


def _sentence_split(text: str) -> List[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", text.strip())
    return [p.strip() for p in parts if p.strip()]


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9]+", text.lower())


def _load_docs() -> Dict[str, Dict[str, str]]:
    """
    Load legal documents from the docs directory.
    Falls back to hardcoded documents if files are not found or empty.
    Returns a dictionary mapping document IDs to their metadata and content.
    """
    docs: Dict[str, Dict[str, str]] = {}

    # Try to load from files first
    if DOCS_DIR.exists():
        txt_files = sorted(DOCS_DIR.glob("*.txt"))
        for file_path in txt_files:
            try:
                text = file_path.read_text(encoding="utf-8").strip()
                if text:
                    doc_id = file_path.stem
                    title = doc_id.replace("_", " ").replace("-", " ").title()
                    docs[doc_id] = {"title": title, "text": text}
                else:
                    print(f"Warning: {file_path.name} is empty and will be skipped.")
            except Exception as e:
                print(f"Error reading {file_path.name}: {e}")
                continue

    # Fallback to hardcoded documents if no files were loaded
    if not docs:
        print("No documents found in files. Using fallback embedded documents.")
        docs = {
            "doc1": {
                "title": "Civil Liability Basics",
                "text": (
                    "Tort law addresses civil wrongs causing harm or loss to individuals or their property. "
                    "The fundamental principle of tort law is to provide compensation to victims who have suffered injury due to another party's wrongful conduct. "
                    "Negligence is a key concept requiring four essential elements: duty of care, breach of that duty, causation, and damages. "
                    "Duty of care establishes a legal obligation to exercise reasonable care towards others. "
                    "Breach occurs when the standard of care is not met. "
                    "Causation requires both factual and legal cause connecting the breach to the harm. "
                    "Damages refer to the actual injury or loss suffered. "
                    "Remedies in tort law include compensatory damages for economic and non-economic losses, punitive damages in cases of egregious conduct, and injunctions to prevent future harm. "
                    "Tort law serves to deter negligent behavior, compensate victims, and maintain social order by holding individuals accountable for their actions."
                ),
            },
            "doc2": {
                "title": "Contract Formation Guide",
                "text": (
                    "A valid contract requires several essential elements: offer, acceptance, consideration, and intention to create legal relations. "
                    "An offer is a clear proposal made by one party to another with the intent to be bound upon acceptance. "
                    "Acceptance must be unequivocal and communicated to the offeror. "
                    "Consideration represents something of value exchanged between parties, which distinguishes contracts from mere promises. "
                    "The intention to create legal relations demonstrates that parties intend their agreement to be legally enforceable. "
                    "Breach of contract occurs when a party fails to perform their obligations as specified in the agreement. "
                    "Material breaches substantially deprive the innocent party of the contract's benefit, while minor breaches are less significant. "
                    "Remedies for breach include damages to compensate for losses, specific performance to enforce the contract's terms, and rescission to cancel the agreement. "
                    "Contract law ensures predictability in commercial transactions and provides mechanisms for enforcing agreements fairly and efficiently."
                ),
            },
            "doc3": {
                "title": "Criminal Procedure Overview",
                "text": (
                    "Criminal procedure governs the process for investigating, prosecuting, and adjudicating alleged criminal offenses. "
                    "The system balances the state's interest in maintaining order with protecting individual rights. "
                    "Fundamental standards include the presumption of innocence, requiring the prosecution to prove guilt beyond reasonable doubt. "
                    "This high standard protects individuals from wrongful conviction. "
                    "The right to counsel ensures defendants have legal representation throughout the process. "
                    "The right to a fair and public trial prevents secret proceedings and ensures transparency. "
                    "Due process guarantees require that procedures be fair, consistent, and follow established legal rules. "
                    "Evidence rules protect against unreliable or prejudicial information influencing verdicts. "
                    "The exclusionary rule prevents illegally obtained evidence from being used in court. "
                    "These procedural safeguards maintain the integrity of the criminal justice system and protect against government overreach while ensuring that those who commit crimes are appropriately held accountable."
                ),
            },
            "doc4": {
                "title": "Property Law Fundamentals",
                "text": (
                    "Property law governs the ownership, use, and transfer of real and personal property. "
                    "Real property refers to land and structures permanently attached to land, while personal property encompasses movable items and intangible assets. "
                    "Ownership rights include the right to possess, use, transfer, and exclude others from the property. "
                    "Title represents legal ownership and can be transferred through sale, gift, inheritance, or adverse possession. "
                    "Easements grant limited rights to use another's property for specific purposes such as access or utilities. "
                    "Leases create temporary property interests where tenants obtain possessory rights for a specified period. "
                    "Zoning laws regulate land use to promote orderly development and protect community interests. "
                    "Eminent domain allows governments to acquire private property for public use with just compensation. "
                    "Property disputes often involve boundary issues, title defects, or conflicting claims that require resolution through negotiation, mediation, or litigation. "
                    "Understanding property law is essential for transactions, estate planning, and resolving ownership conflicts effectively."
                ),
            },
            "doc5": {
                "title": "Constitutional Law Principles",
                "text": (
                    "Constitutional law establishes the framework for government structure, powers, and limitations. "
                    "The constitution serves as the supreme law of the land, establishing the relationship between government branches and protecting individual rights. "
                    "Separation of powers divides authority among executive, legislative, and judicial branches to prevent concentration of power. "
                    "Federalism distributes powers between national and state governments, creating a system of dual sovereignty. "
                    "Judicial review empowers courts to examine and invalidate laws or actions that violate constitutional provisions. "
                    "Fundamental rights include freedom of speech, religion, and assembly protected by the Bill of Rights. "
                    "Equal protection requires that laws apply uniformly without unjust discrimination. "
                    "Due process guarantees fair procedures before deprivation of life, liberty, or property. "
                    "The commerce clause grants federal authority to regulate interstate economic activities. "
                    "Constitutional amendments adapt the document to changing circumstances while maintaining core democratic principles. "
                    "Constitutional interpretation involves balancing textual meaning, historical context, and contemporary needs to maintain a living framework that serves evolving society."
                ),
            },
            "doc6": {
                "title": "Employment Law Essentials",
                "text": (
                    "Employment law regulates the relationship between employers and employees, establishing rights and obligations for both parties. "
                    "Employment relationships may be at-will, where either party can terminate without cause, or governed by contracts specifying terms and conditions. "
                    "Discrimination based on race, gender, age, religion, disability, or other protected characteristics is prohibited by federal and state laws. "
                    "Workplace harassment creates hostile environments and violates anti-discrimination statutes when based on protected characteristics. "
                    "Wage and hour laws mandate minimum wages, overtime pay, and regulate working hours to protect workers' economic interests. "
                    "Workers' compensation provides benefits for job-related injuries or illnesses without requiring proof of employer fault. "
                    "Family and medical leave laws allow employees to take protected time off for health conditions or family responsibilities. "
                    "Occupational safety regulations require employers to provide safe working conditions and comply with health standards. "
                    "Employment contracts may include non-compete clauses, confidentiality agreements, and dispute resolution mechanisms. "
                    "Wrongful termination claims arise when dismissals violate contracts, public policy, or anti-discrimination laws. "
                    "Employment law balances protecting workers' rights with allowing employers flexibility to manage their operations effectively."
                ),
            },
        }
        print(f"✓ Using {len(docs)} fallback embedded document(s)")
    else:
        print(f"✓ Loaded {len(docs)} document(s) from {DOCS_DIR}")

    return docs


# Initialize documents at startup
DOCS = _load_docs()
DOC_SENTENCES = {k: _sentence_split(v["text"]) for k, v in DOCS.items()}


def _score_doc(query_tokens: List[str], text_tokens: List[str]) -> float:
    if not query_tokens or not text_tokens:
        return 0.0
    counts = sum(text_tokens.count(qt) for qt in query_tokens)
    return counts / max(1, len(text_tokens))


def _best_snippets(doc_id: str, query_tokens: List[str]) -> List[str]:
    sents = DOC_SENTENCES.get(doc_id, [])
    ranked: List[Tuple[int, str]] = []
    for s in sents:
        toks = _tokenize(s)
        hit = sum(toks.count(q) for q in query_tokens)
        if hit > 0:
            ranked.append((hit, s))
    ranked.sort(key=lambda x: (-x[0], len(x[1])))
    return [s for _, s in ranked[:MAX_SNIPPETS_PER_DOC]]


def _make_summary(sorted_docs: List[Tuple[str, float]], query_tokens: List[str]) -> str:
    collected: List[str] = []
    target_count = max(MIN_SUMMARY_SENTENCES, len(query_tokens))

    for doc_id, _ in sorted_docs:
        if len(collected) >= target_count:
            break
        sentences = DOC_SENTENCES.get(doc_id, [])
        for s in sentences:
            if len(collected) >= target_count:
                break
            toks = _tokenize(s)
            if query_tokens and any(q in toks for q in query_tokens):
                if s not in collected:
                    collected.append(s)

    if len(collected) < target_count and sorted_docs:
        for doc_id, _ in sorted_docs:
            if len(collected) >= target_count:
                break
            sentences = DOC_SENTENCES.get(doc_id, [])
            for s in sentences:
                if len(collected) >= target_count:
                    break
                if s not in collected:
                    collected.append(s)

    if len(collected) < MIN_SUMMARY_SENTENCES and sorted_docs:
        top_doc = sorted_docs[0][0]
        sentences = DOC_SENTENCES.get(top_doc, [])
        for s in sentences:
            if len(collected) >= MIN_SUMMARY_SENTENCES:
                break
            if s not in collected:
                collected.append(s)

    if not collected and DOC_SENTENCES:
        for doc_id in DOC_SENTENCES.keys():
            sentences = DOC_SENTENCES.get(doc_id, [])
            if sentences:
                collected = sentences[:MIN_SUMMARY_SENTENCES]
                break

    return " ".join(collected) if collected else "No relevant summary could be generated."


@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    if not DOCS:
        raise HTTPException(
            status_code=503,
            detail="Service unavailable: No documents loaded. Please check server configuration.",
        )

    t0 = time.time()
    query = (req.query or "").strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query must not be empty.")
    query_tokens = _tokenize(query)

    scored: List[Tuple[str, float]] = []
    for doc_id, meta in DOCS.items():
        score = _score_doc(query_tokens, _tokenize(meta["text"]))
        if score > 0:
            scored.append((doc_id, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    results: List[SearchResult] = []
    for doc_id, score in scored[:10]:
        snippets = _best_snippets(doc_id, query_tokens)
        results.append(
            SearchResult(
                doc_id=doc_id,
                title=DOCS[doc_id]["title"],
                score=round(float(score), 4),
                snippets=snippets or DOC_SENTENCES.get(doc_id, [])[:1],
            )
        )

    summary = _make_summary(scored, query_tokens)
    took_ms = int((time.time() - t0) * 1000)

    return GenerateResponse(
        query=query,
        results=results,
        summary=summary,
        meta={"took_ms": took_ms, "doc_count": len(DOCS)},
    )


@app.get("/healthz")
def healthz():
    return {"ok": True, "docs": len(DOCS)}


