# OBLATE LOCAL BOUNDARY ENTRY — BAND [31/32, 1] JUDGE RECEIPT

**Status**: `JUDGE_PASS / CONDITIONAL_ON_TWO_LEMMAS / EXTERNAL_AUDIT_PENDING`

~~~
JUDGE_DECISION = PASS
scope   = Claims 1-3 of analysis/LOCAL_ENTRY_BAND_JUDGE_REQUEST.md
request = commit 424b5413c1e44cbaecaec61494a05d1aef28e250  blob 6349489a01c50f937b8d67aa47a05c9335af9a98
judge   = human Judge (repository owner), 2026-09-21
~~~

~~~
conditional_on:
  OBLATE_ENDPOINT_C1_LEMMA                  commit aefa8ed2  blob 5afa815ff24760ab5ebbb63bcbae912c9c7a84c6
  MONOTONE_TUBE_C2_INTERCHANGE_LEMMA_31_32  commit f66ffe5a  blob 5c3dfeb3d0283aae50df7cd26af2621c2fa39aec
  both EXTERNAL_AUDIT_PENDING / NOT_BINDING
~~~

The conditions are the identifications of the machine quantities with `partial_t g_axis_ob` and `g_axis_ob`, and of `g_axis_ob(1,lambda)` with `B_ob(lambda)`. They are discharged when both lemmas pass external audit.

Evidence relied upon: exactly §2–§4 of the request. Runs #87 (33362970980), #101 (33368313307) and #147 (33371387643) of workflow 346289126; blobs 5808e845, c2fee400, fd778d6d, 99c2a196, 61068734, e927cda5, 3d38a16e, 8b3cb9ab, b11617f3, 9f03d6f5; raw audits c3b3666d, 138b3cee, c9e3ef8b; B_ob receipt 705623b0.

Consequences as in §6 of the request, under the same conditions; condition (ii) of the B_ob receipt is thereby discharged for the band. The exclusions of §7 are confirmed. This receipt supersedes the template (blob 5389bfba) as the band's Judge record; the conversation-only approval of 2026-08-31 is not relied upon.
