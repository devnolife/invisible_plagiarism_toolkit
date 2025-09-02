# ✅ Refactor & Enhancement Progress Tracker

Baseline Commit: 2012845264ddff20aecce35d307327a178dc6032  
Date Started: 2025-08-15

Legenda Status:

- [ ] Belum dikerjakan
- [~] Sedang dikerjakan / in progress
- [x] Selesai
- [!] Perlu keputusan / klarifikasi

## Phase 0: Immediate Hygiene / Quick Wins

1. [x] Perbaiki indentasi salah di `invisible_manipulator.py` (blok akhir fungsi `apply_invisible_manipulation`)
2. [x] Perbaiki indentasi salah di `main.py` (fungsi `interactive_mode` baris pemanggilan `process_document`)
3. [x] Bersihkan `requirements.txt` (hapus modul standar library)
4. [x] Satukan mekanisme verifikasi (gunakan `compare_docx_invisibility` di engine)
5. [x] Tambah opsi CLI `--seed` untuk reproducibility (seed random)
6. [x] Tambah file `CHANGELOG.md` (mulai versi 1.1-dev)
7. [x] Tambah file ini (`TODO.md`) untuk tracking

## Phase 1: Konsistensi & Konfigurasi

1. [ ] Validasi schema `config.json` (Pydantic / manual minimal)
2. [ ] Central logging (gantikan print selain CLI)
3. [ ] Tambah `--dry-run` mode (menampilkan rencana perubahan tanpa menulis file)
4. [ ] Idempotency check (flag jika file sudah pernah diproses)

## Phase 2: Metrics & Reporting

1. [ ] Tambah skor risiko (density unicode & zero-width)
2. [ ] HTML/Markdown ringkas per dokumen (selain JSON)
3. [ ] Konsolidasi verifikasi: keluarkan struktur hasil yang sama di semua entry point

## Phase 3: Arsitektur Modular

1. [ ] Ekstrak teknik ke interface `Technique` (plugin-like)
2. [ ] Manager untuk mengatur urutan & agresivitas
3. [ ] Tambah teknik placeholder spacing (masih off)

## Phase 4: Testing & QA

1. [ ] Unit tests untuk header classifier edge cases
2. [ ] Property-based test untuk substitusi (Hypothesis) (opsional)
3. [ ] Test dokumen besar sintetis (performansi)
4. [ ] Test idempotency (proses ulang file yang sudah dimodifikasi)

## Phase 5: UX & CLI

1. [ ] Subcommands (misal `ipt process`, `ipt analyze`) – optional roadmap
2. [ ] Warna output (rich) – optional
3. [ ] Prompt ethics/consent pertama kali

## Phase 6: Dokumentasi & Distribusi

1. [ ] `CHANGELOG.md`
2. [ ] Diagram arsitektur (README update)
3. [ ] Packaging `pyproject.toml`

## Completed Log

- 2025-08-15: [x] Menambahkan `TODO.md` dengan baseline commit
- 2025-08-15: [x] Phase 0 Item 1 & 2 (perbaiki indentasi `invisible_manipulator.py` & `main.py`) – 3 tests passed (`pytest`): total=3, failed=0
- 2025-08-15: [x] Phase 0 Item 3 (clean requirements) – removed python-docx2txt
- 2025-08-15: [x] Phase 0 Item 5 (CLI --seed) – seed disimpan di report
- 2025-08-15: [x] Phase 0 Item 6 (CHANGELOG.md dibuat)
- 2025-08-15: [x] Phase 0 Item 4 (unify verification) – verify_invisibility delegasi ke compare_docx_invisibility

## Catatan

- Setiap selesai item akan ditandai dan contoh output (log ringkas / diff) akan dicantumkan di bagian Completed Log.
- Mohon konfirmasi jika prioritas ingin diubah atau ada item tambahan.
