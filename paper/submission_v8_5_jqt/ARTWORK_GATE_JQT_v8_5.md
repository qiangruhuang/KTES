# JQT v8.5 Artwork Submission Gate

**Date:** 10 October 2026  
**Target:** *Journal of Quality Technology* / Taylor & Francis  
**Status:** **PASS**

## Requirement

Taylor & Francis requires figures to be supplied separately from the main text. Its current artwork guidance recommends EPS for line art and requires adequate line weight and reliable font handling. The v8.3 SVG files remain the reproducible scientific masters.

## Execution

A fail-closed GitHub Actions workflow converted the four frozen anonymous SVG masters to EPS using Inkscape with text converted to paths. No scientific content, coordinates, values, labels, or evidence classification was edited during conversion.

- Workflow: `.github/workflows/export-jqt-v8-5-eps.yml`
- Workflow run: `38006438769`
- Result: `SUCCESS`
- Canonical EPS commit: `4fc03a303aad2526fba8f62e3fd4416e55cc578f`
- Review artifact: `jqt-v8-5-eps-figures`
- Artifact id: `11651591564`

## Canonical EPS hashes

| File | SHA-256 |
|---|---|
| `figures/figure1.eps` | `70e2b02b50ee5968495323c68a0ee0ed212a5f4454a2193785dcd32872a6f802` |
| `figures/figure2.eps` | `dfceab1087f162da0d5b07d75ef05d9cea4eabc8ec57b3d5cb01a2e568ecb479` |
| `figures/figure3.eps` | `c95381f187f094c9b54d9b5f0c92d647ff62c287427952a5ab175321e642f428` |
| `figures/figure4.eps` | `ebd2f3d7f9961598e891a8658aa16d79d1efa093bbbe14a3fdeb2b2934283825` |

## Integrity checks

- all four files start with the EPSF PostScript header;
- all four contain a single-page bounding box;
- reviewer-facing filenames are neutral;
- an identity scan found no author name, email, institution, or public-repository owner string;
- text was exported as vector paths to avoid font-substitution drift;
- original SVG scientific masters remain unchanged and available for future production export.

**Decision:** the artwork portion of the JQT v8.5 submission gate is closed. No figure redesign is required for first submission.
