# iOPN Faucet Auto Bot

Automated bot for claiming tokens from [iOPN Faucet](https://faucet.iopn.tech/)

## Features

- 🤖 Automated faucet claiming
- 🔄 Multiple account support
- 🌐 Proxy support (optional)
- 🧩 Automatic captcha solving via 2captcha
- ⏰ Scheduled claiming cycles (24 hours)
- 📊 Real-time logging with colored output
- 🔒 Secure session management

## Prerequisites

- Python 3.7+
- 2captcha API key
- Cairo library for SVG conversion

## Installation

1. Clone this repository:
```bash
git clone https://github.com/febriyan9346/iOpnFaucet-Auto-Bot.git
cd iOpnFaucet-Auto-Bot
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Install Cairo (required for cairosvg):

**Ubuntu/Debian:**
```bash
sudo apt-get install libcairo2-dev
```

**macOS:**
```bash
brew install cairo
```

**Windows:**
Download and install from [Cairo official website](https://www.cairographics.org/download/)

## Configuration

Create the following files in the project directory:

### 1. `2captcha.txt`
Add your 2captcha API key:
```
YOUR_2CAPTCHA_API_KEY
```

### 2. `address.txt`
Add your wallet addresses (one per line):
```
0xYourWalletAddress1
0xYourWalletAddress2
0xYourWalletAddress3
```

### 3. `proxy.txt` (Optional)
Add proxies in the following formats:
```
ip:port:username:password
ip:port
http://ip:port
http://username:password@ip:port
```

## Usage

Run the bot:
```bash
python bot.py
```

Select your preferred mode:
- **Option 1**: Run with proxy
- **Option 2**: Run without proxy

The bot will:
1. Fetch captcha from the faucet
2. Solve it using 2captcha
3. Submit claim request
4. Wait 24 hours before next cycle

## Requirements.txt

```txt
requests
colorama
pytz
cairosvg
```

## Features Breakdown

- **Multi-Account**: Process multiple wallets in sequence
- **Proxy Rotation**: Automatic proxy rotation for each account
- **Captcha Solving**: Automated SVG captcha solving via 2captcha API
- **Error Handling**: Comprehensive error handling and logging
- **Cycle Management**: Automatic 24-hour cycle with countdown timer
- **Timezone Support**: Uses WIB (Asia/Jakarta) timezone for logging

## Logs

The bot provides detailed colored logs:
- 🔵 **INFO**: General information
- 🟢 **SUCCESS**: Successful operations
- 🔴 **ERROR**: Error messages
- 🟡 **WARNING**: Warning messages
- 🟣 **CYCLE**: Cycle information

## Troubleshooting

**Issue**: Cairo library not found
- **Solution**: Install Cairo library following the installation instructions above

**Issue**: 2captcha timeout
- **Solution**: Check your 2captcha balance and API key

**Issue**: Proxy connection failed
- **Solution**: Verify proxy format and credentials

**Issue**: Claim failed
- **Solution**: Check wallet address format and faucet availability

## Disclaimer

This bot is for educational purposes only. Use at your own risk. Make sure to comply with the faucet's terms of service.

## License

MIT License - Feel free to use and modify as needed.

---

## Support Us with Cryptocurrency

You can make a contribution using any of the following blockchain networks:

| Network | Wallet Address |
|---------|---------------|
| EVM | `0x216e9b3a5428543c31e659eb8fea3b4bf770bdfd` |
| TON | `UQCEzXLDalfKKySAHuCtBZBARCYnMc0QsTYwN4qda3fE6tto` |
| SOL | `9XgbPg8fndBquYXkGpNYKHHhymdmVhmF6nMkPxhXTki` |
| SUI | `0x8c3632ddd46c984571bf28f784f7c7aeca3b8371f146c4024f01add025f993bf` |

---

**Created by FEBRIYAN**