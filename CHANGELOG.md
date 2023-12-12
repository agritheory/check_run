# CHANGELOG



## v14.9.0 (2023-12-12)

### Documentation

* docs: update settings section ([`b9b15f8`](https://github.com/agritheory/check_run/commit/b9b15f8ac16494d53399ccd7ab3f823fd1545620))

### Feature

* feat: add fallbacks for mode of payment per source document type ([`12f9160`](https://github.com/agritheory/check_run/commit/12f916000dbb96db2a1ea3474b55d226a7a1cb5a))

### Fix

* fix: empty string values to NULL in queries ([`75ab1c9`](https://github.com/agritheory/check_run/commit/75ab1c96629b0e2220dd30555a1498ddd2561291))

### Unknown

* Merge pull request #180 from agritheory/default_mode_of_payment_settings

feat: add fallbacks for mode of payment per source document type ([`c609603`](https://github.com/agritheory/check_run/commit/c6096038c1363e14a2ba7abb29f2cf73d25ce860))


## v14.8.4 (2023-12-11)

### Fix

* fix: only fetch check number on &#34;pay&#34; payment types (#179) ([`1b6dd48`](https://github.com/agritheory/check_run/commit/1b6dd488a6cf921c4497737f47d27627f19e510f))


## v14.8.3 (2023-12-11)

### Fix

* fix: mode of payment summary (#176)

* fix: mode of payment summary

* wip: refactor reactivity for performance

* feat: improved reactivity

* style: prettify code

* fix: move built files to dist folder / ignored by git

---------

Co-authored-by: Tyler Matteson &lt;tyler@agritheory.com&gt;
Co-authored-by: agritheory &lt;agritheory@users.noreply.github.com&gt; ([`40fd4ee`](https://github.com/agritheory/check_run/commit/40fd4ee3057f9808944258b9d7807522827f17a6))

### Unknown

* Draft: Paid Invoices appearing in the Check Run (#171)

* wip: add correct setup data to remove payment terms bug

* fix: paid invoices showing in check run

* fix: add payment schedule validation in payment entry

* docs: add purchase invoice payment term considerations

---------

Co-authored-by: Heather Kusmierz &lt;heather.kusmierz@gmail.com&gt; ([`bbb66d6`](https://github.com/agritheory/check_run/commit/bbb66d6b79fd2719b8ba6d691f73302a58362e4d))

* Quick Check (#172)

* feat: quick check poc

* fix: add additional filters in check run settings and also in check run quick entry

* docs: quick check and payment entry customization docs ([`37a39a1`](https://github.com/agritheory/check_run/commit/37a39a17f490e6e3d173707e36cd4467116f4e3b))

* Per supplier invoices per voucher (#165)

* feat: allow per-supplier override for number of invoices per voucher

* docs: add docs for per supplier invoices per voucher ([`567762c`](https://github.com/agritheory/check_run/commit/567762c67c9cbbc89e57f345beca61a64e28961a))


## v14.8.2 (2023-09-22)

### Fix

* fix: required_apps (#162)

* fix: required_apps

* fix: required_apps ([`31b5297`](https://github.com/agritheory/check_run/commit/31b52975839424f9a9bfbded6cc03c241dcb44cd))


## v14.8.1 (2023-09-14)

### Ci

* ci: update release action user and email (#155) ([`a3cfc97`](https://github.com/agritheory/check_run/commit/a3cfc975aac95696b943ecbd809a00cab6159ffd))

### Fix

* fix: customizations leaks, module specificity (#161) ([`ce6b9fc`](https://github.com/agritheory/check_run/commit/ce6b9fc2a79e9a1beea4f514b3c52d4fd442da50))

### Unknown

* Port preview to V14 (#153)

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
Co-authored-by: fproldan &lt;fproldan@users.noreply.github.com&gt;

* feat: use query builder in payables attachments report&#39;

* fix: build

* fix: add remove btn

* style: prettify code

---------

Co-authored-by: Tyler Matteson &lt;tyler@agritheory.com&gt;
Co-authored-by: fproldan &lt;fproldan@users.noreply.github.com&gt; ([`78d2666`](https://github.com/agritheory/check_run/commit/78d2666c2c9b92831b90ee1c647737ef79375a44))


## v14.8.0 (2023-09-08)

### Feature

* feat: add read_only decorator ([`c7bb83c`](https://github.com/agritheory/check_run/commit/c7bb83ceba8fcfd291b6198ff1ee8b92edf1abca))

### Unknown

* Merge pull request #150 from agritheory/read_only

feat: add read_only decorator ([`73d459d`](https://github.com/agritheory/check_run/commit/73d459d616b5190ba85ebe67c115f29cae2d11ba))

* Merge branch &#39;version-14&#39; into read_only ([`aaca764`](https://github.com/agritheory/check_run/commit/aaca76471cb95480aef1a62459ae296767dafcd2))

* Setup mypy (#149)

* chore: add typing

* ci: add mypy to pre-commit and CI

---------

Co-authored-by: Heather Kusmierz &lt;heather.kusmierz@gmail.com&gt; ([`5831fb8`](https://github.com/agritheory/check_run/commit/5831fb85f3b08e76f486c3b01fb671b3dba06225))


## v14.7.0 (2023-09-07)

### Ci

* ci: migrate to python semantic release (#133)

* ci: migrate to python semantic release

* ci: add version variable file

* ci: update remote name ([`d37bca6`](https://github.com/agritheory/check_run/commit/d37bca61505e99476e6fb857fbd36dacc932918a))

### Feature

* feat: disallow cancellation of source documents selected for payment in draft CRs (#126) (#143) ([`bddc888`](https://github.com/agritheory/check_run/commit/bddc8884167c9e3381f519914a278a29fdf345f1))

### Fix

* fix: skip check on draft check runs with no transactions (v14) (#148)

Resolution for `TypeError: the JSON object must be str, bytes or bytearray, not NoneType` when draft check run has no transactions. ([`dadd084`](https://github.com/agritheory/check_run/commit/dadd084c26f50de4e9dff1f360a8d73bbb37e250))

* fix: move bank validation out of override class into hook (#142) ([`f07ad5a`](https://github.com/agritheory/check_run/commit/f07ad5a1c4a9b7e424ad534ec40731f26f6feb0c))

* fix: only increment if check numer is numeric (#139) ([`079aa52`](https://github.com/agritheory/check_run/commit/079aa52bf013e13d3350848ef011b74b99b64bf1))

### Unknown

* Show the quantity and amount of each Mode of Payment (#141)

* feat: mode of payment summary component

* feat: add number_of_invoices_per_voucher to check

* feat: currency format

* chore: fix setup, run formatters against repo

* fix: html formatting

* feat: reactive

* feat: only update when draft

* feat: improvement

* feat: sort mop

* fix: slight refactor, &#39;account&#39; =&gt; &#39;Account&#39;

---------

Co-authored-by: Tyler Matteson &lt;tyler@agritheory.com&gt; ([`a0471a3`](https://github.com/agritheory/check_run/commit/a0471a3304c9610e8be3794599561c7872209e07))

* Use payment schedule as basis for due date and amount in purchase invoice query (#144)

* feat: use payment schedule as basis for due date and amount in purchase invoices

* docs: update setup script path

* fix: typo, add missing query column

---------

Co-authored-by: Heather Kusmierz &lt;heather.kusmierz@gmail.com&gt; ([`4ccba65`](https://github.com/agritheory/check_run/commit/4ccba65818350bf256fa6d25d730ba2abfe36788))

* Query Builder fixes (#145)

* fix: refactor frappe.db.sql to query builder for outstanding

* fix: refactor postive pay to query builder

* chore: remove print statement

* fix: update comparison operator

---------

Co-authored-by: Heather Kusmierz &lt;heather.kusmierz@gmail.com&gt; ([`e00e476`](https://github.com/agritheory/check_run/commit/e00e4768b4634716b417c6798123b44399ef7d2d))

* Update originating dfi id (#135)

According to the NACHA Dev Guide, Originating DFI Identification is supposed to be &#34;The routing number of the DFI originating the entries within the batch.&#34;

Co-authored-by: Trusted Computer &lt;75872475+trustedcomputer@users.noreply.github.com&gt; ([`f16bb24`](https://github.com/agritheory/check_run/commit/f16bb2468231a8221e302109060dee79aa476838))


## v14.6.0 (2023-07-28)

### Chore

* chore: fix account names (#99) ([`7946bdf`](https://github.com/agritheory/check_run/commit/7946bdfb4bb4f7ba96a4939ff36f449bc108fa10))

### Ci

* ci: fix release correctly on V14 also ([`3ff2d65`](https://github.com/agritheory/check_run/commit/3ff2d65dece13db5e8e40b96fbe0ecd8aed4f0be))

* ci: remove registry from package.json ([`607db96`](https://github.com/agritheory/check_run/commit/607db9619e75740c419e01c622ee51374e53aecf))

* ci: fix release CI ([`9c954d5`](https://github.com/agritheory/check_run/commit/9c954d5e6259a3c257036ea066e07e08afb93181))

* ci: update installation and workflows ([`23c4f83`](https://github.com/agritheory/check_run/commit/23c4f838e51882b6f7db6ded58735b18e4f9a0c5))

### Documentation

* docs: add translations page ([`6e9c977`](https://github.com/agritheory/check_run/commit/6e9c9778b25aaa8d2bd8dc77ae87c341fbb1bc23))

### Feature

* feat: add validate when processing, enable on_update_after_submit hook (#115) ([`d58a106`](https://github.com/agritheory/check_run/commit/d58a106bd295c4811ff0722ca0ade7d29a711c34))

* feat: check payment entries for cancelled or paid invoices before submitting (#108) ([`adbca4d`](https://github.com/agritheory/check_run/commit/adbca4df65c3599a213ddebacd9a269d8a2462a1))

* feat: custom immediate origin value in settings (#76)

* feat: custom immediate origin value in settings

* style: prettify code

---------

Co-authored-by: agritheory &lt;agritheory@users.noreply.github.com&gt; ([`813be9e`](https://github.com/agritheory/check_run/commit/813be9e299c2ba42f1bc0de11fabd03d1ab2f0fb))

* feat: port timeout fix to v14 (#62)

* feat: port timeout fix to v14

* fix: indent

* chore: prettier formatting

* style: prettify code

---------

Co-authored-by: agritheory &lt;agritheory@users.noreply.github.com&gt; ([`6f50230`](https://github.com/agritheory/check_run/commit/6f50230a8713c16f1818ba8450abc18cc2535322))

* feat: fix lookup for non-existient bank account info, improve UX ([`4ef8a91`](https://github.com/agritheory/check_run/commit/4ef8a91ed769798d9569edc770ac4bd81a709b14))

* feat: add logic for handling on-hold invoices, setting for automatic release and docs ([`da93c1d`](https://github.com/agritheory/check_run/commit/da93c1d04a58b18d9c098f3661bd731c6761d783))

* feat: update translations to capture button text ([`ccc4b67`](https://github.com/agritheory/check_run/commit/ccc4b6779c869a9786e7f67ded1c09333383439a))

* feat: add Canadian DFI Routing Number validation for bank ([`b4d9df9`](https://github.com/agritheory/check_run/commit/b4d9df97bc1705bd5c622d46bb88e4d7795f8b3d))

* feat: add Canadian/GB English translations ([`1e86c00`](https://github.com/agritheory/check_run/commit/1e86c00beb396499e7ece0eccb0902ab4e3188b0))

* feat: split checks by address ([`b32f0c9`](https://github.com/agritheory/check_run/commit/b32f0c991ba91a8377e87673977a4b651a4f6970))

* feat: validate docstatus of selected invoices still saved/submitted (#44)

* feat: validate docstatus of selected invoices still saved/submitted

* refactor: moved validation code for cancelled transactions to function ([`78b3e25`](https://github.com/agritheory/check_run/commit/78b3e2580e200ce60211ed44d20651f68546eeae))

### Fix

* fix: show purchase returns in check run (#131) ([`b1cd85b`](https://github.com/agritheory/check_run/commit/b1cd85b42284a3ea38aa1c703d1f2ae714ab7f6a))

* fix: broken translation string in csv (#122) ([`9c2ded2`](https://github.com/agritheory/check_run/commit/9c2ded22846e0753a0ed4a7732781fb205a47df4))

* fix: remove check_digit argument in ACH generation (#66) ([`8476235`](https://github.com/agritheory/check_run/commit/8476235f380cfcea81309bd703667f6ff047663d))

* fix: add on hold fixes to query builder ([`a1e3114`](https://github.com/agritheory/check_run/commit/a1e3114e78b3894af61b40d46276c6dd6c0d92d3))

* fix: remove undeclared variable reference ([`6a36c84`](https://github.com/agritheory/check_run/commit/6a36c84c6b3f8b8497ca7bae9e8db24e1e939228))

* fix: MOP ignore keypress if input is focused ([`e073c09`](https://github.com/agritheory/check_run/commit/e073c09a5ed26e61b34a44419f85a939781b1409))

### Test

* test: fix net 14 days ([`3acea48`](https://github.com/agritheory/check_run/commit/3acea48f68560ca417b1d05cd9153635e9cc6c2e))

* test: add payment terms to test data ([`8b4073e`](https://github.com/agritheory/check_run/commit/8b4073eaf7b0016fe7a4e1bd0c014af818d5477c))

* test: add on hold invoice to test data ([`6867d42`](https://github.com/agritheory/check_run/commit/6867d428c77fb096125d17e1e0382a92aabceaa0))

### Unknown

* trans: add error message to translations (#129) ([`1d9f840`](https://github.com/agritheory/check_run/commit/1d9f840aee62ca27203955f204750c2eb47fb4ab))

* V14 pre process validation (#113)

* feat: check payment entries for cancelled or paid invoices before submitting

* fix: add expense calim to pre-process validation ([`232beb7`](https://github.com/agritheory/check_run/commit/232beb78f9855ceaa3b248d246b43dc19477532f))

* V14 ports (#98)

* chore: port payement entry check number fetch/save to V14

* chore: port ach_post procesing hook and company disc data

* chore: port docstatus fix for ach-only crs

* chore: port Update effective entry date

* chore: port large process check run fixes

* chore: debug V14 large process check run fixes

* The hook jenv is deprecated New variable is jinja

* chore: port ach_post procesing hook and company disc data

* fix: fix savepoint wierdness

* fix: company discretionary data fix

---------

Co-authored-by: Mohammad Ali &lt;swe.mirza.ali@gmail.com&gt; ([`b7adf96`](https://github.com/agritheory/check_run/commit/b7adf962e0008a1d02663c84b64fba6fa6b93d03))

* Merge pull request #90 from alibaig4u/version-14

The hook jenv is deprecated New variable is jinja ([`5afcfd1`](https://github.com/agritheory/check_run/commit/5afcfd1cd78e5032698e3227ca1e70ed8a22dd4f))

* The hook jenv is deprecated New variable is jinja ([`6ef71b7`](https://github.com/agritheory/check_run/commit/6ef71b7ae8910e59992ee5051644d1dab9fa35ac))

* Merge pull request #87 from agritheory/v14_ci

V14 ci ([`bf296ec`](https://github.com/agritheory/check_run/commit/bf296ec7757bee477b080e6d4d496a1edeff2f57))

* Merge pull request #85 from agritheory/v14_fix_release

ci: fix release CI ([`997c42c`](https://github.com/agritheory/check_run/commit/997c42c110f2ec82afb3cece3c38e22ec5a6eae1))

* [v14] handle errors in background queue (#72)

* feat: handle errors in background queue

* style: prettify code

* feat: use process_checks instead of submit triggers to manage submission and errors

* style: prettify code

---------

Co-authored-by: agritheory &lt;agritheory@users.noreply.github.com&gt; ([`1b9b592`](https://github.com/agritheory/check_run/commit/1b9b592deb75ed3156f5588a888e7f370158d124))

* V14 party lookup (#68)

* fix: remove check_digit argument in ACH generation

* feat: look up party on PE submission to avoid renaming problems ([`7f940f3`](https://github.com/agritheory/check_run/commit/7f940f3954d8a7d75538e2c9a1fdf8da905acb96))

* V14 timeout fix (#64)

* feat: port timeout fix to v14

* fix: indent

* chore: prettier formatting

* feat: timeout fixes + prettier for v14

* style: prettify code

---------

Co-authored-by: agritheory &lt;agritheory@users.noreply.github.com&gt; ([`825bf70`](https://github.com/agritheory/check_run/commit/825bf70ae1567a3208872baf0e582972524d536c))

* Bank account lookup fix (#61)

* feat: fix lookup for non-existient bank account info, improve UX

* fix: don&#39;t raise exception on bank account lookup ([`c4357a8`](https://github.com/agritheory/check_run/commit/c4357a80305b4b5d2137b132553eb38b4bb6e2a7))


## v14.0.0 (2022-12-30)

### Chore

* chore: conform capitalization ([`b66019f`](https://github.com/agritheory/check_run/commit/b66019f402af8b4ca740565316da452b363806b7))

* chore: use awesomplete z-index number / 1 ([`1b19e30`](https://github.com/agritheory/check_run/commit/1b19e304be1b3ade913f965d3d6cabafccb47a4d))

### Documentation

* docs: update for v14 Payment Ledger and install requirements ([`af2ebf3`](https://github.com/agritheory/check_run/commit/af2ebf3aeef0ba66bd4545cfe906e9fb4fbb6901))

* docs: use tip component in docs ([`94551f7`](https://github.com/agritheory/check_run/commit/94551f7e99d2ace5069ec4aeed04a0cd8e2d797d))

* docs: add docs for example format; disable format ([`6fcf639`](https://github.com/agritheory/check_run/commit/6fcf639a50acd3d5c0f753b381d1e96a46f49562))

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

* feat: convert raw sql statements to use query builder ([`a457067`](https://github.com/agritheory/check_run/commit/a457067f5235972d521c2061a925f1856c37a513))

* feat: add example print format ([`0d316c1`](https://github.com/agritheory/check_run/commit/0d316c178612f893e9e8e67a4599baa3a4a8f6ac))

* feat: port to version-14 ([`cb8f9a5`](https://github.com/agritheory/check_run/commit/cb8f9a5b8cb508acc64ab0c9e36d835a9dd18a8d))

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

* fix: company name in correct header field of NACHA file ([`1e50281`](https://github.com/agritheory/check_run/commit/1e502816a1ade9badd5e0b727857847e4e194c55))

* fix: remove check PDF on confirm print ([`c2d0db9`](https://github.com/agritheory/check_run/commit/c2d0db949f51dc6e232785212212fc12ab4189f5))

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
