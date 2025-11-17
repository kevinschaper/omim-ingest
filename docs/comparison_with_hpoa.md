# Comparison with HPOA ETL Process

## Background

The Human Phenotype Ontology Annotation (HPOA) team previously processed OMIM gene-to-disease associations via MedGen's `genes_to_disease.txt` file. This document compares our direct OMIM morbidmap.txt ingest with HPOA's approach.

## Data Sources

| Pipeline | Source File | Data Origin | Gene IDs | Rows |
|----------|-------------|-------------|----------|------|
| **HPOA** | genes_to_disease.txt | MedGen via OMIM | NCBIGene | 16,966 |
| **HPOA Transformed** | hpoa_gene_to_disease_edges.tsv | HPOA ETL (infores:omim only) | NCBIGene | 9,625 |
| **Our Direct Ingest** | morbidmap.txt | OMIM directly | OMIM gene IDs | 5,990 |

## Key Differences

### 1. Predicate Distribution

**HPOA Edges (infores:omim)**:
- `biolink:causes`: 9,029 (93.81%)
- `biolink:contributes_to`: 596 (6.19%)

**Our Direct OMIM Ingest** (current):
- `biolink:causes`: 6,983 (91.35%)
- `biolink:contributes_to`: 661 (8.65%)

### 2. Association Type Mapping

**HPOA Approach** (from genes_to_disease.txt):

| association_type | Count | HPOA Predicate | HPOA Category |
|------------------|-------|----------------|---------------|
| MENDELIAN | 8,164 | `biolink:causes` (primary) | CausalGeneToDiseaseAssociation |
| MENDELIAN | - | `biolink:contributes_to` (some) | CorrelatedGeneToDiseaseAssociation |
| POLYGENIC | 586 | `biolink:contributes_to` | CorrelatedGeneToDiseaseAssociation |
| UNKNOWN | 8,216 | Varies | - |

**Our Approach** (from morbidmap.txt):

| OMIM Marker | Predicate | Category |
|-------------|-----------|----------|
| Confidence (3), no `{}` | `biolink:causes` | CausalGeneToDiseaseAssociation |
| Confidence (1,2), no `{}` | `biolink:contributes_to` | CorrelatedGeneToDiseaseAssociation |
| Any `{}` marker | `biolink:contributes_to` | CorrelatedGeneToDiseaseAssociation |

## Predicate Agreement Analysis

### Disease Coverage (with newer data)
- **Overlapping diseases**: 6,810
- **HPOA only**: 38
- **Our ingest only**: 46

### Actual Predicate Agreement: 91.1%
- **Total disease-level matches**: 15,352
- **Agreements**: 13,979 (91.1%)
- **Disagreements**: 1,373 (8.9%)

### Agreement Matrix

| HPOA Predicate | Our Predicate | Count | % of Matches |
|----------------|---------------|-------|--------------|
| `biolink:causes` | `biolink:causes` | 11,356 | 73.97% ✓ |
| `biolink:contributes_to` | `biolink:contributes_to` | 2,623 | 17.09% ✓ |
| `biolink:causes` | `biolink:contributes_to` | 761 | 4.96% |
| `biolink:contributes_to` | `biolink:causes` | 612 | 3.99% |

**Total Agreement**: 13,979 / 15,352 = **91.1%**

### Understanding the Agreement

The 91.1% agreement reflects strong alignment where:
- Both use `causes` for non-susceptibility confidence (3) cases (73.97%)
- Both use `contributes_to` for susceptibility/POLYGENIC cases (17.09%)

The 8.9% disagreement represents:
- 4.96%: We use `contributes_to` (detected `{}`), HPOA uses `causes` (classified as MENDELIAN)
- 3.99%: We use `causes` (no `{}`), HPOA uses `contributes_to` (classified as POLYGENIC)

These differences likely stem from:
1. Subtle discrepancies between OMIM's `{}` markers and HPOA's POLYGENIC classification
2. Data differences between morbidmap.txt and MedGen's genes_to_disease.txt

## HPOA Alignment Strategy

### Our Approach

We align with HPOA by **respecting susceptibility markers** `{}`, which correspond to HPOA's POLYGENIC classification:

✅ **Excellent agreement**: 91.1% predicate alignment
✅ **Semantic precision**: Captures OMIM's susceptibility semantics
✅ **HPOA compatibility**: Matches POLYGENIC → `contributes_to` pattern
✅ **Two-predicate model**: Uses causes/contributes_to

### How It Aligns with HPOA

**HPOA's classification**:
- MENDELIAN → `causes`
- POLYGENIC (includes susceptibility) → `contributes_to`

**Our mapping**:
- Confidence (3), no `{}` → `causes` (matches MENDELIAN)
- Any `{}` marker → `contributes_to` (matches POLYGENIC)

This works because OMIM's `{}` susceptibility markers correspond to HPOA's POLYGENIC classification.

## Recommendations

### For Users

✅ **Use this direct OMIM ingest** for:
- Better semantic precision (respects OMIM susceptibility markers)
- Excellent alignment with HPOA (91.1%)
- Direct parsing of morbidmap.txt (no MedGen intermediary)
- Proper handling of susceptibility relationships

### Key Advantage

By parsing `{}` markers directly from morbidmap.txt, we achieve alignment with HPOA's POLYGENIC classification without relying on MedGen's intermediate `association_type` field.

## Data Quality Comparison

| Aspect | HPOA ETL | Our Direct Ingest |
|--------|----------|-------------------|
| Predicate agreement | Baseline | 91.1% |
| Predicate usage | 2 predicates | 2 predicates |
| Susceptibility handling | POLYGENIC classification | `{}` marker detection |
| Semantic precision | Via association_type | Direct from OMIM |
| RO alignment | RO:0002326, RO:0003303 | RO:0002326, RO:0003303 |
| Source | MedGen (indirect) | morbidmap.txt (direct) |

## Conclusion

Our susceptibility-aware approach achieves **91.1% predicate agreement** with HPOA by aligning `{}` markers with HPOA's POLYGENIC classification.

**Key advantages**:
- ✅ Semantic precision: Directly interprets OMIM's susceptibility markers
- ✅ Excellent HPOA alignment: 91.1% agreement
- ✅ Direct source: Parses morbidmap.txt without MedGen intermediary
- ✅ Explicit logic: Clear handling of susceptibility cases
- ✅ Similar distribution: 91.35% causes vs HPOA's 93.81%

The 8.9% disagreement is minimal and reflects edge cases where OMIM's `{}` markers and HPOA's POLYGENIC classification diverge slightly, plus data differences between morbidmap.txt and MedGen's genes_to_disease.txt.

## Analysis Methodology

This comparison was performed using DuckDB to:
1. Load HPOA genes_to_disease.txt (source data)
2. Load HPOA transformed edges filtered to infores:omim
3. Load our OMIM ingest output
4. Join on disease IDs (object) to compare predicates
5. Analyze disagreement patterns by HPOA association_type

Analysis code and detailed results available upon request.
