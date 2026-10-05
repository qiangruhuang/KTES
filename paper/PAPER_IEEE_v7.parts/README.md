# Frozen v7 IEEE manuscript parts

The canonical v7 manuscript is split only because the GitHub connector used for this archival push accepts UTF-8 text bodies rather than a local file stream.

The split is lossless and follows original line boundaries:

- `part01.md`: lines 1–90
- `part02.md`: lines 91–180
- `part03.md`: lines 181–270
- `part04.md`: lines 271–360
- `part05.md`: lines 361–450
- `part06.md`: lines 451–540
- `part07.md`: lines 541–604

Rebuild from the repository root:

```bash
python scripts/rebuild_paper_ieee_v7.py
```

Expected reconstructed artifact:

- file: `paper/PAPER_IEEE_v7.md`
- bytes: `68,278`
- SHA-256: `49f4810fa2cbfe91b9d9143cfa7715b1250939d5d28d7e476b896eb8ca4ce01d`

Part SHA-256 values:

| Part | SHA-256 |
|---|---|
| part01.md | `ea0a18f9f9c30650c6a81d2a075b13cc3d02aa5ceced1f8db7df6feae65a3785` |
| part02.md | `511996db0023f2ba5f702963c58e54e08f1cf4245d13e843f45449e0bccc5efd` |
| part03.md | `9df306a6b6a3a01c950f6c69c94cb4bd546a2bbb87ea3888e1e31f7b9aaf5bde` |
| part04.md | `dca665ccf88a6f99feb1bc08b21db4b972d0ff535e88536bbaa4a8fdc31b8595` |
| part05.md | `f300f963e990c3e24faa20d9787fbbed1ec2b78824fc48e44e5366a64ce7dcd0` |
| part06.md | `d2bffa91c10d1559ab8a0de1d315a5b8dac8483143dcf0ac2e56c1ee9f8cbf5c` |
| part07.md | `091ba41581e8edd298168aa05f257dfb66af9db1bb97eb25fa9998ad213fb6f6` |
