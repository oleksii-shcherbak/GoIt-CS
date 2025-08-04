# GoIT CS Homework 06

Web application with Socket server and MongoDB.

## How to run

```bash
./run.sh
```

This script will:
- Check if Docker is running
- Stop any existing containers
- Build and start the application
- Open http://localhost:3000 in your browser

To stop the application:
```bash
docker-compose down
```

## Check messages in MongoDB

Connect to MongoDB:
```bash
docker exec -it mongodb mongosh
```

Then inside MongoDB shell:
```javascript
use messages_db

db.messages.find().pretty()

exit
```

## Manual run (without script)

```bash
docker-compose up --build
```

Then open http://localhost:3000 manually.

## Note

Port 5000 may be occupied on macOS by AirPlay. If you encounter issues, disable AirPlay Receiver in System Settings > General > AirDrop & Handoff.
