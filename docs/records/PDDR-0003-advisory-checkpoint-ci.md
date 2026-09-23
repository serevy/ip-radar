---
id: PDDR-0003
title: Add advisory checkpoint CI without widening the semantic trust boundary
decision_date: 2026-09-24
recorded_date: 2026-09-24
decision_status: accepted
delivery_status: implemented
scope:
  - project
  - process
owners:
  - serevy
evidence:
  - "Maintainer approved early adoption of hardened checkpoint CI, 2026-09-24 (private)"
  - "https://github.com/serevy/pddr-kit/releases/tag/v0.2.1"
  - ".pddr/pddr_checkpoint.py"
  - ".github/workflows/pddr-checkpoint.yml"
  - ".github/workflows/pddr-checkpoint-marker.yml"
related:
  - PDDR-0001
  - PDDR-0002
supersedes: []
superseded_by: null
---

# PDDR-0003: Add advisory checkpoint CI without widening the semantic trust boundary

## Summary

IP RadarでdurableなProject / Product / Process判断の取りこぼしを減らすため、PDDR Kit v0.2.1のoptional checkpoint CIをrepository-side advisory safety netとして導入する。

このCIはGitHub上のPR metadataとchanged-file surfaceを用いてreview signalを残すだけで、external semantic reasoning、patentability判定、candidate scoring、IP evidence disclosureの境界を広げない。

## Context and observations

- IP Radarは開発履歴、未公開技術情報、security / privacy境界を扱うため、判断記録の理由と適用範囲を後から追跡できる必要がある。
- AGENTS.mdには既にmilestone checkpoint guidanceがあるが、Agent Skillが常時activeでない変更経路ではcheckpoint実施そのものを取りこぼす可能性がある。
- PDDR-0002はexternal semantic reasoningをuntrustedとして扱うsecurity boundaryを定めている。
- Checkpoint CIはそのsemantic boundaryとは別のrepository processであり、外部modelへtechnical evidenceを送る理由にはならない。
- PDDR Kit v0.2.1ではPR headを観測するread-only signal workflowとtrusted default-branch writerへ権限分離されたCheckpoint CIが提供されている。

## Options considered

### Existing AGENTS guidanceだけを使う

- Benefits: CI追加なし。
- Costs / constraints: Agent contextが読み込まれない変更経路でcheckpoint signalが残らない。
- Status: rejected as the only mechanism

### Checkpoint CIにsemantic classificationも持たせる

- Benefits: decision候補をより細かく自動判定できる可能性がある。
- Costs / constraints: PDDR reviewとIP Radarのexternal semantic trust boundaryを混同し、evidence disclosure surfaceを広げる。
- Status: rejected

### Deterministic advisory Checkpoint CIだけを追加する

- Benefits: semantic trust boundaryを広げず、durable decision reviewの取りこぼしを補完できる。
- Costs / constraints: semantic auditはAgent / maintainerに残る。
- Status: accepted

## Decision

- PDDR Kit v0.2.1のhardened Checkpoint CIを導入する。
- signal workflowはPR headを観測するがread-onlyとする。
- PR本文 / commentへのwriteはdefault branchのtrusted `workflow_run` writerだけが担当する。
- privileged writerはPR headのcode / artifactを実行しない。
- Checkpoint SignalはPDDR requiredを意味しない。
- routine implementation、candidate signal、raw observation、experiment completionだけではPDDRを作らない。
- checkpoint CIはexternal semantic provider、patentability判定、novelty判定、candidate scoringを行わない。
- technical evidenceを外部modelへ送るauthorityをこのCIから導かない。
- no durable decisionならno-opを正常結果とする。

## Delivery and validation

detector、read-only signal workflow、trusted marker writer、AGENTS pending-marker guidanceを実装した。

PDDR Kit v0.2.1側では同じ2段構成がconsumer E2E済みである。IP Radar自身では、この導入PRがdefault branchへ入るまでtrusted marker writerのwrite pathを検証できないため、現時点のdeliveryは `implemented` とする。

導入後のhigh-signal PRでpending marker writeとcompleted回収を確認した時点で `validated` を再評価する。

## Consequences

- Agent contextが一時的に失われてもcheckpoint候補をrepository側へ残せる。
- IP Radarのsemantic security boundaryを広げずにProcess reviewを補完できる。
- routine candidate / evidence activityをPDDR volumeへ直接変換しない。
- write-capable tokenとPR head code executionを同じjobに置かない。
- GitHub Actions workflowが増えるが、IP discovery runtimeやLLM provider policyは変更しない。

## Revisit when

- checkpoint CIがsemantic reasoningやIP判定として誤解される場合。
- false positive / false negativeが継続する場合。
- repositoryのsecurity / disclosure modelが変わる場合。
- GitHub Actions以外へCIを移行する場合。

## Evidence

- Maintainer approval of early hardened checkpoint CI adoption, 2026-09-24 (private).
- [PDDR Kit v0.2.1](https://github.com/serevy/pddr-kit/releases/tag/v0.2.1)
- `.pddr/pddr_checkpoint.py`
- `.github/workflows/pddr-checkpoint.yml`
- `.github/workflows/pddr-checkpoint-marker.yml`
- `AGENTS.md`

## Related records

- PDDR-0001: Keep IP Radar focused on evidence-backed provenance reconstruction
- PDDR-0002: Put untrusted semantic reasoning behind a layered security boundary
