<!-- Copyright (c) 2026, AgriTheory and contributors
For license information, please see license.txt-->

# Changelog

This changelog was automatically generated from GitHub releases and pull requests.

## [v15.10.0] - 2025-09-10

### Release Notes

## v15.10.0 (2025-09-10)

### Bug Fixes

- Dates control ([`b04a9bb`](https://github.com/agritheory/check_run/commit/b04a9bb81ec0cbf5f0170d4e5836f8bdad86a68f))

- Mandatory field ([`bb35197`](https://github.com/agritheory/check_run/commit/bb35197a74bed207c52b55f8fb37f5246b86b6dc))

- Naming and precise dates to test edge cases ([`c7de096`](https://github.com/agritheory/check_run/commit/c7de0969c1d28f2053e63416ea5e8c22dbb1ec8d))

- Numer to number ([`47c445e`](https://github.com/agritheory/check_run/commit/47c445e0d946fea4591d609af6ac11061a766e29))

- Posting_date moved ([`f9c49dd`](https://github.com/agritheory/check_run/commit/f9c49dd4ae59606f8993333e4930e743558f29a9))

- Posting_date str to obj ([`74a7fa8`](https://github.com/agritheory/check_run/commit/74a7fa80105e358ab132d5acd6c7309e54c82cff))

- Reduce the Paid Amount field by the discount ([`f6da84c`](https://github.com/agritheory/check_run/commit/f6da84cb92ee1908c8beafa8f52e539678484b06))

- Show discount and due_date format ([`5ba1567`](https://github.com/agritheory/check_run/commit/5ba156720c99ae57ac9ba3178b5298553ac76d85))

### Chores

- Yarn.lock ignored ([`177e0b3`](https://github.com/agritheory/check_run/commit/177e0b33470059d354b7156ff44ba1eb07b4133f))

### Features

- Calculate_payment_term_discount ([`46d1c98`](https://github.com/agritheory/check_run/commit/46d1c98d16f91376094db74b3f662ecabdc0078d))

- Discount applied on submit ([`e35a6c2`](https://github.com/agritheory/check_run/commit/e35a6c21ac1455705eccd081e84aed98afcdb7bf))

- Discounts test data ([`48fa6a5`](https://github.com/agritheory/check_run/commit/48fa6a53cef798bb955770a9fbd7675c0e3a5340))

- Payment Discount Account field ([`dd60801`](https://github.com/agritheory/check_run/commit/dd60801c50f26c2146e90724d2d1038e19cfe555))

- Tests discounts ([`eaa35ea`](https://github.com/agritheory/check_run/commit/eaa35ea58325acdc562f79bbc9a33b04c402e7cd))

---

**Detailed Changes**: [v15.9.1...v15.10.0](https://github.com/agritheory/check_run/compare/v15.9.1...v15.10.0)


### Changes from Pull Requests

Added a new field for Payment Discount Account in Check Run Settings. Fixed an issue where valid payment term discounts were not applied to invoices.
  _Source: PR #373_

## [v15.9.1] - 2025-08-18

### Release Notes

## v15.9.1 (2025-08-18)

### Bug Fixes

- Disallow save until table renders (#380) (#381) ([#381](https://github.com/agritheory/check_run/pull/381), [`71afea9`](https://github.com/agritheory/check_run/commit/71afea9712d2fcf1c33ee17f39f1e5afa52374bf))

---

**Detailed Changes**: [v15.9.0...v15.9.1](https://github.com/agritheory/check_run/compare/v15.9.0...v15.9.1)


### Changes from Pull Requests

Fixed an issue where saving was allowed before the table rendered. Corrected the mode of payment summary.
  _Source: PR #381_

Added a new action to generate changelogs automatically. This simplifies tracking updates and improvements in the project.
  _Source: PR #375_

## [v15.9.0] - 2025-07-10

### Release Notes

## v15.9.0 (2025-07-10)

### Features

- Add amount to positive pay (#369) (#371) ([#371](https://github.com/agritheory/check_run/pull/371), [`8f7168c`](https://github.com/agritheory/check_run/commit/8f7168c4320cf9ac3252453278870062078c71e9))

---

**Detailed Changes**: [v15.8.0...v15.9.0](https://github.com/agritheory/check_run/compare/v15.8.0...v15.9.0)


### Changes from Pull Requests

Added amount field to positive pay feature.
  _Source: PR #371_

Backported issue 355 to version 15. Fixed issues with on_hold status and added tests for check_run functionality.
  _Source: PR #362_

## [v15.8.0] - 2025-06-24

### Release Notes

## v15.8.0 (2025-06-24)

### Features

- Backport issue_355 (#361) ([#361](https://github.com/agritheory/check_run/pull/361), [`925bb23`](https://github.com/agritheory/check_run/commit/925bb231f112ab2799ddc5e35e99682b5c3ba402))

---

**Detailed Changes**: [v15.7.4...v15.8.0](https://github.com/agritheory/check_run/compare/v15.7.4...v15.8.0)


### Changes from Pull Requests

Backported issue 355 to version 15. Updated check run settings and fixed issues in CheckRun.vue component.
  _Source: PR #361_

## [v15.7.4] - 2025-06-22

### Release Notes

## v15.7.4 (2025-06-22)

### Bug Fixes

- Ensure that on-hold invoices are not preselected for payment (#358) (#360) ([#360](https://github.com/agritheory/check_run/pull/360), [`554b755`](https://github.com/agritheory/check_run/commit/554b755be3fbea77ff73fb08633ac27c6b862b0b))

---

**Detailed Changes**: [v15.7.3...v15.7.4](https://github.com/agritheory/check_run/compare/v15.7.3...v15.7.4)


### Changes from Pull Requests

Fixed an issue where on-hold invoices were being preselected for payment. This ensures a smoother and more accurate billing process for users.
  _Source: PR #360_

## [v15.7.3] - 2025-06-18

### Release Notes

## v15.7.3 (2025-06-18)

### Bug Fixes

- Use correct keyword argument for v15 (#356) ([#356](https://github.com/agritheory/check_run/pull/356), [`8c429e8`](https://github.com/agritheory/check_run/commit/8c429e8b379810745a74a5331173c2e81a3c139e))

---

**Detailed Changes**: [v15.7.2...v15.7.3](https://github.com/agritheory/check_run/compare/v15.7.2...v15.7.3)


### Changes from Pull Requests

Fixed an issue where the wrong keyword argument was used for v15, ensuring compatibility and functionality.
  _Source: PR #356_

## [v15.7.2] - 2025-06-11

### Release Notes

## v15.7.2 (2025-06-11)

### Bug Fixes

- Filters mop (#341) ([#352](https://github.com/agritheory/check_run/pull/352), [`bac67ba`](https://github.com/agritheory/check_run/commit/bac67ba96df124333805152b130a561ebe2ecfa4))

---

**Detailed Changes**: [v15.7.1...v15.7.2](https://github.com/agritheory/check_run/compare/v15.7.1...v15.7.2)


### Changes from Pull Requests

Fixed an issue with filters in the application. Added new pay filter options.
  _Source: PR #352_

## [v15.7.1] - 2025-06-11

### Release Notes

## v15.7.1 (2025-06-11)

### Bug Fixes

- Backport-335-to-version-15 ([#344](https://github.com/agritheory/check_run/pull/344), [`b155a6c`](https://github.com/agritheory/check_run/commit/b155a6c77703b9bc68191c681dee4acb07dd715e))

---

**Detailed Changes**: [v15.7.0...v15.7.1](https://github.com/agritheory/check_run/compare/v15.7.0...v15.7.1)


### Changes from Pull Requests

Fixed an issue that caused problems in version 15. Improved linting and updated JavaScript configuration files for better performance.
  _Source: PR #344_

## [v15.7.0] - 2025-06-11

### Release Notes

## v15.7.0 (2025-06-11)

### Features

- Base Example Voucher MICR print format off Payment Entry ([#351](https://github.com/agritheory/check_run/pull/351), [`bb874e4`](https://github.com/agritheory/check_run/commit/bb874e4fcf038c2656143842c52c5ee0e1bd8d99))

---

**Detailed Changes**: [v15.6.0...v15.7.0](https://github.com/agritheory/check_run/compare/v15.6.0...v15.7.0)


### Changes from Pull Requests

Added a new MICR print format for Payment Entries in Example Vouchers. This update addresses issue #348 and improves the clarity and functionality of payment documents.
  _Source: PR #351_

## [v15.6.0] - 2025-06-11

### Release Notes

## v15.6.0 (2025-06-11)

### Features

- Check run settings quick entry override ([#350](https://github.com/agritheory/check_run/pull/350), [`e778743`](https://github.com/agritheory/check_run/commit/e778743dfc25adeafadfcedb6d8216a087e649b9))

---

**Detailed Changes**: [v15.5.0...v15.6.0](https://github.com/agritheory/check_run/compare/v15.5.0...v15.6.0)


### Changes from Pull Requests

Bank Account and Payable Account fields now preload their values correctly. The Payable Account field also filters properly.
  _Source: PR #350_

## [v15.5.0] - 2025-06-11

### Release Notes

## v15.5.0 (2025-06-11)

### Features

- Add setting to automatically attach positive pay to Check Run ([#347](https://github.com/agritheory/check_run/pull/347), [`9cc13df`](https://github.com/agritheory/check_run/commit/9cc13df7e29366b1e424d1a432d591519b33c2f6))

---

**Detailed Changes**: [v15.4.0...v15.5.0](https://github.com/agritheory/check_run/compare/v15.4.0...v15.5.0)


### Changes from Pull Requests

Added an option to automatically attach Positive Pay to Check Runs. This feature was backported from a newer version to ensure compatibility and functionality in `version-15`.
  _Source: PR #347_

## [v15.4.0] - 2025-05-29

### Release Notes

## v15.4.0 (2025-05-29)

### Chores

- Bp ([#327](https://github.com/agritheory/check_run/pull/327), [`3426dd8`](https://github.com/agritheory/check_run/commit/3426dd8ab48bfc64c229122ff0f0473fe5898fb0))

- Fix merge ([#306](https://github.com/agritheory/check_run/pull/306), [`c8e8317`](https://github.com/agritheory/check_run/commit/c8e8317677c43f64f42db4c8516fab20ed74cc42))

### Features

- Add permissioned signature API ([#339](https://github.com/agritheory/check_run/pull/339), [`5f0d019`](https://github.com/agritheory/check_run/commit/5f0d019b0a9e8d71caf93ca613d2e4aa20695b2d))

### Testing

- Backport posting date config tests, add pytest-order ([#311](https://github.com/agritheory/check_run/pull/311), [`eb1f540`](https://github.com/agritheory/check_run/commit/eb1f540a1753b671cc38cbb8be5879c9aa936a9a))

---

**Detailed Changes**: [v15.3.1...v15.4.0](https://github.com/agritheory/check_run/compare/v15.3.1...v15.4.0)


### Changes from Pull Requests

Added permissioned signature API for enhanced security and control.
  _Source: PR #339_

Updated approval workflow for RFPs. Fixed issues in check run settings and documentation.
  _Source: PR #327_

Handling keydown events now supported. Fixed issues with asset caching and user experience.
  _Source: PR #319_

Added permission checks for custom buttons and process check run API. Updated documentation on permissions.
  _Source: PR #312_

Backported new posting date config tests and added pytest-order markers. Fixed issues related to test organization in `version-15`.
  _Source: PR #311_

In Check Run Settings, the Company, Bank Account, and Payable Account fields are now mandatory. This ensures that all necessary information is provided during checks, preventing errors in processing payments.
  _Source: PR #306_

## [v15.3.1] - 2025-04-15

### Release Notes

## v15.3.1 (2025-04-15)

### Bug Fixes

- Remove unnecessary self typing ([#296](https://github.com/agritheory/check_run/pull/296), [`c5ca969`](https://github.com/agritheory/check_run/commit/c5ca96919a6131b9e86631f49abc6d2b1ffc61ff))

Co-authored-by: Rohan Bansal <rohan@agritheory.dev>

Co-authored-by: Tyler Matteson <support@agritheory.dev>

---

**Detailed Changes**: [v15.3.0...v15.3.1](https://github.com/agritheory/check_run/compare/v15.3.0...v15.3.1)


### Changes from Pull Requests

Removed unnecessary self typing in codebase. Fixed potential issues related to type inference by IDEs.
  _Source: PR #296_

Ports config posting date feature to version-15. Fixed issues with node action/cache and pre-commit configuration. Updated documentation for settings.
  _Source: PR #301_

## [v15.3.0] - 2025-04-15

### Release Notes

## v15.3.0 (2025-04-15)

### Features

- Make Posting Date read only if Set Payment Entry Posting Date == Use Todays Date" (#303) ([#309](https://github.com/agritheory/check_run/pull/309), [`88c0863`](https://github.com/agritheory/check_run/commit/88c0863ceaa5f43924bb4d17b0e8e960c98e988a))

(cherry picked from commit 61a43b32978927982369fa88afc85abc249ac910)

Co-authored-by: Francisco Roldán <franciscoproldan@gmail.com>

---

**Detailed Changes**: [v15.2.1...v15.3.0](https://github.com/agritheory/check_run/compare/v15.2.1...v15.3.0)


### Changes from Pull Requests

Make Posting Date read only if Set Payment Entry Posting Date is set to 'Use Today's Date'. This change ensures that users cannot manually edit the posting date when it is automatically determined.
  _Source: PR #309_

## [v15.2.1] - 2025-04-01

### Release Notes

## v15.2.1 (2025-04-01)

### Bug Fixes

- Respect settings date config (#298) ([#299](https://github.com/agritheory/check_run/pull/299), [`fcb2ab5`](https://github.com/agritheory/check_run/commit/fcb2ab574fa35e4a3fa507186f17112d258e9404))

(cherry picked from commit 8edbbffd1a8787102a30bce37ae9917c62c5f5d7)

Co-authored-by: Tyler Matteson <support@agritheory.dev>

---

**Detailed Changes**: [v15.2.0...v15.2.1](https://github.com/agritheory/check_run/compare/v15.2.0...v15.2.1)


### Changes from Pull Requests

Fixed an issue where settings date config was not being respected. This update ensures that the system now correctly applies the configured date settings.
  _Source: PR #299_

## [v15.2.0] - 2025-01-28

### Release Notes

## v15.2.0 (2025-01-28)

### Continuous Integration

- Backport config (#271) ([#272](https://github.com/agritheory/check_run/pull/272), [`db40e9f`](https://github.com/agritheory/check_run/commit/db40e9f69444da2857be322a82851210c7a23e1f))

Co-authored-by: Tyler Matteson <support@agritheory.dev>

(cherry picked from commit 438efdea82cc67cbeeb5df59c237e0450721d263)

Co-authored-by: Myuddin Khatri <53251406+MyuddinKhatri@users.noreply.github.com>

- Change backport config (#273) ([#275](https://github.com/agritheory/check_run/pull/275), [`48eebf7`](https://github.com/agritheory/check_run/commit/48eebf7efd5071ced8b9299862afe28652b4288d))

(cherry picked from commit 76fc626c6fa697cfd914ddef26e2c6b4ed3ba8c8)

Co-authored-by: Myuddin Khatri <53251406+MyuddinKhatri@users.noreply.github.com>

### Features

- Add MICR Encoding Print Format and docs ([#282](https://github.com/agritheory/check_run/pull/282), [`2b9f51a`](https://github.com/agritheory/check_run/commit/2b9f51a6145ee3c474c5949b75a12a346b15f359))

* feat: add print format applying MICR Encoding font

* test: add company address to test data

* docs: add MICR Encoding print format

---

**Detailed Changes**: [v15.1.2...v15.2.0](https://github.com/agritheory/check_run/compare/v15.1.2...v15.2.0)


### Changes from Pull Requests

Added MICR Encoding print format for checks. Updated documentation with rendering caveats.
  _Source: PR #282_

Added a new GitHub Action to print diff formats, improving readability and usability.
  _Source: PR #284_

Updated backport configuration to streamline the process. Removed old configuration file and updated workflow for better automation.
  _Source: PR #275_

This update includes new configuration files for continuous integration backporting. Users can now benefit from automated backport processes, enhancing efficiency and reducing manual errors in version management.
  _Source: PR #272_

## [v15.1.2] - 2024-07-18

### Release Notes

# v15.1.2 (2024-07-18)

## Fix

* fix: serialize null transactions(v15) (#262)

* fix: serialize null transactions(v15)

* fix: remove ci jobs dependency ([`5e13ec7`](https://github.com/agritheory/check_run/commit/5e13ec7514b78ce6d2596ed5c640e4f2c1d9bada))

## Unknown

* Allow or Disallow stand-alone debit note in check run -- Version 15 (#257)

* allow or disallow standalone debit note

* test cases changes&#39; ([`e0707df`](https://github.com/agritheory/check_run/commit/e0707df4fba64ac63e9fd4d36627c792748db292))

* Fix payment schedule outstanding v15 (#254)

* fix: fix payment schedule outstanding

* test: assert parent doc amount matches

* tests: fix matching error message

* feat: on_cancel hook and tests

* feat: minor changes, add precision (#253)

* fix: isort, JE generation issue

---------

Co-authored-by: Francisco Roldán &lt;franciscoproldan@gmail.com&gt; ([`624f36e`](https://github.com/agritheory/check_run/commit/624f36ebf195e734795216cdc790b0b1112ee802))

### Changes from Pull Requests

Fixed an issue where null transactions were not being serialized correctly. Removed unnecessary CI jobs dependency.
  _Source: PR #262_

Users can now allow or disallow standalone debit notes in check runs. This change includes updated settings and test cases for better functionality.
  _Source: PR #257_

## [v14.11.7] - 2024-06-29

### Release Notes

# v14.11.7 (2024-06-29)

## Fix

* fix: clean up and upgrade dependencies in v14 (#259) ([`ae18154`](https://github.com/agritheory/check_run/commit/ae181546d750bf2c6a3f5e2308f0721f75d8eb74))

## [v14.11.6] - 2024-06-29

### Release Notes

# v14.11.6 (2024-06-29)

## Ci

* ci: track overrides for Payment Entry (#248) ([`fc3d902`](https://github.com/agritheory/check_run/commit/fc3d9028a46f6cf31ff0c96cfc87a29f83a37c7a))

## Fix

* fix: File preview (#256)

* fix: File preview

* feat: refactor to jQuery

---------

Co-authored-by: Tyler Matteson &lt;tyler@agritheory.com&gt; ([`061be4e`](https://github.com/agritheory/check_run/commit/061be4ed28531be1b6f4fed5cb07bec8295a4699))

## Unknown

* Secondary Print Format (#209)

* fix: customization on split payment entry

* changes to remove pre-commit error

* changes to remove pre-commit error

* new print format Secondery sample

* rename print format

* on header check number added

* cheque number added

* set print format

* payment currency added

* print format changes

* comma saperated on bothe tablec

* commit to solve linter test

* secondary print format with same attechment

* change field name in print format

* split pdf in two attechment

* comment to run lint

* fix: customization on split payment entry

* fix:resolve conflict

* fix: resolve conflict

* Check PDF name changes

---------

Co-authored-by: viralpatel15 &lt;viralkansodiya167@gmail.com&gt; ([`9eda182`](https://github.com/agritheory/check_run/commit/9eda182dccd211090ce7f4c84399c1e863758ad4))

* Fix payment schedule outstanding (#251)

* fix: fix payment schedule outstanding

* test: assert parent doc amount matches

* tests: fix matching error message

* feat: on_cancel hook and tests

* feat: minor changes, add precision (#253)

---------

Co-authored-by: Francisco Roldán &lt;franciscoproldan@gmail.com&gt; ([`46a084a`](https://github.com/agritheory/check_run/commit/46a084a3cf862e06bbd3a0b9c81ecd5e6a683d07))

* Allow and Disallow setting  to create stand-alone debit note (#232)

* Seetng added for stand-alon credit note

* remove field from check run settings

* custom field Allow stand-alone debit notes?

* correct the spelling mistake

* move setting from company level to check run settings level

* reformat by pre-commit

* chore: prettier

* chore: remove old linters

* chore: fix checkout GHA depth from forks

* ci: fix python version

* test: add test for excluding purchase invoice return

---------

Co-authored-by: Tyler Matteson &lt;tyler@agritheory.com&gt; ([`f76ad3a`](https://github.com/agritheory/check_run/commit/f76ad3acc971ff59fe8ffd0332a5339ac8f84b62))

* Add documentation and tests for returns (#222)

* docs: add screen shot and explanation around returns

* test: add return test

* ci: replace cypress with pytest tests

* ci: add pytest dependency ([`48bd0c2`](https://github.com/agritheory/check_run/commit/48bd0c274429cd8f1bb034d551f99bb23277056e))

* Staging (#220)

* fix: add supplier bank field (#219)

was removed previously in error

* remove irrelevant code (#217)

---------

Co-authored-by: ViralKansodiya-Fosserp &lt;141210323+viralkansodiya@users.noreply.github.com&gt; ([`cf8e1fe`](https://github.com/agritheory/check_run/commit/cf8e1fe1cc4f1aa5915a0f91e42c2a3ba5c39fdb))

### Changes from Pull Requests

Fixed issues with payment schedule outstanding. Added new tests and hooks for better functionality.
  _Source: PR #254_

## [v15.1.1] - 2024-05-29

### Release Notes

# v15.1.1 (2024-05-29)

## Ci

* ci: add conftest file updated for json (#228) ([`dc306c3`](https://github.com/agritheory/check_run/commit/dc306c3364ac9ecb2d02003137284a138340ef42))

* ci: remove cypress, fix hrms install, conform (#221)

* ci: remove cypress, fix hrms install, conform

* ci: fix mypy error ([`f6b629b`](https://github.com/agritheory/check_run/commit/f6b629b7876a14795f39dc6d853ea5b7f8722098))

## Fix

* fix: bankaccount =&gt; bank typing (#247) ([`da77cc3`](https://github.com/agritheory/check_run/commit/da77cc329e28d95f84783d98dbd204addb39d0e8))

## Test

* test: add tests, remove cypress (#238) ([`c20ed6e`](https://github.com/agritheory/check_run/commit/c20ed6e23fc744f0718dd85665f407c134bb7a56))

## Unknown

* Grant file download access for multiple downloads only to specific roles (#237)

* ach file download access

* replace super class validate

* chore: prettier

* ci: remove old linters

---------

Co-authored-by: Tyler Matteson &lt;tyler@agritheory.com&gt; ([`160f609`](https://github.com/agritheory/check_run/commit/160f6090b3e3061f12c8f9649c4755bb358a8f70))

### Changes from Pull Requests

Fixed a typo in the code: changed "bankaccount" to "bank". This change improves readability and consistency.
  _Source: PR #247_

#216: Grant file download access for multiple downloads only to specific roles. Fixed old linters and updated code formatting.
  _Source: PR #237_

Added new tests for check runs and removed old Cypress files.
  _Source: PR #238_

Added an updated `conftest.py` file that now uses JSON references instead of TXT. This change enhances configuration management and flexibility in tests.
  _Source: PR #228_

Removed Cypress for UI tests, fixed HRMS installation issues, and added a pytest workflow.
  _Source: PR #221_

## [v15.1.0] - 2024-03-18

### Release Notes

# v15.1.0 (2024-03-18)

## Feature

* feat: add v15 to release config ([`41e329d`](https://github.com/agritheory/check_run/commit/41e329d5f58b8d2c1550a334495fe2c57ff0bc5b))

* feat: update init version ([`f53307b`](https://github.com/agritheory/check_run/commit/f53307bbdd631b1e2dd869cb2c3a7892d9acc870))

* feat: release version-15 ([`6cd1a27`](https://github.com/agritheory/check_run/commit/6cd1a2788dc6597b3236d867b2dfd3f047dd4d6f))

* feat: version-15 ([`0f2cd0a`](https://github.com/agritheory/check_run/commit/0f2cd0ada07d1cb3e13ebe5325a0b9d6ab2e3876))

## [v14.11.5] - 2024-02-06

### Release Notes

# v14.11.5 (2024-02-06)

## Fix

* fix: disallow mop selection on submitted doc, fix indicator (#207) ([`0429e48`](https://github.com/agritheory/check_run/commit/0429e484c38227ac0f4136f94d128d5ef26580f9))

* fix: onchanges of mode_of_payment make enable to save form (#206)

Co-authored-by: viralpatel15 &lt;viralkansodiya167@gmail.com&gt; ([`0b4bff0`](https://github.com/agritheory/check_run/commit/0b4bff0d5de5e76d6e0127e53081775a8056554b))

## Unknown

* Override a function to improve error msg (#205)

* Allocated ammount validation override for msg improvement

* comment add

* add a comment on function

* Refactor: Rename &#39;uniq_vouchers&#39; to &#39;unique_vouchers&#39; in payment_entry.py

---------

Co-authored-by: viralpatel15 &lt;viralkansodiya167@gmail.com&gt; ([`80fa4cf`](https://github.com/agritheory/check_run/commit/80fa4cf564b8f437eaccfc042af10c23b54b895b))

* Remove paid document on Process check run  (#202)

* class name has been change

* fix: remove paid invoice and changes related to manually paid case

* changes to remove class name changes ([`43cc33e`](https://github.com/agritheory/check_run/commit/43cc33ee6f192271b5c10b5c1efea7c09b17375f))

* class name has been changed (#201) ([`8d46b53`](https://github.com/agritheory/check_run/commit/8d46b535748949e1d5467b05f69abc6d68dc077b))


## [v14.11.4] - 2024-01-22

### Release Notes

# v14.11.4 (2024-01-22)

## Fix

* fix: always include payment term for purchase invoice (#197)

* ci: update app name in path string check

* fix: add PI payment term in Pmt Entry outside a Check Run

* tests: add manual payment entry to test payment term

* docs: update for Payment Entry payment term customizations ([`1156621`](https://github.com/agritheory/check_run/commit/1156621b4b80f0e7a5cc3f7c10076910305ad29b))


## [v14.11.3] - 2024-01-18

### Release Notes

# v14.11.3 (2024-01-18)

## Fix

* fix: add docstatus check first before fetching supplier MOP (#195) ([`9691364`](https://github.com/agritheory/check_run/commit/9691364f52248e4dfd2c79eaa89bdaba41c5d148))


## [v14.11.2] - 2024-01-18

### Release Notes

# v14.11.2 (2024-01-18)

## Fix

* fix: remove validation (#194) ([`efda8ae`](https://github.com/agritheory/check_run/commit/efda8ae0f58ce272eae7888a0dd867a7ede4c792))


## [v14.11.1] - 2024-01-18

### Release Notes

# v14.11.1 (2024-01-18)

## Fix

* fix: payment terms validation (#192) ([`036177d`](https://github.com/agritheory/check_run/commit/036177d6e4b82455e90e9e9d5d58e60f58845749))

## Unknown

* Optionally validate if check number has been used already (#189)

* feat: add &#34;validate unique check number&#34; setting

* feat: Optionally validate if check number has been used already

* feat: Optionally validate if check number has been used already

* fix: tabulation ([`e374b97`](https://github.com/agritheory/check_run/commit/e374b9797985a9842541335cba3bfb40f9e74bfd))

* File preview in check run (#182)

* feat: file preview

* feat: improvement

* feat: file preview treshold

* fix: refactor filters to work with prettier, also fix rendering bug

---------

Co-authored-by: Tyler Matteson &lt;tyler@agritheory.com&gt; ([`1e8cd26`](https://github.com/agritheory/check_run/commit/1e8cd268786cb8dcea94bb7f279643a48570aa77))

* Validate customizations (#166)

* fix: validate customizations

* Per supplier invoices per voucher (#165)

* feat: allow per-supplier override for number of invoices per voucher

* docs: add docs for per supplier invoices per voucher

* Quick Check (#172)

* feat: quick check poc

* fix: add additional filters in check run settings and also in check run quick entry

* docs: quick check and payment entry customization docs

* fix: validate customizations

* chore: prettier ([`6fd59cb`](https://github.com/agritheory/check_run/commit/6fd59cb5dea2f7b7e84387796c18ebd83ad18442))

* Add workflow for voided check  (#187)

* feat: voided check

* style: prettify code

* fix: rename workflow

* chore: remove list JS, use workflow instead

* chore: tab spacing

---------

Co-authored-by: fproldan &lt;fproldan@users.noreply.github.com&gt;
Co-authored-by: Tyler Matteson &lt;tyler@agritheory.com&gt; ([`a84c566`](https://github.com/agritheory/check_run/commit/a84c5667edafa09b876a17f80661f0ced65a796e))


## [v14.11.0] - 2024-01-08

### Release Notes

# v14.11.0 (2024-01-08)

## Feature

* feat: Filter check run settings print format to only show enabled and Payment Entry formats (#186) ([`fc0f7d7`](https://github.com/agritheory/check_run/commit/fc0f7d776f83f8bc8b3b194b0362de3e27aa1baa))

## Unknown

* patch: update outsanting in old payment schedule entries (#183) ([`a9e3e8b`](https://github.com/agritheory/check_run/commit/a9e3e8b1685cdad2c243e6c383ad0563f31f5c27))


## [v14.10.0] - 2023-12-14

### Release Notes

# v14.10.0 (2023-12-14)

## Feature

* feat: ignore PI where debit not has been issued (#181) ([`e085e96`](https://github.com/agritheory/check_run/commit/e085e9675a70c81fdc560e2341472d345c92ee70))


## [v14.9.0] - 2023-12-12

### Release Notes

# v14.9.0 (2023-12-12)

## Documentation

* docs: update settings section ([`b9b15f8`](https://github.com/agritheory/check_run/commit/b9b15f8ac16494d53399ccd7ab3f823fd1545620))

## Feature

* feat: add fallbacks for mode of payment per source document type ([`12f9160`](https://github.com/agritheory/check_run/commit/12f916000dbb96db2a1ea3474b55d226a7a1cb5a))

## Fix

* fix: empty string values to NULL in queries ([`75ab1c9`](https://github.com/agritheory/check_run/commit/75ab1c96629b0e2220dd30555a1498ddd2561291))

## Unknown

* Merge pull request #180 from agritheory/default_mode_of_payment_settings

feat: add fallbacks for mode of payment per source document type ([`c609603`](https://github.com/agritheory/check_run/commit/c6096038c1363e14a2ba7abb29f2cf73d25ce860))


## [v14.8.4] - 2023-12-11

### Release Notes

# v14.8.4 (2023-12-11)

## Fix

* fix: only fetch check number on &#34;pay&#34; payment types (#179) ([`1b6dd48`](https://github.com/agritheory/check_run/commit/1b6dd488a6cf921c4497737f47d27627f19e510f))


## [v14.8.3] - 2023-12-11

### Release Notes

# v14.8.3 (2023-12-11)

## Fix

* fix: mode of payment summary (#176)

* fix: mode of payment summary

* wip: refactor reactivity for performance

* feat: improved reactivity

* style: prettify code

* fix: move built files to dist folder / ignored by git

---------

Co-authored-by: Tyler Matteson &lt;tyler@agritheory.com&gt;
Co-authored-by: agritheory &lt;agritheory@users.noreply.github.com&gt; ([`40fd4ee`](https://github.com/agritheory/check_run/commit/40fd4ee3057f9808944258b9d7807522827f17a6))

## Unknown

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


## [v14.8.2] - 2023-09-22

### Release Notes

# v14.8.2 (2023-09-22)

## Fix

* fix: required_apps (#162)

* fix: required_apps

* fix: required_apps ([`31b5297`](https://github.com/agritheory/check_run/commit/31b52975839424f9a9bfbded6cc03c241dcb44cd))


## [v14.8.1] - 2023-09-14

### Release Notes

# v14.8.1 (2023-09-14)

## Ci

* ci: update release action user and email (#155) ([`a3cfc97`](https://github.com/agritheory/check_run/commit/a3cfc975aac95696b943ecbd809a00cab6159ffd))

## Fix

* fix: customizations leaks, module specificity (#161) ([`ce6b9fc`](https://github.com/agritheory/check_run/commit/ce6b9fc2a79e9a1beea4f514b3c52d4fd442da50))

## Unknown

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


## [v14.8.0] - 2023-09-08

### Release Notes

# v14.8.0 (2023-09-08)

## Feature

* feat: add read_only decorator ([`c7bb83c`](https://github.com/agritheory/check_run/commit/c7bb83ceba8fcfd291b6198ff1ee8b92edf1abca))

## Unknown

* Merge pull request #150 from agritheory/read_only

feat: add read_only decorator ([`73d459d`](https://github.com/agritheory/check_run/commit/73d459d616b5190ba85ebe67c115f29cae2d11ba))

* Merge branch &#39;version-14&#39; into read_only ([`aaca764`](https://github.com/agritheory/check_run/commit/aaca76471cb95480aef1a62459ae296767dafcd2))

* Setup mypy (#149)

* chore: add typing

* ci: add mypy to pre-commit and CI

---------

Co-authored-by: Heather Kusmierz &lt;heather.kusmierz@gmail.com&gt; ([`5831fb8`](https://github.com/agritheory/check_run/commit/5831fb85f3b08e76f486c3b01fb671b3dba06225))


## [v14.7.0] - 2023-09-07

### Release Notes

# v14.7.0 (2023-09-07)

## Ci

* ci: migrate to python semantic release (#133)

* ci: migrate to python semantic release

* ci: add version variable file

* ci: update remote name ([`d37bca6`](https://github.com/agritheory/check_run/commit/d37bca61505e99476e6fb857fbd36dacc932918a))

## Feature

* feat: disallow cancellation of source documents selected for payment in draft CRs (#126) (#143) ([`bddc888`](https://github.com/agritheory/check_run/commit/bddc8884167c9e3381f519914a278a29fdf345f1))

## Fix

* fix: skip check on draft check runs with no transactions (v14) (#148)

Resolution for `TypeError: the JSON object must be str, bytes or bytearray, not NoneType` when draft check run has no transactions. ([`dadd084`](https://github.com/agritheory/check_run/commit/dadd084c26f50de4e9dff1f360a8d73bbb37e250))

* fix: move bank validation out of override class into hook (#142) ([`f07ad5a`](https://github.com/agritheory/check_run/commit/f07ad5a1c4a9b7e424ad534ec40731f26f6feb0c))

* fix: only increment if check numer is numeric (#139) ([`079aa52`](https://github.com/agritheory/check_run/commit/079aa52bf013e13d3350848ef011b74b99b64bf1))

## Unknown

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


## [v13.3.3] - 2023-09-07

### Release Notes

# v13.3.3 (2023-09-07)

## Fix

* fix: skip check on draft check runs with no transactions (#147)

Resolution for `TypeError: the JSON object must be str, bytes or bytearray, not NoneType` when draft check run has no transactions. ([`b3821cb`](https://github.com/agritheory/check_run/commit/b3821cb7332414ce5049a2f9bf355cd4f9e4ae1e))


## [v13.3.2] - 2023-09-07

### Release Notes

# v13.3.2 (2023-09-07)

## Ci

* ci: migrate to python semantic release (#134)

* ci: migrate to python semantic release

* ci: add version variable file

* ci: update remote name ([`404edf3`](https://github.com/agritheory/check_run/commit/404edf35cae2180a02a45be875fcb54ef7e92cef))

## Fix

* fix: only increment if check numer is numeric (#138) ([`30679db`](https://github.com/agritheory/check_run/commit/30679db1985fcc0a41238d8860a17c019b751d98))

## Unknown

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


## [v13.3.1] - 2023-08-03

### Release Notes

## What's Changed
* trans: add error message to translations by @HKuz in https://github.com/agritheory/check_run/pull/128


## [v14.6.0] - 2023-08-03

### Release Notes

## What's Changed
* feat: validate docstatus of selected invoices still saved/submitted by @HKuz in https://github.com/agritheory/check_run/pull/44
* Port recent version-13 changes by @HKuz in https://github.com/agritheory/check_run/pull/50
* feat: Canadian regionalization by @HKuz in https://github.com/agritheory/check_run/pull/45
* V14 on hold invoice by @agritheory in https://github.com/agritheory/check_run/pull/55
* Bank account lookup fix by @agritheory in https://github.com/agritheory/check_run/pull/59
* Bank account lookup fix by @agritheory in https://github.com/agritheory/check_run/pull/61
* feat: port timeout fix to v14 by @agritheory in https://github.com/agritheory/check_run/pull/62
* V14 timeout fix by @agritheory in https://github.com/agritheory/check_run/pull/64
* fix: remove check_digit argument in ACH generation by @agritheory in https://github.com/agritheory/check_run/pull/66
* V14 party lookup by @agritheory in https://github.com/agritheory/check_run/pull/68
* [v14] handle errors in background queue by @agritheory in https://github.com/agritheory/check_run/pull/72
* feat: custom immediate origin value in settings by @agritheory in https://github.com/agritheory/check_run/pull/76
* ci: fix release CI by @agritheory in https://github.com/agritheory/check_run/pull/85
* V14 ci by @agritheory in https://github.com/agritheory/check_run/pull/87
* The hook jenv is deprecated New variable is jinja by @alibaig4u in https://github.com/agritheory/check_run/pull/90
* chore: fix account names by @HKuz in https://github.com/agritheory/check_run/pull/99
* V14 ports by @agritheory in https://github.com/agritheory/check_run/pull/98
* Pre-processing validation by @agritheory in https://github.com/agritheory/check_run/pull/108
* V14 pre process validation by @agritheory in https://github.com/agritheory/check_run/pull/113
* feat: add validate when processing, enable on_update_after_submit hook by @HKuz in https://github.com/agritheory/check_run/pull/115
* fix: broken translation string in csv by @HKuz in https://github.com/agritheory/check_run/pull/122
* fix: show purchase returns in check run by @agritheory in https://github.com/agritheory/check_run/pull/131
* trans: add error message to translations by @HKuz in https://github.com/agritheory/check_run/pull/129

## New Contributors
* @alibaig4u made their first contribution in https://github.com/agritheory/check_run/pull/90

**Full Changelog**: https://github.com/agritheory/check_run/compare/v14.0.0...v14.6.0

## [v14.5.1] - 2023-07-28

### Release Notes

## [14.5.1](https://github.com/agritheory/check_run/compare/v14.5.0...v14.5.1) (2023-07-28)


### Bug Fixes

* show purchase returns in list ([#130](https://github.com/agritheory/check_run/issues/130)) ([c504828](https://github.com/agritheory/check_run/commit/c504828c1bbe1552e9a3cc87f87082c5f89dae7b))





## [v14.5.0] - 2023-07-24

### Release Notes

# [14.5.0](https://github.com/agritheory/check_run/compare/v14.4.0...v14.5.0) (2023-07-24)


### Features

* migrate validation to doc_events from doctype override ([#127](https://github.com/agritheory/check_run/issues/127)) ([45c9598](https://github.com/agritheory/check_run/commit/45c959834a60d57148b4443e902f25c2c56a30ff)), closes [#126](https://github.com/agritheory/check_run/issues/126) [#126](https://github.com/agritheory/check_run/issues/126)





## [v14.4.0] - 2023-07-24

### Release Notes

# [14.4.0](https://github.com/agritheory/check_run/compare/v14.3.2...v14.4.0) (2023-07-24)


### Features

* disallow cancellation of source documents selected for payment in draft CRs ([#126](https://github.com/agritheory/check_run/issues/126)) ([329c41c](https://github.com/agritheory/check_run/commit/329c41c9d1470a97deaa45b7972c9e6818c8aa3b))





## [v14.3.2] - 2023-07-19

### Release Notes

## [14.3.2](https://github.com/agritheory/check_run/compare/v14.3.1...v14.3.2) (2023-07-19)


### Bug Fixes

* broken translation string in csv ([#121](https://github.com/agritheory/check_run/issues/121)) ([e3c87b4](https://github.com/agritheory/check_run/commit/e3c87b415fe54e94562cc712948b44d33b0d8519))





## [v14.3.1] - 2023-06-11

### Release Notes

## [14.3.1](https://github.com/agritheory/check_run/compare/v14.3.0...v14.3.1) (2023-06-11)


### Bug Fixes

* add check for expense claim in pre-process validation ([#112](https://github.com/agritheory/check_run/issues/112)) ([1503fa9](https://github.com/agritheory/check_run/commit/1503fa9cad5e7e0a74614a2dcd63eea1797024cc))





## [v14.3.0] - 2023-06-11

### Release Notes

# [14.3.0](https://github.com/agritheory/check_run/compare/v14.2.2...v14.3.0) (2023-06-11)


### Features

* add validate when processing, enable on_update_after_submit hook ([#111](https://github.com/agritheory/check_run/issues/111)) ([2e87a26](https://github.com/agritheory/check_run/commit/2e87a260035cfd81466cb0206f8d718a2d107551))





## [v14.2.2] - 2023-05-12

### Release Notes

## [14.2.2](https://github.com/agritheory/check_run/compare/v14.2.1...v14.2.2) (2023-05-12)


### Bug Fixes

* reprint button text color ([#103](https://github.com/agritheory/check_run/issues/103)) ([7101284](https://github.com/agritheory/check_run/commit/7101284f5007723877d312efa753b9c16a6efb2e))





## [V13.3.0] - 2023-04-21

### Release Notes

## What's Changed
* Code style by @agritheory in https://github.com/agritheory/check_run/pull/96
* Fix process check run by @agritheory in https://github.com/agritheory/check_run/pull/97


**Full Changelog**: https://github.com/agritheory/check_run/compare/v13.2.2...V13.3.0

## [v13.2.2] - 2023-04-17

### Release Notes

## What's Changed
* Use Posting Date for Effective Entry Date by @put3r-r00t3r in https://github.com/agritheory/check_run/pull/89


**Full Changelog**: https://github.com/agritheory/check_run/compare/v13.2.1...v13.2.2

## [v13.2.1] - 2023-04-17

### Release Notes

## What's Changed
* fix: check for docstatus instead of status by @agritheory in https://github.com/agritheory/check_run/pull/93


**Full Changelog**: https://github.com/agritheory/check_run/compare/v13.2.0...v13.2.1

## [v13.1.0] - 2023-04-03

### Release Notes

# [14.1.0](https://github.com/agritheory/check_run/compare/v14.0.0...v14.1.0) (2023-04-03)


### Bug Fixes

* address PR requests ([084fb22](https://github.com/agritheory/check_run/commit/084fb2253b62908440df0d3b4993eb4b1f0d376b))
* company name in correct header field of NACHA file ([81afb09](https://github.com/agritheory/check_run/commit/81afb09c3b1d3e34774d67dc7e838ff2b69900ee))
* don't raise exception on bank account lookup, better UX ([#60](https://github.com/agritheory/check_run/issues/60)) ([1d5d018](https://github.com/agritheory/check_run/commit/1d5d018c9e1703b41ee568482f9fb0f57f2d4c62))
* fallbacks and length limitations for discretionary data ([f783951](https://github.com/agritheory/check_run/commit/f7839517f043fa811ab030b92608826e4bbb0f0e))
* MOP ignore keypress if input is focused ([8d2d697](https://github.com/agritheory/check_run/commit/8d2d6975973041e07616fb6704b72ffe3655cd04))
* release ([8a8ec06](https://github.com/agritheory/check_run/commit/8a8ec062f263d49a9bcd7487af6f5de9372fcde1))
* release ([#82](https://github.com/agritheory/check_run/issues/82)) ([9b32e9b](https://github.com/agritheory/check_run/commit/9b32e9b036f0ff16d21d65ba96851bc8d03e8c5a))
* remove check PDF on confirm print ([4b96835](https://github.com/agritheory/check_run/commit/4b96835d8415bd0e9b2a9bf07a90a2e450559573))
* remove mimesis import ([bdbadea](https://github.com/agritheory/check_run/commit/bdbadea1759c0cf4ad469677606704dbf02bf078))
* test release ([f5cd245](https://github.com/agritheory/check_run/commit/f5cd245154802b1c4c78b4dcce47677064ec7ddb))
* validate if there are any transactions before validating them ([2aa94a7](https://github.com/agritheory/check_run/commit/2aa94a7306db4107d7e15ddd33767169f52a06b7))


### Features

* add Canadian regionalization for v-13 ([5cbd277](https://github.com/agritheory/check_run/commit/5cbd277c7979e54c545e04c415dd2f836a3c6dd4))
* add example print format ([521bff5](https://github.com/agritheory/check_run/commit/521bff50d3f1e4f5d141ef12f6ed05663d2c070a))
* add field for immediate origin ([#75](https://github.com/agritheory/check_run/issues/75)) ([531b307](https://github.com/agritheory/check_run/commit/531b3077316af0fdfcef5cfd4ece04bc29b95493))
* add logic for handling on-hold invoices, setting for automatic release and docs ([63bd16e](https://github.com/agritheory/check_run/commit/63bd16eaf6aa1b2f9f4738ad0f860c731e84d721))
* add more detail to cancelled document validation error message ([6a99349](https://github.com/agritheory/check_run/commit/6a9934956d7f62cfc5b286e8ab06c621b15071b8))
* add omit origin ach setting ([b72901e](https://github.com/agritheory/check_run/commit/b72901e0a6bf806c012a91bbba28ee765efecac0))
* increment check number from payment ([#70](https://github.com/agritheory/check_run/issues/70)) ([00706ff](https://github.com/agritheory/check_run/commit/00706ff8c17a20f99ddff53beb62e450ff09eb5c))
* look up party on PE submission to avoid renaming problems ([#67](https://github.com/agritheory/check_run/issues/67)) ([4cdf7de](https://github.com/agritheory/check_run/commit/4cdf7de5d648bcd37cb19ce67d899804f7107ad3))
* split checks by address ([f091550](https://github.com/agritheory/check_run/commit/f09155050ea8a64ee7fdb3ba8f3596eb936fd871))
* validate docstatus of selected invoices in Check Run still saved/submitted ([9bf5605](https://github.com/agritheory/check_run/commit/9bf56054041c341fc23c4cdf0a9449ca32ef8ba5))
