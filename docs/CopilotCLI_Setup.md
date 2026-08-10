# GitHub Copilot CLI Setup Guide

This guide covers the installation and initial setup of GitHub Copilot CLI on Windows and Linux.

## 1. Prerequisites

* GitHub account with access to GitHub Copilot
* GitHub Copilot Extension installed in VS Code.
* Node.js **22 or above** when using the npm installation method
* ONLY FOR WINDOWS USERS IF BLOCKED BY PROXY: [Proxy Setup Guide](https://inside-docupedia.bosch.com/confluence/spaces/DIGITMEMS/pages/7113779255/Installing+Github+Copilot+CLI)

Check Node.js and npm:

```bash
node --version
npm --version
```

---

## 2. Install GitHub Copilot CLI

Choose **one** of the following installation methods.

### Universal — npm

Works on Windows and Linux.

```bash
npm install -g @github/copilot
```

Verify:

```bash
copilot --version
```

> The npm installation method requires Node.js 22+ and npm.

### Installing npm on Linux

For Ubuntu/Debian-based Linux:

```bash
sudo apt update
sudo apt install -y npm
```

Verify:

```bash
node --version
npm --version
```

If the installed Node.js version is below 22, use NVM:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
source ~/.bashrc
nvm install 22
nvm use 22
nvm alias default 22
```

Verify:

```bash
node --version
npm --version
```

Then install Copilot:

```bash
npm install -g @github/copilot
```

---

### Linux Only — Install Script

This method does not require Node.js or npm.

Using `curl`:

```bash
curl -fsSL https://gh.io/copilot-install | bash
```

Or using `wget`:

```bash
wget -qO- https://gh.io/copilot-install | bash
```

Verify:

```bash
copilot --version
```

---

### Windows Only — WinGet

Open PowerShell and run:

```powershell
winget install GitHub.Copilot
```

Verify:

```powershell
copilot --version
```

---

## 3. Start GitHub Copilot CLI

Navigate to your project directory.

Linux:

```bash
cd /path/to/your/project
```

Windows:

```powershell
cd C:\path\to\your\project
```

Start Copilot CLI:

```bash
copilot
```

---

## 4. GitHub Authentication

If authentication is required, start Copilot CLI and run:

```text
/login
```

Follow the authentication instructions in the terminal to sign in to your GitHub account.

Once authenticated, GitHub Copilot CLI is ready to use.
