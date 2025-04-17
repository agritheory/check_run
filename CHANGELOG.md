# CHANGELOG


## v15.3.1 (2025-04-15)

### Bug Fixes

- Remove unnecessary self typing ([#296](https://github.com/agritheory/check_run/pull/296),
  [`c5ca969`](https://github.com/agritheory/check_run/commit/c5ca96919a6131b9e86631f49abc6d2b1ffc61ff))

Co-authored-by: Rohan Bansal <rohan@agritheory.dev>

Co-authored-by: Tyler Matteson <support@agritheory.dev>


## v15.3.0 (2025-04-15)

### Features

- Make Posting Date read only if Set Payment Entry Posting Date == Use Todays Date" (#303)
  ([#309](https://github.com/agritheory/check_run/pull/309),
  [`88c0863`](https://github.com/agritheory/check_run/commit/88c0863ceaa5f43924bb4d17b0e8e960c98e988a))

(cherry picked from commit 61a43b32978927982369fa88afc85abc249ac910)

Co-authored-by: Francisco Roldán <franciscoproldan@gmail.com>


## v15.2.1 (2025-04-01)

### Bug Fixes

- Respect settings date config (#298) ([#299](https://github.com/agritheory/check_run/pull/299),
  [`fcb2ab5`](https://github.com/agritheory/check_run/commit/fcb2ab574fa35e4a3fa507186f17112d258e9404))

(cherry picked from commit 8edbbffd1a8787102a30bce37ae9917c62c5f5d7)

Co-authored-by: Tyler Matteson <support@agritheory.dev>


## v15.2.0 (2025-01-28)

### Continuous Integration

- Backport config (#271) ([#272](https://github.com/agritheory/check_run/pull/272),
  [`db40e9f`](https://github.com/agritheory/check_run/commit/db40e9f69444da2857be322a82851210c7a23e1f))

Co-authored-by: Tyler Matteson <support@agritheory.dev> (cherry picked from commit
  438efdea82cc67cbeeb5df59c237e0450721d263)

Co-authored-by: Myuddin Khatri <53251406+MyuddinKhatri@users.noreply.github.com>

- Change backport config (#273) ([#275](https://github.com/agritheory/check_run/pull/275),
  [`48eebf7`](https://github.com/agritheory/check_run/commit/48eebf7efd5071ced8b9299862afe28652b4288d))

(cherry picked from commit 76fc626c6fa697cfd914ddef26e2c6b4ed3ba8c8)

Co-authored-by: Myuddin Khatri <53251406+MyuddinKhatri@users.noreply.github.com>

### Features

- Add MICR Encoding Print Format and docs ([#282](https://github.com/agritheory/check_run/pull/282),
  [`2b9f51a`](https://github.com/agritheory/check_run/commit/2b9f51a6145ee3c474c5949b75a12a346b15f359))

* feat: add print format applying MICR Encoding font

* test: add company address to test data

* docs: add MICR Encoding print format


## v15.1.2 (2024-07-18)

### Bug Fixes

- Serialize null transactions(v15) ([#262](https://github.com/agritheory/check_run/pull/262),
  [`5e13ec7`](https://github.com/agritheory/check_run/commit/5e13ec7514b78ce6d2596ed5c640e4f2c1d9bada))

* fix: serialize null transactions(v15)

* fix: remove ci jobs dependency


## v15.1.1 (2024-05-29)

### Bug Fixes

- Bankaccount => bank typing ([#247](https://github.com/agritheory/check_run/pull/247),
  [`da77cc3`](https://github.com/agritheory/check_run/commit/da77cc329e28d95f84783d98dbd204addb39d0e8))

### Continuous Integration

- Add conftest file updated for json ([#228](https://github.com/agritheory/check_run/pull/228),
  [`dc306c3`](https://github.com/agritheory/check_run/commit/dc306c3364ac9ecb2d02003137284a138340ef42))

- Remove cypress, fix hrms install, conform
  ([#221](https://github.com/agritheory/check_run/pull/221),
  [`f6b629b`](https://github.com/agritheory/check_run/commit/f6b629b7876a14795f39dc6d853ea5b7f8722098))

* ci: remove cypress, fix hrms install, conform

* ci: fix mypy error

### Testing

- Add tests, remove cypress ([#238](https://github.com/agritheory/check_run/pull/238),
  [`c20ed6e`](https://github.com/agritheory/check_run/commit/c20ed6e23fc744f0718dd85665f407c134bb7a56))


## v15.1.0 (2024-03-18)

### Features

- Add v15 to release config
  ([`41e329d`](https://github.com/agritheory/check_run/commit/41e329d5f58b8d2c1550a334495fe2c57ff0bc5b))

- Release version-15
  ([`6cd1a27`](https://github.com/agritheory/check_run/commit/6cd1a2788dc6597b3236d867b2dfd3f047dd4d6f))

- Update init version
  ([`f53307b`](https://github.com/agritheory/check_run/commit/f53307bbdd631b1e2dd869cb2c3a7892d9acc870))

- Version-15
  ([`0f2cd0a`](https://github.com/agritheory/check_run/commit/0f2cd0ada07d1cb3e13ebe5325a0b9d6ab2e3876))


## v15.0.0 (2024-03-05)

### Continuous Integration

- Add frappe black to CI ([#214](https://github.com/agritheory/check_run/pull/214),
  [`771e57c`](https://github.com/agritheory/check_run/commit/771e57c166f6516c4a518d5960ff1371b254b038))

* ci: add frappe black to CI

* chore: black, flake8


## v14.11.5 (2024-02-06)

### Bug Fixes

- Disallow mop selection on submitted doc, fix indicator
  ([#207](https://github.com/agritheory/check_run/pull/207),
  [`0429e48`](https://github.com/agritheory/check_run/commit/0429e484c38227ac0f4136f94d128d5ef26580f9))

- Onchanges of mode_of_payment make enable to save form
  ([#206](https://github.com/agritheory/check_run/pull/206),
  [`0b4bff0`](https://github.com/agritheory/check_run/commit/0b4bff0d5de5e76d6e0127e53081775a8056554b))

Co-authored-by: viralpatel15 <viralkansodiya167@gmail.com>


## v14.11.4 (2024-01-22)

### Bug Fixes

- Always include payment term for purchase invoice
  ([#197](https://github.com/agritheory/check_run/pull/197),
  [`1156621`](https://github.com/agritheory/check_run/commit/1156621b4b80f0e7a5cc3f7c10076910305ad29b))

* ci: update app name in path string check

* fix: add PI payment term in Pmt Entry outside a Check Run

* tests: add manual payment entry to test payment term

* docs: update for Payment Entry payment term customizations


## v14.11.3 (2024-01-18)

### Bug Fixes

- Add docstatus check first before fetching supplier MOP
  ([#195](https://github.com/agritheory/check_run/pull/195),
  [`9691364`](https://github.com/agritheory/check_run/commit/9691364f52248e4dfd2c79eaa89bdaba41c5d148))


## v14.11.2 (2024-01-18)

### Bug Fixes

- Remove validation ([#194](https://github.com/agritheory/check_run/pull/194),
  [`efda8ae`](https://github.com/agritheory/check_run/commit/efda8ae0f58ce272eae7888a0dd867a7ede4c792))


## v14.11.1 (2024-01-18)

### Bug Fixes

- Payment terms validation ([#192](https://github.com/agritheory/check_run/pull/192),
  [`036177d`](https://github.com/agritheory/check_run/commit/036177d6e4b82455e90e9e9d5d58e60f58845749))


## v14.11.0 (2024-01-08)

### Features

- Filter check run settings print format to only show enabled and Payment Entry formats
  ([#186](https://github.com/agritheory/check_run/pull/186),
  [`fc0f7d7`](https://github.com/agritheory/check_run/commit/fc0f7d776f83f8bc8b3b194b0362de3e27aa1baa))


## v14.10.0 (2023-12-14)

### Features

- Ignore PI where debit not has been issued
  ([#181](https://github.com/agritheory/check_run/pull/181),
  [`e085e96`](https://github.com/agritheory/check_run/commit/e085e9675a70c81fdc560e2341472d345c92ee70))


## v14.9.0 (2023-12-12)

### Bug Fixes

- Empty string values to NULL in queries
  ([`75ab1c9`](https://github.com/agritheory/check_run/commit/75ab1c96629b0e2220dd30555a1498ddd2561291))

### Documentation

- Update settings section
  ([`b9b15f8`](https://github.com/agritheory/check_run/commit/b9b15f8ac16494d53399ccd7ab3f823fd1545620))

### Features

- Add fallbacks for mode of payment per source document type
  ([`12f9160`](https://github.com/agritheory/check_run/commit/12f916000dbb96db2a1ea3474b55d226a7a1cb5a))


## v14.8.4 (2023-12-11)

### Bug Fixes

- Only fetch check number on "pay" payment types
  ([#179](https://github.com/agritheory/check_run/pull/179),
  [`1b6dd48`](https://github.com/agritheory/check_run/commit/1b6dd488a6cf921c4497737f47d27627f19e510f))


## v14.8.3 (2023-12-11)

### Bug Fixes

- Mode of payment summary ([#176](https://github.com/agritheory/check_run/pull/176),
  [`40fd4ee`](https://github.com/agritheory/check_run/commit/40fd4ee3057f9808944258b9d7807522827f17a6))

* fix: mode of payment summary

* wip: refactor reactivity for performance

* feat: improved reactivity

* style: prettify code

* fix: move built files to dist folder / ignored by git

---------

Co-authored-by: Tyler Matteson <tyler@agritheory.com>

Co-authored-by: agritheory <agritheory@users.noreply.github.com>


## v14.8.2 (2023-09-22)

### Bug Fixes

- Required_apps ([#162](https://github.com/agritheory/check_run/pull/162),
  [`31b5297`](https://github.com/agritheory/check_run/commit/31b52975839424f9a9bfbded6cc03c241dcb44cd))

* fix: required_apps


## v14.8.1 (2023-09-14)

### Bug Fixes

- Customizations leaks, module specificity
  ([#161](https://github.com/agritheory/check_run/pull/161),
  [`ce6b9fc`](https://github.com/agritheory/check_run/commit/ce6b9fc2a79e9a1beea4f514b3c52d4fd442da50))

### Continuous Integration

- Update release action user and email ([#155](https://github.com/agritheory/check_run/pull/155),
  [`a3cfc97`](https://github.com/agritheory/check_run/commit/a3cfc975aac95696b943ecbd809a00cab6159ffd))


## v14.8.0 (2023-09-08)

### Features

- Add read_only decorator
  ([`c7bb83c`](https://github.com/agritheory/check_run/commit/c7bb83ceba8fcfd291b6198ff1ee8b92edf1abca))


## v14.7.0 (2023-09-07)

### Bug Fixes

- Move bank validation out of override class into hook
  ([#142](https://github.com/agritheory/check_run/pull/142),
  [`f07ad5a`](https://github.com/agritheory/check_run/commit/f07ad5a1c4a9b7e424ad534ec40731f26f6feb0c))

- Only increment if check numer is numeric
  ([#139](https://github.com/agritheory/check_run/pull/139),
  [`079aa52`](https://github.com/agritheory/check_run/commit/079aa52bf013e13d3350848ef011b74b99b64bf1))

- Skip check on draft check runs with no transactions (v14)
  ([#148](https://github.com/agritheory/check_run/pull/148),
  [`dadd084`](https://github.com/agritheory/check_run/commit/dadd084c26f50de4e9dff1f360a8d73bbb37e250))

Resolution for `TypeError: the JSON object must be str, bytes or bytearray, not NoneType` when draft
  check run has no transactions.

### Continuous Integration

- Migrate to python semantic release ([#133](https://github.com/agritheory/check_run/pull/133),
  [`d37bca6`](https://github.com/agritheory/check_run/commit/d37bca61505e99476e6fb857fbd36dacc932918a))

* ci: migrate to python semantic release

* ci: add version variable file

* ci: update remote name

### Features

- Disallow cancellation of source documents selected for payment in draft CRs (#126)
  ([#143](https://github.com/agritheory/check_run/pull/143),
  [`bddc888`](https://github.com/agritheory/check_run/commit/bddc8884167c9e3381f519914a278a29fdf345f1))


## v14.6.0 (2023-07-28)

### Bug Fixes

- Add on hold fixes to query builder
  ([`a1e3114`](https://github.com/agritheory/check_run/commit/a1e3114e78b3894af61b40d46276c6dd6c0d92d3))

- Broken translation string in csv ([#122](https://github.com/agritheory/check_run/pull/122),
  [`9c2ded2`](https://github.com/agritheory/check_run/commit/9c2ded22846e0753a0ed4a7732781fb205a47df4))

- Mop ignore keypress if input is focused
  ([`e073c09`](https://github.com/agritheory/check_run/commit/e073c09a5ed26e61b34a44419f85a939781b1409))

- Remove check_digit argument in ACH generation
  ([#66](https://github.com/agritheory/check_run/pull/66),
  [`8476235`](https://github.com/agritheory/check_run/commit/8476235f380cfcea81309bd703667f6ff047663d))

- Remove undeclared variable reference
  ([`6a36c84`](https://github.com/agritheory/check_run/commit/6a36c84c6b3f8b8497ca7bae9e8db24e1e939228))

- Show purchase returns in check run ([#131](https://github.com/agritheory/check_run/pull/131),
  [`b1cd85b`](https://github.com/agritheory/check_run/commit/b1cd85b42284a3ea38aa1c703d1f2ae714ab7f6a))

### Chores

- Fix account names ([#99](https://github.com/agritheory/check_run/pull/99),
  [`7946bdf`](https://github.com/agritheory/check_run/commit/7946bdfb4bb4f7ba96a4939ff36f449bc108fa10))

### Continuous Integration

- Fix release CI
  ([`9c954d5`](https://github.com/agritheory/check_run/commit/9c954d5e6259a3c257036ea066e07e08afb93181))

- Fix release correctly on V14 also
  ([`3ff2d65`](https://github.com/agritheory/check_run/commit/3ff2d65dece13db5e8e40b96fbe0ecd8aed4f0be))

- Remove registry from package.json
  ([`607db96`](https://github.com/agritheory/check_run/commit/607db9619e75740c419e01c622ee51374e53aecf))

- Update installation and workflows
  ([`23c4f83`](https://github.com/agritheory/check_run/commit/23c4f838e51882b6f7db6ded58735b18e4f9a0c5))

### Documentation

- Add translations page
  ([`6e9c977`](https://github.com/agritheory/check_run/commit/6e9c9778b25aaa8d2bd8dc77ae87c341fbb1bc23))

### Features

- Add Canadian DFI Routing Number validation for bank
  ([`b4d9df9`](https://github.com/agritheory/check_run/commit/b4d9df97bc1705bd5c622d46bb88e4d7795f8b3d))

- Add Canadian/GB English translations
  ([`1e86c00`](https://github.com/agritheory/check_run/commit/1e86c00beb396499e7ece0eccb0902ab4e3188b0))

- Add logic for handling on-hold invoices, setting for automatic release and docs
  ([`da93c1d`](https://github.com/agritheory/check_run/commit/da93c1d04a58b18d9c098f3661bd731c6761d783))

- Add validate when processing, enable on_update_after_submit hook
  ([#115](https://github.com/agritheory/check_run/pull/115),
  [`d58a106`](https://github.com/agritheory/check_run/commit/d58a106bd295c4811ff0722ca0ade7d29a711c34))

- Check payment entries for cancelled or paid invoices before submitting
  ([#108](https://github.com/agritheory/check_run/pull/108),
  [`adbca4d`](https://github.com/agritheory/check_run/commit/adbca4df65c3599a213ddebacd9a269d8a2462a1))

- Custom immediate origin value in settings ([#76](https://github.com/agritheory/check_run/pull/76),
  [`813be9e`](https://github.com/agritheory/check_run/commit/813be9e299c2ba42f1bc0de11fabd03d1ab2f0fb))

* feat: custom immediate origin value in settings

* style: prettify code

---------

Co-authored-by: agritheory <agritheory@users.noreply.github.com>

- Fix lookup for non-existient bank account info, improve UX
  ([`4ef8a91`](https://github.com/agritheory/check_run/commit/4ef8a91ed769798d9569edc770ac4bd81a709b14))

- Port timeout fix to v14 ([#62](https://github.com/agritheory/check_run/pull/62),
  [`6f50230`](https://github.com/agritheory/check_run/commit/6f50230a8713c16f1818ba8450abc18cc2535322))

* feat: port timeout fix to v14

* fix: indent

* chore: prettier formatting

* style: prettify code

---------

Co-authored-by: agritheory <agritheory@users.noreply.github.com>

- Split checks by address
  ([`b32f0c9`](https://github.com/agritheory/check_run/commit/b32f0c991ba91a8377e87673977a4b651a4f6970))

- Update translations to capture button text
  ([`ccc4b67`](https://github.com/agritheory/check_run/commit/ccc4b6779c869a9786e7f67ded1c09333383439a))

- Validate docstatus of selected invoices still saved/submitted
  ([#44](https://github.com/agritheory/check_run/pull/44),
  [`78b3e25`](https://github.com/agritheory/check_run/commit/78b3e2580e200ce60211ed44d20651f68546eeae))

* feat: validate docstatus of selected invoices still saved/submitted

* refactor: moved validation code for cancelled transactions to function

### Testing

- Add on hold invoice to test data
  ([`6867d42`](https://github.com/agritheory/check_run/commit/6867d428c77fb096125d17e1e0382a92aabceaa0))

- Add payment terms to test data
  ([`8b4073e`](https://github.com/agritheory/check_run/commit/8b4073eaf7b0016fe7a4e1bd0c014af818d5477c))

- Fix net 14 days
  ([`3acea48`](https://github.com/agritheory/check_run/commit/3acea48f68560ca417b1d05cd9153635e9cc6c2e))


## v14.0.0 (2022-12-30)

### Bug Fixes

- Add bank account to payment entry form
  ([`3316d61`](https://github.com/agritheory/check_run/commit/3316d61fcce6b5de35cc029c52a9a1e57a507102))

- Change employee party field so payment entry can properly link to it
  ([`5f96753`](https://github.com/agritheory/check_run/commit/5f96753e1a27304565c59c39c150112b65aba50d))

- Checkrun rerender on document change
  ([`eabf8a5`](https://github.com/agritheory/check_run/commit/eabf8a55e9d2bd01fffdfbc6a24e41f8391a3981))

- Company name in correct header field of NACHA file
  ([`1e50281`](https://github.com/agritheory/check_run/commit/1e502816a1ade9badd5e0b727857847e4e194c55))

- Conform demo mode of payment types to docs recommendations
  ([`44cb68c`](https://github.com/agritheory/check_run/commit/44cb68c3f5ce79f863ea79b988c3fca3a639481d))

- Don't trigger settings change for check run creation
  ([`a672f46`](https://github.com/agritheory/check_run/commit/a672f467a1b3ceda3eb725e4bf605ecbc82933aa))

- Field name and type issues when creating NACHA file
  ([`7ded221`](https://github.com/agritheory/check_run/commit/7ded221b633e6330520508d497f4ce6c49cede78))

- Include built JS
  ([`12492b8`](https://github.com/agritheory/check_run/commit/12492b8573985470f5339ef37f71fd8c951da9e2))

- Line height and checkbox alignment
  ([`232fff6`](https://github.com/agritheory/check_run/commit/232fff641db11dc821051154788ffbd35e4760e5))

- Remove check PDF on confirm print
  ([`c2d0db9`](https://github.com/agritheory/check_run/commit/c2d0db949f51dc6e232785212212fc12ab4189f5))

- Reorder Supplier json to show bank account field in form
  ([#12](https://github.com/agritheory/check_run/pull/12),
  [`5d05e38`](https://github.com/agritheory/check_run/commit/5d05e38f4004f5f36735e43b1a229a46b4762c48))

- Set fields in test script expense claim generation
  ([`3152aac`](https://github.com/agritheory/check_run/commit/3152aac10b283aa92fdbd3f8e44a010b1d15b09c))

- Update installation guide link
  ([`bbc0a0e`](https://github.com/agritheory/check_run/commit/bbc0a0e47a64227ede7207803beac5e428ee45fe))

### Chores

- Conform capitalization
  ([`b66019f`](https://github.com/agritheory/check_run/commit/b66019f402af8b4ca740565316da452b363806b7))

- Use awesomplete z-index number / 1
  ([`1b19e30`](https://github.com/agritheory/check_run/commit/1b19e304be1b3ade913f965d3d6cabafccb47a4d))

### Documentation

- Add ACH generation infoand screen shot
  ([`2501cee`](https://github.com/agritheory/check_run/commit/2501cee0c8e19547febf500ccd952791960b2ab1))

- Add and re-order config section
  ([`c0ac8e5`](https://github.com/agritheory/check_run/commit/c0ac8e5da2d000a3170c40f617035493262247c3))

- Add directory structure, index, and photo assets
  ([`cf4e5d9`](https://github.com/agritheory/check_run/commit/cf4e5d9e1641b8e747326634716ae088d80a45cb))

- Add docs for example data and print format
  ([`9f6761b`](https://github.com/agritheory/check_run/commit/9f6761b4a0dfd3093a33447e3d4e6e5158b9f38d))

- Add docs for example format; disable format
  ([`6fcf639`](https://github.com/agritheory/check_run/commit/6fcf639a50acd3d5c0f753b381d1e96a46f49562))

- Add docs link
  ([`a264a21`](https://github.com/agritheory/check_run/commit/a264a21aabe82ea6686710098125790c22079f27))

- Add employee configuration image
  ([`fc4db1c`](https://github.com/agritheory/check_run/commit/fc4db1cae998baf8e65812a6c75024e05cc83e62))

- Add install instructions to readme
  ([`e055a03`](https://github.com/agritheory/check_run/commit/e055a03a7a6d305e1fe75660378fb646f8aed091))

- Add placeholder docs, start configuration
  ([`f3b6210`](https://github.com/agritheory/check_run/commit/f3b6210e43e00741791ef9693597c05fa3a1e6b3))

- Add Positive Pay screen shot
  ([`eaa596d`](https://github.com/agritheory/check_run/commit/eaa596dd172dd0dc7a672f99a9da507f76581a94))

- Add positive pay, links to index
  ([`ade8adb`](https://github.com/agritheory/check_run/commit/ade8adbf5b1f462ba4a90230b30feddbae34eea3))

- Add print confirmation screen shot
  ([`0b9ee06`](https://github.com/agritheory/check_run/commit/0b9ee062469f620f99556c0ec062e3ce9063ad06))

- Add settings docs and screen shots
  ([`c56f917`](https://github.com/agritheory/check_run/commit/c56f917f291ed9941592a4c26d558c9cf3bcf075))

- Add supplier config image and update text
  ([`06989a6`](https://github.com/agritheory/check_run/commit/06989a623fe5d787299c76d8b7933bc0c517ff96))

- Change 'todo' to 'coming soon'
  ([`be8af10`](https://github.com/agritheory/check_run/commit/be8af10e82751d513aa10e163d5363bef6c341cb))

- Edit config information
  ([`eabf6d0`](https://github.com/agritheory/check_run/commit/eabf6d0f74f33ec1ab9198645b85a76d6536defd))

- Edit permissions information
  ([`472abfc`](https://github.com/agritheory/check_run/commit/472abfca6a632ad50a2c24d0e66e2fffe7baafe1))

- Flatten directory structure
  ([`900fd2f`](https://github.com/agritheory/check_run/commit/900fd2f4af7dfc0822ad7962bcebd43c52281214))

- Minor formatting
  ([`d1bf1f5`](https://github.com/agritheory/check_run/commit/d1bf1f571874f916421540d0af7b19f106f3e6d4))

- Move installation instructions to doc page, link to that in README
  ([`427f4ae`](https://github.com/agritheory/check_run/commit/427f4ae4d77d4a72275278da74b45c357fe39803))

- Restructure index and update links
  ([`b423605`](https://github.com/agritheory/check_run/commit/b423605480909fe525aa70271b93c99b62190074))

- Spacing edits
  ([`ce4ec3a`](https://github.com/agritheory/check_run/commit/ce4ec3a91fa9ce5841d3a86704d7f878c3a704e3))

- Update config with mop type
  ([`8e26dc9`](https://github.com/agritheory/check_run/commit/8e26dc9b8b9575d65c4abc529be9c183132d7247))

- Update configuration with images
  ([`a2ca105`](https://github.com/agritheory/check_run/commit/a2ca1056ab7d24b79fc6e3034f9f89c58332b5d8))

- Update developer installation instructions
  ([`6f16336`](https://github.com/agritheory/check_run/commit/6f16336bb8b3ac9bdc98ca2637d4e987515e3538))

- Update for v14 Payment Ledger and install requirements
  ([`af2ebf3`](https://github.com/agritheory/check_run/commit/af2ebf3aeef0ba66bd4545cfe906e9fb4fbb6901))

- Update image
  ([`55e0be1`](https://github.com/agritheory/check_run/commit/55e0be170f3b375dfec8861dbce913bc9a3bf68c))

- Update screen shot
  ([`42b3e16`](https://github.com/agritheory/check_run/commit/42b3e16b3da18e0df17b3ce46cd565536f9ef212))

- Update screen shots and information
  ([`6aabb43`](https://github.com/agritheory/check_run/commit/6aabb43086e071e55e2b380fe358286bca8f45f6))

- Use tip component in docs
  ([`94551f7`](https://github.com/agritheory/check_run/commit/94551f7e99d2ace5069ec4aeed04a0cd8e2d797d))

### Features

- Ach integration
  ([`b3864c7`](https://github.com/agritheory/check_run/commit/b3864c76e710e0499b72eb619c4ec6987a8618df))

- Add example print format
  ([`0d316c1`](https://github.com/agritheory/check_run/commit/0d316c178612f893e9e8e67a4599baa3a4a8f6ac))

- Add files for employee and suppleir bank account obfuscation
  ([`f7ada06`](https://github.com/agritheory/check_run/commit/f7ada0650d035cadbe1d059c92c51947c5b119f5))

- Add mop alert
  ([`ba6029a`](https://github.com/agritheory/check_run/commit/ba6029a6ccf843acd70393a505fc1ff885cba206))

- Add more permissions topics
  ([`3f61a25`](https://github.com/agritheory/check_run/commit/3f61a2522348dfeb08e2f3f12901981b91df1083))

- Add positive pay report
  ([`128b5d6`](https://github.com/agritheory/check_run/commit/128b5d6fda4013a58930b7f426c9e676552dfb8e))

- Allow normal cusomtization workflow with multiple installed apps
  ([`1001b75`](https://github.com/agritheory/check_run/commit/1001b75a24564ba139bc3d6ab2a9873b419bb320))

- Check run settings
  ([`26c560d`](https://github.com/agritheory/check_run/commit/26c560db8fffb9dd73d6d403c1015f7eb8da2328))

- Convert raw sql statements to use query builder
  ([`a457067`](https://github.com/agritheory/check_run/commit/a457067f5235972d521c2061a925f1856c37a513))

- Expand permissions
  ([`e02c6cd`](https://github.com/agritheory/check_run/commit/e02c6cd4526a962023933e96040478ce9b7a93bb))

- Initialize App
  ([`cf39bb7`](https://github.com/agritheory/check_run/commit/cf39bb7679becd8a39c9ad20ea1aa7603a93ca52))

- Key nav
  ([`ae5bb24`](https://github.com/agritheory/check_run/commit/ae5bb245c807ea6fd812cc60f9e13ab1bd4726da))

- Port to version-14
  ([`cb8f9a5`](https://github.com/agritheory/check_run/commit/cb8f9a5b8cb508acc64ab0c9e36d835a9dd18a8d))

- Update SQL to use filter.bank_account in query
  ([`fa3580b`](https://github.com/agritheory/check_run/commit/fa3580b1ea7c2ba742047e9aa81a11b22e65fae3))

- Use variables to respect dark mode
  ([`b0bb4ae`](https://github.com/agritheory/check_run/commit/b0bb4ae7ddceda28ff51a7b72a21290c3e7f2d88))
