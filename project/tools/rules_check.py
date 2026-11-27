#!/usr/bin/env python3
"""Lint knowledge-base files and benchmark questions. Run before every merge: python3 project/tools/rules_check.py
Exit code 0 = pass, 1 = problems found. Allowed values come from
project/tools/rules_check_values.yaml."""
import glob, hashlib, os, re, sys, yaml

# Windows returns paths with '\'; every check here compares paths with '/' (the repository's form).
_glob_native = glob.glob
glob.glob = lambda pattern, **kw: [p.replace(os.sep, '/') for p in _glob_native(pattern, **kw)]

HARNESS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'harness')
sys.path.insert(0, HARNESS)
from knowledge_loader import split, NOT_INDEXED, FILE_LINK  # noqa: E402  (the parser the harness uses, so lint and retrieval read files the same way)

# Old id -> current id for moved knowledge files. A repository tool, not product: the harness never reads it.
MOVED_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'moved_ids.yaml')
MOVED = (yaml.safe_load(open(MOVED_FILE, encoding='utf-8')) or {}) if os.path.exists(MOVED_FILE) else {}

TERMS = 'project/tools/rules_check_values.yaml'
REQUIRED = ['id', 'retriever_guide', 'scope', 'technology', 'pillar', 'product',
            'source', 'corrections', 'review_notes', 'status']
LIST_FIELDS = ['technology', 'pillar', 'product', 'object', 'instance', 'layer']
LINK_FIELDS = ['related', 'internal_derive', 'same_name', 'same_meaning']
OLD_FIELDS = ['type', 'resources', 'objects', 'derived_from', 'same_name_as', 'kind']

def load_allowed():
    return yaml.safe_load(open(TERMS, encoding='utf-8'))

def main():
    allowed = load_allowed()
    problems = []
    def bad(path, msg): problems.append(f'{path}: {msg}')
    linked_images = set()

    files = [f for f in sorted(glob.glob('knowledge/**/*.md', recursive=True)) if f not in NOT_INDEXED]  # up-front text: checked in check_terms
    docs = {}
    for f in files:
        fm, body = split(f)
        if fm is None:
            bad(f, 'no metadata block at the end (## Metadata + yaml)'); continue
        docs[f] = (fm, body)

    ids = {fm.get('id') for fm, _ in docs.values()}
    EXEMPT_WORDS = {'knowledge/glossary.md'}  # defines the avoided words
    for f, (fm, body) in docs.items():
        expected = f[len('knowledge/'):-3]
        if f.endswith('/README.md'):  # a folder's main file: README.md opens on GitHub; its id keeps a descriptive name
            if not (str(fm.get('id', '')).startswith(expected[:-len('README')]) and '/' not in fm['id'][len(expected) - len('README'):]
                    and not fm['id'].endswith('/README')):
                bad(f, f'id "{fm.get("id")}" of a README.md must be "{expected[:-len("README")]}<descriptive-name>"')
        elif fm.get('id') != expected:
            bad(f, f'id "{fm.get("id")}" does not match path "{expected}"')
        for k in REQUIRED:
            if k not in fm: bad(f, f'missing field "{k}"')
        for k in OLD_FIELDS:
            if k in fm: bad(f, f'old field "{k}" is no longer used')
        for k in ['retriever_guide', 'scope', 'metric_class', 'status']:
            v = fm.get(k)
            if v is not None and v not in allowed[k]:
                bad(f, f'{k} "{v}" not allowed. Allowed: {", ".join(allowed[k])}')
        for k in LIST_FIELDS:
            v = fm.get(k)
            if v is None: continue
            if not isinstance(v, list): bad(f, f'{k} must be a list'); continue
            for x in v:
                if x not in allowed[k]:
                    hint = ' (vCPU is an instance: use instance: per-vcpu)' if k == 'object' and str(x).lower() == 'vcpu' else ''
                    bad(f, f'{k} "{x}" not allowed{hint}. Allowed: {", ".join(allowed[k])}')
        for k in LINK_FIELDS:
            for r in fm.get(k) or []:
                if r not in ids: bad(f, f'{k} link "{r}" does not exist')
        # every image link needs an entry in metadata 'images' with valid tags
        entries = {e.get('path'): e for e in (fm.get('images') or []) if isinstance(e, dict)}
        body_imgs = set(re.findall(r'!\[[^\]]*\]\(([^)]+)\)', body))
        for p in body_imgs - set(entries): bad(f, f'image {p} has no entry in metadata images')
        for p in set(entries) - body_imgs: bad(f, f'metadata images entry {p} is not linked in the body')
        for p, e in entries.items():
            for k in ('product', 'object', 'image_type'):
                vals = e.get(k)
                if not vals: bad(f, f'images entry {p}: {k} missing'); continue
                for x in (vals if isinstance(vals, list) else [vals]):
                    if x not in allowed[k]: bad(f, f'images entry {p}: {k} "{x}" not allowed')
            if not e.get('metric') and not e.get('topic'):
                bad(f, f'images entry {p}: needs metric or topic')
        for img in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', body):
            full = os.path.normpath(os.path.join(os.path.dirname(f), img))
            linked_images.add(full)
            if not os.path.exists(full):
                bad(f, f'image not found: {img}')
        for r in re.findall(r'`((?:vsphere|guest-os|sp5-framework|vcf-operations)/[a-z0-9\-/]+)`', body):
            if r not in ids: bad(f, f'inline link "{r}" does not exist')
        # vSphere folders: architecture/, technology/<tech>/, object-types/<object>/, tools/<ui>/ (esxtop, vsphere-client; screens/ inside).
        if f.startswith('knowledge/vsphere/'):
            parts = f.split('/')
            if parts[2] not in VSPHERE_TOP:
                bad(f, f'knowledge/vsphere/ holds only {", ".join(VSPHERE_TOP)}/')
            elif parts[2] == 'technology' and parts[3] not in allowed['technology']:
                bad(f, f'technology folder "{parts[3]}" is not a technology tag value')
            elif parts[2] == 'object-types' and parts[3] not in OBJECT_FOLDERS:
                bad(f, f'object-types folder "{parts[3]}" not allowed. Allowed: {", ".join(OBJECT_FOLDERS)}')
            elif parts[2] == 'tools' and parts[3] not in allowed['ui']:
                bad(f, f'tools folder "{parts[3]}" is not a ui tag value ({", ".join(allowed["ui"])})')
        if f.endswith('-alerts.md'):
            if not ALERT_FILE.fullmatch(f[len('knowledge/'):-3]):
                bad(f, 'alert file must be vsphere/object-types/<object>/<object>-alerts, or guest-os/guest-os-alerts: an alert fires on one object type, never on a technology')
            if fm.get('retriever_guide') != 'what-to-set': bad(f, 'alert file must have retriever_guide: what-to-set')
        if f.startswith('knowledge/sp5-framework/'):
            if fm.get('scope') != 'sp5-framework': bad(f, 'file in knowledge/sp5-framework/ must have scope: sp5-framework')
            if len(f.split('/')) > 3 and f.split('/')[2] not in PILLAR_FOLDERS: bad(f, f'pillar folder not allowed. Allowed: {", ".join(PILLAR_FOLDERS)}')
        if '/screens/' in f:
            if fm.get('ui') not in allowed['ui']: bad(f, f'screen file needs ui: {", ".join(allowed["ui"])}')
            if not fm.get('ui_version'): bad(f, 'screen file needs ui_version')
            for r in fm.get('metrics_shown') or []:
                if r not in ids: bad(f, f'metrics_shown link "{r}" does not exist')
        if f.startswith('knowledge/vcf-operations/'):
            if fm.get('scope') != 'vcf-operations': bad(f, 'file in knowledge/vcf-operations/ must have scope: vcf-operations')
            if len(f.split('/')) > 3 and f.split('/')[2] not in VCF_OPERATIONS_TOP: bad(f, f'knowledge/vcf-operations/ holds files and only {", ".join(VCF_OPERATIONS_TOP)}/')
        # A VM is a virtual motherboard. The Guest OS (Windows, Linux) is not a Broadcom product and not part of the VM:
        # its knowledge lives in knowledge/guest-os/, outside knowledge/vsphere/.
        layer = fm.get('layer') or []
        title = body.lstrip().split('\n', 1)[0]
        if f.startswith('knowledge/guest-os/'):
            if fm.get('scope') != 'guest-os': bad(f, 'file in knowledge/guest-os/ must have scope: guest-os')
            if layer != ['guest-os']: bad(f, 'file in knowledge/guest-os/ must have layer: [guest-os]')
            if 'VirtualMachine' in (fm.get('object') or []): bad(f, 'Guest OS file must not have object VirtualMachine: the Guest OS is a layer, not the VM')
        else:
            # Boundary files (Guest OS vs VM, Guest OS sizing from VM data) stay in vSphere; Guest OS metrics never do.
            if 'guest-os' in layer or fm.get('scope') == 'guest-os' or (fm.get('retriever_guide') == 'metric-meaning' and title.startswith(('# Guest OS ', '# Windows', '# Linux'))):
                bad(f, 'Guest OS knowledge must live in knowledge/guest-os/, not under vSphere')
        # The kind of a file is its retriever_guide, not its folder: a kind folder exists only with 2 or more files (2026-11-12).
        if '/metrics/' in f and fm.get('retriever_guide') != 'metric-meaning': bad(f, 'file in metrics/ must have retriever_guide: metric-meaning')
        if fm.get('retriever_guide') == 'metric-meaning' and '/tools/' not in f and not f.startswith('knowledge/sp5-framework/'):
            if f.startswith('knowledge/guest-os/'):
                pass  # Guest OS metrics have no vSphere object; rules below
            elif not fm.get('object'): bad(f, 'metric file must have object')
            if '/metrics/virtual-motherboard/' in f and (fm.get('layer') or []) != ['virtual-motherboard']:
                bad(f, 'VM metric file must have layer: [virtual-motherboard]')
            if not fm.get('metric_class'): bad(f, 'metric file must have metric_class')
            m = re.search(r'/metrics/(virtual-motherboard|host|cluster|datastore|distributed-switch)/', f)
            if m and len(fm.get('object') or []) != 1:
                bad(f, f'a metric file in metrics/{m.group(1)}/ has exactly one object type')
        # Writing style (audit markers, words to avoid, AI-speak) is the review's job, not lint's (2026-11-10). Titles and headings: check_titles (Q-E2-181).

    seen_ids, level_numbers, pairs = {}, {}, {}
    for f in sorted(glob.glob('benchmark/questions/**/*.md', recursive=True)):
        t = open(f, encoding='utf-8').read()  # benchmark questions: metadata at the end, like knowledge files
        if t.startswith('---\n'): bad(f, 'front matter at the top: move it to a ## Metadata section at the end')
        fm, _ = split(f)
        if fm is None: bad(f, 'missing ## Metadata section with one yaml block at the end'); fm = {}
        for r in (fm or {}).get('knowledge') or []:
            if r in MOVED: bad(f, f'knowledge link "{r}" moved: use "{MOVED[r]}" (project/tools/moved_ids.yaml)')
            elif r not in ids: bad(f, f'knowledge link "{r}" does not exist')
        for k in ('product', 'technology'):
            v = (fm or {}).get(k)
            if not isinstance(v, list) or not v: bad(f, f'{k} must be a non-empty list')
            else:
                for x in v:
                    if x not in allowed[k]: bad(f, f'{k} "{x}" not allowed')
        if os.path.dirname(f) != 'benchmark/questions': bad(f, 'questions live in one flat folder: benchmark/questions/')
        qid = str((fm or {}).get('id') or '')
        if not re.fullmatch(r'\d{4}', qid): bad(f, 'id must be a stable 4-digit number, quoted, e.g. "0007" (benchmark/README.md)')
        elif qid in seen_ids: bad(f, f'id {qid} is also used by {seen_ids[qid]}')
        else: seen_ids[qid] = f
        if 'pair' in (fm or {}): pairs[qid] = (f, str((fm or {}).get('pair') or ''))  # paired questions (benchmark/design.md, section 3.9)
        lv = (fm or {}).get('level')
        mm = re.match(r'L(\d)-(\d{3})-', os.path.basename(f))
        if not mm or not isinstance(lv, int) or int(mm.group(1)) != lv // 100:
            bad(f, f'file name must start with L{(lv or 0) // 100}-<nn>- (benchmark/README.md); run project/tools/question_renumber.py')
        else: level_numbers.setdefault(lv, []).append(int(mm.group(2)))
        for a in (fm or {}).get('attachments') or []:
            if not str(a).startswith(f'{qid}/'): bad(f, f'attachment {a} must live in the folder {qid}/')
        for k in ('scope', 'area', 'tests', 'pillar', 'format', 'input_type'):
            if k in (fm or {}): bad(f, f'tag "{k}" is no longer used (benchmark/README.md, section Tags removed)')
        if (fm or {}).get('task') not in ('read-metric', 'troubleshoot', 'decide-capacity', 'explain-mechanism', 'judge-setting'):
            bad(f, 'task must be read-metric, troubleshoot, decide-capacity, explain-mechanism or judge-setting (benchmark/design.md, section 3.1)')
        if (fm or {}).get('origin') not in ('book', 'quiz', 'real-ticket', 'synthetic'):
            bad(f, 'origin must be book, quiz, real-ticket or synthetic')
        st = (fm or {}).get('status')
        if st not in allowed['question_status']:
            bad(f, f'status must be one of {", ".join(allowed["question_status"])}')
        for k, allowed_k in (('object', 'question_object'), ('tool', 'question_tool')):
            v = (fm or {}).get(k)
            if v is not None and (not isinstance(v, list) or any(x not in allowed[allowed_k] for x in v)):
                bad(f, f'{k} must be a list of {", ".join(allowed[allowed_k])}')
        if st in ('draft', 'reviewed'):  # coverage tags on every question that runs (benchmark/design.md, section 3)
            for k in ('object', 'tool', 'knowledge_main', 'misconception_type'):
                if k not in (fm or {}): bad(f, f'{k} is missing (benchmark/README.md, section Metadata tags)')
        mt = (fm or {}).get('misconception_type') or []
        if not isinstance(mt, list): bad(f, 'misconception_type must be a list')
        else:
            for x in mt:
                if x not in allowed['misconception_type']: bad(f, f'misconception_type "{x}" not allowed')
        prompt_m = re.search(r'## Prompt\n(.*?)\n## ', t, re.S)
        prompt_t = prompt_m.group(1) if prompt_m else ''
        if st not in ('retired', 'deferred', 'awaiting-input'):  # every question that runs
            seen = '\n'.join([t.split('\n', 1)[0], prompt_t] + [m.group(1) for m in re.finditer(
                r'^## (?:Answers|Explanation)\n(.*?)(?=^## |\Z)', t, re.S | re.M)])
            for pat, hint in allowed['question_fairness'].items():
                m = re.search(pat, seen)
                if m: bad(f, f'fairness: "{m.group(0)}" is not public vocabulary ({hint}; benchmark/design.md, section 6.1)')
            stem_t = re.split(r'\n\s*- [A-Y]\. ', '\n' + prompt_t, maxsplit=1)[0]  # options are claims, not hints
            for pat, hint in allowed['question_prompt_hints'].items():
                if 'plural' in hint and re.search(r'(?i)which statements are correct', stem_t):
                    continue  # a part question inside a plural closing line ("What is the most likely cause ...? Which statements are correct?")
                m = re.search(pat, stem_t if 'plural' in hint else '\n'.join(
                    l for l in prompt_t.split('\n') if not re.match(r'\s*- [A-Y]\. ', l)))  # stem and footer
                if m: bad(f, f'prompt: "{m.group(0)}" {hint} (benchmark/design.md, section 6.2)')
        if st not in ('retired', 'awaiting-input'):
            atts_q = [str(a) for a in (fm or {}).get('attachments') or []]
            linked = re.findall(r'\]\((\d{4}/[^)\s]+)\)', prompt_t)
            for a in atts_q:
                if a not in linked: bad(f, f'attachment {a} is not linked in ## Prompt: link the words that refer to it, e.g. [the attached chart]({a})')
                if a.lower().endswith('.csv') and os.path.exists(os.path.join('benchmark', 'questions', a)):
                    n = len(open(os.path.join('benchmark', 'questions', a), encoding='utf-8-sig').read())
                    if n > allowed['question_csv_max_chars']:
                        bad(f, f'{a} has {n} characters, above {allowed["question_csv_max_chars"]}: the runner puts it in the prompt')
            for a in linked:
                if a not in atts_q: bad(f, f'## Prompt links {a}, which is not in attachments')
        if (fm or {}).get('status') == 'awaiting-input' and '\n## Input to supply\n' not in t:
            bad(f, 'awaiting-input question needs a ## Input to supply section describing the screenshot or table')
        if not (fm or {}).get('knowledge'):
            bad(f, 'knowledge must list at least one knowledge id')
        km = (fm or {}).get('knowledge_main')
        if km is not None and km not in ((fm or {}).get('knowledge') or []):
            bad(f, f'knowledge_main "{km}" must also be listed in knowledge (benchmark/README.md)')
        at = (fm or {}).get('answer_type')
        if at != 'deterministic':
            bad(f, f'answer_type "{at}" must be deterministic: every question is multiple choice (Q-E2-199; benchmark/design.md, section 3.3)')
        if (fm or {}).get('level') not in (100, 200, 300, 400):
            bad(f, 'level must be 100, 200, 300 or 400 (benchmark/design.md, section 3.2)')
        atts = (fm or {}).get('attachments') or []
        derived = ([ 'table'] if any(a.lower().endswith(('.csv', '.xlsx', '.xls')) for a in atts) else []) + \
                  (['screenshot'] if any(a.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) for a in atts) else [])
        if sorted((fm or {}).get('input') or []) != sorted(derived or ['text']):
            bad(f, f'input must be {derived or ["text"]}, from the attachments (benchmark/design.md, section 3.4)')
        if at == 'deterministic':
            prompt = re.search(r'## Prompt\n(.*?)\n## ', t, re.S)
            letters = set(re.findall(r'^(?:[-*]\s+)?([A-Y])\.\s', prompt.group(1), re.M)) if prompt else set()
            if 'answer' in fm: bad(f, 'metadata "answer" is no longer used: the key is the section ## Answers (benchmark/README.md)')
            am = re.search(r'^## Answers\n(.*?)(?=^## |\Z)', t, re.S | re.M)
            if not am or not re.fullmatch(r'[A-Y](, [A-Y])*', am.group(1).strip()):
                bad(f, '## Answers must hold the correct letters only, e.g. "A, C, D" (benchmark/README.md)')
            else:
                for x in am.group(1).strip().split(', '):
                    if x not in letters: bad(f, f'## Answers letter {x} is not an option in ## Prompt')
            em = re.search(r'^## Explanation\n(.*?)(?=^## |\Z)', t, re.S | re.M)
            if not em: bad(f, 'no ## Explanation: one bullet per option, why it is right or wrong (benchmark/README.md)')
            else:
                for x in sorted(letters):
                    if not re.search(rf'^- {x}\b', em.group(1), re.M): bad(f, f'## Explanation has no bullet for option {x}')
            for x in fm.get('misconception') or []:
                if str(x) not in letters: bad(f, f'misconception letter {x} is not an option in ## Prompt')
            for old_h in ('Expected key points', 'Likely wrong answer'):
                if re.search(rf'^## {old_h}$', t, re.M): bad(f, f'section ## {old_h} is replaced by ## Answers and ## Explanation')
        for att in (fm or {}).get('attachments') or []:
            if not os.path.exists(os.path.join('benchmark', 'questions', att)) and (fm or {}).get('status') not in ('awaiting-input', 'deferred'):
                bad(f, f'attachment not found: {att}')

    kb_images = {hashlib.sha256(open(p_, 'rb').read()).hexdigest(): p_ for p_ in glob.glob('knowledge/**/*', recursive=True)
                 if p_.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))}
    for f in sorted(glob.glob('benchmark/questions/*/*')):  # an attachment that is a knowledge image leaks its text (benchmark/README.md)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            k = kb_images.get(hashlib.sha256(open(f, 'rb').read()).hexdigest())
            if k: bad(f, f'same image as {k}: the reading set would hold its facts; use another screenshot')
    for qid, (f, other) in pairs.items():
        if other not in seen_ids: bad(f, f'pair "{other}" is not a question id')
        elif pairs.get(other, (None, None))[1] != qid: bad(f, f'pair "{other}" must point back to "{qid}"')
    for lv, ns in level_numbers.items():
        if sorted(ns) != list(range(1, len(ns) + 1)):
            bad('benchmark/questions', f'level {lv} file numbers must run 001..{len(ns):03d} without gaps; run project/tools/question_renumber.py')
    sys.path.insert(0, 'project/tools')
    from link_rewriter import DOCS as LINKED_DOCS, others, bare_ids
    for f in others():
        for r in bare_ids(f): bad(f, f'`{r}` should be a link [`{r}`](relative/path.md) (run project/tools/link_rewriter.py)')
    for d in LINKED_DOCS:
        for ref in re.findall(r'benchmark/questions/(L\d-\d+-[\w-]+\.md)', open(d, encoding='utf-8').read()):
            if not os.path.exists(os.path.join('benchmark', 'questions', ref)): bad(d, f'link to a question that does not exist: {ref}')
    for f in files + sorted(glob.glob('benchmark/questions/*.md')):
        text = open(f, encoding='utf-8').read()
        for pat in allowed.get('injection_patterns', []):
            if re.search(pat, text): bad(f, f'possible prompt injection or hidden text (pattern {pat})')
    import knowledge_loader as _kb, upfront_knowledge  # agent up-front blocks: sources present, size within budget (harness/AGENT.md, section 3)
    pdocs, _ = _kb.load()
    for b in upfront_knowledge.BLOCKS:
        if not upfront_knowledge.build(pdocs, {b: True}): bad('harness/upfront_knowledge.py', f'up-front block "{b}" is empty: its source section is missing')
    n = upfront_knowledge.tokens(upfront_knowledge.build(pdocs, {b: True for b in upfront_knowledge.BLOCKS}))
    if n > upfront_knowledge.BUDGET_TOKENS: bad('harness/upfront_knowledge.py', f'up-front blocks are {n} tokens, above the budget of {upfront_knowledge.BUDGET_TOKENS}')
    # Links the reading plan follows (harness/AGENT.md, section 6): same_name is symmetric, and every metric file
    # names the mechanism files it follows from (internal_derive), so the mechanism tier can reach them.
    for d in pdocs.values():
        p = os.path.join('knowledge', d.id + '.md')
        for t in d.meta.get('same_name') or []:
            if t in pdocs and d.id not in (pdocs[t].meta.get('same_name') or []):
                bad(p, f'same_name "{t}" does not link back: same_name is symmetric')
        if d.meta.get('retriever_guide') == 'metric-meaning' and not d.meta.get('internal_derive'):
            bad(p, 'metric file has no internal_derive: name the mechanism files it follows from (harness/AGENT.md, section 6)')
    check_moved(ids, bad)
    check_file_types(bad)
    check_terminology(pdocs, bad)
    check_catalog(allowed, ids, {fm.get('id'): FILE_LINK.sub(r'\1', body) for fm, body in docs.values()}, bad)
    check_metric_names(allowed, bad)
    check_flows({fm.get('id'): (fm, body) for fm, body in docs.values()}, bad)
    check_flow_map(bad, pdocs)
    check_source_document({fm.get('id'): (fm, body) for fm, body in docs.values()}, bad)
    check_image_text(allowed, bad)
    check_diagram_text(bad)
    check_titles(bad)  # titles and headings are machine input: harness/knowledge_loader.py puts both in front of every chunk (Q-E2-181)

    # every image file must be linked from a knowledge file, so the AI gets its context
    for img in glob.glob('knowledge/**/images/*.png', recursive=True):
        if os.path.normpath(img) not in linked_images:
            bad(img, 'image not linked from any knowledge file')

    for p in problems: print(p)
    print(f'{len(docs)} knowledge files checked, {len(problems)} problems')
    return 1 if problems else 0

def check_repo_terms(allowed, bad):
    """One word per concept in the repository (project/terms.md): flag the replaced words.
    Not called: lint does not check writing style in Markdown; the review checks these words (project/knowledge-rules/writing.md)."""
    skip = ('project/terms.md', 'project/author-questions.md', 'project/author-questions-resolved.md', 'project/tools/rules_check_values.yaml')
    records = ('project/review-', 'benchmark/results/')
    for f in sorted(glob.glob('**/*.md', recursive=True)):
        if f in skip or f.startswith(records):
            continue
        for i, line in enumerate(open(f, encoding='utf-8').read().split('\n'), 1):
            for pat, use in (allowed.get('avoid_repo_terms') or {}).items():
                if re.search(pat, line):
                    bad(f, f'line {i}: repository term "{re.search(pat, line).group(0)}": use "{use}" (project/terms.md)')
            for pat, use in (allowed.get('avoid_ai_speak') or {}).items():
                if re.search(pat, line):
                    bad(f, f'line {i}: AI-speak "{re.search(pat, line).group(0)}": {use} (project/knowledge-rules/writing.md)')


def check_image_text(allowed, bad):
    """AI-speak phrases (avoid_ai_speak) in diagram labels: the one style check lint runs, because no pattern or review reads an SVG otherwise."""
    for f in sorted(glob.glob('images/*.svg')):
        for i, line in enumerate(open(f, encoding='utf-8').read().split('\n'), 1):
            for pat, use in (allowed.get('avoid_ai_speak') or {}).items():
                if re.search(pat, line):
                    bad(f, f'line {i}: AI-speak "{re.search(pat, line).group(0)}": {use} (project/knowledge-rules/writing.md)')

def check_diagram_text(bad):
    """The text of each SVG diagram under its image in the root documents is generated from the SVG (diagram_text.py)."""
    import diagram_text
    diagram_text.check(bad)

def check_terminology(docs, bad):
    """Glossary entries and misconceptions, as the harness reads them (project/knowledge-rules/terminology.md)."""
    import knowledge_loader as _kb
    g = 'knowledge/glossary.md'
    if 'glossary' in docs:
        area = ''
        for line in docs['glossary'].body.split('\n'):
            if line.startswith('## '): bad(g, f'areas are ### headings, so the glossary stays one chunk and never outranks the files: {line}')
            if line.startswith('### '): area = line[4:].strip()
            if area:
                if line.startswith('- ') and not _kb.GLOSSARY_ENTRY.match(line):
                    bad(g, f'section "{area}": an entry reads "- **Term**: meaning": {line[:50]}')
                if line.startswith('  - '):
                    field, sep, value = line[4:].partition(': ')
                    if not sep or not (field in ('Also called', 'File') + _kb.LABEL_FIELDS or field.startswith('Not to confuse with ')):
                        bad(g, f'section "{area}": entry lines are {", ".join(_kb.GLOSSARY_FIELDS)}: {line[:50]}')
                    elif field.startswith('Not to confuse with ') and len(field.split()) > 10:
                        bad(g, f'section "{area}": "Not to confuse with Other term: difference" (other term up to 6 words): {line[:50]}')
        seen = set()
        for e in _kb.glossary(docs):
            t = e['term']
            if t.lower() in seen: bad(g, f'term "{t}" has two entries')
            seen.add(t.lower())
            if e['file'] and e['file'] not in docs: bad(g, f'term "{t}": File {e["file"]} is not a knowledge id')
            if e['label'] or e['invites'] or e['better']:  # a product label entry (KNOWLEDGE-ENGINEERING.md, Product label and better model)
                if not (e['label'] and e['invites'] and e['better'] and all(e['better']) and e['file']):
                    bad(g, f'term "{t}": a product label entry has Product label, Invites, "Better name: Name: better model" and File')
    import upfront_knowledge as _primer  # up-front misconceptions: one home, the marked line of a file (Q-E2-211)
    for i, d in docs.items():
        b = d.meta.get('up_front')
        if b and not _primer.up_front_line(d, b):
            bad(d.path, f'up_front "{b[:40]}" must match exactly one line of ## Misconceptions that starts with - "{b[:20]}..."')


def check_file_types(bad):
    """Every file under knowledge/ has a known type: a knowledge file without .md is never indexed or checked."""
    for f in sorted(glob.glob('knowledge/**/*', recursive=True)):
        if os.path.isfile(f) and not f.endswith(('.md', '.yaml', '.png', '.jpg', '.jpeg', '.webp', '.drawio')):
            bad(f, 'unknown file type in knowledge/: a knowledge file needs .md')


def check_moved(ids, bad):
    """project/tools/moved_ids.yaml points to files that exist; active files use current ids, not moved ones."""
    for old, new in MOVED.items():
        if new not in ids: bad('project/tools/moved_ids.yaml', f'"{old}" points to "{new}", which does not exist')
        if old in ids: bad('project/tools/moved_ids.yaml', f'"{old}" is moved but a file with that id exists')
    if not MOVED:
        return
    old_ids = '|'.join(re.escape(o) for o in sorted(MOVED, key=len, reverse=True))
    pat = re.compile(r'(?:`(' + old_ids + r')`|blob/main/knowledge/(' + old_ids + r')\.md)')
    records = ('project/review-', 'benchmark/results/')
    for f in sorted(glob.glob('**/*.md', recursive=True)):
        if f.startswith(records):
            continue
        for i, line in enumerate(open(f, encoding='utf-8').read().split('\n'), 1):
            for m in pat.finditer(line):
                o = m.group(1) or m.group(2)
                bad(f, f'line {i}: moved id "{o}": use "{MOVED[o]}" (run project/tools/link_rewriter.py for links)')


def check_flow_map(bad, docs):
    """REPOSITORY-MAP.md, section Flows, lists every flow file, and its map of hand-offs is current."""
    import flow_map_diagram
    if os.path.exists('REPOSITORY-MAP.md') and flow_map_diagram.updated(open('REPOSITORY-MAP.md', encoding='utf-8').read(), docs) != open('REPOSITORY-MAP.md', encoding='utf-8').read():
        bad('REPOSITORY-MAP.md', 'the map of hand-offs is out of date: run python3 project/tools/flow_map_diagram.py')
    text = open('REPOSITORY-MAP.md', encoding='utf-8').read() if os.path.exists('REPOSITORY-MAP.md') else ''
    for f in sorted(glob.glob('knowledge/**/*.md', recursive=True)):
        guide = (split(f)[0] or {}).get('retriever_guide')
        if guide in ('health-check', 'troubleshooting', 'decision-tree'):
            if f'({f})' not in text:
                bad('REPOSITORY-MAP.md', f'flow {f} not listed in section Flows')
        if guide == 'health-check' and ('/technology/' in f or f.startswith('knowledge/sp5-framework/')):
            bad(f, 'a health check is on an object type, never on a technology or a pillar: '
                   'use object-types/<object>/<object>-health-check, or a decision tree for one operational question')
    # A folder named for a file kind needs 2 or more files; with one, the file sits in the parent folder.
    for d in sorted({p.rstrip('/') for p in glob.glob('knowledge/**/', recursive=True)}):
        if os.path.basename(d) in KIND_FOLDERS:
            n = len(glob.glob(f'{d}/**/*.md', recursive=True))
            if n < 2: bad(d, f'kind folder "{os.path.basename(d)}/" holds {n} file: move the file to the parent folder (its kind is its retriever_guide)')


def check_titles(bad):
    """Short titles and headings: the title is prefixed to every chunk (harness/knowledge_loader.py), so a list of contents in it repeats in every chunk."""
    opener = re.compile(r'(How|Why|What|When|Where|Which|Who)\b')
    for f in sorted(glob.glob('knowledge/**/*.md', recursive=True)):
        text = open(f, encoding='utf-8').read()
        question_title = 'retriever_guide: decision-tree' in text  # a decision tree title is the question users ask
        for i, line in enumerate(text.split('\n'), 1):
            m = re.match(r'(#{1,3}) (.*)', line)
            if not m:
                continue
            words, limit = len([w for w in re.sub(r'\([^)]*\)', '', m.group(2)).split() if w != '|']), (8 if m.group(1) == '#' else 9)
            if words > limit:
                bad(f, f'line {i}: heading of {words} words; at most {limit}: name the topic, put details in the body')
            if m.group(1) == '#' and ': ' in m.group(2) and m.group(2).split(': ', 1)[1].count(',') >= 2:
                bad(f, f'line {i}: title lists its contents after a colon; name the topic only')
            if opener.match(m.group(2)) and not (m.group(1) == '#' and question_title):
                bad(f, f'line {i}: heading starts with "{opener.match(m.group(2)).group(1)}": a noun phrase names the topic (project/knowledge-rules/writing.md)')


def check_tables(bad):
    """Tables need a blank line before (else they render as text) and after (else the next line becomes a table row)."""
    for f in sorted(glob.glob('**/*.md', recursive=True)):
        if f.startswith('benchmark/results/'):
            continue
        lines, fence = open(f, encoding='utf-8').read().split('\n'), False
        for i, line in enumerate(lines):
            if line.startswith('```'):
                fence = not fence
            if (not fence and i > 0 and line.startswith('|') and i + 1 < len(lines) and lines[i + 1].startswith('|---')
                    and lines[i - 1].strip() and not lines[i - 1].startswith(('|', '#'))):
                bad(f, f'line {i + 1}: table needs a blank line before it')
            if (not fence and line.startswith('|') and i + 1 < len(lines) and lines[i + 1].strip()
                    and not lines[i + 1].startswith('|')):
                bad(f, f'line {i + 2}: blank line needed after a table (an image or text right after it becomes a table row)')


VSPHERE_TOP = ['architecture', 'technology', 'object-types', 'tools']
VCF_OPERATIONS_TOP = ['concepts', 'features', 'dashboards', 'reports', 'alerts', 'troubleshooting', 'health-check']  # VCF Operations itself only (author, 2026-11-08)
OBJECT_FOLDERS = ['vm', 'esxi', 'cluster', 'resource-pool', 'datastore', 'datastore-cluster', 'datacenter', 'vcenter', 'distributed-switch', 'distributed-port-group']
# Folders named for a file kind. A kind folder holds 2 or more Markdown files; one file sits in its parent instead (2026-11-12).
# Not kind folders: areas, technologies, object types, metrics/<object>/, images/.
KIND_FOLDERS = ('concepts', 'metrics', 'configuration', 'health-check', 'troubleshooting', 'decision-tree', 'kpis', 'models',
                'comparisons', 'alerts', 'features', 'dashboards', 'reports', 'screens')
PILLAR_FOLDERS = ['concepts', 'observability', 'outputs', 'performance', 'capacity']  # SP5 Framework parts (2026-11-11)
CATALOG = 'knowledge/catalog'
THRESHOLD_SOURCES = ['knowledge-base', 'vsphere-9.1-docs', 'performance-best-practices-9.1', 'microsoft']
# Threshold files and their sections, named by use. A section name is the use the Harness shows with each value.
THRESHOLD_SECTIONS = {
    'thresholds-performance.yaml': ('kpi', 'change', 'flow'),
    'thresholds-capacity.yaml': ('model', 'score', 'sizing', 'decisions', 'rules'),
    'thresholds-risk.yaml': ('model', 'score'),
    'thresholds-alerts.yaml': ('symptoms', 'alerts'),
}
CLASSES = ('gold', 'silver', 'bronze')  # class of service
ROW_CLASSES = CLASSES + ('all', 'production', 'non-production')

OPERATORS = ['>', '>=', '<', '<=', '=', 'range']
# Alerts fire on one object type, so the recommended alerts live with the object type (2026-11-12).
ALERT_FILE = re.compile(r'vsphere/object-types/([a-z-]+)/\1-alerts|guest-os/guest-os-alerts')
FLOW_CHECKS = re.compile(r'^## Checks, in order\s*$', re.M)
FLOW_STEP = re.compile(r'^(\d+)\.\s', re.M)
ALERT_VALUE = re.compile(r'\d+(?:[.,]\d+)?\s?(?:%|ms|GHz|MHz|MB|GB|IOPS|minutes?|cycles?)(?![a-z])')


def check_metric_names(allowed, bad):
    """Metric names a user sees carry no comma (author, 2026-11-18). The rules section, Agent E2's internal planning and sizing rules, is not checked.
    Names the author still renames at the source are listed in rules_check_values.yaml (metric_comma_pending)."""
    pending = set(allowed.get('metric_comma_pending') or [])
    found = set()
    def walk(path, node):
        if isinstance(node, dict):
            m = node.get('metric')
            if isinstance(m, str) and ',' in m:
                found.add(m)
                if m not in pending:
                    bad(path, f'metric name "{m}" has a comma: put the unit in brackets at the end')
            for k, v in node.items():
                if k not in ('meta', 'rules'): walk(path, v)  # rules: Agent E2's internal planning and sizing rules, not shown in a UI
        elif isinstance(node, list):
            for v in node: walk(path, v)
    for path in sorted(glob.glob('knowledge/catalog/thresholds-*.yaml')):
        walk(path, yaml.safe_load(open(path, encoding='utf-8')))
    for m in sorted(pending - found):
        bad('project/tools/rules_check_values.yaml', f'metric_comma_pending lists "{m}", which no longer has a comma: remove it')

def check_catalog(allowed, ids, bodies, bad, docs=None):
    """knowledge/catalog/*.yaml: parses, required fields, valid tags, existing knowledge ids; a quote, where a row still has one, is still in its file."""
    objects = set(allowed['object'])
    seen_thresholds, kpi_all, seen_kpi = set(), [], set()
    def check_kpi_line(path, w, lv):
        """One line of a kpi, model or score section: five limits [best, green, yellow, orange, zero-at] per interval, worsening
        in its direction; one line per metric (catalog/thresholds-performance, meta, limits_fields)."""
        for k in ('object', 'metric', 'group', 'direction', 'kb'):
            if not lv.get(k): bad(path, f'{w}: {k} missing')
        if lv.get('direction') not in ('above', 'below'): bad(path, f'{w}: direction must be above or below')
        if lv.get('metric') in seen_kpi: bad(path, f'{w}: duplicate metric')
        seen_kpi.add(lv.get('metric'))
        for iv in ('5m', '20s', '2s'):
            v = lv.get(iv, 'missing')
            if v == 'missing': bad(path, f'{w}: {iv} missing (write null until a value is entered)')
            elif v is not None and (not isinstance(v, list) or len(v) != 5): bad(path, f'{w}: {iv} needs five limits [best, green, yellow, orange, zero-at]')
            elif v is not None:
                x = [float(i) for i in v]
                if x != sorted(x, reverse=lv.get('direction') == 'below'): bad(path, f'{w}: {iv} limits must worsen from best to zero-at')
    def check_alerts(path, data):
        """Symptoms (one test each, written once) and alert definitions that refer to them by id."""
        def objs(o): return o if isinstance(o, list) else [o]
        sym, tests, alert_names = {}, set(), {}
        for n, s in enumerate(data.get('symptoms') or []):
            w = f'symptoms row {n + 1} ({s.get("id")})'
            for k in ('id', 'object', 'metric', 'operator', 'value', 'source', 'kb'):
                if s.get(k) in (None, ''): bad(path, f'{w}: {k} missing')
            if not str(s.get('id', '')).startswith('sym-'): bad(path, f'{w}: id must start with sym-')
            if s.get('id') in seen_thresholds: bad(path, f'{w}: duplicate id (ids are unique across the threshold files)')
            seen_thresholds.add(s.get('id'))
            sym[s.get('id')] = s
            for o in objs(s.get('object')):
                if o not in objects: bad(path, f'{w}: object "{o}" not allowed')
            if s.get('layer') and s['layer'] not in allowed['layer']: bad(path, f'{w}: layer "{s["layer"]}" not allowed')
            if s.get('operator') not in OPERATORS or s.get('operator') == 'range': bad(path, f'{w}: operator "{s.get("operator")}" not allowed')
            if s.get('interval') and s['interval'] not in ('2s', '20s', '5m', '1d'): bad(path, f'{w}: interval must be 2s, 20s, 5m or 1d')
            if s.get('role', 'issue') not in ('issue', 'gate'): bad(path, f'{w}: role must be issue or gate')
            if s.get('source') not in THRESHOLD_SOURCES: bad(path, f'{w}: source "{s.get("source")}" not allowed')
            for k in ('condition', 'criticality', 'meaning', 'value_high'):
                if k in s: bad(path, f'{w}: {k} does not belong on a symptom: one test each; the alert combines them')
            key = (tuple(objs(s.get('object'))), s.get('metric'), s.get('interval'), s.get('operator'), s.get('value'))
            if key in tests: bad(path, f'{w}: same test as another symptom: refer to that one')
            tests.add(key)
            kb_ok(path, w, s.get('kb'))
            if 'quote' in s: bad(path, f'{w}: no quote: alert values live only here; the knowledge files hold the reasons')
        used = set()
        for n, a in enumerate(data.get('alerts') or []):
            w = f'alerts row {n + 1} ({a.get("id")})'
            for k in ('id', 'name', 'criticality', 'pillar', 'object', 'match', 'sets', 'wait_cycles', 'source', 'kb'):
                if a.get(k) in (None, '', []): bad(path, f'{w}: {k} missing')
            if not str(a.get('id', '')).startswith('alert-'): bad(path, f'{w}: id must start with alert-')
            if a.get('id') in seen_thresholds: bad(path, f'{w}: duplicate id (ids are unique across the threshold files)')
            seen_thresholds.add(a.get('id'))
            for k in ('metric', 'operator', 'value', 'unit', 'condition'):
                if k in a: bad(path, f'{w}: {k} belongs on a symptom, not on the alert')
            if a.get('criticality') not in ('red', 'orange'): bad(path, f'{w}: criticality must be red or orange (no yellow alert)')
            if a.get('pillar') not in allowed['pillar']: bad(path, f'{w}: pillar "{a.get("pillar")}" not allowed')
            if a.get('match') not in ('all', 'any'): bad(path, f'{w}: match must be all or any')
            if not isinstance(a.get('wait_cycles'), int) or a['wait_cycles'] < 1: bad(path, f'{w}: wait_cycles must be a whole number, 1 or more')
            if a.get('source') not in THRESHOLD_SOURCES: bad(path, f'{w}: source "{a.get("source")}" not allowed')
            for o in objs(a.get('object')):
                if o not in objects: bad(path, f'{w}: object "{o}" not allowed')
            kb_ok(path, w, a.get('kb'))
            if len(objs(a.get('object'))) != 1: bad(path, f'{w}: one object type per alert: an alert fires on one object type')
            if a.get('kb') and not ALERT_FILE.fullmatch(a['kb']): bad(path, f'{w}: kb must be the alert file of its object type (<object>/<object>-alerts)')
            elif a.get('kb') in bodies:
                heads = [h.lower() for h in re.findall(r'^## (.+)$', bodies[a['kb']], re.M)]
                if not any(str(a.get('name', '')).lower() in h for h in heads):
                    bad(path, f'{w}: name "{a.get("name")}" is not a ## heading of {a["kb"]}: the file explains each alert under its name')
                alert_names.setdefault(a['kb'], set()).add(str(a.get('name', '')).lower())
            for m, st in enumerate(a.get('sets') or []):
                ws = f'{w} set {m + 1}'
                if st.get('match') not in ('all', 'any'): bad(path, f'{ws}: match must be all or any')
                if st.get('relation') == 'self':
                    if 'population' in st or 'object' in st: bad(path, f'{ws}: object and population only for relation: child')
                    on = objs(a.get('object'))
                elif st.get('relation') == 'child':
                    if st.get('object') not in objects: bad(path, f'{ws}: relation child needs object')
                    if not re.fullmatch(r'(>|>=) \d+%', str(st.get('population', ''))): bad(path, f'{ws}: population must read "> 25%" or ">= 50%"')
                    on = [st.get('object')]
                else:
                    bad(path, f'{ws}: relation must be self or child'); on = []
                if not st.get('symptoms'): bad(path, f'{ws}: symptoms missing')
                for sid in st.get('symptoms') or []:
                    used.add(sid)
                    if sid not in sym: bad(path, f'{ws}: symptom "{sid}" does not exist'); continue
                    miss = [o for o in on if o not in objs(sym[sid].get('object'))]
                    if miss: bad(path, f'{ws}: symptom "{sid}" is not defined on {", ".join(miss)}')
        for sid in sym:
            if sid not in used: bad(path, f'symptom "{sid}" is used by no alert')
        # One place per number: a section that explains a catalog alert, and the correction of a misconception, hold no alert values.
        for kb_id, names in alert_names.items():
            section = ''
            for line in bodies.get(kb_id, '').split('\n'):
                if line.startswith('## '):
                    section = line[3:].lower(); continue
                text = line.split('→', 1)[1] if section == 'misconceptions' and '→' in line else line
                checked = section == 'misconceptions' or any(n in section for n in names)
                if checked and ALERT_VALUE.search(text):
                    bad(f'knowledge/{kb_id}.md', f'section "{section}": alert value "{ALERT_VALUE.search(text).group(0)}" in prose: values live only in catalog/thresholds-alerts.yaml')
    def check_flow_row(path, w, r):
        """A flow test: one number that one numbered step of its kb flow file compares a reading with."""
        if not str(r.get('id', '')).startswith('flow-'): bad(path, f'{w}: id must start with flow-')
        if r.get('unit') in (None, ''): bad(path, f'{w}: unit missing')
        if r.get('operator') == 'range': bad(path, f'{w}: a flow test is one comparison, not a range')
        if not isinstance(r.get('step'), int) or isinstance(r.get('step'), bool):
            bad(path, f'{w}: step must be the number of a step in the kb flow file'); return
        if r.get('kb') in bodies:
            m = FLOW_CHECKS.search(bodies[r['kb']])
            steps = FLOW_STEP.findall(bodies[r['kb']][m.end():].split('\n## ', 1)[0]) if m else []
            if not steps: bad(path, f'{w}: kb {r["kb"]} has no "## Checks, in order": a flow row names a flow file')
            elif str(r['step']) not in steps: bad(path, f'{w}: no step {r["step"]} in {r["kb"]}')
    def kb_ok(path, where, ref):
        if ref and ref not in ids and not ref.startswith('catalog/'):
            bad(path, f'{where}: kb "{ref}" does not exist')
    for path in sorted(glob.glob(f'{CATALOG}/*.yaml')):
        try:
            data = yaml.safe_load(open(path, encoding='utf-8'))
        except yaml.YAMLError as e:
            bad(path, f'yaml error: {e}'); continue
        meta = data.get('meta') or {}
        for k in ('id', 'title', 'review_notes', 'status'):
            if k not in meta: bad(path, f'meta.{k} missing')
        if meta.get('status') not in allowed['status']: bad(path, f'meta.status "{meta.get("status")}" not allowed')
        if meta.get('id') != path.replace(os.sep, '/')[len('knowledge/'):-5]: bad(path, f'meta.id "{meta.get("id")}" does not match path')
        name = os.path.basename(path)
        rows = data.get('rows') or []
        if name == 'vcenter-counters.yaml':
            for n, r in enumerate(rows):
                w = f'row {n + 1} ({r.get("counter")})'
                for k in ('counter', 'object', 'chart', 'label', 'unit', 'stat_type', 'rollup', 'level', 'page'):
                    if r.get(k) in (None, ''): bad(path, f'{w}: {k} missing')
                if r.get('object') not in objects: bad(path, f'{w}: object "{r.get("object")}" not allowed')
                if r.get('level') not in (1, 2, 3, 4): bad(path, f'{w}: level must be 1-4')
                if r.get('minmax_level') not in (None, 4): bad(path, f'{w}: minmax_level must be 4')
                if r.get('stat_type') not in ('Rate', 'Absolute', 'Delta'): bad(path, f'{w}: stat_type "{r.get("stat_type")}"')
                if r.get('rollup') not in ('Average', 'Summation', 'Latest', 'Minimum', 'Maximum'): bad(path, f'{w}: rollup "{r.get("rollup")}"')
                kb_ok(path, w, r.get('kb'))
        elif name == 'vcenter-api-counters.yaml':
            for n, r in enumerate(rows):
                w = f'row {n + 1} ({r.get("counter")})'
                for k in ('counter', 'object', 'rollup', 'stat_type', 'unit', 'level'):
                    if r.get(k) in (None, ''): bad(path, f'{w}: {k} missing')
                if r.get('object') not in objects: bad(path, f'{w}: object "{r.get("object")}" not allowed')
                if r.get('stat_type') not in ('rate', 'absolute', 'delta'): bad(path, f'{w}: stat_type "{r.get("stat_type")}"')
                if r.get('level') not in (1, 2, 3, 4): bad(path, f'{w}: level must be 1-4')
                kb_ok(path, w, r.get('kb'))
        elif name == 'esxtop-fields.yaml':
            for n, r in enumerate(rows):
                for k in ('panel', 'field', 'description', 'page'):
                    if r.get(k) in (None, ''): bad(path, f'row {n + 1}: {k} missing')
        elif name in THRESHOLD_SECTIONS:
            # Sections are named by use; the section name is the use (no use field on the rows).
            for k in data:
                if k != 'meta' and k not in THRESHOLD_SECTIONS[name]:
                    bad(path, f'section "{k}" not allowed: use {", ".join(THRESHOLD_SECTIONS[name])}')
            if name == 'thresholds-alerts.yaml':
                check_alerts(path, data)
                continue
            for section in THRESHOLD_SECTIONS[name]:
                for n, r in enumerate(data.get(section) or []):
                    w = f'{section} row {n + 1} ({r.get("id") or r.get("metric")})'
                    if section in ('kpi', 'model', 'score'):
                        check_kpi_line(path, w, r)
                        kpi_all.append((path, r))
                        if 'id' in r or 'bands' in r: bad(path, f'{w}: a {section} line has no id or bands: five limits per interval')
                        continue
                    if 'kind' in r: bad(path, f'{w}: kind is gone: the section is the use')
                    if r.get('id') in seen_thresholds: bad(path, f'{w}: duplicate id (ids are unique across the threshold files)')
                    seen_thresholds.add(r.get('id'))
                    if r.get('interval') and r['interval'] not in ('2s', '20s', '5m', '1d'): bad(path, f'{w}: interval must be 2s, 20s, 5m or 1d')
                    if r.get('source') not in THRESHOLD_SOURCES: bad(path, f'{w}: source "{r.get("source")}" not allowed')
                    kb_ok(path, w, r.get('kb'))
                    if section == 'sizing':
                        for k in ('id', 'metric', 'bands', 'source', 'kb'):
                            if r.get(k) in (None, ''): bad(path, f'{w}: {k} missing')
                        bd = r.get('bands') or {}
                        if any(bd.get(k) in (None, '') for k in ('green', 'yellow', 'orange', 'red')): bad(path, f'{w}: bands need green, yellow, orange, red')
                        continue
                    for k in ('id', 'metric', 'operator', 'value', 'meaning', 'source', 'kb'):
                        if r.get(k) in (None, ''): bad(path, f'{w}: {k} missing')
                    if r.get('operator') not in OPERATORS: bad(path, f'{w}: operator "{r.get("operator")}" not allowed')
                    if r.get('operator') == 'range' and r.get('value_high') is None: bad(path, f'{w}: range needs value_high')
                    if r.get('object') and r['object'] not in objects: bad(path, f'{w}: object "{r["object"]}" not allowed')
                    if r.get('layer') and r['layer'] not in allowed['layer']: bad(path, f'{w}: layer "{r["layer"]}" not allowed')
                    if 'class' in r and r['class'] not in ROW_CLASSES: bad(path, f'{w}: class must be one of {", ".join(ROW_CLASSES)}')
                    if 'criticality' in r: bad(path, f'{w}: criticality belongs to alert rows')
                    if section == 'flow':
                        check_flow_row(path, w, r)
                    elif 'step' in r: bad(path, f'{w}: step belongs to flow rows')
                    if r.get('kb') in bodies and r.get('quote') and r['quote'] not in bodies[r['kb']]:
                        bad(path, f'{w}: quote no longer in {r["kb"]}: update the row or the file')
        elif name == 'user-terms.yaml':
            import user_terms as _terms  # product label rows take their note from the glossary (Q-E2-208)
            labels, labelled = _terms.labels(), {}
            seen = set()
            for n, r in enumerate(rows):
                w = f'row {n + 1} ({r.get("id")})'
                for k in ('id', 'match', 'means') + (() if r.get('label') else ('note', 'files')):
                    if not r.get(k): bad(path, f'{w}: {k} missing')
                if r.get('id') in seen: bad(path, f'{w}: duplicate id')
                seen.add(r.get('id'))
                if r.get('label'):
                    lb = r['label']
                    if r.get('note'): bad(path, f'{w}: a label row has no note: its note comes from the glossary entry "{lb}" (one home)')
                    if lb not in labels: bad(path, f'{w}: label "{lb}" is not a glossary entry with a Product label line')
                    if lb in labelled: bad(path, f'{w}: label "{lb}" already has row {labelled[lb]}: one row per label')
                    labelled.setdefault(lb, r.get('id'))
                    try:
                        if not any(re.search(p, lb, re.I) for p in r.get('match') or []):
                            bad(path, f'{w}: no match pattern matches the label term "{lb}", so a question that names it gets no note')
                    except re.error:
                        pass  # reported below
                for pat in (r.get('match') or []) + ([r['unless']] if r.get('unless') else []):
                    try:
                        re.compile(pat)
                    except re.error as e:
                        bad(path, f'{w}: bad pattern {pat!r}: {e}')
                for fid in r.get('files') or []:
                    kb_ok(path, w, fid)
            for lb in labels:
                if lb not in labelled:
                    bad('knowledge/glossary.md', f'term "{lb}": a product label entry needs a term-map row (label: {lb}) in {path}, so its note reaches the model')
        elif name == 'objects.yaml':
            types = set()
            for o in data.get('objects') or []:
                types.add(o.get('type'))
                if o.get('type') not in objects: bad(path, f'object "{o.get("type")}" not allowed')
                if o.get('layer') and o['layer'] not in allowed['layer']: bad(path, f'{o.get("type")}: layer "{o["layer"]}" not allowed')
                for ref in o.get('kb') or []: kb_ok(path, o.get('type'), ref)
            for r in data.get('relations') or []:
                for end in ('from', 'to'):
                    if r.get(end) not in types: bad(path, f'relation {r}: "{r.get(end)}" is not in objects')
            for l in data.get('layers') or []:
                if l.get('layer') not in allowed['layer']: bad(path, f'layer "{l.get("layer")}" not allowed')
        else:
            bad(path, 'unknown catalog file: add its checks to project/tools/rules_check.py')

    # Thresholds live only in the catalog (one place): a knowledge file must not carry a colour-band table.
    import knowledge_loader as _kb, catalog_database as _cat
    for b in _cat.bands_from_docs(_kb.load()[0]):
        bad(f'knowledge/{b["kb"]}.md', f'colour-band table row "{b["metric"]}": thresholds live only in knowledge/catalog/thresholds-*.yaml')
    for path, lv in kpi_all:
        if lv.get('kb') not in ids: bad(path, f'line "{lv.get("metric")}": kb "{lv.get("kb")}" does not exist')
        elif os.path.exists(f'knowledge/{lv["kb"]}.md') and str(lv.get('metric')).replace('|', '\\|') not in open(f'knowledge/{lv["kb"]}.md', encoding='utf-8').read():
            bad(f'knowledge/{lv["kb"]}.md', f'sub-metric table: no cell names the catalog line "{lv.get("metric")}"')

def check_source_document(docs, bad):
    """source.document names no author material (book, spreadsheet): sources are stated once (KNOWLEDGE-ENGINEERING.md, section 2).
    A source note cited in source.path must exist, hold the cited headings and carry its evidence (project/tools/source_trace.py)."""
    import source_trace
    pat = re.compile(r'Private Cloud Management|Capacity Planning Stage|\bbook\b|isvara', re.I)
    for i, (fm, _) in docs.items():
        doc = str(((fm or {}).get('source') or {}).get('document', ''))
        if pat.search(doc):
            bad(f'knowledge/{i}.md', f'source.document names the author\'s material ("{pat.search(doc).group(0)}"): write Knowledge base (KNOWLEDGE-ENGINEERING.md, section 2)')
        for note, heads in source_trace.refs(((fm or {}).get('source') or {}).get('path')):
            for msg in source_trace.check(note, heads):
                bad(f'knowledge/{i}.md', f'source.path {msg} (project/sources/README.md)')
        for k in ('corrections', 'review_notes'):
            for n in (fm or {}).get(k) or []:
                if isinstance(n, str) and re.search(r'(?i)the source document|\bthe book\b', n):
                    bad(f'knowledge/{i}.md', f'{k}: "the book" or "the source document": state the fact (project/knowledge-rules/vocabulary.md)')


def check_flows(docs, bad):
    """Flow files must parse into steps for the flow executor (harness/flow_executor.py); step references must exist."""
    import flow_executor

    class _Doc:
        def __init__(self, i, fm, body):
            self.id, self.meta, self.title = i, fm, body.lstrip().split('\n', 1)[0].lstrip('# ')
            parts = [p.strip() for p in re.split(r'\n(?=## )', body.strip()) if p.strip()]
            self.sections = [(p.split('\n', 1)[0].lstrip('# ').strip() if p.startswith('## ') else 'Intro', p) for p in parts]
    flow_docs = {i: _Doc(i, fm, body) for i, (fm, body) in docs.items()}
    for i, msg in flow_executor.check(flow_docs):
        bad(f'knowledge/{i}.md', msg)
    for i in flow_executor.flow_ids(flow_docs):
        for msg in flow_chart_problems(docs[i][1], flow_executor.steps_of(flow_docs[i]), set(flow_executor.flow_ids(flow_docs))):
            bad(f'knowledge/{i}.md', msg)


# The Mermaid chart of a flow is the master of its structure: the author edits the chart, Claude updates the numbered steps
# (project/knowledge-rules/flows.md, author 2026-11-24). This check keeps the two the same.
MERMAID_BLOCK = re.compile(r'```mermaid\n(.*?)\n```', re.S)
CHART_NODE = re.compile(r'([A-Za-z_]\w*)\s*(?:\(\[|\[\[|\[\(|\(\(|\{\{|\[|\{|\(|>)(.*?)(?:\]\)|\]\]|\)\]|\)\)|\}\}|\]|\}|\))\s*$')
CHART_ARROW = re.compile(r'\s*(?:-->|-\.->|==>)\s*(?:\|[^|]*\|\s*)?')
STEP_NODE = re.compile(r'^"?(\d+|[a-h])\.\s')
STEP_BRANCH = re.compile(r'→\s*(?:go to\s+)?step\s+(\d+|[a-h])\b', re.I)


def chart_edges(chart):
    """Step-to-step edges of a Mermaid flowchart: {(from, to)}, step keys as text, and the set of step keys with a box.
    A box is a step when its text starts with the step key ('1. ...', 'a. ...'). An arrow through boxes that are not steps
    (another flow, a verdict) counts as an edge between the steps on either side."""
    key, succ = {}, {}
    for line in chart.split('\n')[1:]:
        line = line.strip()
        if not line or line.startswith(('subgraph', 'end', '%%', 'classDef', 'class ', 'style', 'direction', 'linkStyle', 'click')):
            continue
        groups = []
        for part in CHART_ARROW.split(line):
            ids = []
            for p in part.split('&'):
                p = p.strip()
                m = CHART_NODE.match(p)
                node = m.group(1) if m else (re.match(r'([A-Za-z_]\w*)', p) or [None])[0]
                if m:
                    k = STEP_NODE.match(m.group(2).strip())
                    if k:
                        key[node] = k.group(1).lower()
                if node:
                    ids.append(node)
            groups.append(ids)
        for a, b in zip(groups, groups[1:]):
            for x in a:
                succ.setdefault(x, set()).update(b)
    edges = set()
    for node, k in key.items():
        seen, todo = set(), list(succ.get(node, ()))
        while todo:
            n = todo.pop()
            if n in seen:
                continue
            seen.add(n)
            if n in key:
                if key[n] != k:
                    edges.add((k, key[n]))
            else:
                todo.extend(succ.get(n, ()))
    return edges, set(key.values())


CHART_CLICK = re.compile(r'^\s*click\s+\w+\s+"[^"]*/knowledge/([^"]+)\.md"', re.M)


def flow_chart_problems(text, steps, flows=None):
    """A flow needs one Mermaid flowchart that matches its steps: a box per step, and the same branches. A step's branches
    are its '→ step N'; a step with none ends the flow."""
    charts = [c for c in MERMAID_BLOCK.findall(text) if re.match(r'\s*(flowchart|graph)\b', c)]
    if not charts:
        return ['flow without a Mermaid flowchart: the chart is the master of the flow (project/knowledge-rules/flows.md)']
    edges, boxes = chart_edges(charts[0])
    keys = [k.lower() for k, _ in steps]
    out = []
    for k in sorted(set(keys) - boxes):
        out.append(f'step {k} has no box in the chart (box text starts "{k}. ")')
    for k in sorted(boxes - set(keys)):
        out.append(f'chart box {k} has no step {k}')
    text_edges = set()
    for k, t in steps:
        targets = [r.lower() for r in STEP_BRANCH.findall(t)]
        text_edges.update((k.lower(), r) for r in targets if r != k.lower())
    for a, b in sorted(edges - text_edges):
        out.append(f'chart arrow {a} → {b} is not in the steps (step {a} needs "→ step {b}")')
    for a, b in sorted(text_edges - edges):
        out.append(f'step {a} goes to step {b}, but the chart has no arrow {a} → {b}')
    if flows is not None:
        # A hand-off ('→ <flow id>' in a step) is a box in the chart with a click line that opens that flow, and the reverse.
        import flow_map_diagram
        offs = {x for _, t in steps for x in flow_map_diagram.HAND_OFF.findall(t) if x in flows}
        clicks = set(CHART_CLICK.findall(charts[0]))
        for x in sorted(offs - clicks):
            out.append(f'hand-off to {x} has no box with a click line in the chart')
        for x in sorted(clicks - offs):
            out.append(f'chart box opens {x}, but no step hands off to it (→ `{x}`)')
    return out


if __name__ == '__main__':
    sys.exit(main())
