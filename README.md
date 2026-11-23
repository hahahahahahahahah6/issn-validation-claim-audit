# Documentation claim audit

This offline tool compares selected documentation statements with Python call shapes. It examines a serial number's check digit. It never executes source code or uses the network.

Install and run:

```sh
issn-validation-claim-audit audit . --verbose
issn-validation-claim-audit audit . --json --fail-on medium
python3 -m issn_validation_claim_audit --version
```

The optional path defaults to the current directory. Repeat `--ignore PREFIX` to exclude path prefixes. Findings at the selected threshold produce exit code 2; errors produce 1 and a clean result produces 0. The default threshold is high. Markdown in the root README and directories named `docs` is scanned, excluding fenced blocks. Inline code counts. Python files are parsed statically; test evidence is reported separately. Source under fixtures, examples, and docs is excluded. Symbolic links are skipped.

Finding identifiers:

```
documented-issn-validation-claim-false
documented-no-issn-validation-claim-false
```

## Differentiation

This scope is a serial number's check digit of ISSN. Other families cover generic input checks, ISBN-10 and ISBN-13 book number checks, payment processing, credit-card extraction, account confirmation by one-time code or link, password authentication, password hashing, password generation, PDF encryption, email sending, SMS sending, document extraction, barcode scanning, email address checks, phone number checks, password strength, JSON Schema checks, calendar date checks, credit-card checks, domain checks, URL checks and IP address checks.

Other tasks include JSON decoding, regex matching, URL parsing, network fetching, DNS resolution, barcode generation, reading a serial from a document, reshaping or converting a serial to EAN-13, and publication registry lookup. Other claim-audit families cover spreadsheet reading and generation, word-document reading and generation, presentation reading and generation, PDF extraction, generation, merging, splitting, rotation, form-filling, watermarking, redaction, compression and annotation, table extraction, OCR, document extraction, e-signature, screen recording, video generation, QR code generation, barcode generation and scanning, audio mixing, generation and editing, source separation, speech recognition, text-to-speech, noise suppression, music generation and transcription.

## Limitations

Exact phrase matching cannot infer intent. Each expression below can describe a different activity and cause a false positive; a human must decide.

```
validate issn
```

This expression can refer to a catalogue lookup.

```
check issn
```

This expression can refer to a manual runbook step.

```
issn validation
```

This expression can refer to a roadmap feature.

```
issn validator
```

This expression can refer to a hosted page.

```
valid issn
```

This expression can refer to reader advice.

```
issn is valid
```

This expression can refer to a successful lookup.

```
issn number validation
```

This expression can refer to a specification section.

```
validate serial number
```

This expression can refer to a publisher list lookup.

```
verify issn
```

This expression can refer to a catalogue lookup.

```
detect invalid issn
```

This expression can refer to a length-only rule.

```
issn well formed
```

This expression can refer to a theoretical discussion.

```
is valid issn
```

This expression can refer to a generated value.

```
issn format validation
```

This expression can refer to a hyphen layout rule.

```
validate issn code
```

This expression can refer to an allow-list lookup.

```
issn check
```

This expression can refer to a manual runbook step.

```
serial number validation
```

This expression can refer to a specification section.

```
issn serial validation
```

This expression can refer to a design discussion.

A compact call only reshapes a value and does not count.

A format call only reshapes a value and does not count.

A check-digit calculation alone does not count, even if compared afterward.

Conversion to EAN-13 does not count.

A registry data lookup does not count.

An ISBN-10 call does not count.

An ISBN-13 call does not count.

A barcode class construction does not count.

A regular expression match alone does not count.

An untraceable variable chain can hide a real library call.

A bare import does not count.

A roadmap statement is still treated as a claim.

A changelog statement is still treated as a claim.

A TODO statement is still treated as a claim.

An unlisted denial may be missed while an included positive expression still matches.

A top-level changelog outside the selected documentation paths is ignored.

Evidence split across modules is missed.

Local definitions can shadow route names, including wrappers.

Dead code counts because execution is not inspected.

A subprocess invocation does not count.

A generic input check alone does not count.

An email address check alone does not count.

A phone number check alone does not count.

A URL check alone does not count.

An IP address check alone does not count.

A domain check alone does not count.

A book number check alone does not count.

An extraction call alone does not count.

A locally defined generic route is shadowed.

A generic route behind an untraceable alias chain is missed.

Paraphrases outside the lists are missed; listed expressions in unrelated contexts can be flagged.

Implementations in other languages are invisible.

Runtime-only plugins and dynamic imports are invisible.
