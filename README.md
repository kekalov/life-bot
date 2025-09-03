# 🗓️ Life Calendar Bot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A beautiful Telegram bot that creates life calendar visualizations in weeks, similar to the famous "A 90-Year Human Life in Weeks" diagram.

## 🎯 Features

- **Life Visualization**: Shows your life as a grid of weeks
- **Gender-based Statistics**: Different life expectancy for males (75 years) and females (82 years)
- **Age Calculator**: Precise age calculation in years, months, and days
- **Life Progress**: Percentage of life lived with visual progress bar
- **Beautiful Design**: Professional visualization optimized for mobile devices
- **English Labels**: Clean, international design

## 🖼️ Example Visualization

The bot creates beautiful images showing:
- Red squares = weeks you've lived
- White squares = weeks ahead of you
- Life statistics in organized blocks
- Professional design ready for social media

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/life-calendar-bot.git
cd life-calendar-bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create Telegram bot
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` command
3. Follow instructions and get your bot token

### 4. Configure environment
```bash
cp env_example.txt .env
# Edit .env and add your BOT_TOKEN
```

### 5. Run the bot
```bash
python bot.py
```

## 📱 Bot Commands

- `/start` - Start the bot
- `/setgender <gender>` - Set gender (male/female)
- `/setbirth <date>` - Set birth date (DD.MM.YYYY)
- `/show` - Show life calendar
- `/age` - Show precise age
- `/week` - Show week statistics
- `/percentage` - Show life progress
- `/help` - Show help

## 🎨 Visualization Features

- **Grid Size**: 52 weeks × life expectancy years
- **Colors**: Red (lived), White (remaining)
- **Statistics**: Age, weeks lived/remaining, life progress
- **Design**: Professional layout with rounded boxes
- **Format**: PNG, ~70KB, optimized for Telegram

## 🔧 Configuration

Edit `config.py` to customize:
- Life expectancy by gender
- Colors and styling
- Grid dimensions
- Text formatting

## 📊 Life Expectancy Statistics

- **Males**: 75 years (3,900 weeks)
- **Females**: 82 years (4,264 weeks)
- **Default**: 80 years (4,160 weeks)

## 🛠️ Technical Details

- **Language**: Python 3.8+
- **Dependencies**: python-telegram-bot, matplotlib, Pillow
- **Platform**: Cross-platform (Windows, macOS, Linux)
- **Architecture**: Modular design with separate visualizer

## 📁 Project Structure

```
life-calendar-bot/
├── bot.py                 # Main bot file
├── life_visualizer.py     # Visualization generator
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── .env                   # Environment variables
├── README.md             # This file
├── SETUP.md              # Setup instructions
├── USAGE.md              # Usage guide
└── test_visualization.py # Test script
```

## 🧪 Testing

Test the visualization before running the bot:
```bash
python test_visualization.py
```

This creates sample images for different genders.

## 🚀 Deployment

### Local Development
```bash
python bot.py
```

### Production
```bash
./run_bot.sh
```

### Docker (coming soon)
```bash
docker build -t life-calendar-bot .
docker run -d life-calendar-bot
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the "A 90-Year Human Life in Weeks" visualization
- Built with [python-telegram-bot](https://python-telegram-bot.org/)
- Visualization powered by [matplotlib](https://matplotlib.org/)

## 📞 Support

- Create an [issue](https://github.com/yourusername/life-calendar-bot/issues) for bugs
- Start a [discussion](https://github.com/yourusername/life-calendar-bot/discussions) for questions
- Check [USAGE.md](USAGE.md) for detailed instructions

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/life-calendar-bot&type=Date)](https://star-history.com/#yourusername/life-calendar-bot&Date)

---

**Made with ❤️ for life reflection and motivation**
