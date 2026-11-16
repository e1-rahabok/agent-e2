#!/usr/bin/env python3
"""Scan the benchmark question bank for answer cues and coverage.

Usage:
  python3 project/tools/question_scan.py [--status draft,reviewed,awaiting-input] [--json PATH]

Default: the running set (draft + reviewed) for all statistics, plus a second
section that lists awaiting-input questions separately. Retired and deferred
questions are never counted. Questions: benchmark/questions/*.md (flat; the
subfolders hold attachments). Knowledge: knowledge/**/*.md.
Plain text to stdout. --json writes every per-question and per-option record.
"""
import argparse
import collections
import glob
import json
import os
import re
import statistics
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
from harness.kb import split  # noqa: E402  (the lint tool does the same; harness never imports this file)

RUNNING = ('draft', 'reviewed')
HEDGE = ['can', 'may', 'might', 'if', 'usually', 'often', 'depends', 'typically']
ABSOLUTE = ['always', 'never', 'only', 'all', 'none', 'every', 'cannot', 'must']
NEG = ['not', 'no', 'never', 'none', 'cannot', 'without', 'neither', 'nor']
NEG_RE = re.compile(r"\b(?:%s)\b|n't" % '|'.join(NEG), re.I)
ALL_ABOVE = re.compile(r"\b(?:all|both|none|neither)\s+(?:of\s+)?(?:the\s+)?(?:above|these|them|options|answers|statements)\b"
                       r"|\ball\s+(?:of\s+)?(?:the\s+)?(?:above|apply|applies)\b|\ball\s+apply\b", re.I)
OPT_RE = re.compile(r'^\s*[-*]\s+([A-Y])\.\s+(.*\S)\s*$')
MULTI_STEM = re.compile(r"which\s+(?:of\s+the\s+following\s+)?(?:statements|options|answers|actions|causes|metrics|settings|steps|factors|values|are|do|can)\b[^?]*\b(?:are|is)?\s*(?:correct|true|valid)|"
                        r"which\s+statements|choose\s+all|select\s+all|all\s+that\s+apply|(?:choose|select)\s+(?:two|three|four|2|3|4)|which\s+(?:\w+\s+){0,3}(?:are|do|can|would)\b", re.I)
SINGLE_STEM = re.compile(r"\bwhich\s+one\b|\bthe\s+(?:best|most|single|one|only|first|main|primary|likely|correct)\b|\bwhich\s+(?:\w+\s+){0,3}(?:is|does|would|should)\b|\bwhat\s+is\b", re.I)


def words(s):
    return re.findall(r"[a-z']+", s.lower())


def has_word(s, lst):
    w = set(words(s))
    return any(x in w for x in lst)


def knowledge_ids():
    out = {}
    for p in glob.glob(os.path.join(ROOT, 'knowledge', '**', '*.md'), recursive=True):
        out[os.path.relpath(p, os.path.join(ROOT, 'knowledge'))[:-3]] = p
    return out


def parse_question(path):
    """Return (record, problems)."""
    problems = []
    meta, body = split(path)
    if meta is None:
        return None, ['no metadata block']
    m = re.search(r'\n## Prompt[ \t]*\n(.*?)(?=\n## |\Z)', body, re.S)
    if not m:
        return None, ['no ## Prompt']
    prompt = m.group(1)
    options, stem_lines = [], []
    cur = None
    for line in prompt.split('\n'):
        o = OPT_RE.match(line)
        if o:
            cur = {'letter': o.group(1), 'text': o.group(2)}
            options.append(cur)
        elif cur is not None and line.strip() and not OPT_RE.match(line):
            # a non-bullet line after options: wrapped option text or trailing prose
            problems.append('text after options (wrapped option?): %r' % line.strip()[:60])
        elif cur is None:
            stem_lines.append(line)
    stem = '\n'.join(stem_lines).strip()
    answer = meta.get('answer') or []
    if isinstance(answer, str):
        answer = [x.strip() for x in re.split(r'[,\s]+', answer) if x.strip()]
    answer = [str(a).strip().upper() for a in answer]
    letters = [o['letter'] for o in options]
    if not options:
        problems.append('no options found')
    if len(set(letters)) != len(letters):
        problems.append('duplicate option letters')
    if letters and letters != [chr(65 + i) for i in range(len(letters))]:
        problems.append('option letters not consecutive from A: %s' % ''.join(letters))
    for a in answer:
        if a not in letters:
            problems.append('answer letter %s has no option' % a)
    if not answer and meta.get('status') in RUNNING:
        problems.append('no answer')
    for o in options:
        o['correct'] = o['letter'] in answer
        o['chars'] = len(o['text'])
    # the sentence that asks: last paragraph of the stem that holds a '?', else last paragraph
    paras = [p.strip() for p in re.split(r'\n\s*\n', stem) if p.strip()]
    ask = ''
    for p in reversed(paras):
        if '?' in p:
            ask = p
            break
    if not ask and paras:
        ask = paras[-1]
    ask = ' '.join(ask.split())
    rec = {
        'id': str(meta.get('id', os.path.basename(path)[:-3])),
        'file': os.path.relpath(path, ROOT),
        'title': meta.get('title'),
        'status': meta.get('status'),
        'level': meta.get('level'),
        'answer': answer,
        'n_options': len(options),
        'n_correct': len(answer),
        'technology': meta.get('technology') or [],
        'task': meta.get('task'),
        'misconception_type': meta.get('misconception_type') or [],
        'object': meta.get('object') or [],
        'tool': meta.get('tool') or [],
        'knowledge': meta.get('knowledge') or [],
        'knowledge_main': meta.get('knowledge_main'),
        'input': meta.get('input') or [],
        'attachments': meta.get('attachments') or [],
        'pair': meta.get('pair'),
        'stem_question': ask,
        'options': options,
    }
    return rec, problems


def pct(a, b):
    return '%.1f%%' % (100.0 * a / b) if b else 'n/a'


def listify(v):
    return v if isinstance(v, list) else ([] if v is None else [v])


def group_of(kid):
    p = kid.split('/')
    if kid == 'glossary':
        return 'glossary'
    if p[:2] == ['vsphere', 'technology'] and len(p) > 2:
        return 'vsphere/technology/' + p[2]
    if p[:2] == ['vsphere', 'object-types'] and len(p) > 2:
        return 'vsphere/object-types/' + p[2]
    if p[:2] == ['vsphere', 'tools']:
        return 'vsphere/tools'
    if p[0] == 'vsphere' and len(p) > 2:
        return 'vsphere/' + p[1]
    return p[0]


def section(title):
    print('\n' + '=' * 78 + '\n' + title + '\n' + '=' * 78)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--status', default=None, help='comma list of statuses to analyse (default draft,reviewed; awaiting-input shown separately)')
    ap.add_argument('--ids', default=None, help='comma list of question ids to analyse (subset)')
    ap.add_argument('--json', dest='json_path', help='write all per-question and per-option data as JSON')
    args = ap.parse_args()
    wanted = tuple(s.strip() for s in args.status.split(',')) if args.status else RUNNING

    files = sorted(glob.glob(os.path.join(ROOT, 'benchmark', 'questions', '*.md')))
    allq, problems = [], []
    for f in files:
        try:
            rec, pr = parse_question(f)
        except Exception as e:  # report, keep going
            rec, pr = None, ['parse error: %s' % e]
        for x in pr:
            problems.append((os.path.relpath(f, ROOT), x))
        if rec:
            allq.append(rec)

    status_count = collections.Counter(q['status'] for q in allq)
    qs = [q for q in allq if q['status'] in wanted]
    if args.ids:
        idset = {i.strip().zfill(4) for i in args.ids.split(',')}
        qs = [q for q in qs if q['id'] in idset]
    awaiting = [q for q in allq if q['status'] == 'awaiting-input' and 'awaiting-input' not in wanted]
    kids = knowledge_ids()

    section('0. Files')
    print('Question files read: %d (benchmark/questions/*.md)' % len(files))
    print('Parsed: %d. Problems: %d' % (len(allq), len(problems)))
    for f, x in problems:
        print('  PROBLEM %s: %s' % (f, x))
    print('Analysed statuses: %s' % ', '.join(wanted))
    if awaiting:
        print('Listed separately (not in the stats): awaiting-input (%d)' % len(awaiting))

    section('1. Counts')
    print('By status (all files): ' + ', '.join('%s=%d' % kv for kv in sorted(status_count.items(), key=lambda kv: str(kv[0]))))
    print('Analysed questions: %d' % len(qs))
    lv = collections.Counter(q['level'] for q in qs)
    print('By level: ' + ', '.join('%s=%d' % (k, lv[k]) for k in sorted(lv, key=str)))
    if awaiting:
        al = collections.Counter(q['level'] for q in awaiting)
        print('Awaiting-input by level: ' + ', '.join('%s=%d' % (k, al[k]) for k in sorted(al, key=str)))
    no = [q['n_options'] for q in qs]
    if no:
        print('Options per question: min %d, median %s, max %d' % (min(no), statistics.median(no), max(no)))
        print('Distribution: ' + ', '.join('%d options=%d' % (k, v) for k, v in sorted(collections.Counter(no).items())))
    single = [q for q in qs if q['n_correct'] == 1]
    multi = [q for q in qs if q['n_correct'] > 1]
    print('Single-answer: %d (%s). Multi-answer: %d (%s)' % (len(single), pct(len(single), len(qs)), len(multi), pct(len(multi), len(qs))))
    print('Correct options per question: ' + ', '.join('%d=%d' % kv for kv in sorted(collections.Counter(q['n_correct'] for q in qs).items())))
    print('Answer = all options: %d' % sum(1 for q in qs if q['n_correct'] == q['n_options'] and q['n_options']))

    # ------------------------------------------------------------------ 2
    section('2. Length cue')
    usable = [q for q in qs if q['options'] and 0 < q['n_correct'] < q['n_options']]
    print('Questions with at least one correct and one wrong option: %d' % len(usable))

    def longest_correct(q):
        mx = max(o['chars'] for o in q['options'])
        top = [o for o in q['options'] if o['chars'] == mx]
        return any(o['correct'] for o in top), mx, top

    def shortest_wrong(q):
        mn = min(o['chars'] for o in q['options'])
        bot = [o for o in q['options'] if o['chars'] == mn]
        return all(not o['correct'] for o in bot)

    n_lc = sum(1 for q in usable if longest_correct(q)[0])
    chance = sum(q['n_correct'] / q['n_options'] for q in usable)
    print('Longest option is correct (ties count if any tied option is correct): %d of %d = %s' % (n_lc, len(usable), pct(n_lc, len(usable))))
    print('Expected by chance: %.1f%%' % (100 * chance / len(usable) if usable else 0))
    n_sw = sum(1 for q in usable if shortest_wrong(q))
    print('Shortest option is wrong: %d of %d = %s (chance: %.1f%%)' % (
        n_sw, len(usable), pct(n_sw, len(usable)),
        100 * sum((q['n_options'] - q['n_correct']) / q['n_options'] for q in usable) / len(usable) if usable else 0))
    n_strict = sum(1 for q in usable if longest_correct(q)[0] and len(longest_correct(q)[2]) == 1)
    print('Strict (unique longest option is correct; ties excluded from the hits): %d of %d = %s' % (n_strict, len(usable), pct(n_strict, len(usable))))
    print('Tied longest options: %d questions' % sum(1 for q in usable if len(longest_correct(q)[2]) > 1))
    print('\nBy level (longest correct / n, chance):')
    for lvl in sorted({q['level'] for q in usable}, key=str):
        g = [q for q in usable if q['level'] == lvl]
        c = sum(1 for q in g if longest_correct(q)[0])
        ch = 100 * sum(q['n_correct'] / q['n_options'] for q in g) / len(g)
        print('  level %s: %d/%d = %s (chance %.1f%%)' % (lvl, c, len(g), pct(c, len(g)), ch))
    print('\nBy answer count (longest correct / n, chance):')
    for label, g in (('single', [q for q in usable if q['n_correct'] == 1]), ('multi', [q for q in usable if q['n_correct'] > 1])):
        if g:
            c = sum(1 for q in g if longest_correct(q)[0])
            ch = 100 * sum(q['n_correct'] / q['n_options'] for q in g) / len(g)
            print('  %s: %d/%d = %s (chance %.1f%%)' % (label, c, len(g), pct(c, len(g)), ch))
    co = [o['chars'] for q in qs for o in q['options'] if o['correct']]
    wo = [o['chars'] for q in qs for o in q['options'] if not o['correct']]
    if co and wo:
        print('\nMean characters: correct %.1f (n=%d), wrong %.1f (n=%d), ratio %.2f' % (statistics.mean(co), len(co), statistics.mean(wo), len(wo), statistics.mean(co) / statistics.mean(wo)))
        print('Median characters: correct %s, wrong %s' % (statistics.median(co), statistics.median(wo)))
    # rank of mean correct-option length: 1 = longest. Normalised to 0..1 by number of option-length classes.
    ranks = []
    for q in usable:
        mc = statistics.mean(o['chars'] for o in q['options'] if o['correct'])
        allc = sorted((o['chars'] for o in q['options']), reverse=True)
        # average rank (1 = longest) of the position mean-correct would take among all options
        r = 1 + sum(1 for c in allc if c > mc)
        q['_len_rank'] = r
        q['_len_rank_rel'] = (r - 1) / (q['n_options'] - 1) if q['n_options'] > 1 else 0
        ranks.append(q['_len_rank_rel'])
    if ranks:
        print('Rank of mean correct-option length among all options (0 = longest, 1 = shortest): mean %.3f (0.5 means no cue)' % statistics.mean(ranks))
        bins = collections.Counter(min(int(r * 3), 2) for r in ranks)
        print('  top third: %d, middle third: %d, bottom third: %d' % (bins[0], bins[1], bins[2]))
    strong = []
    for q in usable:
        ok, mx, top = longest_correct(q)
        wrongs = [o['chars'] for o in q['options'] if not o['correct']]
        if ok and any(o['correct'] for o in top) and len(top) == 1 and wrongs and mx >= 1.3 * statistics.mean(wrongs):
            strong.append((q['id'], mx, statistics.mean(wrongs)))
    print('\nStrong cue (unique longest option is correct AND >= 1.3x mean wrong length): %d questions' % len(strong))
    for i, mx, mw in strong:
        print('  %s  longest=%d  mean wrong=%.0f  ratio=%.2f' % (i, mx, mw, mx / mw))

    # ------------------------------------------------------------------ 3
    section('3. Word cues')
    opts = [(q, o) for q in qs for o in q['options']]
    nc = sum(1 for _, o in opts if o['correct'])
    nw = len(opts) - nc
    print('Options: %d correct, %d wrong' % (nc, nw))
    print('%-22s %10s %10s' % ('Cue', 'correct', 'wrong'))
    for label, test in (('hedging (%s)' % ','.join(HEDGE), lambda t: has_word(t, HEDGE)),
                        ('absolute (%s)' % ','.join(ABSOLUTE), lambda t: has_word(t, ABSOLUTE)),
                        ('because', lambda t: 'because' in words(t))):
        c = sum(1 for _, o in opts if o['correct'] and test(o['text']))
        w = sum(1 for _, o in opts if not o['correct'] and test(o['text']))
        print('%s\n  %-20s %4d %5s %4d %5s' % (label, '', c, pct(c, nc), w, pct(w, nw)))
    for lst in HEDGE + ABSOLUTE:
        c = sum(1 for _, o in opts if o['correct'] and lst in words(o['text']))
        w = sum(1 for _, o in opts if not o['correct'] and lst in words(o['text']))
        if c + w:
            print('    %-10s correct %3d (%s)  wrong %3d (%s)' % (lst, c, pct(c, nc), w, pct(w, nw)))
    fw = collections.defaultdict(lambda: [0, 0])
    for _, o in opts:
        ws = words(o['text'])
        if ws:
            fw[ws[0]][0 if o['correct'] else 1] += 1
    top = sorted(fw.items(), key=lambda kv: -(kv[1][0] + kv[1][1]))[:25]
    print('\nFirst word, 25 most common: count correct / wrong / pct wrong (overall wrong share %s)' % pct(nw, nc + nw))
    for w, (c, x) in top:
        print('  %-14s correct %3d  wrong %3d  wrong %s' % (w, c, x, pct(x, c + x)))

    # ------------------------------------------------------------------ 4
    section('4. Options with two or more negation tokens')
    n = 0
    for q in qs:
        for o in q['options']:
            hits = NEG_RE.findall(o['text'])
            if len(hits) >= 2:
                n += 1
                print('  %s %s %s [%s] %s' % (q['id'], o['letter'], 'CORRECT' if o['correct'] else 'wrong  ', ','.join(h.lower() for h in hits), o['text'][:110]))
    print('Total: %d' % n)

    # ------------------------------------------------------------------ 5
    section('5. "All of the above" style options')
    n = 0
    for q in qs:
        for o in q['options']:
            if ALL_ABOVE.search(o['text']):
                n += 1
                print('  %s %s %s %s' % (q['id'], o['letter'], 'CORRECT' if o['correct'] else 'wrong  ', o['text'][:110]))
    print('Total: %d' % n)

    # ------------------------------------------------------------------ 6
    section('6. Stem wording vs answer count (judge by eye)')
    multi_words = re.compile(r"choose\s+the\s+correct|which\s+(?:of\s+(?:the\s+following|these)\s+)?(?:\w+\s+){0,3}(?:are|apply)\s+(?:correct|true)|which\s+findings|which\s+of\s+these|which\s+(?:of\s+the\s+following\s+)?statements|choose\s+all|select\s+all|all\s+that\s+apply|all\s+of\s+the\s+following|"
                             r"which\s+(?:of\s+the\s+following\s+)?(?:\w+\s+){0,2}(?:are|apply)\b|(?:choose|select)\s+(?:two|three|four|\d)|which\s+\w+s\s+are\b", re.I)
    single_words = re.compile(r"\bwhich\s+one\b|\bwhat\s+is\s+the\b|\bthe\s+best\b|\bthe\s+most\s+likely\b|\bthe\s+main\b", re.I)
    # strict plural markers decide (a) and (b); the broad set only decides (c)
    multi_strict = re.compile(r"which\s+(?:of\s+the\s+following\s+)?statements|choose\s+all|select\s+all|all\s+that\s+apply|all\s+of\s+the\s+following|"
                              r"which\s+(?:of\s+(?:the\s+following|these)\s+)?(?:\w+\s+){0,2}(?:are|apply)\s+(?:correct|true)\b|which\s+readings\s+are|choose\s+the\s+correct|(?:choose|select)\s+(?:two|three|four|\d)", re.I)
    a, b = [], []
    for q in qs:
        s = q['stem_question']
        if q['n_correct'] == 1 and multi_strict.search(s) and not single_words.search(s):
            a.append(q)
        elif q['n_correct'] > 1 and single_words.search(s) and not multi_words.search(s) and not multi_strict.search(s):
            b.append(q)
    print('(a) Plural / select-all style stem, exactly one answer letter: %d' % len(a))
    for q in a:
        print('  %s answer=%s | %s' % (q['id'], ''.join(q['answer']), q['stem_question'][:240]))
    print('\n(b) Singular / "which one" / "the best" stem, several answer letters: %d' % len(b))
    for q in b:
        print('  %s answer=%s | %s' % (q['id'], ''.join(q['answer']), q['stem_question'][:240]))
    print('\n(c) Multi-answer questions whose stem has no plural / select-all marker at all: ')
    c = [q for q in qs if q['n_correct'] > 1 and not multi_words.search(q['stem_question'])]
    print('    %d' % len(c))
    for q in c:
        print('  %s answer=%s | %s' % (q['id'], ''.join(q['answer']), q['stem_question'][:240]))

    # ------------------------------------------------------------------ 7
    section('7. Answer letter position (informational: the runner shuffles options)')
    letters = collections.Counter(a for q in qs for a in q['answer'])
    print('Correct letters: ' + ', '.join('%s=%d' % (k, letters[k]) for k in sorted(letters)))
    rel = collections.Counter()
    for q in qs:
        n = q['n_options']
        for a in q['answer']:
            i = ord(a) - 65
            if n <= 1:
                continue
            f = i / (n - 1)
            rel['first third' if f < 1 / 3 else ('middle third' if f < 2 / 3 else 'last third')] += 1
    tot = sum(rel.values())
    for k in ('first third', 'middle third', 'last third'):
        print('  %-13s %4d  %s' % (k, rel[k], pct(rel[k], tot)))
    print('  First option is correct: %d of %d questions; last option is correct: %d' % (
        sum(1 for q in qs if 'A' in q['answer']), len(qs),
        sum(1 for q in qs if q['n_options'] and chr(64 + q['n_options']) in q['answer'])))

    # ------------------------------------------------------------------ 8
    section('8. Knowledge coverage')
    cited = collections.defaultdict(list)
    cited_main = collections.defaultdict(list)
    for q in qs:
        for k in listify(q['knowledge']):
            cited[k].append(q['id'])
        if q['knowledge_main']:
            cited_main[q['knowledge_main']].append(q['id'])
    cited_aw = collections.defaultdict(list)
    for q in awaiting:
        for k in listify(q['knowledge']):
            cited_aw[k].append(q['id'])
    print('Knowledge files on disk: %d' % len(kids))
    print('Distinct ids in `knowledge` (analysed questions): %d' % len(cited))
    print('Distinct ids as `knowledge_main`: %d' % len(cited_main))
    missing_main = [q['id'] for q in qs if not q['knowledge_main']]
    print('Questions without knowledge_main: %d %s' % (len(missing_main), ' '.join(missing_main)))
    uncited = sorted(k for k in kids if k not in cited)
    print('\nKnowledge files cited by NO analysed question: %d of %d (%s)' % (len(uncited), len(kids), pct(len(uncited), len(kids))))
    byg = collections.defaultdict(list)
    for k in uncited:
        byg[group_of(k)].append(k)
    allg = collections.Counter(group_of(k) for k in kids)
    for g in sorted(byg):
        print('\n[%s] %d uncited of %d' % (g, len(byg[g]), allg[g]))
        for k in byg[g]:
            note = '   (cited by awaiting-input: %s)' % ' '.join(cited_aw[k]) if k in cited_aw else ''
            print('  ' + k + note)
    if awaiting:
        only_aw = sorted(k for k in uncited if k in cited_aw)
        print('\nUncited by analysed questions but cited by awaiting-input: %d' % len(only_aw))
    print('\nPer group: cited / total')
    for g in sorted(allg):
        c = sum(1 for k in kids if group_of(k) == g and k in cited)
        print('  %-40s %3d / %3d' % (g, c, allg[g]))
    print('\nClusters: knowledge files that are knowledge_main of 4 or more analysed questions')
    for k, ids in sorted(cited_main.items(), key=lambda kv: -len(kv[1])):
        if len(ids) >= 4:
            print('  %2d  %s\n      %s' % (len(ids), k, ' '.join(sorted(ids))))
    print('\nHistogram of questions per knowledge_main file: ' + ', '.join(
        '%d q=%d files' % kv for kv in sorted(collections.Counter(len(v) for v in cited_main.values()).items())))

    # ------------------------------------------------------------------ 9
    section('9. Knowledge ids that do not exist as files (all non-retired questions)')
    n = 0
    for q in allq:
        if q['status'] in ('retired', 'deferred'):
            continue
        refs = listify(q['knowledge']) + listify(q['knowledge_main'])
        for k in sorted(set(refs)):
            if k not in kids:
                n += 1
                print('  %s (%s): %s' % (q['id'], q['status'], k))
        if q['knowledge_main'] and q['knowledge_main'] not in listify(q['knowledge']):
            print('  %s: knowledge_main not in knowledge list: %s' % (q['id'], q['knowledge_main']))
    print('Total missing: %d' % n)

    # ------------------------------------------------------------------ 10
    section('10. Cross-tabs (analysed questions; multi-valued tags count once per value)')

    def xtab(title, rowf, colf):
        t = collections.defaultdict(collections.Counter)
        cols = collections.Counter()
        for q in qs:
            for r in rowf(q):
                for c in colf(q):
                    t[r][c] += 1
                    cols[c] += 1
        cl = sorted(cols, key=str)
        rows = sorted(t, key=str)
        print('\n%s' % title)
        w = max([len(str(c)) for c in cl] + [5])
        print('  %-8s' % '' + ' '.join('%*s' % (w, c) for c in cl) + ' %*s' % (w, 'total'))
        for r in rows:
            print('  %-8s' % r + ' '.join('%*d' % (w, t[r][c]) for c in cl) + ' %*d' % (w, sum(t[r].values())))
        print('  %-8s' % 'total' + ' '.join('%*d' % (w, cols[c]) for c in cl))

    lvl = lambda q: [q['level']]
    xtab('level x technology', lvl, lambda q: q['technology'] or ['(none)'])
    xtab('level x task', lvl, lambda q: listify(q['task']) or ['(none)'])
    xtab('level x misconception_type', lvl, lambda q: q['misconception_type'] or ['(none)'])
    xtab('level x object', lvl, lambda q: q['object'] or ['(none)'])
    xtab('level x tool', lvl, lambda q: q['tool'] or ['(none)'])
    xtab('level x input', lvl, lambda q: q['input'] or ['(none)'])
    xtab('technology x task', lambda q: q['technology'] or ['(none)'], lambda q: listify(q['task']) or ['(none)'])
    for name, f in (('object', lambda q: q['object']), ('tool', lambda q: q['tool']), ('misconception_type', lambda q: q['misconception_type'])):
        c = collections.Counter(x for q in qs for x in f(q))
        print('\nSingle counts, %s: ' % name + ', '.join('%s=%d' % kv for kv in c.most_common()))

    # ------------------------------------------------------------------ awaiting
    if awaiting:
        section('Awaiting-input questions (separate; not in the numbers above)')
        print('Count: %d' % len(awaiting))
        for q in awaiting:
            print('  %s level=%s answer=%s options=%d tech=%s | %s' % (q['id'], q['level'], ''.join(q['answer']), q['n_options'], ','.join(q['technology']), q['title']))
        print('\nBasic checks on awaiting-input: with answer %d, with options %d, knowledge ids missing: %d' % (
            sum(1 for q in awaiting if q['answer']), sum(1 for q in awaiting if q['options']),
            sum(1 for q in awaiting for k in set(listify(q['knowledge'])) if k not in kids)))

    if args.json_path:
        for q in allq:
            for k in [k for k in q if k.startswith('_')]:
                del q[k]
        for q in qs:
            pass
        out = {'statuses': dict(status_count), 'analysed_statuses': list(wanted), 'problems': problems,
               'questions': allq,
               'knowledge_cited': {k: v for k, v in cited.items()},
               'knowledge_main': {k: v for k, v in cited_main.items()},
               'knowledge_uncited': uncited}
        with open(args.json_path, 'w') as fh:
            json.dump(out, fh, indent=1, ensure_ascii=False, default=str)
        print('\nJSON written: %s' % args.json_path)


if __name__ == '__main__':
    main()
