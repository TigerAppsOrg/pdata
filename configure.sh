# configure.sh
# Author: Michael Friedman
#
# Configures your environment with necessary dependencies to work on the
# project.

# Check usage
if [ $# -ne 0 ]; then
  echo "Usage: ./configure.sh"
  exit
fi

#-------------------------------------------------------------------------------

echo "Setting up Python environment..."

# Create virtual environment
if [ ! -d "venv" ]; then
  virtualenv venv
fi

# Install Python dependencies
source venv/bin/activate
pip install django==1.11 djangorestframework
deactivate

echo "Done"
