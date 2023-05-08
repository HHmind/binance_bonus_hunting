# Binance Trading Script - Bonus Hunt

This repository contains a Python script to buy or sell BUSD/USDT on Binance based on given floor and ceiling prices. The script is executed using GitHub Actions, and the balance is updated in the `data/balance.json` file.

## Getting Started

Follow these steps to set up the project:

1. **Fork the repo**: Click the "Fork" button in the top-right corner of this repository page to create a copy of the repo in your GitHub account.

2. **Add GitHub Secrets**: Go to your forked repository's "Settings" tab and navigate to the "Secrets" section on the left sidebar. Add the following secrets:
   - `API_KEY`: Your Binance API key
   - `SECRET_KEY`: Your Binance Secret key
   - `floor_price`: The floor price for trading (as a string, e.g., "0.9999")
   - `ceil_price`: The ceiling price for trading (as a string, e.g., "1.0000")

3. **Modify the `data/balance.json` file**: Update the `data/balance.json` file to reflect your initial balances. Make sure that one of the balances (BUSD or USDT) is set to 0. The file should look like this:

```json
{
  "BUSD": 0,
  "USDT": 1000,
  "open_order": null,
  "fees": 0.0
}
```

Replace 1000 with your initial USDT balance. If you want to start with BUSD, set the USDT balance to 0 and update the BUSD balance.

4. Modify the GitHub Actions workflow: Uncomment the schedule section in the .github/workflows/main.yml file to enable the script to run every 5 minutes:

```yaml
on:
  push:
    branches:
      - main
  schedule:
    - cron: '*/5 * * * *'
```

Also, change the (if: false) line to (if: true) in the jobs section:

```yaml
jobs:
  execute-script:
    if: true
    runs-on: ubuntu-latest
```

5. Monitor the GitHub Actions tab: Once you have made the necessary changes, commit and push them to your repository. The script will start executing according to the specified schedule. You can monitor the progress and status of the GitHub Actions workflow by navigating to the "Actions" tab of your repository.

# Important Note

Be aware that running the workflow frequently may consume your GitHub Actions minutes, especially for private repositories with limited minutes per month.
