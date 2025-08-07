<div align="center" markdown="1">

<a href="https://github.com/agritheory/check_run">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./.github/assets/aticonwhitehex.svg">
    <img alt="AgriTheory Logo" src="./.github/assets/aticonrusthex.svg" width="100">
  </picture>
</a>

# Check Run

**Enterprise payables management and check printing for ERPNext**


  [![GitHub Stars][stars-shield]][stars-url]
  [![GitHub Forks][forks-shield]][forks-url]
  [![MIT License][license-shield]][license-url]

<p align="center">
  <a href="https://agritheory.com/documentation/check_run/"><strong>Explore the docs »</strong></a>
  <br />
  <br />
  <a href="https://github.com/agritheory/check_run/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
  ·
  <a href="https://github.com/agritheory/check_run/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
</p>

</div>

<a id="readme-top"></a>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

Check Run is a powerful ERPNext extension that provides payables-related utilities including a single-page payment mechanism, check printing, and bank-friendly reports for enterprise-grade payables management.

**Key Features:**
- **Single-Page Payment Processing**: Collect and process all outstanding payables for a company in one streamlined interface
- **Professional Check Printing**: Customizable check formats with voucher support
- **ACH File Generation**: Generate NACHA-compliant ACH files for electronic payments
- **Bank-Friendly Reports**: Positive Pay reports for fraud prevention and reconciliation
- **Payment Scheduling**: Support for complex payment terms and schedules
- **Multi-Mode Payments**: Support for checks, ACH, wire transfers, and more
- **Returns Handling**: Process debit notes and returns against purchase invoices
- **Keyboard Navigation**: Full keyboard shortcuts support for efficient data entry

The Check Run feature collects all outstanding payables for a given company and account head, defaulting to payables up to the current date (adjustable as needed). Users select invoices to pay and payment methods, then on submission, it creates payment entries and provides options for check printing and ACH file generation.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

<div align="left">

[![Python][Python.py]][Python-url]
[![Frappe][Frappe.io]][Frappe-url]
[![ERPNext][ERPNext.com]][ERPNext-url]
[![JavaScript][JavaScript.js]][JavaScript-url]
[![Vue][Vue.js]][Vue-url]

</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Check Run requires an existing ERPNext installation. For detailed installation instructions for both production and development environments, see our [installation guide](./docs/version-14/en/installationguide.md).

### Prerequisites

* ERPNext Version 14
* Python 3.10+
* Node.js 16+
* Frappe Framework

### Installation

1. Get the app from GitHub
   ```sh
   bench get-app check_run https://github.com/agritheory/check_run
   ```

2. Install the app to your site
   ```sh
   bench --site {{ site name }} install-app check_run
   ```

3. Configure your bank accounts and payment methods
   ```sh
   # See configuration guide for detailed setup
   ```

For complete development setup instructions, see our [installation guide](./docs/version-14/en/installationguide.md).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

### Quick Start

1. Search for **"Check Run List"** in the AwesomeBar
2. Click the **Add Check Run** button
3. In the dialogue box, select:
   - Company
   - Bank account (Paid From)
   - Payables account head
4. Review the returned list of outstanding payables
5. Check which invoices to pay and select payment methods for each
6. Use keyboard shortcuts for efficiency:
   - Arrow keys to navigate rows
   - Spacebar to select/deselect payments
   - Type letters to auto-complete Mode of Payment
7. Submit and choose to print checks or generate ACH files

### Example Workflow

```python
# Optional: Install demo data to test functionality
bench execute 'check_run.tests.setup.before_test'
```

_For detailed examples and configuration, please refer to the [Documentation](./docs/version-14/en/index.md) or visit the [official Check Run documentation](https://agritheory.com/documentation/check_run/)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- FEATURES -->
## Features

- **Single-Page Payment Processing** - Process multiple payables in one streamlined operation
- **Professional Check Printing** - Customizable check formats with voucher support
- **ACH File Generation** - NACHA-compliant electronic payments
- **Bank-Friendly Reports** - Positive Pay reports for fraud prevention
- **Payment Scheduling** - Support for complex payment terms and schedules
- **Returns Handling** - Process debit notes against purchase invoices
- **Keyboard Navigation** - Full keyboard shortcuts for efficient data entry
- **Multi-Currency Support** - Handle international payments
- **Approval Workflows** - Configurable approval processes

See the [official documentation](https://agritheory.com/documentation/check_run/) or [local docs](./docs/version-14/en/index.md) for complete details.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```shell
# Install pre-commit hooks
pre-commit install

# Run type checking
source env/bin/activate
mypy ./apps/check_run/check_run --ignore-missing-imports
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `license.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Want to reach out? - [Contact Us](https://agritheory.com/contact)

AgriTheory - [@agritheory](https://github.com/agritheory)

Repo: [https://github.com/agritheory/check_run](https://github.com/agritheory/check_run)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/agritheory/check_run.svg?style=flat
[contributors-url]: https://github.com/agritheory/check_run/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/agritheory/check_run.svg?style=flat
[forks-url]: https://github.com/agritheory/check_run/network/members
[stars-shield]: https://img.shields.io/github/stars/agritheory/check_run.svg?style=flat
[stars-url]: https://github.com/agritheory/check_run/stargazers
[issues-shield]: https://img.shields.io/github/issues/agritheory/check_run.svg?style=flat
[issues-url]: https://github.com/agritheory/check_run/issues
[license-shield]: https://img.shields.io/github/license/agritheory/check_run?style=green
[license-url]: https://github.com/agritheory/check_run/blob/version-14/license.txt

[Python.py]: https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white
[Python-url]: https://python.org/
[Frappe.io]: https://img.shields.io/badge/Frappe-0089FF?style=flat&logo=frappe&logoColor=white
[Frappe-url]: https://frappeframework.com/
[ERPNext.com]: https://img.shields.io/badge/ERPNext-0089FF?style=flat&logo=erpnext&logoColor=white
[ERPNext-url]: https://erpnext.com/
[JavaScript.js]: https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black
[JavaScript-url]: https://developer.mozilla.org/en-US/docs/Web/JavaScript
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=flat&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
