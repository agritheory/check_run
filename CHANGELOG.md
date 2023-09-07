# CHANGELOG



## v13.3.2 (2023-09-07)

### Ci

* ci: migrate to python semantic release (#134)

* ci: migrate to python semantic release

* ci: add version variable file

* ci: update remote name ([`404edf3`](https://github.com/agritheory/check_run/commit/404edf35cae2180a02a45be875fcb54ef7e92cef))

### Fix

* fix: only increment if check numer is numeric (#138) ([`30679db`](https://github.com/agritheory/check_run/commit/30679db1985fcc0a41238d8860a17c019b751d98))

### Unknown

* File Preview (#140)

* wip: file preview

* feat: preview in check run, allow to preview in non submittable documents

* feat: WIP payables attachment report

* feat: wip preview of attachments

* style: prettify code

* feat: close with space

* fix: do not open sidebar in check run

* wip: multiple attachments in check run

* fix: merge

* style: prettify code

* fix: df-preview-wrapper-fw

* feat: improve code

* feat: improve code

* feat: columns

---------

Co-authored-by: Tyler Matteson &lt;tyler@agritheory.com&gt;
Co-authored-by: fproldan &lt;fproldan@users.noreply.github.com&gt; ([`a698431`](https://github.com/agritheory/check_run/commit/a698431b7ac850b5dc4203ecbb8c65ada0f0a152))


## v13.3.1 (2023-07-28)

### Unknown

* trans: add error message to translations (#128) ([`6f17c03`](https://github.com/agritheory/check_run/commit/6f17c034cffa18e28a2b1633f40b270853a21b01))


## v14.5.1 (2023-07-28)

### Fix

* fix: show purchase returns in list (#130) ([`c504828`](https://github.com/agritheory/check_run/commit/c504828c1bbe1552e9a3cc87f87082c5f89dae7b))


## v14.5.0 (2023-07-24)

### Feature

* feat: migrate validation to doc_events from doctype override (#127)

* feat: migrate validation to doc_events from doctype override

* feat: disallow cancellation of source documents selected for payment in draft CRs (#126)

* feat: migrate validation to doc_events from doctype override

* feat: disallow cancellation of source documents selected for payment in draft CRs (#126) ([`45c9598`](https://github.com/agritheory/check_run/commit/45c959834a60d57148b4443e902f25c2c56a30ff))


## v14.4.0 (2023-07-24)

### Feature

* feat: disallow cancellation of source documents selected for payment in draft CRs (#126) ([`329c41c`](https://github.com/agritheory/check_run/commit/329c41c9d1470a97deaa45b7972c9e6818c8aa3b))


## v14.3.2 (2023-07-19)

### Fix

* fix: broken translation string in csv (#121) ([`e3c87b4`](https://github.com/agritheory/check_run/commit/e3c87b415fe54e94562cc712948b44d33b0d8519))


## v14.3.1 (2023-06-11)

### Fix

* fix: add check for expense claim in pre-process validation (#112) ([`1503fa9`](https://github.com/agritheory/check_run/commit/1503fa9cad5e7e0a74614a2dcd63eea1797024cc))


## v14.3.0 (2023-06-11)

### Feature

* feat: add validate when processing, enable on_update_after_submit hook (#111)

* feat: add manual validate when processing and enable on_update_after_submit hook

* feat: update db call to prevent timestamp mismatches ([`2e87a26`](https://github.com/agritheory/check_run/commit/2e87a260035cfd81466cb0206f8d718a2d107551))

### Unknown

* Pre process validation (#107)

* fix: add de-duplication API

* feat: check payment entries for cancelled or paid invoices before submitting ([`666f1cb`](https://github.com/agritheory/check_run/commit/666f1cbbf096c7b2c3f9267197143bc8cd64a505))

* New Pull Request for Adding Individual ID Number (#102)

* Update achgeneration.md

Add Individual ID Number documentation

* Update check_run_settings.json

Add field for Individual ID Number From to select the source as None, Naming Series, or Party Name

* Update check_run.py

Add logic to use choice made in check_run settings to assign the appropriate value to individual_id_number

* Fix syntax errors

The new if/elif/else clauses for individual_id_number_from around lines 687-694 were incorrectly pasted into the prior exceptions.append parenthesis ([`7228c51`](https://github.com/agritheory/check_run/commit/7228c518bbdf23777a35df2f8eca60d49865ee63))


## v14.2.2 (2023-05-12)

### Chore

* chore: fix account names in test data (#100) ([`025a61d`](https://github.com/agritheory/check_run/commit/025a61d67cb9b2604b7802d178bfc1c71fc5d758))

### Fix

* fix: reprint button text color (#103) ([`7101284`](https://github.com/agritheory/check_run/commit/7101284f5007723877d312efa753b9c16a6efb2e))

### Unknown

* Fix process check run (#97)

* feat: disallow processing twice from front end

* feat: push status change to Vue with reactivity for UX

* feat: use global default flag to prevent refresh-related errors

* feat: disallow submission of _all_ Check Runs while one is submitting ([`6651b64`](https://github.com/agritheory/check_run/commit/6651b6494be15d8ef359b4a4eb1bccc66ea04215))

* Code style (#96)

* chore: black

* chore: prettier

* chore: remove json diff ([`5512249`](https://github.com/agritheory/check_run/commit/55122496b879d4edf3252d333c231903bd26fcc5))


## v13.2.2 (2023-04-18)

### Unknown

* Update ACH Documentation

Documents the use of the posting date as the Effective Entry Date in ACH file generation ([`1386f8b`](https://github.com/agritheory/check_run/commit/1386f8b3b54e13f66bcb799f479254df4555c04e))

* Update effective entry date

Update effective entry date to posting date in check_run.py ([`49b2f3d`](https://github.com/agritheory/check_run/commit/49b2f3d851664bbb77a32426d81cab39218842f2))


## v14.2.1 (2023-04-17)

### Fix

* fix: check for docstatus instead of status ([`c8c138a`](https://github.com/agritheory/check_run/commit/c8c138abf931e76d690110a81c293a223445602b))

### Unknown

* Merge pull request #93 from agritheory/new_check_run_fix

fix: check for docstatus instead of status ([`c9fc0c7`](https://github.com/agritheory/check_run/commit/c9fc0c796b3f45c3f007e8687875421e85ae6ea4))


## v14.2.0 (2023-04-06)

### Chore

* chore: prettify ([`3859c9e`](https://github.com/agritheory/check_run/commit/3859c9e07861a5c0ce2c934560ac98a5fbffabe3))

### Unknown

* Merge pull request #79 from agritheory/ach_post_processing_hook

ACH post processing hook ([`14defa3`](https://github.com/agritheory/check_run/commit/14defa322c4eac0fec74322ec2a643be16ac6576))

* Merge branch &#39;version-13&#39; into ach_post_processing_hook ([`e436183`](https://github.com/agritheory/check_run/commit/e4361830ba08c45bf81d255bb9d95af6f45d273d))

* Merge pull request #88 from agritheory/ci

chore: prettify ([`2facc33`](https://github.com/agritheory/check_run/commit/2facc333dd019ff293ddc5f231564c4c393fa9af))

* Merge pull request #86 from agritheory/ci

Ci ([`07be876`](https://github.com/agritheory/check_run/commit/07be8763bf16ca3eeac509490ac8c3fa1e3a22e5))


## v13.1.0 (2023-04-04)

### Ci

* ci: get release working correctly ([`3b01c36`](https://github.com/agritheory/check_run/commit/3b01c36ce6d33a8779d5ef383e50b6180ced88ed))


## v14.1.0 (2023-04-04)

### Chore

* chore: fix typo, remove reference to undeclared variable ([`9d3ca6f`](https://github.com/agritheory/check_run/commit/9d3ca6f146d37e6532dc77720f5788519e101fba))

### Ci

* ci: remove registry from package.json ([`4143e2d`](https://github.com/agritheory/check_run/commit/4143e2daadda69ba4eff53685ba26225a2b463aa))

* ci: replace lock file ([`5cea502`](https://github.com/agritheory/check_run/commit/5cea502f9b2b6f475a389c213c96090e6b4ce082))

* ci: working release workflow ([`58df7f6`](https://github.com/agritheory/check_run/commit/58df7f6583d48fcc887118a45c001de8ac5e2053))

* ci: fix install problem ([`9db35ab`](https://github.com/agritheory/check_run/commit/9db35aba0202285237dafdbec4aca45c8b1e229a))

* ci: fix install problem ([`67743f3`](https://github.com/agritheory/check_run/commit/67743f3ba6a0580b6d466428d826fb7902af9023))

* ci: fix install problem ([`8b38ead`](https://github.com/agritheory/check_run/commit/8b38ead4d69416c37942d42063b68226e79c0612))

* ci: fix install problem ([`7726477`](https://github.com/agritheory/check_run/commit/772647701db65c3bf7453a29727aa2c6ef9bb5a7))

* ci: fix install problem ([`7357dbf`](https://github.com/agritheory/check_run/commit/7357dbfb05a5e8891768b76f2e547c0aa68d0862))

### Documentation

* docs: document new ACH features ([`a9a0e72`](https://github.com/agritheory/check_run/commit/a9a0e7247dace4ce63bcd201db42af6edaaf5f3a))

### Feature

* feat: add ach post processing hook ([`5619b3d`](https://github.com/agritheory/check_run/commit/5619b3d0c58a13288e937c5c5c6e36fa4d6a87c0))

* feat: add field for immediate origin (#75) ([`531b307`](https://github.com/agritheory/check_run/commit/531b3077316af0fdfcef5cfd4ece04bc29b95493))

* feat: increment check number from payment (#70)

* feat: increment check number from payment

* style: prettify code

---------

Co-authored-by: agritheory &lt;agritheory@users.noreply.github.com&gt; ([`00706ff`](https://github.com/agritheory/check_run/commit/00706ff8c17a20f99ddff53beb62e450ff09eb5c))

* feat: look up party on PE submission to avoid renaming problems (#67) ([`4cdf7de`](https://github.com/agritheory/check_run/commit/4cdf7de5d648bcd37cb19ce67d899804f7107ad3))

* feat: add logic for handling on-hold invoices, setting for automatic release and docs ([`63bd16e`](https://github.com/agritheory/check_run/commit/63bd16eaf6aa1b2f9f4738ad0f860c731e84d721))

* feat: add Canadian regionalization for v-13 ([`5cbd277`](https://github.com/agritheory/check_run/commit/5cbd277c7979e54c545e04c415dd2f836a3c6dd4))

* feat: add more detail to cancelled document validation error message ([`6a99349`](https://github.com/agritheory/check_run/commit/6a9934956d7f62cfc5b286e8ab06c621b15071b8))

* feat: validate docstatus of selected invoices in Check Run still saved/submitted ([`9bf5605`](https://github.com/agritheory/check_run/commit/9bf56054041c341fc23c4cdf0a9449ca32ef8ba5))

* feat: add omit origin ach setting ([`b72901e`](https://github.com/agritheory/check_run/commit/b72901e0a6bf806c012a91bbba28ee765efecac0))

### Fix

* fix: release (#82)

* fix: release

* fix: test release ([`9b32e9b`](https://github.com/agritheory/check_run/commit/9b32e9b036f0ff16d21d65ba96851bc8d03e8c5a))

* fix: test release ([`f5cd245`](https://github.com/agritheory/check_run/commit/f5cd245154802b1c4c78b4dcce47677064ec7ddb))

* fix: release ([`8a8ec06`](https://github.com/agritheory/check_run/commit/8a8ec062f263d49a9bcd7487af6f5de9372fcde1))

* fix: fallbacks and length limitations for discretionary data ([`f783951`](https://github.com/agritheory/check_run/commit/f7839517f043fa811ab030b92608826e4bbb0f0e))

* fix: don&#39;t raise exception on bank account lookup, better UX (#60) ([`1d5d018`](https://github.com/agritheory/check_run/commit/1d5d018c9e1703b41ee568482f9fb0f57f2d4c62))

* fix: validate if there are any transactions before validating them ([`2aa94a7`](https://github.com/agritheory/check_run/commit/2aa94a7306db4107d7e15ddd33767169f52a06b7))

* fix: address PR requests ([`084fb22`](https://github.com/agritheory/check_run/commit/084fb2253b62908440df0d3b4993eb4b1f0d376b))

* fix: MOP ignore keypress if input is focused ([`8d2d697`](https://github.com/agritheory/check_run/commit/8d2d6975973041e07616fb6704b72ffe3655cd04))

* fix: remove mimesis import ([`bdbadea`](https://github.com/agritheory/check_run/commit/bdbadea1759c0cf4ad469677606704dbf02bf078))

### Test

* test: fix net 14 days ([`140657a`](https://github.com/agritheory/check_run/commit/140657a181fcee15b34b5753c6ab81eba0d65e4a))

* test: make release_date greater than due_date ([`9c05d82`](https://github.com/agritheory/check_run/commit/9c05d825e8d8c26ea2b38e7d141e4662ac784d03))

* test: add payment terms to test data ([`d24ff79`](https://github.com/agritheory/check_run/commit/d24ff79d5db4324503515ac9df60d9bb425475e1))

* test: add on hold invoice to test data ([`c8776ec`](https://github.com/agritheory/check_run/commit/c8776ec29ebe89bdcf787701b7c5421ff9e00eaf))

### Unknown

* Merge pull request #84 from agritheory/fix_release

Fix release ([`7fa06b7`](https://github.com/agritheory/check_run/commit/7fa06b72bd8404e877cf35f1d36b9b8b6bb75a9a))

* Merge branch &#39;version-13&#39; into fix_release ([`d023ccb`](https://github.com/agritheory/check_run/commit/d023ccb187cb0c5de9a89e1acd550a0ebad7e1fb))

* Merge pull request #78 from put3r-r00t3r/version-13

Add max length 10 for ACH Description field ([`a2f5498`](https://github.com/agritheory/check_run/commit/a2f5498e9fbf8301f47b842bb19078f2d4a90c97))

* Update check_run_settings.json

Add missing comma ([`1579fbc`](https://github.com/agritheory/check_run/commit/1579fbc158ff982eb778a327bc418701067de6a6))

* Update check_run_settings.json

Update modified timestamp. ([`0fb2c70`](https://github.com/agritheory/check_run/commit/0fb2c70e4dcb30c165378c09bab9c459949bb575))

* Update check_run.py

Add maximum length 10 for Company Entry Description to maintain proper format of batch header in NACHA file output. ([`26bee17`](https://github.com/agritheory/check_run/commit/26bee17f39318ca2c6b1a79683a0cf758c2cdb76))

* Update check_run_settings.json

Add maximum length 10 for ACH Description to maintain proper format of batch header in NACHA file output. ([`abb82ea`](https://github.com/agritheory/check_run/commit/abb82eaf808917f4bac285b301f93d2f27672f39))

* Merge pull request #77 from put3r-r00t3r/version-13

Add field for Discrectionary Company Data ([`bff59b9`](https://github.com/agritheory/check_run/commit/bff59b9826c63ce23a2923ef3d4dedd74b0c9634))

* Merge pull request #1 from agritheory/disc_data

fix: fallbacks and length limitations for discretionary data ([`0b285f2`](https://github.com/agritheory/check_run/commit/0b285f2eb261482e1cc5764f38de48885e0362a6))

* Merge branch &#39;version-13&#39; into disc_data ([`c00ca48`](https://github.com/agritheory/check_run/commit/c00ca48b136a5373c7f4750c92e1405e424590d6))

* Update check_run_settings.json ([`b92b01f`](https://github.com/agritheory/check_run/commit/b92b01fd7894499c7a0a8f9b9a0ee86dbe1c0481))

* Update check_run.json ([`b95f3d6`](https://github.com/agritheory/check_run/commit/b95f3d6ab9e738c6465b6a4c8f13222b431bb2dc))

* Update company_discretionary_data field

Hide the field until docstatus &gt;0 ([`3d78e85`](https://github.com/agritheory/check_run/commit/3d78e854ed43c387294fff6d69edb6182b76ecb4))

* Update check_run.py

Added company_discretionary_data to check_run.py ([`61ba9f2`](https://github.com/agritheory/check_run/commit/61ba9f2503ca1f2e5cdfe4a13e454bc0baadcb29))

* Update check_run.json

Add &#34;company_discretionary_data&#34; field to check_run.json ([`ecfe547`](https://github.com/agritheory/check_run/commit/ecfe5471413839f0c58b33cf924918171bd4b83d))

* Add field for discretionary company data ([`95e7b8f`](https://github.com/agritheory/check_run/commit/95e7b8f99c163b742846c985a95532e13b2d3143))

* [v13] Error handing in large check runs (#71)

* wip: this should work, it matches a working V14 solution

* wip: trying rollback

* feat: replace primary action with custom processing to allow rollback without submit

* fix: stop popagation on set_route to error log

* style: prettify code

---------

Co-authored-by: agritheory &lt;agritheory@users.noreply.github.com&gt; ([`b6b4eff`](https://github.com/agritheory/check_run/commit/b6b4eff5c1368f9b8a9f9492146e59980d79dca9))

* Timeout fix (#65)

* feat: add enqueue for large check runs

* feat: emit js on enqueued rendered checks

* feat: submit timeout fix and render timeout fix

* style: prettify code

* feat: add js linters

* chore: prettier update

* style: prettify code

* wip: add additional validations, improve settings workflow

* wip: add additional validations, improve settings workflow

* fix: remove check_digit argument in ACH generation

---------

Co-authored-by: agritheory &lt;agritheory@users.noreply.github.com&gt; ([`7fb606e`](https://github.com/agritheory/check_run/commit/7fb606e0a6341bf9de855bd7c3105986f0eb17ea))

* Timeout fix (#63)

* feat: add enqueue for large check runs

* feat: emit js on enqueued rendered checks

* feat: submit timeout fix and render timeout fix

* style: prettify code

* feat: add js linters

* chore: prettier update

* style: prettify code

---------

Co-authored-by: agritheory &lt;agritheory@users.noreply.github.com&gt; ([`0182084`](https://github.com/agritheory/check_run/commit/0182084bb4073600af7feb759ade76ea7524583e))

* Add timeout on large check runs (#51)

* feat: add enqueue for large check runs

* feat: emit js on enqueued rendered checks

* feat: submit timeout fix and render timeout fix

* style: prettify code

---------

Co-authored-by: agritheory &lt;agritheory@users.noreply.github.com&gt; ([`62bbe5a`](https://github.com/agritheory/check_run/commit/62bbe5a7cda20753aa4a82f86b886f3c1cd6fcc1))

* Merge pull request #48 from agritheory/smallfixes

chore: fix typo, remove reference to undeclared variable ([`ed2e79c`](https://github.com/agritheory/check_run/commit/ed2e79c17482112aedaa843925bb8b7cbb91f011))

* Merge pull request #47 from agritheory/fix_invoice_validation

fix: validate if there are any transactions before validating them ([`ffaa57c`](https://github.com/agritheory/check_run/commit/ffaa57ccfb687cb85ad3d5fd45be9aabd0b7b936))

* Merge pull request #43 from agritheory/inv_docstatus

feat: validate docstatus of selected invoices still saved/submitted ([`582847e`](https://github.com/agritheory/check_run/commit/582847e5c1e301a1ab72589c267b0625b5f4d069))

* Merge pull request #38 from agritheory/split_by_address

feat: split checks by address ([`b2e8905`](https://github.com/agritheory/check_run/commit/b2e89051836827637e3500654bf4cc670143f984))

* Merge branch &#39;version-13&#39; of github.com:agritheory/check_run into split_by_address ([`7140698`](https://github.com/agritheory/check_run/commit/7140698aad7205ec82960270eddcf4f47463bc07))

* wip: split address by checks ([`c37a0d0`](https://github.com/agritheory/check_run/commit/c37a0d0361d347d2e7defb67a7eee0c57f076b8e))

* wip: ci test branch name ([`87dbe07`](https://github.com/agritheory/check_run/commit/87dbe07b94dcea8192274ec52a0bd65850b086f1))

* wip: testing check run install ([`5f9e503`](https://github.com/agritheory/check_run/commit/5f9e5037c99f01dd27a2c5f531204eb7d0114fc4))

* wip: testing ci ([`0c3242d`](https://github.com/agritheory/check_run/commit/0c3242dc8e3cc31e2af334e52e7339bb474ddc41))

* CI: testing ([`601c249`](https://github.com/agritheory/check_run/commit/601c249d2c65944ba3e7a3c69b4dadcb8fda2ea0))

* CI: testing ([`b8e36bc`](https://github.com/agritheory/check_run/commit/b8e36bcadb9a15b76e30de1804e098b4c552af91))

* CI: testing ([`70c9f38`](https://github.com/agritheory/check_run/commit/70c9f38a7275dda8a0970e69a57a8f7bf24dc4a0))

* wip: CI fixes ([`12dc456`](https://github.com/agritheory/check_run/commit/12dc456e22f9c5e9d18abc43d7129fcd31725373))

* Merge branch &#39;version-14&#39; into split_by_address ([`5bbac53`](https://github.com/agritheory/check_run/commit/5bbac53c1f36f808350b8445d162eddc24c7c257))


## v14.0.0 (2022-12-30)

### Chore

* chore: conform capitalization ([`b66019f`](https://github.com/agritheory/check_run/commit/b66019f402af8b4ca740565316da452b363806b7))

* chore: conform capitalization ([`b8fe2e7`](https://github.com/agritheory/check_run/commit/b8fe2e7a49bebcf858ce5371bb7bbb7860740aeb))

### Documentation

* docs: update for v14 Payment Ledger and install requirements ([`af2ebf3`](https://github.com/agritheory/check_run/commit/af2ebf3aeef0ba66bd4545cfe906e9fb4fbb6901))

* docs: use tip component in docs ([`94551f7`](https://github.com/agritheory/check_run/commit/94551f7e99d2ace5069ec4aeed04a0cd8e2d797d))

* docs: add docs for example format; disable format ([`6fcf639`](https://github.com/agritheory/check_run/commit/6fcf639a50acd3d5c0f753b381d1e96a46f49562))

* docs: use tip component in docs ([`2349d1d`](https://github.com/agritheory/check_run/commit/2349d1ddafbeea411d1a7c3854e1e391cd952e7e))

### Feature

* feat: split checks by address ([`f091550`](https://github.com/agritheory/check_run/commit/f09155050ea8a64ee7fdb3ba8f3596eb936fd871))

* feat: convert raw sql statements to use query builder ([`a457067`](https://github.com/agritheory/check_run/commit/a457067f5235972d521c2061a925f1856c37a513))

* feat: add example print format ([`0d316c1`](https://github.com/agritheory/check_run/commit/0d316c178612f893e9e8e67a4599baa3a4a8f6ac))

* feat: port to version-14 ([`cb8f9a5`](https://github.com/agritheory/check_run/commit/cb8f9a5b8cb508acc64ab0c9e36d835a9dd18a8d))

### Fix

* fix: company name in correct header field of NACHA file ([`1e50281`](https://github.com/agritheory/check_run/commit/1e502816a1ade9badd5e0b727857847e4e194c55))

* fix: remove check PDF on confirm print ([`c2d0db9`](https://github.com/agritheory/check_run/commit/c2d0db949f51dc6e232785212212fc12ab4189f5))

* fix: company name in correct header field of NACHA file ([`81afb09`](https://github.com/agritheory/check_run/commit/81afb09c3b1d3e34774d67dc7e838ff2b69900ee))

### Test

* test: add login to avoid 403 errors ([`af136fa`](https://github.com/agritheory/check_run/commit/af136fa479a8dfc4b7bdceaf79557a2ebb7e7ba0))

* test: refactor existing Cypress tests and add Check Run Settings tests ([`8e964a0`](https://github.com/agritheory/check_run/commit/8e964a0a3278976a0ddd8592ac9715ea974cebfa))

### Unknown

* tests: start new cypress tests for settings ([`03301a4`](https://github.com/agritheory/check_run/commit/03301a4cbf79fda26b9627801cc535ce1a98e093))


## v13.0.0 (2022-09-01)

### Chore

* chore: use awesomplete z-index number / 1 ([`1b19e30`](https://github.com/agritheory/check_run/commit/1b19e304be1b3ade913f965d3d6cabafccb47a4d))

### Documentation

* docs: add docs for example format; disable format ([`343575e`](https://github.com/agritheory/check_run/commit/343575e7249ff16f58f8e2ab31c3e523828337bf))

* docs: change &#39;todo&#39; to &#39;coming soon&#39; ([`be8af10`](https://github.com/agritheory/check_run/commit/be8af10e82751d513aa10e163d5363bef6c341cb))

* docs: update screen shot ([`42b3e16`](https://github.com/agritheory/check_run/commit/42b3e16b3da18e0df17b3ce46cd565536f9ef212))

* docs: update screen shots and information ([`6aabb43`](https://github.com/agritheory/check_run/commit/6aabb43086e071e55e2b380fe358286bca8f45f6))

* docs: edit permissions information ([`472abfc`](https://github.com/agritheory/check_run/commit/472abfca6a632ad50a2c24d0e66e2fffe7baafe1))

* docs: edit config information ([`eabf6d0`](https://github.com/agritheory/check_run/commit/eabf6d0f74f33ec1ab9198645b85a76d6536defd))

* docs: add settings docs and screen shots ([`c56f917`](https://github.com/agritheory/check_run/commit/c56f917f291ed9941592a4c26d558c9cf3bcf075))

* docs: add print confirmation screen shot ([`0b9ee06`](https://github.com/agritheory/check_run/commit/0b9ee062469f620f99556c0ec062e3ce9063ad06))

* docs: add Positive Pay screen shot ([`eaa596d`](https://github.com/agritheory/check_run/commit/eaa596dd172dd0dc7a672f99a9da507f76581a94))

* docs: add ACH generation infoand screen shot ([`2501cee`](https://github.com/agritheory/check_run/commit/2501cee0c8e19547febf500ccd952791960b2ab1))

* docs: spacing edits ([`ce4ec3a`](https://github.com/agritheory/check_run/commit/ce4ec3a91fa9ce5841d3a86704d7f878c3a704e3))

* docs: minor formatting ([`d1bf1f5`](https://github.com/agritheory/check_run/commit/d1bf1f571874f916421540d0af7b19f106f3e6d4))

* docs: add and re-order config section ([`c0ac8e5`](https://github.com/agritheory/check_run/commit/c0ac8e5da2d000a3170c40f617035493262247c3))

* docs: add docs link ([`a264a21`](https://github.com/agritheory/check_run/commit/a264a21aabe82ea6686710098125790c22079f27))

* docs: update configuration with images ([`a2ca105`](https://github.com/agritheory/check_run/commit/a2ca1056ab7d24b79fc6e3034f9f89c58332b5d8))

* docs: flatten directory structure ([`900fd2f`](https://github.com/agritheory/check_run/commit/900fd2f4af7dfc0822ad7962bcebd43c52281214))

* docs: update config with mop type ([`8e26dc9`](https://github.com/agritheory/check_run/commit/8e26dc9b8b9575d65c4abc529be9c183132d7247))

* docs: add docs for example data and print format ([`9f6761b`](https://github.com/agritheory/check_run/commit/9f6761b4a0dfd3093a33447e3d4e6e5158b9f38d))

* docs: restructure index and update links ([`b423605`](https://github.com/agritheory/check_run/commit/b423605480909fe525aa70271b93c99b62190074))

* docs: update image ([`55e0be1`](https://github.com/agritheory/check_run/commit/55e0be170f3b375dfec8861dbce913bc9a3bf68c))

* docs: add supplier config image and update text ([`06989a6`](https://github.com/agritheory/check_run/commit/06989a623fe5d787299c76d8b7933bc0c517ff96))

* docs: move installation instructions to doc page, link to that in README ([`427f4ae`](https://github.com/agritheory/check_run/commit/427f4ae4d77d4a72275278da74b45c357fe39803))

* docs: add employee configuration image ([`fc4db1c`](https://github.com/agritheory/check_run/commit/fc4db1cae998baf8e65812a6c75024e05cc83e62))

* docs: add placeholder docs, start configuration ([`f3b6210`](https://github.com/agritheory/check_run/commit/f3b6210e43e00741791ef9693597c05fa3a1e6b3))

* docs: add positive pay, links to index ([`ade8adb`](https://github.com/agritheory/check_run/commit/ade8adbf5b1f462ba4a90230b30feddbae34eea3))

* docs: add directory structure, index, and photo assets ([`cf4e5d9`](https://github.com/agritheory/check_run/commit/cf4e5d9e1641b8e747326634716ae088d80a45cb))

* docs: update developer installation instructions ([`6f16336`](https://github.com/agritheory/check_run/commit/6f16336bb8b3ac9bdc98ca2637d4e987515e3538))

* docs: add install instructions to readme ([`e055a03`](https://github.com/agritheory/check_run/commit/e055a03a7a6d305e1fe75660378fb646f8aed091))

### Feature

* feat: add example print format ([`521bff5`](https://github.com/agritheory/check_run/commit/521bff50d3f1e4f5d141ef12f6ed05663d2c070a))

* feat: add more permissions topics ([`3f61a25`](https://github.com/agritheory/check_run/commit/3f61a2522348dfeb08e2f3f12901981b91df1083))

* feat: expand permissions ([`e02c6cd`](https://github.com/agritheory/check_run/commit/e02c6cd4526a962023933e96040478ce9b7a93bb))

* feat: check run settings
 - include invoices, journal entries and expense claims discreetly
 - pre-check overdue items
 - number of invoices per voucher
 - ACH file extension and company description
 - ACH service class code and standard class code
 - allow/ disallow cancellation w/ unlinking
 - cascade cancellation to cancel payment entries ([`26c560d`](https://github.com/agritheory/check_run/commit/26c560db8fffb9dd73d6d403c1015f7eb8da2328))

* feat: ach integration ([`b3864c7`](https://github.com/agritheory/check_run/commit/b3864c76e710e0499b72eb619c4ec6987a8618df))

* feat: add mop alert ([`ba6029a`](https://github.com/agritheory/check_run/commit/ba6029a6ccf843acd70393a505fc1ff885cba206))

* feat: use variables to respect dark mode ([`b0bb4ae`](https://github.com/agritheory/check_run/commit/b0bb4ae7ddceda28ff51a7b72a21290c3e7f2d88))

* feat: key nav ([`ae5bb24`](https://github.com/agritheory/check_run/commit/ae5bb245c807ea6fd812cc60f9e13ab1bd4726da))

* feat: update SQL to use filter.bank_account in query ([`fa3580b`](https://github.com/agritheory/check_run/commit/fa3580b1ea7c2ba742047e9aa81a11b22e65fae3))

* feat: add positive pay report ([`128b5d6`](https://github.com/agritheory/check_run/commit/128b5d6fda4013a58930b7f426c9e676552dfb8e))

* feat: add files for employee and suppleir bank account obfuscation ([`f7ada06`](https://github.com/agritheory/check_run/commit/f7ada0650d035cadbe1d059c92c51947c5b119f5))

* feat: allow normal cusomtization workflow with multiple installed apps ([`1001b75`](https://github.com/agritheory/check_run/commit/1001b75a24564ba139bc3d6ab2a9873b419bb320))

* feat: Initialize App ([`cf39bb7`](https://github.com/agritheory/check_run/commit/cf39bb7679becd8a39c9ad20ea1aa7603a93ca52))

### Fix

* fix: remove check PDF on confirm print ([`4b96835`](https://github.com/agritheory/check_run/commit/4b96835d8415bd0e9b2a9bf07a90a2e450559573))

* fix: don&#39;t trigger settings change for check run creation ([`a672f46`](https://github.com/agritheory/check_run/commit/a672f467a1b3ceda3eb725e4bf605ecbc82933aa))

* fix: conform demo mode of payment types to docs recommendations ([`44cb68c`](https://github.com/agritheory/check_run/commit/44cb68c3f5ce79f863ea79b988c3fca3a639481d))

* fix: change employee party field so payment entry can properly link to it ([`5f96753`](https://github.com/agritheory/check_run/commit/5f96753e1a27304565c59c39c150112b65aba50d))

* fix: set fields in test script expense claim generation ([`3152aac`](https://github.com/agritheory/check_run/commit/3152aac10b283aa92fdbd3f8e44a010b1d15b09c))

* fix: update installation guide link ([`bbc0a0e`](https://github.com/agritheory/check_run/commit/bbc0a0e47a64227ede7207803beac5e428ee45fe))

* fix: field name and type issues when creating NACHA file ([`7ded221`](https://github.com/agritheory/check_run/commit/7ded221b633e6330520508d497f4ce6c49cede78))

* fix: reorder Supplier json to show bank account field in form (#12) ([`5d05e38`](https://github.com/agritheory/check_run/commit/5d05e38f4004f5f36735e43b1a229a46b4762c48))

* fix: add bank account to payment entry form ([`3316d61`](https://github.com/agritheory/check_run/commit/3316d61fcce6b5de35cc029c52a9a1e57a507102))

* fix: line height and checkbox alignment ([`232fff6`](https://github.com/agritheory/check_run/commit/232fff641db11dc821051154788ffbd35e4760e5))

* fix: checkrun rerender on document change ([`eabf8a5`](https://github.com/agritheory/check_run/commit/eabf8a55e9d2bd01fffdfbc6a24e41f8391a3981))

* fix: include built JS ([`12492b8`](https://github.com/agritheory/check_run/commit/12492b8573985470f5339ef37f71fd8c951da9e2))

### Unknown

* wip: add print format to crs, don&#39;t override payable account if provided ([`6dca9fa`](https://github.com/agritheory/check_run/commit/6dca9fafb68119a8d11e373c170c9504d5e465ca))

* wip: add some asides and warnings, permissions section ([`d5a13a3`](https://github.com/agritheory/check_run/commit/d5a13a39343d63d2615845eb57386e9c62a31b41))

* feat/wip: check run settings
- include invoices, journal entries and expense claims discreetly
- pre-check overdue items
- number of invoices per voucher
- ACH file extension and company description
- ACH service class code and standard class code

Not implemented yet:
 - allow/ disallow cancellation w/ unlinking
 - cascade cancellation to cancel payment entries ([`73ae78f`](https://github.com/agritheory/check_run/commit/73ae78fde383bf8242926b27d030b8e59afb310b))

* feat/wip: check run settings

- include invoices, journal entries and expense claims discreetly
- pre-check overdue items
- number of invoices per voucher
- ACH file extension and company description

Not implemented yet:
 - allow/ disallow cancellation w/ unlinking
 - cascade cancellation t ocancel payment entries
 - ACH service class code and standard class code ([`2e03e13`](https://github.com/agritheory/check_run/commit/2e03e13d1e5a64fc7a699a8e9eca174eb28e0532))

* CI (#8)

* wip: json and py validate, semantic, and frappe json diff

* test: stub UI test yaml - copied from Frappe

* test: add helper shell files, remove job contitionals

* test: remove producer/consumer test dbs from install script

* test: correct install file / install dependency file

* test: echo helper folder to debug path error

* test: move helper folder out of workflows

* test: remove echo

* test: install erpnext

* test: create site in sintall script

* test: skip assets on erpnext install

* test: remove frappe-path argument from bench init

* wip: update JSON ci

* test: remove python setup, already in ubuntu

* test: frappe-bench needs 3.10

* test: python3.9

* test: no mariadb password

* test: blank password

* test: mysql password 123

* test: using frappe/erpnext workflow

* test: allow empty password = yes

* test: file wasnt saved

* test: mariadb version 10.5 =&gt; 10.3

* test: various

* test: reinsert pip install

* test: fix typo

* test: remove space (typo)

* test: fix syntax

* test: remove site setup

* test: restore site without building frappe

* test: remove db setup, only ui test

* test: remove strawberry output for site setup

* test: use check run test

* test: cypress test data path

* test: install apps on site

* test: cypress path

* test: bench restart after install, set developer mode

* test: CI=Yes bench command

* test: install apps

* test: add site adn skip assets

* test: ci=yes install-app

* test: wildcard frappe user, remove ci bench install-app

* test: update localhost wildcard both commands

* text: bench execute command

* test: revert mariadb wildcard and install-app

* test: remove bench restart

* test: remove CI=yes execute

* wip: cypress testing fixup

* wip: ach workflows

* wip: ach generation

* wip: check run ui tests V1

* test: fix cypress command path

* test: cypress command

* test: cypress response timeout

* test: remove headless

* test: cypress action

* test: rerun

* test: &#34;8000&#34; + &#34;/&#34;

* test: use cypress config

* test: add bench restart

* test: update baseUrl to match site_config.json

* test: no recordings

* test: video, screenshots off

* wip: remove unused env vars, set script clone depth, remove commented yarn run, fix spec.js typo

Co-authored-by: Robert Duncan &lt;robirtduncan@gmail.com&gt; ([`350bb6e`](https://github.com/agritheory/check_run/commit/350bb6e5648ed63c7086a9bd89f5acb194a5c85f))

* Merge pull request #10 from agritheory/fixbankacct

fix: add bank account to payment entry form ([`da6c487`](https://github.com/agritheory/check_run/commit/da6c487a2917e6e778a8cde010fcdd34f83393a5))

* Merge pull request #9 from agritheory/ach_workflows

ACH workflows ([`a739cb0`](https://github.com/agritheory/check_run/commit/a739cb0eee246703c7af61d1b9e9d1fe92df6625))

* wip: ach generation ([`fde92d7`](https://github.com/agritheory/check_run/commit/fde92d71fbfbb54c02ead2acf4a5670b94183fb7))

* wip: ach workflows ([`00081ee`](https://github.com/agritheory/check_run/commit/00081ee21eeed2846558899a48938b76f4a00fb5))

* Merge pull request #7 from agritheory/table-fixes

fixes: consistent row height, payment entry link ([`4911093`](https://github.com/agritheory/check_run/commit/4911093b152c595a43c160b527ec63e28200eb66))

* fixes: consistent row height, payment entry link ([`3c1eaf3`](https://github.com/agritheory/check_run/commit/3c1eaf3806817a4ae7674b1df89d37ed80b8e6ee))

* Merge pull request #6 from agritheory/test_setup

Test setup ([`62363ce`](https://github.com/agritheory/check_run/commit/62363cedbd9fcd4228f8adae416ff1521e8a018e))

* wip: testing and setup ([`219ea34`](https://github.com/agritheory/check_run/commit/219ea34b926162829971b1b6dd23587a95e8f45a))

* wip: quick entry improvements, general refactoring ([`eaf4cfe`](https://github.com/agritheory/check_run/commit/eaf4cfedbab535f1417eab13d46aea319f1077d4))

* Merge pull request #4 from agritheory/key-nav

changes: spacebar checks/unchecks pay, keys a-z open MOP / starts search ([`121932a`](https://github.com/agritheory/check_run/commit/121932a6d5fb4a9aca5bd1b534d99548e239dfb2))

* Merge branch &#39;test_and_cleanup&#39; into key-nav ([`a478f7f`](https://github.com/agritheory/check_run/commit/a478f7fe61e01b3386bf866a78742d81458c1c0a))

* Merge branch &#39;key-nav&#39; of github.com:agritheory/check_run into key-nav ([`33bc96b`](https://github.com/agritheory/check_run/commit/33bc96bee34f91eddd83b530ae638f8a0e3dcde2))

* changes: spacebar checks/unchecks pay, keys a-z open MOP / starts search ([`0873c5d`](https://github.com/agritheory/check_run/commit/0873c5d395c07891a5bffd83734918adeaa44bb1))

* Merge branch &#39;version-13&#39; of github.com:agritheory/check_run into test_and_cleanup ([`6fba403`](https://github.com/agritheory/check_run/commit/6fba403ca20fbd56f022e0af8856e09681b19ef2))

* Merge pull request #3 from agritheory/key-nav

Key nav ([`0823fc5`](https://github.com/agritheory/check_run/commit/0823fc56926e40b30060b97d661c622f06c5466e))

* refactor ADropdown isOpen binding ([`46598c1`](https://github.com/agritheory/check_run/commit/46598c1194da0cc047f969eb2f5ee62058c8af9b))

* update checkrun total field ([`65e10b8`](https://github.com/agritheory/check_run/commit/65e10b829267784192e815e8d2bc03830b87dcd0))

* wip: test stubbed and some reactivity improvements ([`d5364dc`](https://github.com/agritheory/check_run/commit/d5364dc17cac516a162f654f1637b2393b731ce1))

* Merge pull request #2 from agritheory/version-13-hotfix

Check run render fixes ([`8d740bd`](https://github.com/agritheory/check_run/commit/8d740bdda360bb4d2488810e3845df53e66fb700))

* cleanup: removed default span in check_run_table, removed is_dirty function ([`bc05bde`](https://github.com/agritheory/check_run/commit/bc05bde2fdbe8feb852a8f851bf64ed2897d9d7d))

* Merge pull request #1 from agritheory/positivepay

feat: add positive pay report ([`df8692b`](https://github.com/agritheory/check_run/commit/df8692b91c45b8d47b2eebbd8519bee1d05314f4))

* fixes: check run table save and render on save ([`0e1c27a`](https://github.com/agritheory/check_run/commit/0e1c27a362c6107d877a270bbe9f0a4e56ca82a8))

* wip: table not rendering on save ([`08d48c7`](https://github.com/agritheory/check_run/commit/08d48c7836a34027fd3027c6c26dc369067be644))

* wip: test fixtures and stubbed setup ([`1f8e415`](https://github.com/agritheory/check_run/commit/1f8e415868a80cee3c38260b756d0e845c4f0c30))

* wip: refactor for changing accounts, add JE ([`ef42f68`](https://github.com/agritheory/check_run/commit/ef42f6876d8a5e7a9dbe16e1191f8c3102afd677))

* cust: add customization files ([`679d3df`](https://github.com/agritheory/check_run/commit/679d3dfdace31283d779e8704dcef0dea744ea9d))
