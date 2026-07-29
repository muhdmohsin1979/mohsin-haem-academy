#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'evidence.json').read_text())
lines=[]
lines += [
'# MCL regimen / dose / schedule evidence package',
'',
'> **REPORT ONLY — NOT PHARMACY VERIFIED.** This is a source extraction, not a prescribing protocol. A human oncology/haematology pharmacist must verify the live SmPCs, all combination-agent SmPCs, local protocols, interactions, organ-function adjustments, supportive care and monitoring before clinical use.',
'',
f"- Package: `{data['package_id']}`",
f"- Created/cut-off: `{data['created_on']}`",
f"- Scope: {data['scope']}",
'- Machine-readable controlling index: [`evidence.json`](evidence.json)',
'- Packaged official source PDFs: [`pdfs/`](pdfs/)',
'- Page-marked text extractions: [`extracted-text/`](extracted-text/)',
'- Quote validator: `python3 validate_quotes.py`',
'- Package validator: `python3 validate_package.py`',
'',
'## Coverage',
'',
'Included: 10 licensed-MCL treatment records resolving to 8 unique MHRA SmPC PDFs. Excluded from dose extraction because the status matrix records no current GB MCL indication: ibrutinib–venetoclax, glofitamab and epcoritamab.',
'',
'## Source documents',
''
]
for s in data['source_documents']:
    lines += [f"- **{s['source_id']}** — [official MHRA SmPC]({s['official_url']})",f"  - SHA-256: `{s['sha256']}`",f"  - PDF: [`{s['local_pdf']}`]({s['local_pdf']})",f"  - text: [`{s['local_extracted_text']}`]({s['local_extracted_text']})"]

def emit_section(title,obj):
    lines.extend([f'### {title}', '', f"**Anchor:** {obj.get('anchor','See linked record/source.')}", ''])
    vals=[]
    if 'quote' in obj: vals.append(obj['quote'])
    vals.extend(obj.get('quotes',[]))
    for q in vals:
        lines.extend([f'> {q}', ''])
    for key in ('duration_boundary','non_inference_note','note','combination_agent_boundary','table_boundary_note'):
        if key in obj: lines.extend([f"**{key.replace('_',' ').title()}:** {obj[key]}",''])
    for key in ('verbatim_table_transcription','verbatim_dose_level_transcription'):
        if key in obj:
            lines.extend([f"**{key.replace('_',' ').title()}:**",''])
            val=obj[key]
            if isinstance(val,dict):
                for k,v in val.items(): lines.append(f"- **{k.replace('_',' ')}:** {v}")
            else:
                for v in val: lines.append(f'- {v}')
            lines.append('')

for i,r in enumerate(data['licensed_mcl_treatments'],1):
    lines += [f"## {i}. {r['treatment']}",'',f"- Status-matrix ID(s): `{', '.join(r['status_matrix_ids'])}`",f"- Official source: [{r['source_id']}]({r['official_source_url']})",f"- PDF SHA-256: `{r['pdf_sha256']}`",'']
    emit_section('Section 4.1 indication',r['indication'])
    emit_section('Section 4.2 dose, schedule and duration',r['dose_schedule_duration'])
    emit_section('Administration boundaries',r['administration_boundaries'])
    emit_section('High-level modification / monitoring constraints',r['modification_monitoring_constraints'])

lines += ['## Human pharmacy verification checklist','']
for item in data['verification_checklist']: lines.append(f'- [ ] {item}')
lines += ['','## Interpretation boundaries','',f"- {data['safety_notice']}",'- Exact quoted passages are whitespace-normalised from the packaged page-marked text and checked by `validate_quotes.py`. Table transcriptions are labelled separately because PDF table extraction does not preserve a simple reading order.','- The PDFs, not the text extraction or this report, are controlling sources.','- No missing combination-agent dose has been inferred. Where the SmPC redirects to another product SmPC, this package preserves that boundary.','']
(ROOT/'README.md').write_text('\n'.join(lines))
print(f"wrote {ROOT/'README.md'} ({len(lines)} lines)")
