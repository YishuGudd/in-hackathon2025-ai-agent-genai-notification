#!/bin/bash

echo "🚀 Setting up Snowflake Data Analytics Environment..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip --quiet

# Install requirements
echo "📦 Installing Python packages..."
pip install -r requirements.txt --quiet

echo ""
echo "✅ Installation complete!"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your Snowflake credentials."
    echo ""
    echo "   nano .env"
    echo "   or"
    echo "   code .env"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Setup complete! Next steps:"
echo ""
echo "1. Edit .env file with your Snowflake credentials:"
echo "   nano .env"
echo ""
echo "2. Test the connection:"
echo "   python snowflake_connector.py"
echo ""
echo "3. Start Jupyter notebook for data analytics:"
echo "   jupyter notebook data_analytics.ipynb"
echo ""
echo "Happy analyzing! 📊"

