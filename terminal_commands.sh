# Check if Redis is running
redis-cli ping

# Check if port 8000 is in use
lsof -i :8000

# Check if port 3000 is in use
lsof -i :3000

# Restart Redis if needed
sudo systemctl restart redis-server
